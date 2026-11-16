package com.driveease.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

/**
 * DTO representing current currency exchange rates relative to the base currency (INR).
 */
public class CurrencyRatesDto {

    private String baseCurrency = "INR";
    private List<String> availableCurrencies;
    private Map<String, BigDecimal> rates;
    private LocalDateTime lastUpdated;
    private boolean fallback;

    public CurrencyRatesDto() {
    }

    public CurrencyRatesDto(String baseCurrency, List<String> availableCurrencies,
                            Map<String, BigDecimal> rates, LocalDateTime lastUpdated,
                            boolean fallback) {
        this.baseCurrency = baseCurrency;
        this.availableCurrencies = availableCurrencies;
        this.rates = rates;
        this.lastUpdated = lastUpdated;
        this.fallback = fallback;
    }

    public String getBaseCurrency() {
        return baseCurrency;
    }

    public void setBaseCurrency(String baseCurrency) {
        this.baseCurrency = baseCurrency;
    }

    public List<String> getAvailableCurrencies() {
        return availableCurrencies;
    }

    public void setAvailableCurrencies(List<String> availableCurrencies) {
        this.availableCurrencies = availableCurrencies;
    }

    public Map<String, BigDecimal> getRates() {
        return rates;
    }

    public void setRates(Map<String, BigDecimal> rates) {
        this.rates = rates;
    }

    public LocalDateTime getLastUpdated() {
        return lastUpdated;
    }

    public void setLastUpdated(LocalDateTime lastUpdated) {
        this.lastUpdated = lastUpdated;
    }

    public boolean isFallback() {
        return fallback;
    }

    public void setFallback(boolean fallback) {
        this.fallback = fallback;
    }
}
