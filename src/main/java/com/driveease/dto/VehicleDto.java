package com.driveease.dto;

import com.driveease.model.*;
import java.math.BigDecimal;

public class VehicleDto {

    private Long id;
    private String brand;
    private String model;
    private String fullName;
    private VehicleCategory category;
    private FuelType fuelType;
    private TransmissionType transmission;
    private BigDecimal dailyRate;
    private BigDecimal securityDeposit;
    private String imageUrl;
    private String description;
    private boolean available;
    private Double rating;
    private String location;
    private String features;
    private String specificationsSummary;
    private boolean isPremium;
    private VehicleOrigin vehicleOrigin;
    private String baseCurrency = "INR";

    // Car specific
    private Integer seatingCapacity;
    private Integer luggageCapacity;
    private String bodyType;
    private Boolean hasAirConditioning;

    // Bike specific
    private Integer engineCc;
    private String bikeType;
    private Boolean hasHelmetIncluded;

    public VehicleDto() {
    }

    public VehicleDto(Vehicle vehicle) {
        if (vehicle != null) {
            this.id = vehicle.getId();
            this.brand = vehicle.getBrand();
            this.model = vehicle.getModel();
            this.fullName = vehicle.getFullName();
            this.category = vehicle.getCategory();
            this.fuelType = vehicle.getFuelType();
            this.transmission = vehicle.getTransmission();
            this.dailyRate = vehicle.getDailyRate();
            this.securityDeposit = vehicle.getSecurityDeposit();
            this.imageUrl = vehicle.getImageUrl();
            this.description = vehicle.getDescription();
            this.available = vehicle.isAvailable();
            this.rating = vehicle.getRating();
            this.location = vehicle.getLocation();
            this.features = vehicle.getFeatures();
            this.specificationsSummary = vehicle.getVehicleSpecificationsSummary();
            this.isPremium = vehicle.isPremium();
            this.vehicleOrigin = vehicle.getVehicleOrigin();
            this.baseCurrency = vehicle.getBaseCurrency() != null ? vehicle.getBaseCurrency() : "INR";

            if (vehicle instanceof Car car) {
                this.seatingCapacity = car.getSeatingCapacity();
                this.luggageCapacity = car.getLuggageCapacity();
                this.bodyType = car.getBodyType();
                this.hasAirConditioning = car.isHasAirConditioning();
            } else if (vehicle instanceof Motorcycle bike) {
                this.engineCc = bike.getEngineCc();
                this.bikeType = bike.getBikeType();
                this.hasHelmetIncluded = bike.isHasHelmetIncluded();
            }
        }
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

    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
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

    public String getSpecificationsSummary() {
        return specificationsSummary;
    }

    public void setSpecificationsSummary(String specificationsSummary) {
        this.specificationsSummary = specificationsSummary;
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

    public boolean isPremium() {
        return isPremium;
    }

    public boolean getIsPremium() {
        return isPremium;
    }

    public void setPremium(boolean premium) {
        this.isPremium = premium;
    }

    public void setIsPremium(boolean premium) {
        this.isPremium = premium;
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
