package com.driveease.controller;

import com.driveease.dto.*;
import com.driveease.service.BookingService;
import com.driveease.service.DashboardService;
import com.driveease.service.UserService;
import com.driveease.service.VehicleService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/admin")
public class AdminController {

    private final DashboardService dashboardService;
    private final VehicleService vehicleService;
    private final BookingService bookingService;
    private final UserService userService;

    public AdminController(DashboardService dashboardService,
                           VehicleService vehicleService,
                           BookingService bookingService,
                           UserService userService) {
        this.dashboardService = dashboardService;
        this.vehicleService = vehicleService;
        this.bookingService = bookingService;
        this.userService = userService;
    }

    @GetMapping("/dashboard")
    public ResponseEntity<ApiResponse<DashboardSummaryDto>> getDashboardSummary() {
        DashboardSummaryDto summary = dashboardService.getDashboardSummary();
        return ResponseEntity.ok(ApiResponse.success(summary));
    }

    @GetMapping("/bookings")
    public ResponseEntity<ApiResponse<List<BookingDto>>> getAllBookings() {
        List<BookingDto> bookings = bookingService.getAllBookings();
        return ResponseEntity.ok(ApiResponse.success(bookings));
    }

    @PatchMapping("/bookings/{id}/status")
    public ResponseEntity<ApiResponse<BookingDto>> updateBookingStatus(
            @PathVariable Long id,
            @Valid @RequestBody BookingStatusRequest request) {
        BookingDto updated = bookingService.updateBookingStatus(id, request.getStatus());
        return ResponseEntity.ok(ApiResponse.success("Booking status updated to " + request.getStatus(), updated));
    }

    @PostMapping("/vehicles")
    public ResponseEntity<ApiResponse<VehicleDto>> createVehicle(@Valid @RequestBody VehicleRequest request) {
        VehicleDto created = vehicleService.createVehicle(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success("Vehicle added to fleet successfully", created));
    }

    @PutMapping("/vehicles/{id}")
    public ResponseEntity<ApiResponse<VehicleDto>> updateVehicle(
            @PathVariable Long id,
            @Valid @RequestBody VehicleRequest request) {
        VehicleDto updated = vehicleService.updateVehicle(id, request);
        return ResponseEntity.ok(ApiResponse.success("Vehicle updated successfully", updated));
    }

    @DeleteMapping("/vehicles/{id}")
    public ResponseEntity<ApiResponse<Void>> deleteVehicle(@PathVariable Long id) {
        vehicleService.deleteVehicle(id);
        return ResponseEntity.ok(ApiResponse.success("Vehicle removed from fleet", null));
    }

    @PatchMapping("/vehicles/{id}/availability")
    public ResponseEntity<ApiResponse<VehicleDto>> toggleAvailability(
            @PathVariable Long id,
            @RequestParam boolean available) {
        VehicleDto updated = vehicleService.toggleAvailability(id, available);
        return ResponseEntity.ok(ApiResponse.success("Vehicle availability updated", updated));
    }

    @PatchMapping("/vehicles/{id}/premium")
    public ResponseEntity<ApiResponse<VehicleDto>> togglePremium(
            @PathVariable Long id,
            @RequestParam boolean premium) {
        VehicleDto updated = vehicleService.togglePremium(id, premium);
        return ResponseEntity.ok(ApiResponse.success("Vehicle premium status updated", updated));
    }

    @GetMapping("/customers")
    public ResponseEntity<ApiResponse<List<UserDto>>> getAllCustomers() {
        List<UserDto> customers = userService.getAllCustomers();
        return ResponseEntity.ok(ApiResponse.success(customers));
    }
}
