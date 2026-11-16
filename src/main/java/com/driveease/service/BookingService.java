package com.driveease.service;

import com.driveease.dto.BookingDto;
import com.driveease.dto.BookingRequest;
import com.driveease.model.BookingStatus;

import java.util.List;

public interface BookingService {

    BookingDto createBooking(BookingRequest request, String userEmail);

    List<BookingDto> getBookingsForUser(String userEmail);

    BookingDto getBookingById(Long id, String userEmail);

    BookingDto cancelBooking(Long id, String userEmail);

    List<BookingDto> getAllBookings();

    BookingDto updateBookingStatus(Long id, BookingStatus status);
}
