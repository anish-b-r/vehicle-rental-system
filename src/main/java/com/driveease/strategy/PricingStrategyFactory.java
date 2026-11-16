package com.driveease.strategy;

import org.springframework.stereotype.Component;

/**
 * Factory class to dynamically select the appropriate pricing strategy based on rental duration.
 * Demonstrates the Factory Pattern in Java.
 */
@Component
public class PricingStrategyFactory {

    private final StandardPricingStrategy standardPricingStrategy;
    private final WeeklyDiscountPricingStrategy weeklyDiscountPricingStrategy;

    public PricingStrategyFactory(StandardPricingStrategy standardPricingStrategy,
                                  WeeklyDiscountPricingStrategy weeklyDiscountPricingStrategy) {
        this.standardPricingStrategy = standardPricingStrategy;
        this.weeklyDiscountPricingStrategy = weeklyDiscountPricingStrategy;
    }

    public RentalPricingStrategy getStrategy(int days) {
        if (days >= 7) {
            return weeklyDiscountPricingStrategy;
        }
        return standardPricingStrategy;
    }
}
