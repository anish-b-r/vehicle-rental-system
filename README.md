# DriveEase — Premium Vehicle Rental System

> **College Java OOP Full-Stack Project**  
> A modern, commercial-grade Vehicle Rental Web Application built with Java 21, Spring Boot, Spring Security, Spring Data JPA, and responsive Bootstrap 5 with custom CSS design tokens.

---

## 🌟 Executive Summary & Design Philosophy

DriveEase is modeled after top-tier automotive and modern mobility platforms (such as Porsche Drive, Silvercar, and minimalist SaaS dashboards) rather than generic student assignments. It provides:
- **Flawless User Experience**: Fluid booking flow, real-time dynamic pricing calculation, responsive layouts across desktop, tablet, and mobile.
- **Enterprise-Grade Architecture**: Single-monolith Spring Boot application serving both RESTful backend APIs and static frontend resources.
- **Robust Security**: BCrypt password encryption, session-based Spring Security with role-based access control (`ROLE_CUSTOMER`, `ROLE_ADMIN`).
- **Flexible Database**: Runs instantly out-of-the-box with embedded in-memory H2 (MySQL mode) or seamlessly connects to a production MySQL 8 instance.

---

## 🏛️ Object-Oriented Programming (OOP) Principles Demonstrated

This project serves as an exemplar of core Object-Oriented Programming concepts in Java:

### 1. Encapsulation
- All domain entity state is strictly encapsulated with `private` fields and accessed via validated accessors and business methods.
- Domain rules are encapsulated inside models (e.g., `Booking.calculatePricing()`, `Booking.canBeCancelled()`, `Booking.cancel()`, `User.isAdmin()`).

### 2. Inheritance & Class Hierarchies
- **`Vehicle` (Abstract Base Entity)**: Uses JPA `@Inheritance(strategy = InheritanceType.SINGLE_TABLE)` with `@DiscriminatorColumn(name = "vehicle_type")`.
  - **`Car`**: Extends `Vehicle`, introducing `seatingCapacity`, `luggageCapacity`, `bodyType`, and `hasAirConditioning`.
  - **`Motorcycle`**: Extends `Vehicle`, introducing `engineCc`, `bikeType`, and `hasHelmetIncluded`.

### 3. Polymorphism
- Abstract methods defined in `Vehicle`:
  - `public abstract String getVehicleSpecificationsSummary();`
  - `public abstract BigDecimal calculateBaseInsurance(int days);`
- Implemented and overridden distinctly in both `Car` and `Motorcycle` subclasses.
- **Strategy Design Pattern**: Polymorphic pricing strategies (`RentalPricingStrategy` implemented by `StandardPricingStrategy` and `WeeklyDiscountPricingStrategy` providing 10% saver discount for week-long rentals).

### 4. Abstraction & Layered Architecture
- Layered separation of concerns:
  - **Controller Layer** (`com.driveease.controller`): Handles HTTP routing, request validation, and API responses.
  - **Service Layer** (`com.driveease.service`): Enforces business transactions and domain logic behind clear interfaces (`VehicleService`, `BookingService`, `UserService`, `DashboardService`).
  - **Data Access Layer** (`com.driveease.repository`): Spring Data JPA repositories with custom JPQL queries.
  - **Data Transfer Objects** (`com.driveease.dto`): Decouples internal database entities from external API contracts.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Language** | Java 21 (Temurin JDK 21 LTS) |
| **Framework** | Spring Boot 4 / Spring WebMVC |
| **Persistence** | Spring Data JPA, Hibernate ORM |
| **Security** | Spring Security (BCrypt hashing, Session management, RBAC) |
| **Build Tool** | Apache Maven with Maven Wrapper (`mvnw` / `mvnw.cmd`) |
| **Database** | MySQL 8 compatible (Default: H2 in-memory in MySQL mode; MySQL 8 ready) |
| **Frontend** | HTML5, CSS3, JavaScript (Fetch API, ES6+), Bootstrap 5.3, Bootstrap Icons |
| **Typography** | Inter (Google Fonts) |

---

## 🎨 Design System & Color Palette

