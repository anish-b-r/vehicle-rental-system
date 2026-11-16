package com.driveease.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;

/**
 * Booking entity representing a rental contract between a customer and a vehicle.
 * Demonstrates OOP business rules, state encapsulation, and domain calculations.
 */
@Entity
@Table(name = "bookings")
public class Booking {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "booking_number", unique = true, nullable = false, length = 32)
    private String bookingNumber;

    @NotNull
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @NotNull
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "vehicle_id", nullable = false)
    private Vehicle vehicle;

    @NotNull
    @Column(name = "start_date", nullable = false)
    private LocalDate startDate;

    @NotNull
    @Column(name = "end_date", nullable = false)
    private LocalDate endDate;

    @Column(name = "total_days", nullable = false)
    private int totalDays;

    @Column(name = "daily_rate", nullable = false, precision = 10, scale = 2)
    private BigDecimal dailyRate;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal subtotal;

    @Column(name = "discount_amount", precision = 10, scale = 2)
    private BigDecimal discountAmount = BigDecimal.ZERO;

    @Column(name = "tax_amount", nullable = false, precision = 10, scale = 2)
    private BigDecimal taxAmount;

    @Column(name = "security_deposit", precision = 10, scale = 2)
    private BigDecimal securityDeposit;

    @Column(name = "total_amount", nullable = false, precision = 10, scale = 2)
    private BigDecimal totalAmount;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private BookingStatus status = BookingStatus.CONFIRMED;

    @Column(name = "pickup_location", length = 120)
    private String pickupLocation = "Downtown Hub";

    @Column(name = "dropoff_location", length = 120)
    private String dropoffLocation = "Downtown Hub";

    @Column(name = "customer_notes", length = 500)
    private String customerNotes;

    @Column(name = "payment_method", length = 50)
    private String paymentMethod = "CREDIT_CARD";

    @Column(name = "payment_status", length = 30)
    private String paymentStatus = "PAID";

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    @Column(name = "cancelled_at")
    private LocalDateTime cancelledAt;

    public Booking() {
    }

    public Booking(User user, Vehicle vehicle, LocalDate startDate, LocalDate endDate,
                   String pickupLocation, String dropoffLocation, String paymentMethod, String notes) {
        this.user = user;
        this.vehicle = vehicle;
        this.startDate = startDate;
        this.endDate = endDate;
        this.pickupLocation = (pickupLocation != null && !pickupLocation.isBlank()) ? pickupLocation : vehicle.getLocation();
        this.dropoffLocation = (dropoffLocation != null && !dropoffLocation.isBlank()) ? dropoffLocation : this.pickupLocation;
        this.paymentMethod = (paymentMethod != null && !paymentMethod.isBlank()) ? paymentMethod : "CREDIT_CARD";
        this.customerNotes = notes;
        this.status = BookingStatus.CONFIRMED;
        this.paymentStatus = "PAID";
        this.createdAt = LocalDateTime.now();
        this.dailyRate = vehicle.getDailyRate();

        // Calculate days and pricing
        calculatePricing();
    }

    /**
     * Domain business method to calculate days, subtotal, tax, deposit, and total.
     */
    public void calculatePricing() {
        if (startDate == null || endDate == null) {
            return;
        }
        long days = ChronoUnit.DAYS.between(startDate, endDate);
        if (days <= 0) {
            days = 1; // minimum 1 day rental
        }
        this.totalDays = (int) days;
        this.dailyRate = vehicle != null ? vehicle.getDailyRate() : BigDecimal.ZERO;
        this.subtotal = dailyRate.multiply(BigDecimal.valueOf(this.totalDays));

        // Weekly discount of 10% for rentals >= 7 days (OOP business rule)
        if (this.totalDays >= 7) {
            this.discountAmount = subtotal.multiply(new BigDecimal("0.10"));
        } else {
            this.discountAmount = BigDecimal.ZERO;
        }

        BigDecimal netSubtotal = subtotal.subtract(this.discountAmount);
        // 10% tax rate
        this.taxAmount = netSubtotal.multiply(new BigDecimal("0.10"));
        this.securityDeposit = vehicle != null ? vehicle.getSecurityDeposit() : new BigDecimal("200.00");
        this.totalAmount = netSubtotal.add(this.taxAmount).add(this.securityDeposit);
    }

    /**
     * Business method to check if this booking can be cancelled.
     * Rule: Can be cancelled if status is PENDING or CONFIRMED and start date is in the future.
     */
    public boolean canBeCancelled() {
        if (this.status == BookingStatus.CANCELLED || this.status == BookingStatus.COMPLETED) {
            return false;
        }
        return !startDate.isBefore(LocalDate.now());
    }

    /**
     * Business method to cancel booking.
     */
    public void cancel() {
        if (!canBeCancelled()) {
            throw new IllegalStateException("Booking cannot be cancelled at this stage");
        }
        this.status = BookingStatus.CANCELLED;
        this.cancelledAt = LocalDateTime.now();
        this.paymentStatus = "REFUNDED";
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getBookingNumber() {
        return bookingNumber;
    }

    public void setBookingNumber(String bookingNumber) {
        this.bookingNumber = bookingNumber;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public Vehicle getVehicle() {
        return vehicle;
    }

    public void setVehicle(Vehicle vehicle) {
        this.vehicle = vehicle;
    }

    public LocalDate getStartDate() {
        return startDate;
    }

    public void setStartDate(LocalDate startDate) {
        this.startDate = startDate;
    }

    public LocalDate getEndDate() {
        return endDate;
    }

    public void setEndDate(LocalDate endDate) {
        this.endDate = endDate;
    }

    public int getTotalDays() {
        return totalDays;
    }

    public void setTotalDays(int totalDays) {
        this.totalDays = totalDays;
    }

    public BigDecimal getDailyRate() {
        return dailyRate;
    }

    public void setDailyRate(BigDecimal dailyRate) {
        this.dailyRate = dailyRate;
    }

    public BigDecimal getSubtotal() {
        return subtotal;
    }

    public void setSubtotal(BigDecimal subtotal) {
        this.subtotal = subtotal;
    }

    public BigDecimal getDiscountAmount() {
        return discountAmount;
    }

    public void setDiscountAmount(BigDecimal discountAmount) {
        this.discountAmount = discountAmount;
    }

    public BigDecimal getTaxAmount() {
        return taxAmount;
    }

    public void setTaxAmount(BigDecimal taxAmount) {
        this.taxAmount = taxAmount;
    }

    public BigDecimal getSecurityDeposit() {
        return securityDeposit;
    }

    public void setSecurityDeposit(BigDecimal securityDeposit) {
        this.securityDeposit = securityDeposit;
    }

    public BigDecimal getTotalAmount() {
        return totalAmount;
    }

    public void setTotalAmount(BigDecimal totalAmount) {
        this.totalAmount = totalAmount;
    }

    public BookingStatus getStatus() {
        return status;
    }

    public void setStatus(BookingStatus status) {
        this.status = status;
    }

    public String getPickupLocation() {
        return pickupLocation;
    }

    public void setPickupLocation(String pickupLocation) {
        this.pickupLocation = pickupLocation;
    }

    public String getDropoffLocation() {
        return dropoffLocation;
    }

    public void setDropoffLocation(String dropoffLocation) {
        this.dropoffLocation = dropoffLocation;
    }

    public String getCustomerNotes() {
        return customerNotes;
    }

    public void setCustomerNotes(String customerNotes) {
        this.customerNotes = customerNotes;
    }

    public String getPaymentMethod() {
        return paymentMethod;
    }

    public void setPaymentMethod(String paymentMethod) {
        this.paymentMethod = paymentMethod;
    }

    public String getPaymentStatus() {
        return paymentStatus;
    }

    public void setPaymentStatus(String paymentStatus) {
        this.paymentStatus = paymentStatus;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public LocalDateTime getCancelledAt() {
        return cancelledAt;
    }

    public void setCancelledAt(LocalDateTime cancelledAt) {
        this.cancelledAt = cancelledAt;
    }
}
