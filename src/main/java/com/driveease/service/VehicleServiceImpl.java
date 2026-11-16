package com.driveease.service;

import com.driveease.dto.VehicleDto;
import com.driveease.dto.VehicleRequest;
import com.driveease.exception.ResourceNotFoundException;
import com.driveease.model.*;
import com.driveease.repository.VehicleRepository;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class VehicleServiceImpl implements VehicleService {

    private final VehicleRepository vehicleRepository;

    public VehicleServiceImpl(VehicleRepository vehicleRepository) {
        this.vehicleRepository = vehicleRepository;
    }

    @Override
    @Transactional(readOnly = true)
    public List<VehicleDto> getAllVehicles(VehicleCategory category,
            String search,
            FuelType fuelType,
            TransmissionType transmission,
            Boolean availableOnly,
            Boolean premium,
            VehicleOrigin origin,
            BigDecimal minPrice,
            BigDecimal maxPrice,
            String sortBy) {
        Sort sort = Sort.by(Sort.Direction.ASC, "dailyRate");
        if ("price_desc".equalsIgnoreCase(sortBy)) {
            sort = Sort.by(Sort.Direction.DESC, "dailyRate");
        } else if ("rating".equalsIgnoreCase(sortBy)) {
            sort = Sort.by(Sort.Direction.DESC, "rating");
        } else if ("brand".equalsIgnoreCase(sortBy)) {
            sort = Sort.by(Sort.Direction.ASC, "brand");
        }

        return vehicleRepository
                .searchVehicles(category, fuelType, transmission, availableOnly, premium, origin, minPrice, maxPrice,
                        search, sort)
                .stream()
                .map(VehicleDto::new)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<VehicleDto> getPremiumVehicles() {
        Sort sort = Sort.by(Sort.Direction.DESC, "dailyRate");
        return vehicleRepository.findByIsPremiumTrueAndAvailableTrue(sort)
                .stream()
                .map(VehicleDto::new)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public VehicleDto getVehicleById(Long id) {
        return new VehicleDto(getVehicleEntity(id));
    }

    @Override
    @Transactional(readOnly = true)
    public Vehicle getVehicleEntity(Long id) {
        return vehicleRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Vehicle not found with id: " + id));
    }

    @Override
    @Transactional(readOnly = true)
    public List<VehicleDto> getAvailableVehicles() {
        return vehicleRepository.findByAvailableTrue()
                .stream()
                .map(VehicleDto::new)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<VehicleDto> getFeaturedVehicles() {
        // Return available vehicles ordered by rating (top 6)
        return vehicleRepository.findByAvailableTrue()
                .stream()
                .sorted((a, b) -> Double.compare(b.getRating() != null ? b.getRating() : 0,
                        a.getRating() != null ? a.getRating() : 0))
                .limit(6)
                .map(VehicleDto::new)
                .collect(Collectors.toList());
    }

    @Override
    public VehicleDto createVehicle(VehicleRequest req) {
        Vehicle vehicle;

        if (req.getCategory() == VehicleCategory.BIKE) {
            Motorcycle bike = new Motorcycle();
            bike.setEngineCc(req.getEngineCc() != null ? req.getEngineCc() : 650);
            bike.setBikeType(req.getBikeType() != null ? req.getBikeType() : "Sport");
            bike.setHasHelmetIncluded(req.getHasHelmetIncluded() != null ? req.getHasHelmetIncluded() : true);
            vehicle = bike;
        } else {
            Car car = new Car();
            car.setSeatingCapacity(req.getSeatingCapacity() != null ? req.getSeatingCapacity() : 5);
            car.setLuggageCapacity(req.getLuggageCapacity() != null ? req.getLuggageCapacity() : 2);
            car.setBodyType(req.getBodyType() != null ? req.getBodyType() : "Sedan");
            car.setHasAirConditioning(req.getHasAirConditioning() != null ? req.getHasAirConditioning() : true);
            vehicle = car;
        }

        populateCommonVehicleFields(vehicle, req);
        Vehicle saved = vehicleRepository.save(vehicle);
        return new VehicleDto(saved);
    }

    @Override
    public VehicleDto updateVehicle(Long id, VehicleRequest req) {
        Vehicle vehicle = getVehicleEntity(id);

        populateCommonVehicleFields(vehicle, req);

        if (vehicle instanceof Car car) {
            if (req.getSeatingCapacity() != null)
                car.setSeatingCapacity(req.getSeatingCapacity());
            if (req.getLuggageCapacity() != null)
                car.setLuggageCapacity(req.getLuggageCapacity());
            if (req.getBodyType() != null)
                car.setBodyType(req.getBodyType());
            if (req.getHasAirConditioning() != null)
                car.setHasAirConditioning(req.getHasAirConditioning());
        } else if (vehicle instanceof Motorcycle bike) {
            if (req.getEngineCc() != null)
                bike.setEngineCc(req.getEngineCc());
            if (req.getBikeType() != null)
                bike.setBikeType(req.getBikeType());
            if (req.getHasHelmetIncluded() != null)
                bike.setHasHelmetIncluded(req.getHasHelmetIncluded());
        }

        Vehicle updated = vehicleRepository.save(vehicle);
        return new VehicleDto(updated);
    }

    @Override
    public void deleteVehicle(Long id) {
        Vehicle vehicle = getVehicleEntity(id);
        vehicleRepository.delete(vehicle);
    }

    @Override
    public VehicleDto toggleAvailability(Long id, boolean available) {
        Vehicle vehicle = getVehicleEntity(id);
        vehicle.setAvailable(available);
        return new VehicleDto(vehicleRepository.save(vehicle));
    }

    @Override
    public VehicleDto togglePremium(Long id, boolean premium) {
        Vehicle vehicle = getVehicleEntity(id);
        vehicle.setPremium(premium);
        return new VehicleDto(vehicleRepository.save(vehicle));
    }

    private void populateCommonVehicleFields(Vehicle vehicle, VehicleRequest req) {
        vehicle.setBrand(req.getBrand().trim());
        vehicle.setModel(req.getModel().trim());
        vehicle.setCategory(req.getCategory());
        vehicle.setFuelType(req.getFuelType());
        vehicle.setTransmission(req.getTransmission());
        vehicle.setDailyRate(req.getDailyRate());
        if (req.getSecurityDeposit() != null) {
            vehicle.setSecurityDeposit(req.getSecurityDeposit());
        }
        vehicle.setImageUrl(req.getImageUrl());
        vehicle.setDescription(req.getDescription());
        if (req.getAvailable() != null) {
            vehicle.setAvailable(req.getAvailable());
        }
        if (req.getRating() != null) {
            vehicle.setRating(req.getRating());
        }
        if (req.getLocation() != null && !req.getLocation().isBlank()) {
            vehicle.setLocation(req.getLocation());
        }
        vehicle.setFeatures(req.getFeatures());
        if (req.getIsPremium() != null) {
            vehicle.setPremium(req.getIsPremium());
        }
        if (req.getVehicleOrigin() != null) {
            vehicle.setVehicleOrigin(req.getVehicleOrigin());
        }
    }
}
