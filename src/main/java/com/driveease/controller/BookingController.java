package com.driveease.controller;

import com.driveease.dto.ApiResponse;
import com.driveease.dto.BookingDto;
import com.driveease.dto.BookingRequest;
import com.driveease.service.BookingService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/bookings")
public class BookingController {

    private final BookingService bookingService;

    public BookingController(BookingService bookingService) {
        this.bookingService = bookingService;
    }

    @PostMapping
    public ResponseEntity<ApiResponse<BookingDto>> createBooking(@Valid @RequestBody BookingRequest request,
                                                                 Authentication authentication) {
        BookingDto booking = bookingService.createBooking(request, authentication.getName());
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success("Booking confirmed successfully!", booking));
    }

    @GetMapping("/my")
    public ResponseEntity<ApiResponse<List<BookingDto>>> getMyBookings(Authentication authentication) {
        List<BookingDto> bookings = bookingService.getBookingsForUser(authentication.getName());
        return ResponseEntity.ok(ApiResponse.success(bookings));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<BookingDto>> getBookingById(@PathVariable Long id,
                                                                 Authentication authentication) {
        BookingDto booking = bookingService.getBookingById(id, authentication.getName());
        return ResponseEntity.ok(ApiResponse.success(booking));
    }

    @PatchMapping("/{id}/cancel")
    public ResponseEntity<ApiResponse<BookingDto>> cancelBooking(@PathVariable Long id,
                                                                 Authentication authentication) {
        BookingDto booking = bookingService.cancelBooking(id, authentication.getName());
        return ResponseEntity.ok(ApiResponse.success("Booking cancelled successfully. Security deposit refunded.", booking));
    }
}