- **Primary**: Charcoal Black (`#17191D`)
- **Accent / Secondary**: Deep Navy (`#233B5D`)
- **Background**: Off-White (`#F7F8FA`)
- **Card Surfaces**: Pure White (`#FFFFFF`)
- **Muted Elements**: Cool Grey (`#777E87`)
- **Borders**: Subtle Grey (`#E5E8EB`)

---

## 📁 Project Directory Structure

```
c:\Users\B R ANISH\Desktop\oops-project\
├── pom.xml
├── mvnw / mvnw.cmd
├── src
│   ├── main
│   │   ├── java
│   │   │   └── com
│   │   │       └── driveease
│   │   │           ├── DriveeaseApplication.java
│   │   │           ├── config
│   │   │           │   ├── DataInitializer.java        # Fleet & user seeder
│   │   │           │   └── SecurityConfig.java         # Spring Security RBAC
│   │   │           ├── controller
│   │   │           │   ├── AdminController.java        # /api/admin/**
│   │   │           │   ├── AuthController.java         # /api/auth/**
│   │   │           │   ├── BookingController.java      # /api/bookings/**
│   │   │           │   └── VehicleController.java      # /api/vehicles/**
│   │   │           ├── dto                             # Request/Response DTOs
│   │   │           ├── exception                       # Global Exception Handler
│   │   │           ├── model                           # Domain entities & enums
│   │   │           │   ├── Booking.java
│   │   │           │   ├── Car.java
│   │   │           │   ├── Motorcycle.java
│   │   │           │   ├── User.java
│   │   │           │   └── Vehicle.java
│   │   │           ├── repository                      # Spring Data JPA interfaces
│   │   │           ├── service                         # Service contracts & impls
│   │   │           └── strategy                        # Strategy pattern for pricing
│   │   └── resources
│   │       ├── application.properties                  # H2 zero-setup config
│   │       ├── application-mysql.properties            # MySQL 8 config
│   │       ├── schema-mysql.sql                        # Production MySQL 8 DDL
│   │       ├── data-mysql.sql                          # Production MySQL 8 DML
│   │       └── static                                  # Frontend Single-Monolith UI
│   │           ├── index.html                          # Home Page
│   │           ├── vehicles.html                       # Fleet Exploration & Filtering
│   │           ├── vehicle-details.html                # Details & Live Price Calculator
│   │           ├── login.html                          # Sign In (with 1-click test fill)
│   │           ├── register.html                       # Customer Registration
│   │           ├── booking.html                        # Booking Checkout Flow
│   │           ├── my-bookings.html                    # Customer Dashboard
│   │           ├── admin.html                          # Admin Dashboard & Fleet CRUD
│   │           ├── css
│   │           │   ├── style.css                       # Master Design System
│   │           │   └── dashboard.css                   # Admin & Customer Dashboard styles
│   │           └── js
│   │               ├── app.js                          # Core API & Auth State
│   │               ├── auth.js                         # Login/Register validation
│   │               ├── vehicles.js                     # Fleet filter/search logic
│   │               ├── booking.js                      # Details & live calculator
│   │               ├── dashboard.js                    # Customer dashboard & receipts
│   │               └── admin.js                        # Admin KPI & Fleet CRUD
```

---

## 🚀 Quick Start Guide

### 1. Requirements
- **Java 21** (JDK 21 LTS)
- PowerShell or Terminal

### 2. Run the Application
Open PowerShell in the project directory and run:
```powershell
$env:JAVA_HOME = "C:\Users\B R ANISH\.jdks\jdk-21.0.13+9" # or your local JDK 21 path
.\mvnw.cmd spring-boot:run
```

