package com.driveease.service;

import com.driveease.dto.BookingDto;
import com.driveease.dto.DashboardSummaryDto;
import com.driveease.model.Role;
import com.driveease.repository.BookingRepository;
import com.driveease.repository.UserRepository;
import com.driveease.repository.VehicleRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional(readOnly = true)
public class DashboardServiceImpl implements DashboardService {

    private final VehicleRepository vehicleRepository;
    private final UserRepository userRepository;
    private final BookingRepository bookingRepository;

    public DashboardServiceImpl(VehicleRepository vehicleRepository,
                                UserRepository userRepository,
                                BookingRepository bookingRepository) {
        this.vehicleRepository = vehicleRepository;
        this.userRepository = userRepository;
        this.bookingRepository = bookingRepository;
    }

    @Override
    public DashboardSummaryDto getDashboardSummary() {
        long totalVehicles = vehicleRepository.count();
        long availableVehicles = vehicleRepository.countByAvailableTrue();
        long totalCustomers = userRepository.countByRole(Role.ROLE_CUSTOMER);
        long totalBookings = bookingRepository.count();
        long activeBookings = bookingRepository.countActiveBookings();
        BigDecimal totalRevenue = bookingRepository.calculateTotalRevenue();

        List<BookingDto> recentBookings = bookingRepository.findAllByOrderByCreatedAtDesc()
                .stream()
                .limit(6)
                .map(BookingDto::new)
                .collect(Collectors.toList());

        return new DashboardSummaryDto(
                totalVehicles,
                availableVehicles,
                totalCustomers,
                totalBookings,
                activeBookings,
                totalRevenue != null ? totalRevenue : BigDecimal.ZERO,
                recentBookings
        );
    }
}
