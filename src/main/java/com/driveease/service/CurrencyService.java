package com.driveease.service;

import com.driveease.dto.CurrencyRatesDto;
import java.math.BigDecimal;

public interface CurrencyService {

    CurrencyRatesDto getExchangeRates();

    BigDecimal convert(BigDecimal amountInInr, String targetCurrency);

    String getBaseCurrency();
}
