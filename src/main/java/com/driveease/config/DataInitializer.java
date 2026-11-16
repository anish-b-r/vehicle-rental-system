package com.driveease.config;

import com.driveease.model.*;
import com.driveease.repository.BookingRepository;
import com.driveease.repository.UserRepository;
import com.driveease.repository.VehicleRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Component
public class DataInitializer implements CommandLineRunner {

    private final UserRepository userRepository;
    private final VehicleRepository vehicleRepository;
    private final BookingRepository bookingRepository;
    private final PasswordEncoder passwordEncoder;

    public DataInitializer(UserRepository userRepository,
                           VehicleRepository vehicleRepository,
                           BookingRepository bookingRepository,
                           PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.vehicleRepository = vehicleRepository;
        this.bookingRepository = bookingRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public void run(String... args) {
        // Reset and seed data fresh to ensure correct image paths
        bookingRepository.deleteAll();
        vehicleRepository.deleteAll();

        seedUsers();
        seedVehicles();
        seedBookings();
    }

    private void seedUsers() {
        upsertUser("DriveEase Administrator", "admin@driveease.com", "+91 98765 43210", "admin123", Role.ROLE_ADMIN);
        upsertUser("John Doe", "john@example.com", "+1 (555) 342-8819", "customer123", Role.ROLE_CUSTOMER);
        upsertUser("Arjun Sharma", "arjun@example.com", "+91 98201 12345", "customer123", Role.ROLE_CUSTOMER);
        upsertUser("Priya Patel", "priya@example.com", "+91 99302 98765", "customer123", Role.ROLE_CUSTOMER);
    }

    private void upsertUser(String fullName, String email, String phone, String rawPassword, Role role) {
        String cleanEmail = email.trim().toLowerCase();
        User user = userRepository.findByEmail(cleanEmail).orElseGet(() -> {
            User u = new User();
            u.setEmail(cleanEmail);
            return u;
        });
        user.setFullName(fullName);
        user.setPhone(phone);
        user.setPassword(passwordEncoder.encode(rawPassword));
        user.setRole(role);
        userRepository.save(user);
    }

    private void seedVehicles() {
        List<Vehicle> list = new ArrayList<>();

        // ==========================================
        // 1. INDIAN ECONOMY & HATCHBACKS
        // ==========================================
        list.add(new Car(
                "Maruti Suzuki", "Swift ZXi",
                FuelType.PETROL, TransmissionType.MANUAL,
                new BigDecimal("1800.00"), new BigDecimal("3000.00"),
                "/images/vehicles/swift.jpg",
                "India's beloved sporty hatchback featuring zippy K-Series dual-jet engine, agile city handling, and class-leading fuel economy.",
                true, 4.7, "Indira Gandhi International Airport (DEL)",
                "Touchscreen SmartPlay Pro, Keyless Push Start, Reverse Camera, Automatic Climate Control, ISOFIX Child Mounts",
                5, 2, "Hatchback", true, false, VehicleOrigin.INDIAN
        ));

        list.add(new Car(
                "Maruti Suzuki", "Baleno Alpha",
                FuelType.PETROL, TransmissionType.AUTOMATIC,
                new BigDecimal("2000.00"), new BigDecimal("3500.00"),
                "/images/vehicles/baleno.jpg",
                "Premium hatchback with spacious cabin, 360-degree view camera, Head-Up Display, and seamless CVT automatic gearbox.",
                true, 4.8, "Connaught Place Hub",
                "Head-Up Display, 360 View Camera, 9-inch HD Infotainment, Arkamys Surround Sound, Cruise Control",
                5, 2, "Hatchback", true, false, VehicleOrigin.INDIAN
        ));

        list.add(new Car(
                "Maruti Suzuki", "Wagon R ZXi+",
                FuelType.PETROL, TransmissionType.MANUAL,
                new BigDecimal("1500.00"), new BigDecimal("2500.00"),
                "/images/vehicles/wagonr.jpg",
                "The quintessential tall-boy hatchback offering maximum interior headroom, easy ingress, and economical city travel.",
                true, 4.6, "Cyber City Gurgaon",
                "SmartPlay Audio, Dual Airbags, Steering Mounted Controls, Power Windows, Split Folding Rear Seats",
                5, 2, "Hatchback", true, false, VehicleOrigin.INDIAN
        ));

        list.add(new Car(
                "Tata", "Tiago XZ+",
                FuelType.PETROL, TransmissionType.MANUAL,
                new BigDecimal("1600.00"), new BigDecimal("3000.00"),
                "/images/vehicles/tiago.jpg",
                "Robust 4-star GNCAP safety rated compact hatchback with Harman premium acoustic sound and solid highway stability.",
                true, 4.7, "Bangalore Kempegowda Airport (BLR)",
                "Harman 8-Speaker Sound, 7-inch Touchscreen, Corner Stability Control, Rear Parking Camera, Projector Headlamps",
                5, 2, "Hatchback", true, false, VehicleOrigin.INDIAN
        ));

        list.add(new Car(
                "Hyundai", "i20 Asta (O)",
                FuelType.PETROL, TransmissionType.AUTOMATIC,
                new BigDecimal("2200.00"), new BigDecimal("3500.00"),
                "/images/vehicles/i20.jpg",
                "Chic premium hatchback equipped with Bose 7-speaker audio, electric sunroof, and smooth intelligent variable transmission (IVT).",
                true, 4.8, "Mumbai Chhatrapati Shivaji Airport (BOM)",
                "Electric Sunroof, Bose Premium Sound, Wireless Smartphone Charger, BlueLink Connected Car Tech, Air Purifier",
                5, 2, "Hatchback", true, false, VehicleOrigin.INDIAN
        ));

        // ==========================================
        // 2. INDIAN SEDANS
        // ==========================================
        list.add(new Car(
                "Honda", "City ZX",
                FuelType.PETROL, TransmissionType.AUTOMATIC,
                new BigDecimal("3200.00"), new BigDecimal("5000.00"),
                "/images/vehicles/city.jpg",
                "The benchmark executive sedan with silky smooth 1.5L i-VTEC engine, Honda SENSING ADAS suite, and plush leather upholstery.",
                true, 4.9, "Connaught Place Hub",
                "Honda SENSING ADAS, Electric Sunroof, LaneWatch Blind Spot Camera, Leatherette Seats, 8-Speaker Audio",
                5, 3, "Sedan", true, false, VehicleOrigin.INDIAN
        ));

        list.add(new Car(
                "Hyundai", "Verna Turbo SX(O)",
                FuelType.PETROL, TransmissionType.AUTOMATIC,
                new BigDecimal("3400.00"), new BigDecimal("5000.00"),
                "/images/vehicles/verna.jpg",
                "Futuristic fastback sedan with 160 PS turbo-petrol thrust, Level 2 ADAS, dual 10.25-inch panoramic screens, and ventilated seats.",
                true, 4.8, "Cyber City Gurgaon",
                "Level 2 ADAS, Ventilated Front Seats, Dual Curved Displays, Bose 8-Speaker Audio, Switchable Climate/Infotainment Console",
                5, 3, "Sedan", true, false, VehicleOrigin.INDIAN
        ));

        list.add(new Car(
                "Maruti Suzuki", "Dzire ZXi+",
                FuelType.PETROL, TransmissionType.MANUAL,
                new BigDecimal("2100.00"), new BigDecimal("3500.00"),
                "/images/vehicles/dzire.jpg",
                "India's best-selling compact sedan with 5-star safety rating, electric sunroof, refined 3-cylinder Z-Series engine, and high mileage.",
                true, 4.7, "Bangalore Kempegowda Airport (BLR)",
                "Electric Sunroof, 360-Degree Camera, 6 Airbags Standard, Wireless Charging, LED Crystal Vision Headlamps",
                5, 2, "Sedan", true, false, VehicleOrigin.INDIAN
        ));

        list.add(new Car(
                "Volkswagen", "Virtus GT Plus",
                FuelType.PETROL, TransmissionType.AUTOMATIC,
                new BigDecimal("3600.00"), new BigDecimal("6000.00"),
                "/images/vehicles/virtus.jpg",
                "German-engineered performance sedan powered by 1.5L TSI EVO engine with 7-speed DSG, sports paddle shifters, and 5-star GNCAP rating.",
                true, 4.9, "Mumbai Chhatrapati Shivaji Airport (BOM)",
                "1.5L TSI Turbocharged, 7-Speed DSG, Red Painted Calipers, Digital Cockpit Pro, Ventilated Front Seats",
                5, 3, "Sedan", true, false, VehicleOrigin.INDIAN
        ));

        // ==========================================
        // 3. INDIAN SUVS & 4X4s
        // ==========================================
        list.add(new Car(
                "Tata", "Nexon Fearless+ S",
                FuelType.DIESEL, TransmissionType.MANUAL,
                new BigDecimal("2800.00"), new BigDecimal("4000.00"),
                "/images/vehicles/nexon.jpg",
                "India's premier 5-star safety SUV with muscular stance, sequential LED DRLs, 208 mm ground clearance, and punchy diesel torque.",
                true, 4.8, "Indira Gandhi International Airport (DEL)",
                "360 Degree Surround Camera, Ventilated Leatherette Seats, 10.25-inch Touchscreen, JBL Audio with Subwoofer, Express Cool",
                5, 3, "Compact SUV", true, false, VehicleOrigin.INDIAN
        ));

        list.add(new Car(
                "Mahindra", "XUV700 AX7 Luxury Pack",
                FuelType.DIESEL, TransmissionType.AUTOMATIC,
                new BigDecimal("4800.00"), new BigDecimal("8000.00"),
                "/images/vehicles/xuv700.jpg",
                "Flagship 7-seater SUV loaded with Level 2 ADAS, Sony 3D 12-speaker immersive audio, panoramic Skyroof, and exhilarating 185 PS diesel.",
                true, 4.9, "Cyber City Gurgaon",
                "Level 2 ADAS, Sony 12-Speaker 3D Audio, Panoramic Skyroof, Dual 10.25-inch SuperScreens, Smart Door Handles",
                7, 4, "Mid-Size SUV", true, false, VehicleOrigin.INDIAN
        ));

        list.add(new Car(
                "Mahindra", "Scorpio-N Z8L 4XPLOR",
                FuelType.DIESEL, TransmissionType.AUTOMATIC,
                new BigDecimal("4200.00"), new BigDecimal("7000.00"),
                "/images/vehicles/scorpio.jpg",
                "The 'Big Daddy of SUVs' with genuine ladder-frame chassis, 4XPLOR intelligent terrain management, and commanding driving height.",
                true, 4.8, "Connaught Place Hub",
                "4XPLOR Intelligent Terrain Modes, Frequency Dependent Damping, Sony 12-Speaker Sound, Coffee Black Leatherette, Sunroof",
                7, 4, "Rugged SUV", true, false, VehicleOrigin.INDIAN
        ));

        list.add(new Car(
                "Mahindra", "Thar LX 4x4 Hard Top",
                FuelType.DIESEL, TransmissionType.MANUAL,
                new BigDecimal("4500.00"), new BigDecimal("8000.00"),
                "/images/vehicles/thar.jpg",
                "Legendary Indian off-road icon engineered for mountains and trails. Shift-on-the-fly 4WD with mechanical locking rear differential.",
                true, 4.9, "Bangalore Kempegowda Airport (BLR)",
                "True 4x4 with Low-Range Gearbox, Mechanical Locking Differential, Washable Interior, Roll Cage, Adventure Gauges",
                4, 2, "Off-Road 4x4", true, false, VehicleOrigin.INDIAN
        ));

        list.add(new Car(
                "Hyundai", "Creta SX(O)",
                FuelType.DIESEL, TransmissionType.AUTOMATIC,
                new BigDecimal("3500.00"), new BigDecimal("5000.00"),
                "/images/vehicles/creta.jpg",
                "India's favorite mid-size SUV featuring parametric jewel grille, panoramic sunroof, Bose audio, and Level 2 SmartSense ADAS.",
                true, 4.8, "Mumbai Chhatrapati Shivaji Airport (BOM)",
                "Voice Controlled Panoramic Sunroof, Bose Sound System, 8-Way Powered Driver Seat, Level 2 ADAS, Ventilated Front Seats",
                5, 3, "Mid-Size SUV", true, false, VehicleOrigin.INDIAN
        ));

        list.add(new Car(
                "Kia", "Seltos GTX+ Dark Edition",
                FuelType.PETROL, TransmissionType.AUTOMATIC,
                new BigDecimal("3600.00"), new BigDecimal("5000.00"),
                "/images/vehicles/seltos.jpg",
                "Aggressive styling meets premium technology with dual-pane panoramic sunroof, 360-degree blind view monitor, and 1.5L Turbo GDi power.",
                true, 4.8, "Indira Gandhi International Airport (DEL)",
                "Dual Panoramic Sunroof, Dual 10.25-inch Display Cluster, Bose 8-Speaker Audio, Smart Pure Air Purifier, Head-Up Display",
                5, 3, "Mid-Size SUV", true, false, VehicleOrigin.INDIAN
        ));

        list.add(new Car(
                "Maruti Suzuki", "Grand Vitara Alpha+ Hybrid",
                FuelType.HYBRID, TransmissionType.AUTOMATIC,
                new BigDecimal("3400.00"), new BigDecimal("5000.00"),
                "/images/vehicles/grand-vitara.jpg",
                "Strong self-charging hybrid electric SUV delivering silent electric city driving and astonishing 27.97 km/l fuel efficiency.",
                true, 4.7, "Cyber City Gurgaon",
                "Intelligent Electric Hybrid Drive, Panoramic Sunroof, Head-Up Display, 360 View Camera, Ventilated Leatherette Seats",
                5, 3, "Hybrid SUV", true, false, VehicleOrigin.INDIAN
        ));

        list.add(new Car(
                "Toyota", "Fortuner Legender 4x4",
                FuelType.DIESEL, TransmissionType.AUTOMATIC,
                new BigDecimal("7500.00"), new BigDecimal("15000.00"),
                "/images/vehicles/fortuner.jpg",
                "The undisputed king of Indian roads. Imposing road presence, 500 Nm torque, go-anywhere 4WD, and bulletproof Toyota reliability.",
                true, 4.9, "Connaught Place Hub",
                "4x4 Auto with High/Low Range, Catamaran Bumper & Split Roof, Kick-Sensor Powered Tailgate, 11-Speaker JBL Audio, Ventilated Seats",
                7, 4, "Full-Size SUV", true, true, VehicleOrigin.INDIAN
        ));

        list.add(new Car(
                "Tata", "Harrier Fearless+ Dark",
                FuelType.DIESEL, TransmissionType.AUTOMATIC,
                new BigDecimal("4200.00"), new BigDecimal("7000.00"),
                "/images/vehicles/harrier.jpg",
                "Built on Land Rover's legendary D8 platform pedigree. All-black stealth aesthetic, 19-inch aero alloys, and panoramic voice sunroof.",
                true, 4.8, "Bangalore Kempegowda Airport (BLR)",
                "Land Rover Pedigree OMEGARC, Voice-Assisted Panoramic Sunroof, 12.3-inch Touchscreen, JBL Audio, 7 Airbags",
                5, 4, "Premium SUV", true, false, VehicleOrigin.INDIAN
        ));

        // ==========================================
        // 4. ELECTRIC VEHICLES (EVs)
        // ==========================================
        list.add(new Car(
                "Tata", "Nexon EV Empowered+ LR",
                FuelType.ELECTRIC, TransmissionType.AUTOMATIC,
                new BigDecimal("3200.00"), new BigDecimal("5000.00"),
                "/images/vehicles/nexon-ev.jpg",
                "India's best-selling electric vehicle with 465 km ARAI certified range, V2V/V2L charging capability, and cinematic digital cockpit.",
                true, 4.8, "Indira Gandhi International Airport (DEL)",
                "40.5 kWh Long Range Battery, Vehicle-to-Load (V2L) Power Output, Fast DC Charging, 12.3-inch Cinematic Screen, Arcade.ev",
                5, 3, "Electric SUV", true, false, VehicleOrigin.INDIAN
        ));

        list.add(new Car(
                "Tata", "Punch EV Empowered+",
                FuelType.ELECTRIC, TransmissionType.AUTOMATIC,
                new BigDecimal("2600.00"), new BigDecimal("4000.00"),
                "/images/vehicles/punch-ev.jpg",
                "Dedicated acti.ev pure electric platform architecture with frunk front storage, 421 km range, and 360-degree blind camera.",
                true, 4.7, "Cyber City Gurgaon",
                "Frunk Storage, 360 Camera, 35 kWh Fast-Charge Pack, Auto-Hold Electronic Parking Brake, Wireless Apple CarPlay/Android Auto",
                5, 2, "Electric SUV", true, false, VehicleOrigin.INDIAN
        ));

        list.add(new Car(
                "MG", "ZS EV Exclusive Plus",
                FuelType.ELECTRIC, TransmissionType.AUTOMATIC,
                new BigDecimal("4000.00"), new BigDecimal("6000.00"),
                "/images/vehicles/mg-zs.jpg",
                "Global electric crossover with 50.3 kWh prismatic battery, 461 km range, panoramic dual-pane Skyroof, and Level 2 ADAS.",
                true, 4.8, "Mumbai Chhatrapati Shivaji Airport (BOM)",
                "50.3 kWh Prismatic Battery, Panoramic Skyroof, Level 2 ADAS, i-SMART Connected Suite with 75+ Features, Wireless Phone Charging",
                5, 3, "Electric SUV", true, false, VehicleOrigin.INDIAN
        ));

        list.add(new Car(
                "Mahindra", "XUV400 EL Pro",
                FuelType.ELECTRIC, TransmissionType.AUTOMATIC,
                new BigDecimal("3400.00"), new BigDecimal("5000.00"),
                "/images/vehicles/xuv400.jpg",
                "Instant electric acceleration reaching 0-100 km/h in 8.3s with 39.4 kWh battery, copper accents, and class-widest cabin space.",
                true, 4.7, "Bangalore Kempegowda Airport (BLR)",
                "Dual 10.25-inch Screens, Copper Accent Trims, All-Disc Brakes, 39.4 kWh Lithium Pack, Wireless Smartphone Connectivity",
                5, 3, "Electric SUV", true, false, VehicleOrigin.INDIAN
        ));

        // ==========================================
        // 5. DEDICATED PREMIUM CARS COLLECTION
        // ==========================================
        list.add(new Car(
                "Mercedes-Benz", "C-Class C 220d",
                FuelType.DIESEL, TransmissionType.AUTOMATIC,
                new BigDecimal("14000.00"), new BigDecimal("25000.00"),
                "/images/vehicles/mercedes-c.jpg",
                "Referred to as the 'Baby S-Class'. Features 11.9-inch portrait OLED display, 64-color ambient lighting, and serene comfort.",
                true, 4.9, "Indira Gandhi International Airport (DEL)",
                "MBUX 2.0 with Biometric Fingerprint Scanner, Burmester 3D Sound, Panoramic Sliding Sunroof, 64-Color Ambient Light, Agility Control",
                5, 3, "Luxury Sedan", true, true, VehicleOrigin.INTERNATIONAL
        ));

        list.add(new Car(
                "Mercedes-Benz", "E-Class E 220d LWB",
                FuelType.DIESEL, TransmissionType.AUTOMATIC,
                new BigDecimal("18500.00"), new BigDecimal("30000.00"),
                "/images/vehicles/mercedes-e.jpg",
                "Exclusive Long Wheelbase executive chauffeur saloon. Reclining rear seats with memory, dual rear touchscreens, and AIRMATIC suspension.",
                true, 4.9, "Connaught Place Hub",
                "Long Wheelbase with Chauffeur Package, AIRMATIC Air Suspension, Burmester High-End 4D Sound, Dual Rear Touchscreens, Soft-Close Doors",
                5, 4, "Executive Luxury Sedan", true, true, VehicleOrigin.INTERNATIONAL
        ));

        list.add(new Car(
                "BMW", "3 Series Gran Limousine 330Li",
                FuelType.PETROL, TransmissionType.AUTOMATIC,
                new BigDecimal("13500.00"), new BigDecimal("25000.00"),
                "/images/vehicles/bmw-3.jpg",
                "The driver's luxury car with extended wheelbase, 258 hp TwinPower Turbo engine, BMW Curved Display, and Harman Kardon acoustics.",
                true, 4.9, "Cyber City Gurgaon",
                "BMW Curved Display with OS 8, Harman Kardon Surround Sound, Extended Rear Legroom, Vernasca Leather, Panoramic Sunroof",
                5, 3, "Sport Sedan", true, true, VehicleOrigin.INTERNATIONAL
        ));

        list.add(new Car(
                "BMW", "5 Series 520d M Sport",
                FuelType.DIESEL, TransmissionType.AUTOMATIC,
                new BigDecimal("18000.00"), new BigDecimal("30000.00"),
                "/images/vehicles/bmw-5.jpg",
                "Executive athleticism with BMW Interaction Bar, Bowers & Wilkins audio, Highway Assistant, and aerodynamic M Sport exterior.",
                true, 4.9, "Mumbai Chhatrapati Shivaji Airport (BOM)",
                "BMW Interaction Bar, Bowers & Wilkins Diamond Sound, M Aerodynamics Package, Iconic Glow Kidney Grille, Parking Assistant Professional",
                5, 4, "Executive Sedan", true, true, VehicleOrigin.INTERNATIONAL
        ));

        list.add(new Car(
                "Audi", "A4 40 TFSI Technology",
                FuelType.PETROL, TransmissionType.AUTOMATIC,
                new BigDecimal("12500.00"), new BigDecimal("20000.00"),
                "/images/vehicles/audi-a4.jpg",
                "Understated German sophistication with Audi Virtual Cockpit Plus, Matrix LED headlights, and 19-speaker Bang & Olufsen 3D sound.",
                true, 4.8, "Bangalore Kempegowda Airport (BLR)",
                "Audi Virtual Cockpit Plus, Bang & Olufsen 3D Sound System, Matrix LED Headlights, 3-Zone Climate Control, Comfort Keyless Entry",
                5, 3, "Luxury Sedan", true, true, VehicleOrigin.INTERNATIONAL
        ));

        list.add(new Car(
                "Audi", "A6 45 TFSI Technology",
                FuelType.PETROL, TransmissionType.AUTOMATIC,
                new BigDecimal("17000.00"), new BigDecimal("30000.00"),
                "/images/vehicles/audi-a6.jpg",
                "Executive business saloon with dual MMI Touch Response touchscreens, progressive steering, and progressive Quattro all-wheel drive.",
                true, 4.9, "Indira Gandhi International Airport (DEL)",
                "Dual MMI Touch Response Displays, Matrix LED with Dynamic Indicators, Bang & Olufsen Premium Audio, Air Quality Package, Audi Drive Select",
                5, 4, "Executive Sedan", true, true, VehicleOrigin.INTERNATIONAL
        ));

        list.add(new Car(
                "Volvo", "XC60 B5 Ultimate Hybrid",
                FuelType.HYBRID, TransmissionType.AUTOMATIC,
                new BigDecimal("16000.00"), new BigDecimal("25000.00"),
                "/images/vehicles/volvo-xc60.jpg",
                "Scandinavian luxury with Bowers & Wilkins audio, Google built-in infotainment, Orrefors crystal gear selector, and advanced air purifier.",
                true, 4.9, "Cyber City Gurgaon",
                "Bowers & Wilkins 15-Speaker Sound, Orrefors Crystal Shifter, Google Built-in Services, Pilot Assist Semi-Autonomous, Air Purifier PM2.5",
                5, 4, "Luxury SUV", true, true, VehicleOrigin.INTERNATIONAL
        ));

        list.add(new Car(
                "Land Rover", "Defender 110 SE 3.0L",
                FuelType.DIESEL, TransmissionType.AUTOMATIC,
                new BigDecimal("24000.00"), new BigDecimal("40000.00"),
                "/images/vehicles/defender.jpg",
                "Unstoppable 4x4 capability paired with 21st-century luxury. Electronic Air Suspension, 900 mm wading depth, and Meridian 700W sound.",
                true, 5.0, "Connaught Place Hub",
                "Electronic Air Suspension, Terrain Response 2 with Auto, ClearSight Ground View Camera, Meridian 700W Sound, 900mm Wading Depth",
                5, 4, "Luxury Off-Roader", true, true, VehicleOrigin.INTERNATIONAL
        ));

        list.add(new Car(
                "Porsche", "Macan GTS",
                FuelType.PETROL, TransmissionType.AUTOMATIC,
                new BigDecimal("22000.00"), new BigDecimal("35000.00"),
                "/images/vehicles/porsche-macan.jpg",
                "The sports car of compact SUVs. Twin-turbo V6 producing 440 hp, Porsche Active Suspension Management (PASM), and Sport Chrono package.",
                true, 4.9, "Mumbai Chhatrapati Shivaji Airport (BOM)",
                "Sport Chrono Package, Porsche Surface Coated Brakes, GTS Sports Exhaust, BOSE Surround Sound, 18-Way Adaptive Sports Seats",
                5, 3, "Luxury Performance SUV", true, true, VehicleOrigin.INTERNATIONAL
        ));

        list.add(new Car(
                "Porsche", "911 Carrera 4S",
                FuelType.PETROL, TransmissionType.AUTOMATIC,
                new BigDecimal("28000.00"), new BigDecimal("50000.00"),
                "/images/vehicles/porsche-911.jpg",
                "Legendary German performance engineered with 450 hp twin-turbo flat-six, Porsche Doppelkupplung (PDK), and all-wheel drive stability.",
                true, 5.0, "Indira Gandhi International Airport (DEL)",
                "Sport Chrono Package, Burmester High-End 3D Sound, Adaptive 18-Way Sports Seats Plus, Carbon Fiber Roof, Porsche Dynamic Light System Plus",
                4, 2, "Sports Coupe", true, true, VehicleOrigin.INTERNATIONAL
        ));

        // ==========================================
        // 6. MOTORCYCLES (INDIAN & INTERNATIONAL)
        // ==========================================
        list.add(new Motorcycle(
                "Royal Enfield", "Himalayan 450",
                FuelType.PETROL, TransmissionType.MANUAL,
                new BigDecimal("2200.00"), new BigDecimal("4000.00"),
                "/images/vehicles/himalayan.jpg",
                "Built for all roads and no roads. Sherpa 450 liquid-cooled engine, Showa upside-down forks, Google Maps Tripper navigation, and Switchable ABS.",
                true, 4.8, "Connaught Place Hub",
                "Sherpa 450 Liquid-Cooled Engine, Showa USD Suspension, Tripper Dash with Google Maps, Ride-by-Wire with Riding Modes, Switchable ABS",
                452, "Adventure", true, false, VehicleOrigin.INDIAN
        ));

        list.add(new Motorcycle(
                "Ducati", "Panigale V4 S",
                FuelType.PETROL, TransmissionType.MANUAL,
                new BigDecimal("9000.00"), new BigDecimal("15000.00"),
                "/images/vehicles/panigale.jpg",
                "Bred directly from MotoGP. Desmosedici Stradale engine with Öhlins Smart EC 2.0 electronic suspension and carbon aero winglets.",
                true, 4.9, "Cyber City Gurgaon",
                "Öhlins Smart EC 2.0 Electronic Suspension, Cornering ABS EVO, Quick Shift Up/Down, Full Color TFT Display, Multiple Race Modes",
                1103, "Superbike", true, true, VehicleOrigin.INTERNATIONAL
        ));

        list.add(new Motorcycle(
                "BMW", "R 1250 GS Adventure",
                FuelType.PETROL, TransmissionType.MANUAL,
                new BigDecimal("7500.00"), new BigDecimal("12000.00"),
                "/images/vehicles/bmw-gs.jpg",
                "The undisputed king of globe-trotting adventure with Boxer ShiftCam torque, dynamic ESA suspension, and rugged alloy panniers.",
                true, 4.8, "Bangalore Kempegowda Airport (BLR)",
                "ShiftCam Boxer Engine, Dynamic Electronic Suspension (ESA), Heated Grips & Seats, Keyless Ride, Aluminum Touring Panniers, Cruise Control",
                1254, "Adventure Touring", true, true, VehicleOrigin.INTERNATIONAL
        ));

        list.add(new Motorcycle(
                "Harley-Davidson", "Fat Boy 114",
                FuelType.PETROL, TransmissionType.MANUAL,
                new BigDecimal("8000.00"), new BigDecimal("15000.00"),
                "/images/vehicles/harley-fatboy.jpg",
                "Iconic heavyweight cruiser presence with solid Lakester cast disc wheels, Milwaukee-Eight 114 V-Twin muscle, and satin chrome finishes.",
                true, 4.7, "Mumbai Chhatrapati Shivaji Airport (BOM)",
                "Milwaukee-Eight 114 V-Twin Engine, Solid Cast Wheels, Signature LED Lighting, Custom Dual Exhaust, Forward Foot Controls",
                1868, "Cruiser", true, true, VehicleOrigin.INTERNATIONAL
        ));

        vehicleRepository.saveAll(list);
    }

    private void seedBookings() {
        User arjun = userRepository.findByEmail("arjun@example.com").orElse(null);
        User priya = userRepository.findByEmail("priya@example.com").orElse(null);
        User john = userRepository.findByEmail("john@example.com").orElse(null);

        List<Vehicle> allVehicles = vehicleRepository.findAll();
        if (allVehicles.isEmpty()) return;

        Vehicle fortuner = allVehicles.stream().filter(v -> v.getModel().contains("Fortuner")).findFirst().orElse(allVehicles.get(0));
        Vehicle porsche = allVehicles.stream().filter(v -> v.getModel().contains("911")).findFirst().orElse(allVehicles.get(0));
        Vehicle swift = allVehicles.stream().filter(v -> v.getModel().contains("Swift")).findFirst().orElse(allVehicles.get(0));

        if (john != null) {
            // Seed an active upcoming booking for John
            Booking b0 = new Booking(
                    john,
                    swift,
                    LocalDate.now().plusDays(2),
                    LocalDate.now().plusDays(5),
                    "Connaught Place Hub",
                    "Connaught Place Hub",
                    "CREDIT_CARD",
                    "Weekend getaway rental"
            );
            b0.setBookingNumber("DE-2026-88120");
            b0.setDailyRate(swift.getDailyRate());
            BigDecimal days0 = BigDecimal.valueOf(3);
            BigDecimal sub0 = swift.getDailyRate().multiply(days0);
            b0.setSubtotal(sub0);
            b0.setDiscountAmount(BigDecimal.ZERO);
            b0.setTaxAmount(sub0.multiply(new BigDecimal("0.10")));
            b0.setSecurityDeposit(swift.getSecurityDeposit());
            b0.setTotalAmount(sub0.add(b0.getTaxAmount()).add(b0.getSecurityDeposit()));
            b0.setStatus(BookingStatus.CONFIRMED);
            b0.setPaymentStatus("PAID");
            bookingRepository.save(b0);
        }

        if (arjun != null) {
            // Seed a completed past booking
            Booking b1 = new Booking(
                    arjun,
                    swift,
                    LocalDate.now().minusDays(15),
                    LocalDate.now().minusDays(12),
                    "Indira Gandhi International Airport (DEL)",
                    "Indira Gandhi International Airport (DEL)",
                    "UPI",
                    "Weekend city exploration and family visit"
            );
            b1.setBookingNumber("DE-2026-90412");
            b1.setDailyRate(swift.getDailyRate());
            BigDecimal days = BigDecimal.valueOf(3);
            BigDecimal sub = swift.getDailyRate().multiply(days);
            b1.setSubtotal(sub);
            b1.setDiscountAmount(BigDecimal.ZERO);
            b1.setTaxAmount(sub.multiply(new BigDecimal("0.10")));
            b1.setSecurityDeposit(swift.getSecurityDeposit());
            b1.setTotalAmount(sub.add(b1.getTaxAmount()).add(b1.getSecurityDeposit()));
            b1.setStatus(BookingStatus.COMPLETED);
            b1.setPaymentStatus("COMPLETED");
            bookingRepository.save(b1);

            // Seed an upcoming confirmed booking
            Booking b2 = new Booking(
                    arjun,
                    fortuner,
                    LocalDate.now().plusDays(5),
                    LocalDate.now().plusDays(8),
                    "Connaught Place Hub",
                    "Indira Gandhi International Airport (DEL)",
                    "CREDIT_CARD",
                    "Shimla highway road trip"
            );
            b2.setBookingNumber("DE-2026-94819");
            b2.setDailyRate(fortuner.getDailyRate());
            BigDecimal d2 = BigDecimal.valueOf(3);
            BigDecimal sub2 = fortuner.getDailyRate().multiply(d2);
            b2.setSubtotal(sub2);
            b2.setDiscountAmount(BigDecimal.ZERO);
            b2.setTaxAmount(sub2.multiply(new BigDecimal("0.10")));
            b2.setSecurityDeposit(fortuner.getSecurityDeposit());
            b2.setTotalAmount(sub2.add(b2.getTaxAmount()).add(b2.getSecurityDeposit()));
            b2.setStatus(BookingStatus.CONFIRMED);
            b2.setPaymentStatus("PAID");
            bookingRepository.save(b2);
        }

        if (priya != null) {
            // Seed an active rental
            Booking b3 = new Booking(
                    priya,
                    porsche,
                    LocalDate.now().minusDays(1),
                    LocalDate.now().plusDays(2),
                    "Indira Gandhi International Airport (DEL)",
                    "Connaught Place Hub",
                    "CREDIT_CARD",
                    "Executive corporate event arrival"
            );
            b3.setBookingNumber("DE-2026-97103");
            b3.setDailyRate(porsche.getDailyRate());
            BigDecimal d3 = BigDecimal.valueOf(3);
            BigDecimal sub3 = porsche.getDailyRate().multiply(d3);
            b3.setSubtotal(sub3);
            b3.setDiscountAmount(BigDecimal.ZERO);
            b3.setTaxAmount(sub3.multiply(new BigDecimal("0.10")));
            b3.setSecurityDeposit(porsche.getSecurityDeposit());
            b3.setTotalAmount(sub3.add(b3.getTaxAmount()).add(b3.getSecurityDeposit()));
            b3.setStatus(BookingStatus.ACTIVE);
            b3.setPaymentStatus("PAID");
            bookingRepository.save(b3);
        }
    }
}
