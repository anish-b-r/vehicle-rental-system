package com.driveease.strategy;

import org.springframework.stereotype.Component;
import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * Standard pricing strategy with no bulk discounts applied.
 */
@Component("standardPricingStrategy")
public class StandardPricingStrategy implements RentalPricingStrategy {

    @Override
    public BigDecimal calculateSubtotal(BigDecimal dailyRate, int days) {
        return dailyRate.multiply(BigDecimal.valueOf(days)).setScale(2, RoundingMode.HALF_UP);
    }

    @Override
    public BigDecimal calculateDiscount(BigDecimal subtotal, int days) {
        return BigDecimal.ZERO.setScale(2, RoundingMode.HALF_UP);
    }

    @Override
    public String getStrategyName() {
        return "Standard Daily Rate";
    }
}
