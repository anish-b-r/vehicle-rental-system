package com.driveease.service;

import com.driveease.dto.CurrencyRatesDto;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.json.JsonParser;
import org.springframework.boot.json.JsonParserFactory;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * High-precision currency conversion service with in-memory caching
 * and automated external exchange rate fetching with sensible fallback.
 */
@Service
public class CurrencyServiceImpl implements CurrencyService {

    private static final Logger log = LoggerFactory.getLogger(CurrencyServiceImpl.class);

    private static final String BASE_CURRENCY = "INR";
    private static final List<String> SUPPORTED_CURRENCIES = List.of("INR", "USD", "EUR", "GBP", "AED");
    private static final Duration CACHE_TTL = Duration.ofHours(1);

    // Primary exchange rate API endpoint (reliable, free, no key required)
    private static final String API_URL = "https://open.er-api.com/v6/latest/INR";

    // Thread-safe cached rates map
    private final Map<String, BigDecimal> cachedRates = new ConcurrentHashMap<>();
    private LocalDateTime lastFetchTime = null;
    private boolean isFallbackActive = false;

    private final HttpClient httpClient;

    public CurrencyServiceImpl() {
        this.httpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(3))
                .build();
        // Seed default fallback exchange rates immediately
        initFallbackRates();
        // Trigger initial background/asynchronous fetch
        refreshRatesAsync();
    }

    private void initFallbackRates() {
        // Base INR = 1.0
        // Real-market benchmarks:
        // 1 USD ≈ ₹86.20  => 1 INR = 0.01160 USD
        // 1 EUR ≈ ₹90.10  => 1 INR = 0.01110 EUR
        // 1 GBP ≈ ₹107.50 => 1 INR = 0.00930 GBP
        // 1 AED ≈ ₹23.47  => 1 INR = 0.04260 AED
        cachedRates.put("INR", BigDecimal.ONE.setScale(6, RoundingMode.HALF_UP));
        cachedRates.put("USD", new BigDecimal("0.011600"));
        cachedRates.put("EUR", new BigDecimal("0.011100"));
        cachedRates.put("GBP", new BigDecimal("0.009300"));
        cachedRates.put("AED", new BigDecimal("0.042600"));
        lastFetchTime = LocalDateTime.now();
        isFallbackActive = true;
    }

    @Override
    public synchronized CurrencyRatesDto getExchangeRates() {
        if (shouldRefresh()) {
            refreshRates();
        }

        return new CurrencyRatesDto(
                BASE_CURRENCY,
                SUPPORTED_CURRENCIES,
                new HashMap<>(cachedRates),
                lastFetchTime,
                isFallbackActive
        );
    }

    @Override
    public BigDecimal convert(BigDecimal amountInInr, String targetCurrency) {
        if (amountInInr == null) {
            return BigDecimal.ZERO;
        }

        if (targetCurrency == null || targetCurrency.isBlank() || BASE_CURRENCY.equalsIgnoreCase(targetCurrency.trim())) {
            return amountInInr.setScale(2, RoundingMode.HALF_UP);
        }

        String cur = targetCurrency.trim().toUpperCase();
        CurrencyRatesDto current = getExchangeRates();
        BigDecimal rate = current.getRates().get(cur);

        if (rate == null) {
            log.warn("Requested unsupported currency: '{}', defaulting to INR", cur);
            return amountInInr.setScale(2, RoundingMode.HALF_UP);
        }

        return amountInInr.multiply(rate).setScale(2, RoundingMode.HALF_UP);
    }

    @Override
    public String getBaseCurrency() {
        return BASE_CURRENCY;
    }

    private boolean shouldRefresh() {
        if (lastFetchTime == null) {
            return true;
        }
        return Duration.between(lastFetchTime, LocalDateTime.now()).compareTo(CACHE_TTL) > 0;
    }

    private void refreshRatesAsync() {
        Thread thread = new Thread(this::refreshRates, "CurrencyRateFetcher");
        thread.setDaemon(true);
        thread.start();
    }

    private void refreshRates() {
        try {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(API_URL))
                    .timeout(Duration.ofSeconds(4))
                    .header("Accept", "application/json")
                    .GET()
                    .build();

            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() == 200) {
                JsonParser parser = JsonParserFactory.getJsonParser();
                Map<String, Object> json = parser.parseMap(response.body());

                Object ratesObj = json.get("rates");
                if (ratesObj instanceof Map<?, ?> apiRates) {
                    for (String cur : SUPPORTED_CURRENCIES) {
                        if ("INR".equalsIgnoreCase(cur)) {
                            cachedRates.put("INR", BigDecimal.ONE);
                            continue;
                        }
                        Object rateVal = apiRates.get(cur);
                        if (rateVal != null) {
                            BigDecimal rate = new BigDecimal(rateVal.toString()).setScale(6, RoundingMode.HALF_UP);
                            cachedRates.put(cur, rate);
                        }
                    }
                    lastFetchTime = LocalDateTime.now();
                    isFallbackActive = false;
                    log.info("Live exchange rates successfully fetched and cached from external provider.");
                    return;
                }
            }
            log.warn("Exchange rate API returned non-OK status: {}, retaining existing rates.", response.statusCode());
        } catch (Exception e) {
            log.warn("Could not fetch live exchange rates: {}. Operating seamlessly with cached/fallback rates.", e.getMessage());
            isFallbackActive = true;
        }
    }
}
