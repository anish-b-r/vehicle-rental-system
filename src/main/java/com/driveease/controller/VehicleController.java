package com.driveease.controller;

import com.driveease.dto.ApiResponse;
import com.driveease.dto.VehicleDto;
import com.driveease.model.FuelType;
import com.driveease.model.TransmissionType;
import com.driveease.model.VehicleCategory;
import com.driveease.model.VehicleOrigin;
import com.driveease.service.VehicleService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.List;

@RestController
@RequestMapping("/api/vehicles")
public class VehicleController {

    private final VehicleService vehicleService;

    public VehicleController(VehicleService vehicleService) {
        this.vehicleService = vehicleService;
    }

    @GetMapping
    public ResponseEntity<ApiResponse<List<VehicleDto>>> getAllVehicles(
            @RequestParam(required = false) VehicleCategory category,
            @RequestParam(required = false) String search,
            @RequestParam(required = false) FuelType fuelType,
            @RequestParam(required = false) TransmissionType transmission,
            @RequestParam(required = false) Boolean availableOnly,
            @RequestParam(required = false) Boolean premium,
            @RequestParam(required = false) VehicleOrigin origin,
            @RequestParam(required = false) BigDecimal minPrice,
            @RequestParam(required = false) BigDecimal maxPrice,
            @RequestParam(required = false, defaultValue = "price_asc") String sortBy
    ) {
        List<VehicleDto> vehicles = vehicleService.getAllVehicles(category, search, fuelType, transmission, availableOnly, premium, origin, minPrice, maxPrice, sortBy);
        return ResponseEntity.ok(ApiResponse.success(vehicles));
    }

    @GetMapping("/premium")
    public ResponseEntity<ApiResponse<List<VehicleDto>>> getPremiumVehicles() {
        List<VehicleDto> vehicles = vehicleService.getPremiumVehicles();
        return ResponseEntity.ok(ApiResponse.success(vehicles));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<VehicleDto>> getVehicleById(@PathVariable Long id) {
        VehicleDto vehicle = vehicleService.getVehicleById(id);
        return ResponseEntity.ok(ApiResponse.success(vehicle));
    }

    @GetMapping("/available")
    public ResponseEntity<ApiResponse<List<VehicleDto>>> getAvailableVehicles() {
        List<VehicleDto> vehicles = vehicleService.getAvailableVehicles();
        return ResponseEntity.ok(ApiResponse.success(vehicles));
    }

    @GetMapping("/featured")
    public ResponseEntity<ApiResponse<List<VehicleDto>>> getFeaturedVehicles() {
        List<VehicleDto> vehicles = vehicleService.getFeaturedVehicles();
        return ResponseEntity.ok(ApiResponse.success(vehicles));
    }
}
