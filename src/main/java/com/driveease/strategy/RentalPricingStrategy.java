package com.driveease.strategy;

import java.math.BigDecimal;

/**
 * Strategy interface for rental pricing calculations.
 * Demonstrates the Strategy Design Pattern and Polymorphism in OOP.
 */
public interface RentalPricingStrategy {

    /**
     * Calculates the subtotal for a given daily rate and number of days.
     */
    BigDecimal calculateSubtotal(BigDecimal dailyRate, int days);

    /**
     * Calculates any discount applicable.
     */
    BigDecimal calculateDiscount(BigDecimal subtotal, int days);

    /**
     * Returns a descriptive name for this pricing strategy.
     */
    String getStrategyName();
}
