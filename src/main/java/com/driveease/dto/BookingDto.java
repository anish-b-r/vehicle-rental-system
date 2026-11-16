package com.driveease.dto;

import com.driveease.model.Booking;
import com.driveease.model.BookingStatus;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

public class BookingDto {

    private Long id;
    private String bookingNumber;
    private Long userId;
    private String customerName;
    private String customerEmail;
    private String customerPhone;

    private Long vehicleId;
    private String vehicleName;
    private String vehicleBrand;
    private String vehicleModel;
    private String vehicleCategory;
    private String vehicleImageUrl;

    private LocalDate startDate;
    private LocalDate endDate;
    private int totalDays;
    private BigDecimal dailyRate;
    private BigDecimal subtotal;
    private BigDecimal discountAmount;
    private BigDecimal taxAmount;
    private BigDecimal securityDeposit;
    private BigDecimal totalAmount;
    private String currency = "INR";

    private BookingStatus status;
    private String pickupLocation;
    private String dropoffLocation;
    private String paymentMethod;
    private String paymentStatus;
    private String customerNotes;
    private boolean canBeCancelled;
    private LocalDateTime createdAt;
    private LocalDateTime cancelledAt;

    public BookingDto() {
    }

    public BookingDto(Booking booking) {
        if (booking != null) {
            this.id = booking.getId();
            this.bookingNumber = booking.getBookingNumber();

            if (booking.getUser() != null) {
                this.userId = booking.getUser().getId();
                this.customerName = booking.getUser().getFullName();
                this.customerEmail = booking.getUser().getEmail();
                this.customerPhone = booking.getUser().getPhone();
            }

            if (booking.getVehicle() != null) {
                this.vehicleId = booking.getVehicle().getId();
                this.vehicleName = booking.getVehicle().getFullName();
                this.vehicleBrand = booking.getVehicle().getBrand();
                this.vehicleModel = booking.getVehicle().getModel();
                this.vehicleCategory = booking.getVehicle().getCategory().name();
                this.vehicleImageUrl = booking.getVehicle().getImageUrl();
            }

            this.startDate = booking.getStartDate();
            this.endDate = booking.getEndDate();
            this.totalDays = booking.getTotalDays();
            this.dailyRate = booking.getDailyRate();
            this.subtotal = booking.getSubtotal();
            this.discountAmount = booking.getDiscountAmount();
            this.taxAmount = booking.getTaxAmount();
            this.securityDeposit = booking.getSecurityDeposit();
            this.totalAmount = booking.getTotalAmount();
            this.status = booking.getStatus();
            this.pickupLocation = booking.getPickupLocation();
            this.dropoffLocation = booking.getDropoffLocation();
            this.paymentMethod = booking.getPaymentMethod();
            this.paymentStatus = booking.getPaymentStatus();
            this.customerNotes = booking.getCustomerNotes();
            this.canBeCancelled = booking.canBeCancelled();
            this.createdAt = booking.getCreatedAt();
            this.cancelledAt = booking.getCancelledAt();
        }
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

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public String getCustomerName() {
        return customerName;
    }

    public void setCustomerName(String customerName) {
        this.customerName = customerName;
    }

    public String getCustomerEmail() {
        return customerEmail;
    }

    public void setCustomerEmail(String customerEmail) {
        this.customerEmail = customerEmail;
    }

    public String getCustomerPhone() {
        return customerPhone;
    }

    public void setCustomerPhone(String customerPhone) {
        this.customerPhone = customerPhone;
    }

    public Long getVehicleId() {
        return vehicleId;
    }

    public void setVehicleId(Long vehicleId) {
        this.vehicleId = vehicleId;
    }

    public String getVehicleName() {
        return vehicleName;
    }

    public void setVehicleName(String vehicleName) {
        this.vehicleName = vehicleName;
    }

    public String getVehicleBrand() {
        return vehicleBrand;
    }

    public void setVehicleBrand(String vehicleBrand) {
        this.vehicleBrand = vehicleBrand;
    }

    public String getVehicleModel() {
        return vehicleModel;
    }

    public void setVehicleModel(String vehicleModel) {
        this.vehicleModel = vehicleModel;
    }

    public String getVehicleCategory() {
        return vehicleCategory;
    }

    public void setVehicleCategory(String vehicleCategory) {
        this.vehicleCategory = vehicleCategory;
    }

    public String getVehicleImageUrl() {
        return vehicleImageUrl;
    }

    public void setVehicleImageUrl(String vehicleImageUrl) {
        this.vehicleImageUrl = vehicleImageUrl;
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

    public String getCurrency() {
        return currency;
    }

    public void setCurrency(String currency) {
        this.currency = currency;
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

    public String getCustomerNotes() {
        return customerNotes;
    }

    public void setCustomerNotes(String customerNotes) {
        this.customerNotes = customerNotes;
    }

    public boolean isCanBeCancelled() {
        return canBeCancelled;
    }

    public void setCanBeCancelled(boolean canBeCancelled) {
        this.canBeCancelled = canBeCancelled;
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
