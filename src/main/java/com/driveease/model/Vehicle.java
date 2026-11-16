package com.driveease.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * Base abstract class representing any rental vehicle in the DriveEase fleet.
 * Demonstrates OOP Abstraction, Encapsulation, and Polymorphism.
 */
@Entity
@Table(name = "vehicles")
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
@DiscriminatorColumn(name = "vehicle_type", discriminatorType = DiscriminatorType.STRING)
public abstract class Vehicle {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "Brand is required")
    @Column(nullable = false, length = 60)
    private String brand;

    @NotBlank(message = "Model is required")
    @Column(nullable = false, length = 60)
    private String model;

    @NotNull(message = "Vehicle category is required")
    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private VehicleCategory category;

    @NotNull(message = "Fuel type is required")
    @Enumerated(EnumType.STRING)
    @Column(name = "fuel_type", nullable = false, length = 20)
    private FuelType fuelType;

    @NotNull(message = "Transmission is required")
    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private TransmissionType transmission;

    @NotNull(message = "Daily rental price is required")
    @DecimalMin(value = "0.0", inclusive = false, message = "Daily price must be greater than zero")
    @Column(name = "daily_rate", nullable = false, precision = 10, scale = 2)
    private BigDecimal dailyRate;

    @Column(name = "security_deposit", precision = 10, scale = 2)
    private BigDecimal securityDeposit = new BigDecimal("200.00");

    @Column(name = "image_url", length = 500)
    private String imageUrl;

    @Column(length = 1000)
    private String description;

    @Column(name = "is_available", nullable = false)
    private boolean available = true;

    @Column
    private Double rating = 4.8;

    @Column(length = 80)
    private String location = "Downtown Hub";

    @Column(length = 500)
    private String features;

    @Column(name = "is_premium", nullable = false)
    private boolean isPremium = false;

    @Enumerated(EnumType.STRING)
    @Column(name = "vehicle_origin", nullable = false, length = 20)
    private VehicleOrigin vehicleOrigin = VehicleOrigin.INDIAN;

    @Column(name = "base_currency", nullable = false, length = 10)
    private String baseCurrency = "INR";

    // Default constructor for JPA
    protected Vehicle() {
    }

    protected Vehicle(String brand, String model, VehicleCategory category,
            FuelType fuelType, TransmissionType transmission,
            BigDecimal dailyRate, BigDecimal securityDeposit,
            String imageUrl, String description, boolean available,
            Double rating, String location, String features) {
        this(brand, model, category, fuelType, transmission, dailyRate, securityDeposit,
                imageUrl, description, available, rating, location, features, false, VehicleOrigin.INDIAN);
    }

    protected Vehicle(String brand, String model, VehicleCategory category,
            FuelType fuelType, TransmissionType transmission,
            BigDecimal dailyRate, BigDecimal securityDeposit,
            String imageUrl, String description, boolean available,
            Double rating, String location, String features,
            boolean isPremium, VehicleOrigin vehicleOrigin) {
        this.brand = brand;
        this.model = model;
        this.category = category;
        this.fuelType = fuelType;
        this.transmission = transmission;
        this.dailyRate = dailyRate;
        this.securityDeposit = securityDeposit != null ? securityDeposit : new BigDecimal("5000.00");
        this.imageUrl = imageUrl;
        this.description = description;
        this.available = available;
        this.rating = rating != null ? rating : 4.8;
        this.location = location != null ? location : "Downtown Hub";
        this.features = features;
        this.isPremium = isPremium;
        this.vehicleOrigin = vehicleOrigin != null ? vehicleOrigin : VehicleOrigin.INDIAN;
        this.baseCurrency = "INR";
    }

    // OOP Polymorphic Methods
    /**
     * Polymorphic method to get human-readable specifications summary.
     */
    public abstract String getVehicleSpecificationsSummary();

    /**
     * Polymorphic calculation for base insurance fee per day based on vehicle type.
     */
    public abstract BigDecimal calculateBaseInsurance(int days);

    /**
     * Common calculation for rental cost before taxes and discounts.
     */
    public BigDecimal calculateRentalCost(int days) {
        if (days <= 0) {
            throw new IllegalArgumentException("Rental days must be at least 1");
        }
        return dailyRate.multiply(BigDecimal.valueOf(days)).setScale(2, RoundingMode.HALF_UP);
    }

    public String getFullName() {
        return brand + " " + model;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getBrand() {
        return brand;
    }

    public void setBrand(String brand) {
        this.brand = brand;
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }

    public VehicleCategory getCategory() {
        return category;
    }

    public void setCategory(VehicleCategory category) {
        this.category = category;
    }

    public FuelType getFuelType() {
        return fuelType;
    }

    public void setFuelType(FuelType fuelType) {
        this.fuelType = fuelType;
    }

    public TransmissionType getTransmission() {
        return transmission;
    }

    public void setTransmission(TransmissionType transmission) {
        this.transmission = transmission;
    }

    public BigDecimal getDailyRate() {
        return dailyRate;
    }

    public void setDailyRate(BigDecimal dailyRate) {
        this.dailyRate = dailyRate;
    }

    public BigDecimal getSecurityDeposit() {
        return securityDeposit;
    }

    public void setSecurityDeposit(BigDecimal securityDeposit) {
        this.securityDeposit = securityDeposit;
    }

    public String getImageUrl() {
        return imageUrl;
    }

    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public boolean isAvailable() {
        return available;
    }

    public void setAvailable(boolean available) {
        this.available = available;
    }

    public Double getRating() {
        return rating;
    }

    public void setRating(Double rating) {
        this.rating = rating;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getFeatures() {
        return features;
    }

    public void setFeatures(String features) {
        this.features = features;
    }

    public boolean isPremium() {
        return isPremium;
    }

    public void setPremium(boolean premium) {
        isPremium = premium;
    }

    public VehicleOrigin getVehicleOrigin() {
        return vehicleOrigin;
    }

    public void setVehicleOrigin(VehicleOrigin vehicleOrigin) {
        this.vehicleOrigin = vehicleOrigin;
    }

    public String getBaseCurrency() {
        return baseCurrency;
    }

    public void setBaseCurrency(String baseCurrency) {
        this.baseCurrency = baseCurrency;
    }
}
