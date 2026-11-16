package com.driveease.repository;

import com.driveease.model.FuelType;
import com.driveease.model.TransmissionType;
import com.driveease.model.Vehicle;
import com.driveease.model.VehicleCategory;
import com.driveease.model.VehicleOrigin;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.math.BigDecimal;
import java.util.List;

@Repository
public interface VehicleRepository extends JpaRepository<Vehicle, Long> {

    List<Vehicle> findByAvailableTrue();

    List<Vehicle> findByCategory(VehicleCategory category);

    @Query("SELECT v FROM Vehicle v WHERE " +
           "(:category IS NULL OR v.category = :category) AND " +
           "(:fuelType IS NULL OR v.fuelType = :fuelType) AND " +
           "(:transmission IS NULL OR v.transmission = :transmission) AND " +
           "(:availableOnly IS NULL OR :availableOnly = false OR v.available = true) AND " +
           "(:premium IS NULL OR v.isPremium = :premium) AND " +
           "(:origin IS NULL OR v.vehicleOrigin = :origin) AND " +
           "(:minPrice IS NULL OR v.dailyRate >= :minPrice) AND " +
           "(:maxPrice IS NULL OR v.dailyRate <= :maxPrice) AND " +
           "(:search IS NULL OR :search = '' OR " +
           "  LOWER(v.brand) LIKE LOWER(CONCAT('%', :search, '%')) OR " +
           "  LOWER(v.model) LIKE LOWER(CONCAT('%', :search, '%')))")
    List<Vehicle> searchVehicles(
            @Param("category") VehicleCategory category,
            @Param("fuelType") FuelType fuelType,
            @Param("transmission") TransmissionType transmission,
            @Param("availableOnly") Boolean availableOnly,
            @Param("premium") Boolean premium,
            @Param("origin") VehicleOrigin origin,
            @Param("minPrice") BigDecimal minPrice,
            @Param("maxPrice") BigDecimal maxPrice,
            @Param("search") String search,
            Sort sort
    );

    List<Vehicle> findByIsPremiumTrueAndAvailableTrue(Sort sort);

    long countByAvailableTrue();

    long countByIsPremiumTrue();
}
