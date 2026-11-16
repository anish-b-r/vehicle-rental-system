package com.driveease.dto;

import java.math.BigDecimal;
import java.util.List;

public class DashboardSummaryDto {

    private long totalVehicles;
    private long availableVehicles;
    private long totalCustomers;
    private long totalBookings;
    private long activeBookings;
    private BigDecimal totalRevenue;
    private List<BookingDto> recentBookings;

    public DashboardSummaryDto() {
    }

    public DashboardSummaryDto(long totalVehicles, long availableVehicles, long totalCustomers,
                               long totalBookings, long activeBookings, BigDecimal totalRevenue,
                               List<BookingDto> recentBookings) {
        this.totalVehicles = totalVehicles;
        this.availableVehicles = availableVehicles;
        this.totalCustomers = totalCustomers;
        this.totalBookings = totalBookings;
        this.activeBookings = activeBookings;
        this.totalRevenue = totalRevenue;
        this.recentBookings = recentBookings;
    }

    public long getTotalVehicles() {
        return totalVehicles;
    }

    public void setTotalVehicles(long totalVehicles) {
        this.totalVehicles = totalVehicles;
    }

    public long getAvailableVehicles() {
        return availableVehicles;
    }

    public void setAvailableVehicles(long availableVehicles) {
        this.availableVehicles = availableVehicles;
    }

    public long getTotalCustomers() {
        return totalCustomers;
    }

    public void setTotalCustomers(long totalCustomers) {
        this.totalCustomers = totalCustomers;
    }

    public long getTotalBookings() {
        return totalBookings;
    }

    public void setTotalBookings(long totalBookings) {
        this.totalBookings = totalBookings;
    }

    public long getActiveBookings() {
        return activeBookings;
    }

    public void setActiveBookings(long activeBookings) {
        this.activeBookings = activeBookings;
    }

    public BigDecimal getTotalRevenue() {
        return totalRevenue;
    }

    public void setTotalRevenue(BigDecimal totalRevenue) {
        this.totalRevenue = totalRevenue;
    }

    public List<BookingDto> getRecentBookings() {
        return recentBookings;
    }

    public void setRecentBookings(List<BookingDto> recentBookings) {
        this.recentBookings = recentBookings;
    }
}
