package com.driveease.service;

import com.driveease.dto.BookingDto;
import com.driveease.dto.BookingRequest;
import com.driveease.exception.BadRequestException;
import com.driveease.exception.ResourceNotFoundException;
import com.driveease.model.*;
import com.driveease.repository.BookingRepository;
import com.driveease.strategy.PricingStrategyFactory;
import com.driveease.strategy.RentalPricingStrategy;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
@Transactional
public class BookingServiceImpl implements BookingService {

    private final BookingRepository bookingRepository;
    private final UserService userService;
    private final VehicleService vehicleService;
    private final PricingStrategyFactory pricingStrategyFactory;

    public BookingServiceImpl(BookingRepository bookingRepository,
                              UserService userService,
                              VehicleService vehicleService,
                              PricingStrategyFactory pricingStrategyFactory) {
        this.bookingRepository = bookingRepository;
        this.userService = userService;
        this.vehicleService = vehicleService;
        this.pricingStrategyFactory = pricingStrategyFactory;
    }

    @Override
    public BookingDto createBooking(BookingRequest request, String userEmail) {
        User user = userService.findByEmail(userEmail);
        Vehicle vehicle = vehicleService.getVehicleEntity(request.getVehicleId());

        if (!vehicle.isAvailable()) {
            throw new BadRequestException("This vehicle is currently marked unavailable for rent.");
        }

        LocalDate start = request.getStartDate();
        LocalDate end = request.getEndDate();

        if (end.isBefore(start)) {
            throw new BadRequestException("Return date cannot be before pickup date.");
        }

        // Check for conflicting active bookings on these dates
        List<Booking> conflicts = bookingRepository.findConflictingBookings(vehicle.getId(), start, end);
        if (!conflicts.isEmpty()) {
            throw new BadRequestException("The selected vehicle is already booked for these dates. Please choose another date range or vehicle.");
        }

        long daysCount = ChronoUnit.DAYS.between(start, end);
        int days = daysCount <= 0 ? 1 : (int) daysCount;

        // Apply Strategy Pattern for pricing calculation
        RentalPricingStrategy strategy = pricingStrategyFactory.getStrategy(days);
        BigDecimal subtotal = strategy.calculateSubtotal(vehicle.getDailyRate(), days);
        BigDecimal discount = strategy.calculateDiscount(subtotal, days);
        BigDecimal netSubtotal = subtotal.subtract(discount);
        BigDecimal tax = netSubtotal.multiply(new BigDecimal("0.10")).setScale(2, RoundingMode.HALF_UP);
        BigDecimal deposit = vehicle.getSecurityDeposit() != null ? vehicle.getSecurityDeposit() : new BigDecimal("3000.00");
        BigDecimal total = netSubtotal.add(tax).add(deposit);

        Booking booking = new Booking();
        booking.setBookingNumber("DE-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase());
        booking.setUser(user);
        booking.setVehicle(vehicle);
        booking.setStartDate(start);
        booking.setEndDate(end);
        booking.setTotalDays(days);
        booking.setDailyRate(vehicle.getDailyRate());
        booking.setSubtotal(subtotal);
        booking.setDiscountAmount(discount);
        booking.setTaxAmount(tax);
        booking.setSecurityDeposit(deposit);
        booking.setTotalAmount(total);
        booking.setStatus(BookingStatus.CONFIRMED);
        booking.setPickupLocation((request.getPickupLocation() != null && !request.getPickupLocation().isBlank())
                ? request.getPickupLocation() : vehicle.getLocation());
        booking.setDropoffLocation((request.getDropoffLocation() != null && !request.getDropoffLocation().isBlank())
                ? request.getDropoffLocation() : booking.getPickupLocation());
        booking.setPaymentMethod((request.getPaymentMethod() != null && !request.getPaymentMethod().isBlank())
                ? request.getPaymentMethod() : "CREDIT_CARD");
        booking.setPaymentStatus("PAID");
        booking.setCustomerNotes(request.getCustomerNotes());
        booking.setCreatedAt(LocalDateTime.now());

        Booking saved = bookingRepository.save(booking);
        return new BookingDto(saved);
    }

    @Override
    @Transactional(readOnly = true)
    public List<BookingDto> getBookingsForUser(String userEmail) {
        User user = userService.findByEmail(userEmail);
        return bookingRepository.findByUserIdOrderByCreatedAtDesc(user.getId())
                .stream()
                .map(BookingDto::new)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public BookingDto getBookingById(Long id, String userEmail) {
        Booking booking = bookingRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found with id: " + id));

        User user = userService.findByEmail(userEmail);
        if (!user.isAdmin() && !booking.getUser().getId().equals(user.getId())) {
            throw new AccessDeniedException("You are not authorized to view this booking");
        }

        return new BookingDto(booking);
    }

    @Override
    public BookingDto cancelBooking(Long id, String userEmail) {
        Booking booking = bookingRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found with id: " + id));

        User user = userService.findByEmail(userEmail);
        if (!user.isAdmin() && !booking.getUser().getId().equals(user.getId())) {
            throw new AccessDeniedException("You are not authorized to cancel this booking");
        }

        if (!booking.canBeCancelled()) {
            throw new BadRequestException("This booking cannot be cancelled because the rental period has started or it has already been finalized.");
        }

        booking.cancel();
        Booking updated = bookingRepository.save(booking);
        return new BookingDto(updated);
    }

    @Override
    @Transactional(readOnly = true)
    public List<BookingDto> getAllBookings() {
        return bookingRepository.findAllByOrderByCreatedAtDesc()
                .stream()
                .map(BookingDto::new)
                .collect(Collectors.toList());
    }

    @Override
    public BookingDto updateBookingStatus(Long id, BookingStatus status) {
        Booking booking = bookingRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found with id: " + id));

        booking.setStatus(status);
        if (status == BookingStatus.CANCELLED) {
            booking.setCancelledAt(LocalDateTime.now());
            booking.setPaymentStatus("REFUNDED");
        } else if (status == BookingStatus.COMPLETED) {
            booking.setPaymentStatus("COMPLETED");
        }

        Booking updated = bookingRepository.save(booking);
        return new BookingDto(updated);
    }
}
