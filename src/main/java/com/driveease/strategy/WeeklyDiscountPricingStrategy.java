package com.driveease.strategy;

import org.springframework.stereotype.Component;
import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * Extended pricing strategy offering a 10% discount on rentals of 7 days or more.
 */
@Component("weeklyDiscountPricingStrategy")
public class WeeklyDiscountPricingStrategy implements RentalPricingStrategy {

    private static final BigDecimal DISCOUNT_RATE = new BigDecimal("0.10");

    @Override
    public BigDecimal calculateSubtotal(BigDecimal dailyRate, int days) {
        return dailyRate.multiply(BigDecimal.valueOf(days)).setScale(2, RoundingMode.HALF_UP);
    }

    @Override
    public BigDecimal calculateDiscount(BigDecimal subtotal, int days) {
        if (days >= 7) {
            return subtotal.multiply(DISCOUNT_RATE).setScale(2, RoundingMode.HALF_UP);
        }
        return BigDecimal.ZERO.setScale(2, RoundingMode.HALF_UP);
    }

    @Override
    public String getStrategyName() {
        return "Weekly Rental (10% Saver Discount)";
    }
}