Once started, open your web browser at:
👉 **[http://localhost:8080](http://localhost:8080)**

---

## 🔑 Default Evaluation Accounts

The database is pre-seeded with vehicles, sample users, and existing bookings:

| Role | Email | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@driveease.com` | `admin123` | Full access to Admin Portal (`admin.html`), KPI stats, Fleet CRUD, Booking status manager, Customer directory. |
| **Customer** | `john@example.com` | `customer123` | Browse fleet, create bookings, view booking history, cancel eligible reservations. |
| **Customer 2** | `sophia@example.com` | `customer123` | Active sports motorbike rental. |

> **Pro Tip**: On the `login.html` page, click the **"Customer Login"** or **"Admin Login"** buttons to auto-populate the credentials instantly!

---

## 🔌 REST API Endpoints Overview

### Authentication (`/api/auth`)
- `POST /api/auth/register` — Register a new customer
- `POST /api/auth/login` — Sign in and establish session
- `POST /api/auth/logout` — Invalidate session
- `GET /api/auth/me` — Retrieve active user profile

### Vehicles (`/api/vehicles`)
- `GET /api/vehicles` — Filter vehicles (`category`, `search`, `fuelType`, `transmission`, `minPrice`, `maxPrice`, `availableOnly`, `sortBy`)
- `GET /api/vehicles/{id}` — Get single vehicle details
- `GET /api/vehicles/available` — Get available vehicles
- `GET /api/vehicles/featured` — Get top rated featured vehicles

### Bookings (`/api/bookings`)
- `POST /api/bookings` — Create a new rental reservation
- `GET /api/bookings/my` — Get logged-in customer's bookings
- `GET /api/bookings/{id}` — Get booking details
- `PATCH /api/bookings/{id}/cancel` — Cancel booking and initiate deposit refund

### Administrator (`/api/admin`)
- `GET /api/admin/dashboard` — Overview KPI metrics and recent bookings
- `GET /api/admin/bookings` — View all system bookings
- `PATCH /api/admin/bookings/{id}/status` — Update booking status (`CONFIRMED`, `ACTIVE`, `COMPLETED`, `CANCELLED`)
- `POST /api/admin/vehicles` — Add new vehicle to fleet
- `PUT /api/admin/vehicles/{id}` — Update vehicle specifications
- `DELETE /api/admin/vehicles/{id}` — Remove vehicle from fleet
- `PATCH /api/admin/vehicles/{id}/availability` — Quick toggle availability
- `GET /api/admin/customers` — List registered customers

---

---

## ☁️ Deploying to Render

DriveEase includes a pre-configured multi-stage `Dockerfile` and `render.yaml` Blueprint for deployment on [Render](https://render.com).

### Option 1: 1-Click Blueprint (Recommended)
1. Push this repository to your GitHub account (`git push origin main`).
2. Log in to [Render Dashboard](https://dashboard.render.com).
3. Click **New +** → **Blueprint**.
4. Select your `vehicle-rental-system` repository.
5. Click **Apply**. Render will automatically detect `render.yaml`, build the Docker container with Java 21, and deploy the service.

### Option 2: Manual Web Service Setup
1. In Render Dashboard, click **New +** → **Web Service**.
2. Connect your GitHub repository.
3. Configure the following settings:
   - **Name**: `driveease-rental` (or your choice)
   - **Language / Environment**: `Docker`
   - **Dockerfile Path**: `./Dockerfile`
   - **Instance Type**: `Free`
4. Click **Create Web Service**.
5. Once built (takes ~2 minutes on first build), your live URL will be ready at `https://your-service-name.onrender.com`.

> [!NOTE]
> **Zero-Config Database**: By default, the application runs on embedded H2 in MySQL compatibility mode. On startup, it automatically seeds all 36 authentic vehicles, user accounts, sample bookings, and live currency rates.
> 
> **Connecting External MySQL (Optional)**: If you wish to use an external managed MySQL database (e.g. from Aiven, Clever Cloud, or Supabase), simply add these Environment Variables in your Render Service Dashboard:
> - `SPRING_DATASOURCE_URL`: `jdbc:mysql://<host>:<port>/<dbname>?useSSL=true`
> - `SPRING_DATASOURCE_DRIVER_CLASS_NAME`: `com.mysql.cj.jdbc.Driver`
> - `SPRING_DATASOURCE_USERNAME`: `<db_user>`
> - `SPRING_DATASOURCE_PASSWORD`: `<db_password>`
> - `SPRING_JPA_DATABASE_PLATFORM`: `org.hibernate.dialect.MySQLDialect`

