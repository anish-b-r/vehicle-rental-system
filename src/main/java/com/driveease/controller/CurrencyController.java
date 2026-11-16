package com.driveease.controller;

import com.driveease.dto.ApiResponse;
import com.driveease.dto.CurrencyRatesDto;
import com.driveease.service.CurrencyService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.math.BigDecimal;
import java.util.Map;

@RestController
@RequestMapping("/api/currency")
public class CurrencyController {

    private final CurrencyService currencyService;

    public CurrencyController(CurrencyService currencyService) {
        this.currencyService = currencyService;
    }

    @GetMapping("/rates")
    public ResponseEntity<ApiResponse<CurrencyRatesDto>> getRates() {
        CurrencyRatesDto dto = currencyService.getExchangeRates();
        return ResponseEntity.ok(ApiResponse.success(dto));
    }

    @GetMapping("/convert")
    public ResponseEntity<ApiResponse<Map<String, Object>>> convert(
            @RequestParam BigDecimal amount,
            @RequestParam String target) {
        BigDecimal converted = currencyService.convert(amount, target);
        return ResponseEntity.ok(ApiResponse.success(Map.of(
                "baseAmount", amount,
                "baseCurrency", currencyService.getBaseCurrency(),
                "targetCurrency", target.toUpperCase(),
                "convertedAmount", converted
        )));
    }
}
