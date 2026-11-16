-- ==========================================================
-- DriveEase Premium Vehicle Rental System - MySQL 8 Schema
-- ==========================================================

CREATE DATABASE IF NOT EXISTS driveease_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE driveease_db;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'ROLE_CUSTOMER',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. Vehicles Table (Single Table Inheritance for Vehicle, Car, Motorcycle)
CREATE TABLE IF NOT EXISTS vehicles (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    vehicle_type VARCHAR(31) NOT NULL,
    brand VARCHAR(60) NOT NULL,
    model VARCHAR(60) NOT NULL,
    category VARCHAR(20) NOT NULL,
    fuel_type VARCHAR(20) NOT NULL,
    transmission VARCHAR(20) NOT NULL,
    daily_rate DECIMAL(10,2) NOT NULL,
    security_deposit DECIMAL(10,2) DEFAULT 200.00,
    image_url VARCHAR(500),
    description TEXT,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    rating DOUBLE DEFAULT 4.8,
    location VARCHAR(80) DEFAULT 'Downtown Hub',
    features VARCHAR(500),
    -- Car specific columns
    seating_capacity INT,
    luggage_capacity INT,
    car_body_type VARCHAR(40),
    has_air_conditioning BOOLEAN,
    -- Motorcycle specific columns
    engine_cc INT,
    bike_type VARCHAR(40),
    has_helmet_included BOOLEAN
) ENGINE=InnoDB;

-- 3. Bookings Table
CREATE TABLE IF NOT EXISTS bookings (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    booking_number VARCHAR(32) NOT NULL UNIQUE,
    user_id BIGINT NOT NULL,
    vehicle_id BIGINT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_days INT NOT NULL,
    daily_rate DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0.00,
    tax_amount DECIMAL(10,2) NOT NULL,
    security_deposit DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'CONFIRMED',
    pickup_location VARCHAR(120) DEFAULT 'Downtown Hub',
    dropoff_location VARCHAR(120) DEFAULT 'Downtown Hub',
    customer_notes TEXT,
    payment_method VARCHAR(50) DEFAULT 'CREDIT_CARD',
    payment_status VARCHAR(30) DEFAULT 'PAID',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cancelled_at DATETIME NULL,
    CONSTRAINT fk_booking_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_booking_vehicle FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
) ENGINE=InnoDB;
