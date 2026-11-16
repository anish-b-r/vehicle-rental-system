package com.driveease.repository;

import com.driveease.model.Booking;
import com.driveease.model.BookingStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Repository
public interface BookingRepository extends JpaRepository<Booking, Long> {

    List<Booking> findByUserIdOrderByCreatedAtDesc(Long userId);

    List<Booking> findAllByOrderByCreatedAtDesc();

    Optional<Booking> findByBookingNumber(String bookingNumber);

    long countByStatus(BookingStatus status);

    @Query("SELECT COUNT(b) FROM Booking b WHERE b.status = com.driveease.model.BookingStatus.CONFIRMED OR b.status = com.driveease.model.BookingStatus.ACTIVE")
    long countActiveBookings();

    @Query("SELECT COALESCE(SUM(b.totalAmount), 0) FROM Booking b WHERE b.status <> com.driveease.model.BookingStatus.CANCELLED")
    BigDecimal calculateTotalRevenue();

    @Query("SELECT b FROM Booking b WHERE b.vehicle.id = :vehicleId " +
           "AND b.status <> com.driveease.model.BookingStatus.CANCELLED " +
           "AND (b.startDate <= :endDate AND b.endDate >= :startDate)")
    List<Booking> findConflictingBookings(
            @Param("vehicleId") Long vehicleId,
            @Param("startDate") LocalDate startDate,
            @Param("endDate") LocalDate endDate
    );
}
