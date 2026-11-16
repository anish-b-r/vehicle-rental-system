package com.driveease.model;

import jakarta.persistence.Column;
import jakarta.persistence.DiscriminatorValue;
import jakarta.persistence.Entity;
import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * Concrete Car subclass extending Vehicle.
 * Demonstrates OOP Inheritance and Polymorphic method overrides.
 */
@Entity
@DiscriminatorValue("CAR")
public class Car extends Vehicle {

    @Column(name = "seating_capacity")
    private int seatingCapacity = 5;

    @Column(name = "luggage_capacity")
    private int luggageCapacity = 2; // number of bags

    @Column(name = "car_body_type", length = 40)
    private String bodyType = "Sedan"; // Sedan, SUV, Sports, Coupe

    @Column(name = "has_air_conditioning")
    private boolean hasAirConditioning = true;

    public Car() {
        super();
        setCategory(VehicleCategory.CAR);
    }

    public Car(String brand, String model, FuelType fuelType, TransmissionType transmission,
               BigDecimal dailyRate, BigDecimal securityDeposit, String imageUrl,
               String description, boolean available, Double rating, String location,
               String features, int seatingCapacity, int luggageCapacity, String bodyType,
               boolean hasAirConditioning) {
        this(brand, model, fuelType, transmission, dailyRate, securityDeposit, imageUrl,
             description, available, rating, location, features, seatingCapacity, luggageCapacity,
             bodyType, hasAirConditioning, false, VehicleOrigin.INDIAN);
    }

    public Car(String brand, String model, FuelType fuelType, TransmissionType transmission,
               BigDecimal dailyRate, BigDecimal securityDeposit, String imageUrl,
               String description, boolean available, Double rating, String location,
               String features, int seatingCapacity, int luggageCapacity, String bodyType,
               boolean hasAirConditioning, boolean isPremium, VehicleOrigin vehicleOrigin) {
        super(brand, model, VehicleCategory.CAR, fuelType, transmission, dailyRate,
              securityDeposit, imageUrl, description, available, rating, location, features,
              isPremium, vehicleOrigin);
        this.seatingCapacity = seatingCapacity;
        this.luggageCapacity = luggageCapacity;
        this.bodyType = bodyType != null ? bodyType : "Sedan";
        this.hasAirConditioning = hasAirConditioning;
    }

    @Override
    public String getVehicleSpecificationsSummary() {
        return String.format("%d Seats · %d Luggage · %s · %s · %s",
                seatingCapacity, luggageCapacity, bodyType, getTransmission(), getFuelType());
    }

    @Override
    public BigDecimal calculateBaseInsurance(int days) {
        // Luxury car insurance is slightly higher ($15/day)
        return BigDecimal.valueOf(15.00).multiply(BigDecimal.valueOf(days)).setScale(2, RoundingMode.HALF_UP);
    }

    // Getters and Setters
    public int getSeatingCapacity() {
        return seatingCapacity;
    }

    public void setSeatingCapacity(int seatingCapacity) {
        this.seatingCapacity = seatingCapacity;
    }

    public int getLuggageCapacity() {
        return luggageCapacity;
    }

    public void setLuggageCapacity(int luggageCapacity) {
        this.luggageCapacity = luggageCapacity;
    }

    public String getBodyType() {
        return bodyType;
    }

    public void setBodyType(String bodyType) {
        this.bodyType = bodyType;
    }

    public boolean isHasAirConditioning() {
        return hasAirConditioning;
    }

    public void setHasAirConditioning(boolean hasAirConditioning) {
        this.hasAirConditioning = hasAirConditioning;
    }
}
