package com.driveease.dto;

import com.driveease.model.FuelType;
import com.driveease.model.TransmissionType;
import com.driveease.model.VehicleCategory;
import com.driveease.model.VehicleOrigin;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;

public class VehicleRequest {

    @NotBlank(message = "Brand is required")
    private String brand;

    @NotBlank(message = "Model is required")
    private String model;

    @NotNull(message = "Category is required")
    private VehicleCategory category;

    @NotNull(message = "Fuel type is required")
    private FuelType fuelType;

    @NotNull(message = "Transmission is required")
    private TransmissionType transmission;

    @NotNull(message = "Daily rate is required")
    @DecimalMin(value = "0.0", inclusive = false, message = "Daily rate must be positive")
    private BigDecimal dailyRate;

    private BigDecimal securityDeposit;
    private String imageUrl;
    private String description;
    private Boolean available = true;
    private Double rating = 4.8;
    private String location = "Downtown Hub";
    private String features;
    private Boolean isPremium = false;
    private VehicleOrigin vehicleOrigin = VehicleOrigin.INDIAN;

    // Car specific
    private Integer seatingCapacity;
    private Integer luggageCapacity;
    private String bodyType;
    private Boolean hasAirConditioning;

    // Bike specific
    private Integer engineCc;
    private String bikeType;
    private Boolean hasHelmetIncluded;

    public VehicleRequest() {
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

    public Boolean getAvailable() {
        return available;
    }

    public void setAvailable(Boolean available) {
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

    public Integer getSeatingCapacity() {
        return seatingCapacity;
    }

    public void setSeatingCapacity(Integer seatingCapacity) {
        this.seatingCapacity = seatingCapacity;
    }

    public Integer getLuggageCapacity() {
        return luggageCapacity;
    }

    public void setLuggageCapacity(Integer luggageCapacity) {
        this.luggageCapacity = luggageCapacity;
    }

    public String getBodyType() {
        return bodyType;
    }

    public void setBodyType(String bodyType) {
        this.bodyType = bodyType;
    }

    public Boolean getHasAirConditioning() {
        return hasAirConditioning;
    }

    public void setHasAirConditioning(Boolean hasAirConditioning) {
        this.hasAirConditioning = hasAirConditioning;
    }

    public Integer getEngineCc() {
        return engineCc;
    }

    public void setEngineCc(Integer engineCc) {
        this.engineCc = engineCc;
    }

    public String getBikeType() {
        return bikeType;
    }

    public void setBikeType(String bikeType) {
        this.bikeType = bikeType;
    }

    public Boolean getHasHelmetIncluded() {
        return hasHelmetIncluded;
    }

    public void setHasHelmetIncluded(Boolean hasHelmetIncluded) {
        this.hasHelmetIncluded = hasHelmetIncluded;
    }

    public Boolean getIsPremium() {
        return isPremium;
    }

    public void setIsPremium(Boolean isPremium) {
        this.isPremium = isPremium;
    }

    public VehicleOrigin getVehicleOrigin() {
        return vehicleOrigin;
    }

    public void setVehicleOrigin(VehicleOrigin vehicleOrigin) {
        this.vehicleOrigin = vehicleOrigin;
    }
}
