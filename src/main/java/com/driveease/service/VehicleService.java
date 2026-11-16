package com.driveease.service;

import com.driveease.dto.VehicleDto;
import com.driveease.dto.VehicleRequest;
import com.driveease.model.FuelType;
import com.driveease.model.TransmissionType;
import com.driveease.model.Vehicle;
import com.driveease.model.VehicleCategory;
import com.driveease.model.VehicleOrigin;

import java.math.BigDecimal;
import java.util.List;

public interface VehicleService {

    List<VehicleDto> getAllVehicles(
            VehicleCategory category,
            String search,
            FuelType fuelType,
            TransmissionType transmission,
            Boolean availableOnly,
            Boolean premium,
            VehicleOrigin origin,
            BigDecimal minPrice,
            BigDecimal maxPrice,
            String sortBy
    );

    VehicleDto getVehicleById(Long id);

    Vehicle getVehicleEntity(Long id);

    List<VehicleDto> getAvailableVehicles();

    List<VehicleDto> getFeaturedVehicles();

    List<VehicleDto> getPremiumVehicles();

    VehicleDto createVehicle(VehicleRequest request);

    VehicleDto updateVehicle(Long id, VehicleRequest request);

    void deleteVehicle(Long id);

    VehicleDto toggleAvailability(Long id, boolean available);

    VehicleDto togglePremium(Long id, boolean premium);
}
