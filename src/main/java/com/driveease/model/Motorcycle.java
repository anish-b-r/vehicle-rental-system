package com.driveease.model;

import jakarta.persistence.Column;
import jakarta.persistence.DiscriminatorValue;
import jakarta.persistence.Entity;
import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * Concrete Motorcycle / Bike subclass extending Vehicle.
 * Demonstrates OOP Inheritance and Polymorphic method overrides.
 */
@Entity
@DiscriminatorValue("BIKE")
public class Motorcycle extends Vehicle {

    @Column(name = "engine_cc")
    private int engineCc = 650;

    @Column(name = "bike_type", length = 40)
    private String bikeType = "Sport"; // Sport, Cruiser, Adventure, Classic

    @Column(name = "has_helmet_included")
    private boolean hasHelmetIncluded = true;

    public Motorcycle() {
        super();
        setCategory(VehicleCategory.BIKE);
    }

    public Motorcycle(String brand, String model, FuelType fuelType, TransmissionType transmission,
                      BigDecimal dailyRate, BigDecimal securityDeposit, String imageUrl,
                      String description, boolean available, Double rating, String location,
                      String features, int engineCc, String bikeType, boolean hasHelmetIncluded) {
        this(brand, model, fuelType, transmission, dailyRate, securityDeposit, imageUrl,
             description, available, rating, location, features, engineCc, bikeType,
             hasHelmetIncluded, false, VehicleOrigin.INTERNATIONAL);
    }

    public Motorcycle(String brand, String model, FuelType fuelType, TransmissionType transmission,
                      BigDecimal dailyRate, BigDecimal securityDeposit, String imageUrl,
                      String description, boolean available, Double rating, String location,
                      String features, int engineCc, String bikeType, boolean hasHelmetIncluded,
                      boolean isPremium, VehicleOrigin vehicleOrigin) {
        super(brand, model, VehicleCategory.BIKE, fuelType, transmission, dailyRate,
              securityDeposit, imageUrl, description, available, rating, location, features,
              isPremium, vehicleOrigin);
        this.engineCc = engineCc;
        this.bikeType = bikeType != null ? bikeType : "Sport";
        this.hasHelmetIncluded = hasHelmetIncluded;
    }

    @Override
    public String getVehicleSpecificationsSummary() {
        return String.format("%d cc · %s · Helmet Included: %s · %s",
                engineCc, bikeType, hasHelmetIncluded ? "Yes" : "No", getFuelType());
    }

    @Override
    public BigDecimal calculateBaseInsurance(int days) {
        // Motorcycle insurance is $10/day
        return BigDecimal.valueOf(10.00).multiply(BigDecimal.valueOf(days)).setScale(2, RoundingMode.HALF_UP);
    }

    // Getters and Setters
    public int getEngineCc() {
        return engineCc;
    }

    public void setEngineCc(int engineCc) {
        this.engineCc = engineCc;
    }

    public String getBikeType() {
        return bikeType;
    }

    public void setBikeType(String bikeType) {
        this.bikeType = bikeType;
    }

    public boolean isHasHelmetIncluded() {
        return hasHelmetIncluded;
    }

    public void setHasHelmetIncluded(boolean hasHelmetIncluded) {
        this.hasHelmetIncluded = hasHelmetIncluded;
    }
}
