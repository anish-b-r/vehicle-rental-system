import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
import fitz  # PyMuPDF for page inspection

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print total page count ('Page X of Y')
    along with professional running headers and footers on every page except the cover.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Skip header and footer on the cover page (Page 1)
        if self._pageNumber > 1:
            self.saveState()
            
            # Running Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#475569"))
            self.drawString(54, 11 * 72 - 34, "DRIVEEASE — ENTERPRISE VEHICLE RENTAL SYSTEM")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(8.5 * 72 - 54, 11 * 72 - 34, "Technical Architecture & OOP Specification")
            
            # Header Divider Line
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(54, 11 * 72 - 40, 8.5 * 72 - 54, 11 * 72 - 40)

            # Running Footer Divider Line
            self.line(54, 46, 8.5 * 72 - 54, 46)
            
            # Running Footer Text
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(54, 34, "Java 21 LTS • Spring Boot 4 • Object-Oriented Engineering Report")
            self.drawRightString(8.5 * 72 - 54, 34, f"Page {self._pageNumber} of {page_count}")
            
            self.restoreState()


def generate_pdf(filename="DriveEase_Technical_Documentation_and_OOP_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=50
    )

    content_width = 8.5 * 72 - 108  # 504 pt width

    styles = getSampleStyleSheet()

    # Premium Color Palette
    C_PRIMARY = colors.HexColor("#0F172A")    # Deep Slate / Charcoal
    C_ACCENT = colors.HexColor("#1E3A8A")     # Royal Corporate Navy
    C_GOLD = colors.HexColor("#B45309")       # Amber Gold
    C_MUTED = colors.HexColor("#475569")      # Slate text
    C_BG_LIGHT = colors.HexColor("#F8FAFC")   # Light background
    C_BORDER = colors.HexColor("#E2E8F0")     # Subtle border
    C_CODE_BG = colors.HexColor("#F1F5F9")    # Code block background
    C_SUCCESS = colors.HexColor("#047857")    # Deep emerald green

    # Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=C_PRIMARY,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=C_MUTED,
        spaceAfter=14
    )

    meta_label = ParagraphStyle('MLabel', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=C_ACCENT)
    meta_val = ParagraphStyle('MVal', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11, textColor=C_PRIMARY)

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=C_PRIMARY,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=C_ACCENT,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.2,
        textColor=colors.HexColor("#1E293B"),
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3.5
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0F172A")
    )

    th_style = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white)
    td_style = ParagraphStyle('TD', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=10, textColor=C_PRIMARY)
    td_bold = ParagraphStyle('TDBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=C_PRIMARY)

    story = []

    # =========================================================================
    # PAGE 1: EXECUTIVE COVER & SYSTEM PROFILE
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("TECHNICAL SPECIFICATION & OOP ARCHITECTURE REPORT", ParagraphStyle(
        'SuperTag', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=C_GOLD, spaceAfter=6
    )))
    story.append(Paragraph("DriveEase: Enterprise Vehicle Rental System", title_style))
    story.append(Paragraph(
        "A Production-Grade Full-Stack Vehicle Rental & Mobility Platform Built on Java 21, Spring Boot, Spring Security, Spring Data JPA, and Dynamic Multi-Currency Forex Architecture.",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_ACCENT, spaceBefore=0, spaceAfter=12))

    # Project Metadata Matrix
    meta_table_data = [
        [
            Paragraph("System Developer:", meta_label), Paragraph("Anish B R", meta_val),
            Paragraph("Application Framework:", meta_label), Paragraph("Spring Boot 4.0 / Spring WebMVC", meta_val)
        ],
        [
            Paragraph("Primary Language:", meta_label), Paragraph("Java 21 LTS (Oracle / Temurin)", meta_val),
            Paragraph("Data Persistence:", meta_label), Paragraph("Spring Data JPA & Hibernate 6", meta_val)
        ],
        [
            Paragraph("Engineering Context:", meta_label), Paragraph("Java OOP & Web Architecture", meta_val),
            Paragraph("Security & Auth:", meta_label), Paragraph("Spring Security (BCrypt, Session RBAC)", meta_val)
        ],
        [
            Paragraph("Source Repository:", meta_label), Paragraph("anish-b-r/vehicle-rental-system", meta_val),
            Paragraph("Cloud Deployment:", meta_label), Paragraph("Render (Multi-Stage Dockerfile)", meta_val)
        ]
    ]
    t_meta = Table(meta_table_data, colWidths=[105, 147, 115, 137])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 12))

    # Metric Bento Highlights
    stats_data = [
        [
            Paragraph("<font size='14'><b>36</b></font><br/><font color='#64748B' size='7'>AUTHENTIC VEHICLES</font>", ParagraphStyle('S1', parent=styles['Normal'], alignment=1)),
            Paragraph("<font size='14'><b>5</b></font><br/><font color='#64748B' size='7'>CURRENCIES (INR BASE)</font>", ParagraphStyle('S2', parent=styles['Normal'], alignment=1)),
            Paragraph("<font size='14'><b>100%</b></font><br/><font color='#64748B' size='7'>JAVA 21 / OOP CORE</font>", ParagraphStyle('S3', parent=styles['Normal'], alignment=1)),
            Paragraph("<font size='14'><b>4</b></font><br/><font color='#64748B' size='7'>CARDINAL OOP PILLARS</font>", ParagraphStyle('S4', parent=styles['Normal'], alignment=1)),
            Paragraph("<font size='14'><b>LIVE</b></font><br/><font color='#64748B' size='7'>RENDER DOCKER DEPLOY</font>", ParagraphStyle('S5', parent=styles['Normal'], alignment=1))
        ]
    ]
    t_stats = Table(stats_data, colWidths=[100.8]*5)
    t_stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_stats)
    story.append(Spacer(1, 12))

    # Executive Abstract Callout Box
    abstract_text = (
        "<b>Executive Purpose:</b> DriveEase is an enterprise-grade automotive rental and fleet management platform "
        "engineered to demonstrate real-world, commercial software craftsmanship using <b>Object-Oriented Programming (OOP)</b> "
        "and clean layered architecture in Java. Departing from trivial command-line toy projects, DriveEase models an end-to-end "
        "commercial system (resembling Porsche Drive and Silvercar): featuring a unified monolithic architecture serving both "
        "RESTful endpoints and a responsive client UI; an authentic 36-vehicle fleet spanning popular Indian models (Tata, Mahindra, "
        "Maruti Suzuki) and elite international brands (Mercedes, BMW, Audi, Land Rover, Porsche); a dedicated luxury 'Premium Cars' "
        "gallery; a high-precision multi-currency conversion service; and complete role-based reservation lifecycle operations. "
        "This document details its structural design, OOP implementations, database schema, and cloud deployment."
    )
    t_abs = Table([[Paragraph(abstract_text, body_style)]], colWidths=[content_width])
    t_abs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_abs)
    story.append(Spacer(1, 12))

    # Document Index / Contents Overview
    story.append(Paragraph("Document Structure & Topic Roadmap:", h2_style))
    doc_sections = [
        "<b>Section 1:</b> System Capabilities & Core Modules — Fleet scope, Indian vehicle expansion, luxury tier, and operations.",
        "<b>Section 2:</b> Technology Stack Architecture — Complete breakdown of Java 21, Spring Boot, JPA, Security, and Docker.",
        "<b>Section 3:</b> Object-Oriented Principles in Depth — Encapsulation, Inheritance, Polymorphism, Abstraction & Design Patterns.",
        "<b>Section 4:</b> How DriveEase Works — Multi-currency conversion engine, booking lifecycle state machine, and workflows.",
        "<b>Section 5:</b> Relational Database Schema — Table specifications, discriminator columns, foreign keys, and indexes.",
        "<b>Section 6:</b> REST API Contracts — Exhaustive endpoint specification across Auth, Vehicles, Bookings, and Admin.",
        "<b>Section 7:</b> Cloud Deployment & Evaluation — Dockerization, Render setup, and pre-seeded evaluation test accounts."
    ]
    for s in doc_sections:
        story.append(Paragraph(f"• {s}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: SYSTEM OVERVIEW & TECHNOLOGY STACK
    # =========================================================================
    story.append(Paragraph("1. System Overview & Core Capabilities", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "DriveEase delivers an end-to-end commercial mobility platform combining consumer-facing booking tools with back-office fleet administration:",
        body_style
    ))

    sys_pillars = [
        "<b>Comprehensive 36-Vehicle Catalog:</b> Covers Economy Hatchbacks, Compact & Mid-size Sedans, Rugged Off-road SUVs, and Electric Vehicles across Indian domestic manufacturers (Tata Nexon, Mahindra XUV700/Thar, Maruti Swift/Baleno) and international badges (Toyota Fortuner, Land Rover Defender, Porsche 911/Macan).",
        "<b>Dedicated 'Premium Cars' Showcase:</b> A curated, luxury vehicle browsing portal featuring high-end editorial aesthetics and backed by server-side query filtering (<code>GET /api/vehicles?premium=true</code>) rather than superficial CSS hiding.",
        "<b>Live Multi-Currency Engine:</b> Maintains all vehicle rental prices in <b>Indian Rupee (INR ₹)</b> as the canonical base currency to ensure zero ledger corruption. Converts dynamically into <b>USD ($), EUR (€), GBP (£), and AED (د.إ)</b> using real-time cached exchange rates.",
        "<b>Dynamic Booking & Price Estimator:</b> Evaluates rental duration, insurance tier, and automated weekly discounts (10% saver for rentals >= 7 days) using polymorphic strategy algorithms.",
        "<b>Customer Self-Service Hub:</b> Enables authenticated users to track active and historical reservations, review financial cost breakdowns, execute valid reservation cancellations with automated security deposit refunds, and generate printable receipts.",
        "<b>Fleet Operations Control:</b> Empowers administrators to monitor fleet utilization and revenue KPIs, add/modify vehicle specifications, toggle vehicle availability, and control the reservation lifecycle state machine."
    ]
    for p in sys_pillars:
        story.append(Paragraph(f"• {p}", bullet_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("2. Full Technology Stack & Architectural Layers", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    tech_table_data = [
        [Paragraph("Layer", th_style), Paragraph("Component / Library", th_style), Paragraph("Architectural Rationale & Responsibility", th_style)],
        [
            Paragraph("Core Language", td_bold),
            Paragraph("Java 21 LTS (Temurin / OpenJDK)", td_style),
            Paragraph("Leverages modern Java capabilities (pattern matching, enhanced switch expressions, Records, sealed classes, strict static type safety).", td_style)
        ],
        [
            Paragraph("Web Framework", td_bold),
            Paragraph("Spring Boot 4.0 / Spring WebMVC", td_style),
            Paragraph("Single-monolith web container providing IoC dependency injection, RESTful controllers, content negotiation, and auto-configuration.", td_style)
        ],
        [
            Paragraph("Data Persistence", td_bold),
            Paragraph("Spring Data JPA / Hibernate 6", td_style),
            Paragraph("Object-Relational Mapping (ORM) handling single-table entity inheritance, transactional boundaries (<code>@Transactional</code>), and JPQL queries.", td_style)
        ],
        [
            Paragraph("Security & Auth", td_bold),
            Paragraph("Spring Security 6 (BCrypt)", td_style),
            Paragraph("Session-based Role-Based Access Control (RBAC) securing customer vs. admin endpoints with BCrypt salted password hashing.", td_style)
        ],
        [
            Paragraph("Dual-Mode Database", td_bold),
            Paragraph("Embedded H2 & MySQL 8", td_style),
            Paragraph("Instant zero-setup evaluation via in-memory H2 running in MySQL mode. Production-ready to connect to external MySQL via environment variables.", td_style)
        ],
        [
            Paragraph("Currency Integration", td_bold),
            Paragraph("Scheduled Exchange Rate Service", td_style),
            Paragraph("Non-blocking <code>@Scheduled</code> rate synchronization with thread-safe caching (<code>ConcurrentHashMap</code>) and offline fallback.", td_style)
        ],
        [
            Paragraph("Frontend UI & UX", td_bold),
            Paragraph("HTML5, CSS3, ES6+ JS, Bootstrap 5.3", td_style),
            Paragraph("Responsive touch-optimized UI with custom design tokens, client-side currency state sync, async Fetch API, and zero heavy JS framework overhead.", td_style)
        ],
        [
            Paragraph("Container & Cloud", td_bold),
            Paragraph("Docker & Render Cloud Web Service", td_style),
            Paragraph("Multi-stage Dockerfile (JRE 21 runtime) deployed seamlessly to Render free/starter tiers with dynamic <code>$PORT</code> environment binding.", td_style)
        ]
    ]
    t_tech = Table(tech_table_data, colWidths=[90, 134, 280])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_BG_LIGHT])
    ]))
    story.append(t_tech)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: OOP CONCEPTS — ENCAPSULATION & INHERITANCE
    # =========================================================================
    story.append(Paragraph("3. Core Object-Oriented Programming (OOP) Principles", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "DriveEase is structured as a prime exemplar of Object-Oriented software engineering. "
        "Rather than treating classes as simple procedural data structures, every entity and component embodies OOP best practices.",
        body_style
    ))

    # 3.1 ENCAPSULATION
    story.append(Paragraph("3.1 Encapsulation (Data Hiding & Rich Behavioral Domain Models)", h2_style))
    story.append(Paragraph(
        "Encapsulation conceals the internal state of an object and enforces data integrity through controlled interfaces. "
        "DriveEase avoids 'anemic domain models' by embedding core business logic directly within entities:",
        body_style
    ))

    encap_bullets = [
        "<b>Strict State Protection:</b> All instance variables across <code>Vehicle</code>, <code>Car</code>, <code>Motorcycle</code>, <code>Booking</code>, and <code>User</code> are declared <code>private</code>. Access is mediated exclusively through validated accessors.",
        "<b>Encapsulated Financial Calculations:</b> In <code>Booking.java</code>, the method <code>calculatePricing(RentalPricingStrategy)</code> encapsulates the full algorithmic calculation of subtotal, applicable discounts, taxes, and security deposits. External callers cannot arbitrarily modify monetary totals.",
        "<b>State Machine Invariants:</b> The method <code>canBeCancelled()</code> encapsulates the business rule governing cancellations: a booking can only be cancelled if its current status is <code>CONFIRMED</code> and the pickup date has not yet passed.",
        "<b>Atomic State Transition:</b> The method <code>cancel()</code> validates cancellation eligibility, changes the status to <code>CANCELLED</code>, timestamps the cancellation, and triggers security deposit refund logic internally."
    ]
    for b in encap_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))

    # Code Snippet 1
    code_encap = (
        "// File: src/main/java/com/driveease/model/Booking.java\n"
        "public boolean canBeCancelled() {\n"
        "    return this.status == BookingStatus.CONFIRMED && \n"
        "           LocalDate.now().isBefore(this.startDate);\n"
        "}\n\n"
        "public void cancel() {\n"
        "    if (!canBeCancelled()) {\n"
        "        throw new BadRequestException(\"Booking cannot be cancelled in its current state.\");\n"
        "    }\n"
        "    this.status = BookingStatus.CANCELLED;\n"
        "    this.cancelledAt = LocalDateTime.now();\n"
        "    this.depositRefunded = true; // Business invariant: refund deposit on valid cancellation\n"
        "}"
    )
    t_c1 = Table([[Paragraph(code_encap.replace('\n', '<br/>'), code_style)]], colWidths=[content_width])
    t_c1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CODE_BG),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(Spacer(1, 3))
    story.append(t_c1)
    story.append(Spacer(1, 8))

    # 3.2 INHERITANCE
    story.append(Paragraph("3.2 Inheritance & Entity Hierarchies (IS-A Relationships)", h2_style))
    story.append(Paragraph(
        "Inheritance eliminates code redundancy by organizing common attributes and behaviors into a polymorphic base class:",
        body_style
    ))

    inherit_bullets = [
        "<b>Abstract Base Class (<code>Vehicle</code>):</b> Defines 16 shared attributes inherited by all motorized assets: <code>id</code>, <code>brand</code>, <code>model</code>, <code>registrationNumber</code>, <code>pricePerDay</code>, <code>category</code>, <code>fuelType</code>, <code>transmission</code>, <code>isAvailable</code>, <code>isPremium</code>, <code>vehicleOrigin</code>, <code>imageUrl</code>, etc.",
        "<b>Car Subclass (<code>Car extends Vehicle</code>):</b> Inherits all base attributes and introduces car-specific domain fields: <code>seatingCapacity</code>, <code>luggageCapacity</code>, <code>bodyType</code>, and <code>hasAirConditioning</code>.",
        "<b>Motorcycle Subclass (<code>Motorcycle extends Vehicle</code>):</b> Inherits base attributes and adds bike-specific fields: <code>engineCc</code>, <code>bikeType</code>, and <code>hasHelmetIncluded</code>.",
        "<b>Single-Table JPA Inheritance Strategy:</b> Mapped using <code>@Inheritance(strategy = InheritanceType.SINGLE_TABLE)</code> with discriminator column <code>@DiscriminatorColumn(name = \"vehicle_type\")</code> (values: <code>CAR</code> vs <code>MOTORCYCLE</code>), maximizing SQL query performance without multi-table join overhead."
    ]
    for b in inherit_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: OOP CONCEPTS — POLYMORPHISM & ABSTRACTION
    # =========================================================================
    story.append(Paragraph("3.3 Polymorphism (Dynamic Method Dispatch at Runtime)", h2_style))
    story.append(Paragraph(
        "Polymorphism allows specialized subclasses to fulfill abstract base class contracts with distinct implementations. "
        "DriveEase utilizes runtime polymorphic dispatch across multiple domain layers:",
        body_style
    ))

    poly_bullets = [
        "<b>Polymorphic Specification Formatting:</b> The abstract method <code>public abstract String getVehicleSpecificationsSummary();</code> declared in <code>Vehicle</code> is implemented distinctly by subclasses. Calling this method on a <code>Car</code> formats seating and trunk capacity; calling it on a <code>Motorcycle</code> formats engine displacement and helmet inclusion.",
        "<b>Polymorphic Insurance Multipliers:</b> <code>public abstract BigDecimal calculateBaseInsurance(int days);</code> calculates insurance premiums tailored to the risk profile and asset valuation of each vehicle category.",
        "<b>Uniform Service Invocations:</b> The booking and catalog services interact purely with the abstract <code>Vehicle</code> type. Java's Virtual Method Table (vtable) dispatches calls dynamically at runtime without requiring brittle <code>instanceof</code> checks or procedural <code>if-else</code> branching."
    ]
    for b in poly_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))

    # Code Snippet 2
    code_poly = (
        "// Base Abstract Class: Vehicle.java\n"
        "public abstract class Vehicle {\n"
        "    public abstract String getVehicleSpecificationsSummary();\n"
        "    public abstract BigDecimal calculateBaseInsurance(int days);\n"
        "}\n\n"
        "// Subclass 1: Car.java\n"
        "@Override\n"
        "public String getVehicleSpecificationsSummary() {\n"
        "    return seatingCapacity + \" Seats • \" + luggageCapacity + \" Bags • \" + (hasAirConditioning ? \"A/C\" : \"No A/C\");\n"
        "}\n\n"
        "// Subclass 2: Motorcycle.java\n"
        "@Override\n"
        "public String getVehicleSpecificationsSummary() {\n"
        "    return engineCc + \"cc • \" + bikeType + (hasHelmetIncluded ? \" • Helmet Included\" : \"\");\n"
        "}"
    )
    t_c2 = Table([[Paragraph(code_poly.replace('\n', '<br/>'), code_style)]], colWidths=[content_width])
    t_c2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CODE_BG),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(Spacer(1, 3))
    story.append(t_c2)
    story.append(Spacer(1, 8))

    # 3.4 ABSTRACTION
    story.append(Paragraph("3.4 Abstraction & Layered Architecture (Separation of Concerns)", h2_style))
    story.append(Paragraph(
        "Abstraction hides internal implementation complexities behind clean, well-defined boundaries. "
        "DriveEase enforces strict four-tier architectural separation:",
        body_style
    ))

    abstract_bullets = [
        "<b>Presentation Layer (REST Controllers):</b> Exposes HTTP endpoints (<code>/api/vehicles</code>, <code>/api/bookings</code>, <code>/api/currency</code>, <code>/api/admin</code>). Controllers are solely responsible for status codes, request parsing, and response wrapping.",
        "<b>Service Interface Layer (Business Abstraction):</b> Contracts such as <code>VehicleService</code>, <code>BookingService</code>, and <code>CurrencyService</code> define business operations without exposing underlying JPA or transaction mechanics.",
        "<b>Data Access Layer (Repository Abstraction):</b> <code>VehicleRepository</code> and <code>BookingRepository</code> extend Spring Data's <code>JpaRepository</code>, providing robust database querying without raw SQL boilerplate.",
        "<b>Data Transfer Object (DTO) Layer:</b> Prevents internal JPA entity structures from leaking to external clients, protecting against mass assignment vulnerabilities and optimizing payload size."
    ]
    for b in abstract_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: DESIGN PATTERNS IN PRACTICE
    # =========================================================================
    story.append(Paragraph("3.5 Enterprise Design Patterns in Practice", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "To achieve long-term maintainability, DriveEase integrates standard Gang-of-Four (GoF) design patterns:",
        body_style
    ))

    pattern_bullets = [
        "<b>Strategy Pattern (Dynamic Pricing Algorithms):</b> Encapsulates interchangeable pricing models behind the <code>RentalPricingStrategy</code> interface. <code>StandardPricingStrategy</code> calculates regular linear rates. <code>WeeklyDiscountPricingStrategy</code> automatically calculates and deducts a 10% saver discount for bookings extending 7 days or longer.",
        "<b>Factory Method Pattern (Strategy Factory):</b> <code>PricingStrategyFactory.getStrategy(int days)</code> isolates and encapsulates the selection logic, returning the appropriate pricing strategy without polluting caller code with conditional branches.",
        "<b>Singleton Pattern (Spring IoC Managed Beans):</b> All controllers, services, repositories, and security handlers are instantiated as thread-safe Singletons managed by the Spring ApplicationContext container.",
        "<b>Repository Pattern:</b> Decouples domain logic from database drivers and SQL dialects, enabling seamless transitions between in-memory H2 and production MySQL 8."
    ]
    for b in pattern_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))

    # Code Snippet 3
    code_patterns = (
        "// Strategy Interface\n"
        "public interface RentalPricingStrategy {\n"
        "    BigDecimal calculatePrice(BigDecimal pricePerDay, int days);\n"
        "    BigDecimal calculateDiscount(BigDecimal pricePerDay, int days);\n"
        "}\n\n"
        "// Concrete Strategy: 10% Saver Discount for rentals >= 7 days\n"
        "@Component\n"
        "public class WeeklyDiscountPricingStrategy implements RentalPricingStrategy {\n"
        "    @Override\n"
        "    public BigDecimal calculateDiscount(BigDecimal pricePerDay, int days) {\n"
        "        BigDecimal subtotal = pricePerDay.multiply(BigDecimal.valueOf(days));\n"
        "        return subtotal.multiply(new BigDecimal(\"0.10\")).setScale(2, RoundingMode.HALF_UP);\n"
        "    }\n"
        "    @Override\n"
        "    public BigDecimal calculatePrice(BigDecimal pricePerDay, int days) {\n"
        "        return pricePerDay.multiply(BigDecimal.valueOf(days)).subtract(calculateDiscount(pricePerDay, days));\n"
        "    }\n"
        "}\n\n"
        "// Factory Method: Decoupled Strategy Selection\n"
        "@Component\n"
        "public class PricingStrategyFactory {\n"
        "    public RentalPricingStrategy getStrategy(int rentalDays) {\n"
        "        return (rentalDays >= 7) ? weeklyDiscountPricingStrategy : standardPricingStrategy;\n"
        "    }\n"
        "}"
    )
    t_c3 = Table([[Paragraph(code_patterns.replace('\n', '<br/>'), code_style)]], colWidths=[content_width])
    t_c3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CODE_BG),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(Spacer(1, 3))
    story.append(t_c3)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Object-Oriented Design Scorecard & Benefits:", h2_style))
    scorecard_data = [
        [Paragraph("OOP Principle", th_style), Paragraph("Concrete Code Manifestation", th_style), Paragraph("Software Quality Benefit", th_style)],
        [
            Paragraph("Encapsulation", td_bold),
            Paragraph("Private state + rich domain methods in <code>Booking.java</code>", td_style),
            Paragraph("Guarantees data integrity; prevents unauthorized price tampering.", td_style)
        ],
        [
            Paragraph("Inheritance", td_bold),
            Paragraph("<code>Vehicle</code> base class extended by <code>Car</code> & <code>Motorcycle</code>", td_style),
            Paragraph("Eliminates code duplication; unifies fleet data schema.", td_style)
        ],
        [
            Paragraph("Polymorphism", td_bold),
            Paragraph("Abstract spec summaries & insurance calculations", td_style),
            Paragraph("Enables dynamic runtime dispatch without brittle <code>instanceof</code> checks.", td_style)
        ],
        [
            Paragraph("Abstraction", td_bold),
            Paragraph("Interface contracts (<code>VehicleService</code>, <code>JpaRepository</code>)", td_style),
            Paragraph("High cohesion, loose coupling, effortless testability.", td_style)
        ],
        [
            Paragraph("Strategy Pattern", td_bold),
            Paragraph("<code>RentalPricingStrategy</code> implementations", td_style),
            Paragraph("Extensibility: new discount rules added with zero changes to existing code.", td_style)
        ]
    ]
    t_score = Table(scorecard_data, colWidths=[90, 194, 220])
    t_score.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_BG_LIGHT])
    ]))
    story.append(t_score)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: WORKFLOWS & MULTI-CURRENCY FOREX ENGINE
    # =========================================================================
    story.append(Paragraph("4. End-to-End System Workflows & Financial Engine", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("4.1 Multi-Currency Rate Conversion Engine", h2_style))
    story.append(Paragraph(
        "A cornerstone of DriveEase's global readiness is its dynamic forex architecture. Designed to prevent database ledger corruption:",
        body_style
    ))

    currency_bullets = [
        "<b>Canonical Base Currency in INR (₹):</b> All rental prices, optional insurance tiers, security deposits, and historical booking invoices are permanently stored in Indian Rupees (INR). Changing the display currency in the client UI converts amounts dynamically for presentation only, never overwriting historical database records.",
        "<b>Scheduled Forex Synchronization:</b> <code>CurrencyServiceImpl</code> utilizes Spring's <code>@Scheduled(fixedRate = 3600000)</code> to pull real-time exchange rates from an external financial API once per hour, caching the rates in a thread-safe <code>ConcurrentHashMap</code>.",
        "<b>High-Availability Fallback Resilience:</b> If the remote exchange API is temporarily unavailable or blocked by network restrictions, the service immediately falls back to recent cached rates or sensible historical baselines, guaranteeing zero user disruption.",
        "<b>Arbitrary-Precision Financial Arithmetic:</b> All currency conversions and tax estimations use Java <code>BigDecimal</code> with explicit <code>RoundingMode.HALF_UP</code> rounding, completely avoiding the catastrophic rounding drift inherent in floating-point (<code>double</code> / <code>float</code>) arithmetic."
    ]
    for b in currency_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("4.2 Reservation Lifecycle State Machine", h2_style))
    story.append(Paragraph(
        "Reservations progress through a formal state machine strictly managed by business invariants:",
        body_style
    ))

    state_table_data = [
        [Paragraph("Status State", th_style), Paragraph("Triggering Action / Lifecycle Phase", th_style), Paragraph("System Side-Effects & Financial Invariants", th_style)],
        [
            Paragraph("CONFIRMED", td_bold),
            Paragraph("Customer completes reservation checkout", td_style),
            Paragraph("Pricing strategy evaluates duration; rental days calculated; refundable security deposit recorded; canonical booking invoice stored in DB.", td_style)
        ],
        [
            Paragraph("ACTIVE", td_bold),
            Paragraph("Rental start date reached or Admin check-out", td_style),
            Paragraph("Vehicle physical custody transferred to customer; vehicle availability flag temporarily toggled.", td_style)
        ],
        [
            Paragraph("COMPLETED", td_bold),
            Paragraph("Vehicle returned & inspected by Administrator", td_style),
            Paragraph("Rental duration concluded; security deposit refund finalized; vehicle returned to available fleet catalog.", td_style)
        ],
        [
            Paragraph("CANCELLED", td_bold),
            Paragraph("Customer or Admin initiates cancellation before pickup", td_style),
            Paragraph("Validated via <code>canBeCancelled()</code>; status transitioned; cancellation timestamp logged; automated security deposit refund processed.", td_style)
        ]
    ]
    t_state = Table(state_table_data, colWidths=[90, 160, 254])
    t_state.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_BG_LIGHT])
    ]))
    story.append(t_state)
    story.append(Spacer(1, 8))

    story.append(Paragraph("4.3 Indian Vehicle Expansion & Premium Gallery Strategy", h2_style))
    story.append(Paragraph(
        "• <b>Regional Origin Taxonomy:</b> Vehicles are classified by <code>vehicleOrigin</code> (<code>INDIAN</code> vs <code>INTERNATIONAL</code>), enabling domestic market representation alongside global imports.<br/>"
        "• <b>Dedicated Premium Portal:</b> Vehicles tagged with <code>isPremium = true</code> are indexed into a luxury showroom (<code>premium-cars.html</code>) using architectural bento grids and server-filtered REST endpoints.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: DATABASE SCHEMA & REST API SPECIFICATIONS
    # =========================================================================
    story.append(Paragraph("5. Relational Database Schema & Data Dictionary", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    schema_table_data = [
        [Paragraph("Table Name", th_style), Paragraph("Key Constraints", th_style), Paragraph("Core Columns, Data Types & Architectural Purpose", th_style)],
        [
            Paragraph("vehicles", td_bold),
            Paragraph("PK: id (BIGINT)", td_style),
            Paragraph("<code>vehicle_type</code> (CAR/MOTORCYCLE discriminator), <code>brand</code>, <code>model</code>, <code>registration_number</code> (UNIQUE), <code>price_per_day</code> (DECIMAL), <code>is_premium</code> (BOOL), <code>vehicle_origin</code> (VARCHAR), <code>is_available</code> (BOOL), <code>seating_capacity</code>, <code>engine_cc</code>.", td_style)
        ],
        [
            Paragraph("users", td_bold),
            Paragraph("PK: id (BIGINT)", td_style),
            Paragraph("<code>email</code> (VARCHAR UNIQUE), <code>password_hash</code> (VARCHAR BCrypt), <code>full_name</code>, <code>phone_number</code>, <code>role</code> (VARCHAR - ROLE_CUSTOMER, ROLE_ADMIN), <code>created_at</code> (TIMESTAMP).", td_style)
        ],
        [
            Paragraph("bookings", td_bold),
            Paragraph("PK: id (BIGINT)<br/>FK: user_id<br/>FK: vehicle_id", td_style),
            Paragraph("<code>start_date</code> (DATE), <code>end_date</code> (DATE), <code>total_days</code> (INT), <code>daily_rate</code> (DECIMAL), <code>subtotal</code>, <code>discount_amount</code>, <code>security_deposit</code>, <code>tax_amount</code>, <code>total_amount</code>, <code>status</code>, <code>deposit_refunded</code> (BOOL).", td_style)
        ]
    ]
    t_schema = Table(schema_table_data, colWidths=[75, 115, 314])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_BG_LIGHT])
    ]))
    story.append(t_schema)
    story.append(Spacer(1, 8))

    story.append(Paragraph("6. RESTful API Contracts & Endpoints Specification", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    api_table_data = [
        [Paragraph("HTTP Route", th_style), Paragraph("Auth Scope", th_style), Paragraph("Methodology & Contract Description", th_style)],
        [Paragraph("POST /api/auth/register", td_bold), Paragraph("Public", td_style), Paragraph("Registers customer profile with BCrypt salted hash.", td_style)],
        [Paragraph("POST /api/auth/login", td_bold), Paragraph("Public", td_style), Paragraph("Validates credentials and establishes secure HTTP session.", td_style)],
        [Paragraph("GET /api/auth/me", td_bold), Paragraph("Authenticated", td_style), Paragraph("Returns current authenticated user profile and roles.", td_style)],
        [Paragraph("GET /api/vehicles", td_bold), Paragraph("Public", td_style), Paragraph("Filter fleet by category, search, origin, premium, and price.", td_style)],
        [Paragraph("GET /api/vehicles/{id}", td_bold), Paragraph("Public", td_style), Paragraph("Returns detailed technical specifications for single vehicle.", td_style)],
        [Paragraph("GET /api/currency/rates", td_bold), Paragraph("Public", td_style), Paragraph("Returns base currency (INR), live exchange rates & timestamp.", td_style)],
        [Paragraph("POST /api/bookings", td_bold), Paragraph("ROLE_CUSTOMER", td_style), Paragraph("Creates reservation with strategy-calculated pricing.", td_style)],
        [Paragraph("GET /api/bookings/my", td_bold), Paragraph("ROLE_CUSTOMER", td_style), Paragraph("Retrieves logged-in customer's active and historical bookings.", td_style)],
        [Paragraph("PATCH /api/bookings/{id}/cancel", td_bold), Paragraph("ROLE_CUSTOMER", td_style), Paragraph("Cancels eligible booking and initiates security deposit refund.", td_style)],
        [Paragraph("GET /api/admin/dashboard", td_bold), Paragraph("ROLE_ADMIN", td_style), Paragraph("Returns fleet occupancy, booking counts, and revenue KPIs.", td_style)],
        [Paragraph("POST /api/admin/vehicles", td_bold), Paragraph("ROLE_ADMIN", td_style), Paragraph("Creates a new vehicle entity in the fleet database.", td_style)],
        [Paragraph("PATCH /api/admin/vehicles/{id}/premium", td_bold), Paragraph("ROLE_ADMIN", td_style), Paragraph("Toggles premium status of a vehicle dynamically.", td_style)]
    ]
    t_api = Table(api_table_data, colWidths=[155, 85, 264])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_BG_LIGHT])
    ]))
    story.append(t_api)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: CLOUD DEPLOYMENT & EVALUATION CREDENTIALS
    # =========================================================================
    story.append(Paragraph("7. Cloud Deployment & Academic Evaluation Guide", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("7.1 Render Cloud Deployment Architecture", h2_style))
    story.append(Paragraph(
        "DriveEase is configured for zero-friction cloud deployment on <b>Render</b>:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Production Multi-Stage Dockerfile:</b> Stage 1 utilizes <code>eclipse-temurin:21-jdk-jammy</code> to cache Maven dependencies and build the JAR. Stage 2 executes on <code>eclipse-temurin:21-jre-jammy</code>, minimizing attack surface and disk footprint.<br/>"
        "• <b>Dynamic Port Binding:</b> Configured with <code>server.port=${PORT:8080}</code> to bind seamlessly to Render's dynamically allocated <code>$PORT</code>.<br/>"
        "• <b>Container-Aware Memory Flags:</b> <code>-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0</code> ensures safe memory bounds inside Render's 512MB free tier.<br/>"
        "• <b>Zero-Config Evaluation Database:</b> Runs embedded H2 in MySQL compatibility mode with automatic data initialization on startup.",
        body_style
    ))

    story.append(Spacer(1, 6))
    story.append(Paragraph("7.2 Pre-Seeded Evaluation Credentials", h2_style))
    story.append(Paragraph(
        "For immediate evaluation, the database auto-populates the following accounts and data:",
        body_style
    ))

    cred_table_data = [
        [Paragraph("Role / Profile", th_style), Paragraph("Email Address", th_style), Paragraph("Password", th_style), Paragraph("Access Capabilities & Permissions", th_style)],
        [
            Paragraph("System Administrator", td_bold),
            Paragraph("admin@driveease.com", td_style),
            Paragraph("admin123", td_style),
            Paragraph("Full access to <code>admin.html</code> portal, KPI revenue dashboards, fleet CRUD, availability toggles, and reservation status manager.", td_style)
        ],
        [
            Paragraph("Customer (John Doe)", td_bold),
            Paragraph("john@example.com", td_style),
            Paragraph("customer123", td_style),
            Paragraph("Customer profile pre-loaded with confirmed bookings. Access to vehicle booking, cancellation, and receipt generator.", td_style)
        ],
        [
            Paragraph("Customer (Arjun Sharma)", td_bold),
            Paragraph("arjun@example.com", td_style),
            Paragraph("customer123", td_style),
            Paragraph("Secondary test customer profile with active Indian domestic vehicle rentals.", td_style)
        ]
    ]
    t_cred = Table(cred_table_data, colWidths=[95, 125, 74, 210])
    t_cred.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_BG_LIGHT])
    ]))
    story.append(t_cred)
    story.append(Spacer(1, 10))

    # Concluding Remarks
    story.append(Paragraph("8. Concluding Remarks & Project Significance", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "DriveEase demonstrates that core Object-Oriented principles (Encapsulation, Inheritance, Polymorphism, Abstraction) "
        "and clean architectural design patterns are not merely abstract academic concepts, but the foundational pillars of "
        "production-grade software engineering. By unifying strict domain invariants with modern web interfaces, dynamic "
        "multi-currency conversion, and enterprise deployment pipelines, this project stands as a complete, robust, and "
        "commercial-ready showcase of full-stack Java engineering.",
        body_style
    ))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    generate_pdf()
