import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
import fitz

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print total page count ('Page X of Y')
    along with running headers and footers on every page except the cover.
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
        if self._pageNumber > 1:
            self.saveState()
            
            # Running Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#1E293B"))
            self.drawString(45, 11 * 72 - 30, "DRIVEEASE — COMPLETE JAVA CODEBASE & OOP ARCHITECTURE SPECIFICATION")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(8.5 * 72 - 45, 11 * 72 - 30, "Java 21 LTS • Spring Boot 4 • All 52 .java Files")
            
            # Header Divider Line
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(45, 11 * 72 - 36, 8.5 * 72 - 45, 11 * 72 - 36)

            # Running Footer Divider Line
            self.line(45, 40, 8.5 * 72 - 45, 40)
            
            # Running Footer Text
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(45, 28, "Confidential Academic & Professional Reference • Object-Oriented Engineering in Java")
            self.drawRightString(8.5 * 72 - 45, 28, f"Page {self._pageNumber} of {page_count}")
            
            self.restoreState()


def build_pdf(filename="DriveEase_Java_Codebase_and_OOP_Guide.pdf"):
    # Target printable area: Letter size (8.5 x 11 inches) with 45 pt (0.625 in) margins
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=46,
        bottomMargin=46
    )

    content_width = 8.5 * 72 - 90  # 522 pt width

    styles = getSampleStyleSheet()

    # Premium Corporate Palette
    C_PRIMARY = colors.HexColor("#0F172A")    # Deep Slate / Charcoal
    C_ACCENT = colors.HexColor("#1E3A8A")     # Royal Corporate Navy
    C_GOLD = colors.HexColor("#B45309")       # Amber Gold
    C_MUTED = colors.HexColor("#475569")      # Slate text
    C_BG_LIGHT = colors.HexColor("#F8FAFC")   # Light background
    C_BORDER = colors.HexColor("#E2E8F0")     # Subtle border
    C_CODE_BG = colors.HexColor("#F1F5F9")    # Code block background
    C_SUCCESS = colors.HexColor("#047857")    # Deep emerald green
    C_EMPHASIS = colors.HexColor("#0369A1")   # Deep sky blue

    # Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=29,
        textColor=C_PRIMARY,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=15,
        textColor=C_MUTED,
        spaceAfter=12
    )

    meta_label = ParagraphStyle('MLabel', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10.5, textColor=C_ACCENT)
    meta_val = ParagraphStyle('MVal', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10.5, textColor=C_PRIMARY)

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=C_PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14.5,
        textColor=C_ACCENT,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'H3',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=C_PRIMARY,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.8,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.8,
        textColor=colors.HexColor("#1E293B"),
        leftIndent=11,
        firstLineIndent=-7,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )

    th_style = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.white)
    td_style = ParagraphStyle('TD', parent=styles['Normal'], fontName='Helvetica', fontSize=7.2, leading=9.2, textColor=C_PRIMARY)
    td_bold = ParagraphStyle('TDBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.2, leading=9.2, textColor=C_PRIMARY)
    td_code = ParagraphStyle('TDCode', parent=styles['Normal'], fontName='Courier-Bold', fontSize=7, leading=9, textColor=C_ACCENT)

    story = []

    # Helper for code snippet boxes
    def make_code_box(code_text):
        t = Table([[Paragraph(code_text.replace('\n', '<br/>'), code_style)]], colWidths=[content_width])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), C_CODE_BG),
            ('BOX', (0,0), (-1,-1), 1, C_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 7),
            ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ]))
        return t

    # Helper for file explanation cards
    def make_file_box(filename, package, purpose, annotations, methods_fields, oop_notes):
        p_title = f"<b>File:</b> <font color='#1E3A8A'>{filename}</font> | <b>Package:</b> <font color='#475569'>{package}</font>"
        content = [
            Paragraph(p_title, ParagraphStyle('FTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=C_PRIMARY)),
            Paragraph(f"• <b>Purpose & Architectural Role:</b> {purpose}", bullet_style),
            Paragraph(f"• <b>Key Annotations & Framework Integration:</b> {annotations}", bullet_style),
            Paragraph(f"• <b>Core Methods, Fields & Logic:</b> {methods_fields}", bullet_style),
            Paragraph(f"• <b>OOP Concepts & Java Features:</b> {oop_notes}", bullet_style),
        ]
        t = Table([[content]], colWidths=[content_width])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), C_BG_LIGHT),
            ('BOX', (0,0), (-1,-1), 0.75, C_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    # =========================================================================
    # PAGE 1: TITLE & EXECUTIVE JAVA ARCHITECTURE SUMMARY
    # =========================================================================
    story.append(Paragraph("TECHNICAL SPECIFICATION & OBJECT-ORIENTED PROGRAMMING MANUAL", ParagraphStyle(
        'SuperTag', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=C_GOLD, spaceAfter=5
    )))
    story.append(Paragraph("DriveEase: Complete Java Codebase & OOP Guide", title_style))
    story.append(Paragraph(
        "An Exhaustive File-by-File Technical Deep Dive and Engineering Analysis of All 52 Java (.java) Source Files, Core OOP Principles, Gang-of-Four Design Patterns, and Enterprise Spring Boot Architecture.",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_ACCENT, spaceBefore=0, spaceAfter=8))

    # Metadata Table
    meta_data = [
        [
            Paragraph("Primary Language:", meta_label), Paragraph("Java 21 LTS (Oracle / Temurin)", meta_val),
            Paragraph("Application Framework:", meta_label), Paragraph("Spring Boot 4.0 / Spring WebMVC", meta_val)
        ],
        [
            Paragraph("Total Java Files:", meta_label), Paragraph("52 .java Files (10 Packages)", meta_val),
            Paragraph("Data Persistence:", meta_label), Paragraph("Spring Data JPA & Hibernate 6", meta_val)
        ],
        [
            Paragraph("Subject Focus:", meta_label), Paragraph("Pure Java Code & OOP Deep-Dive", meta_val),
            Paragraph("Security & Cryptography:", meta_label), Paragraph("Spring Security 6 (BCrypt Salted Hash)", meta_val)
        ],
        [
            Paragraph("Design Patterns:", meta_label), Paragraph("Strategy, Factory, Singleton, DTO, Repo", meta_val),
            Paragraph("Author / Developer:", meta_label), Paragraph("Anish B R", meta_val)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[105, 156, 115, 146])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # Executive Overview Box
    abs_text = (
        "<b>Executive Purpose:</b> This document serves as the authoritative, definitive reference for every single line "
        "and component of <b>Java code</b> in the DriveEase Vehicle Rental System. Departing strictly from non-Java frontend "
        "concerns, this manual dissects the <b>52 Java source files</b> across all 10 packages. It examines how core "
        "<b>Object-Oriented Programming (OOP)</b> principles (Encapsulation, Inheritance, Polymorphism, Abstraction) and "
        "proven <b>Design Patterns</b> (Strategy, Factory Method, Singleton, Repository, DTO, Controller Advice) are woven "
        "into enterprise-grade Java 21 architectures. Each class, interface, enum, method, and annotation is comprehensively documented."
    )
    t_abs = Table([[Paragraph(abs_text, body_style)]], colWidths=[content_width])
    t_abs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(t_abs)
    story.append(Spacer(1, 8))

    # Package Hierarchy Breakdown Table
    story.append(Paragraph("1. Java Package Architecture & Communication Topology", h1_style))
    story.append(Paragraph(
        "The DriveEase backend is strictly structured into 10 cohesive packages following standard Spring architectural tiers:",
        body_style
    ))

    pkg_summary_data = [
        [Paragraph("Package Name", th_style), Paragraph("Files", th_style), Paragraph("Core Responsibility & Architectural Boundary", th_style)],
        [
            Paragraph("com.driveease", td_code), Paragraph("1", td_bold),
            Paragraph("Root entry point; contains <code>DriveeaseApplication.java</code> bootstrap class with Spring Boot starter.", td_style)
        ],
        [
            Paragraph("com.driveease.config", td_code), Paragraph("2", td_bold),
            Paragraph("Spring configuration beans; database seeder (<code>DataInitializer</code>) and security filter chain (<code>SecurityConfig</code>).", td_style)
        ],
        [
            Paragraph("com.driveease.model", td_code), Paragraph("11", td_bold),
            Paragraph("Rich domain entities (<code>Vehicle</code>, <code>Car</code>, <code>Motorcycle</code>, <code>Booking</code>, <code>User</code>) and 6 domain enums.", td_style)
        ],
        [
            Paragraph("com.driveease.repository", td_code), Paragraph("3", td_bold),
            Paragraph("Spring Data JPA repositories executing type-safe queries and JPQL aggregations on database entities.", td_style)
        ],
        [
            Paragraph("com.driveease.strategy", td_code), Paragraph("4", td_bold),
            Paragraph("Strategy & Factory design patterns implementing dynamic, duration-dependent rental pricing and discounts.", td_style)
        ],
        [
            Paragraph("com.driveease.service", td_code), Paragraph("10", td_bold),
            Paragraph("Interface contracts & concrete implementations containing transactional business logic, caching, and algorithms.", td_style)
        ],
        [
            Paragraph("com.driveease.dto", td_code), Paragraph("12", td_bold),
            Paragraph("Data Transfer Objects decoupling entity persistence structures from external REST client JSON payloads.", td_style)
        ],
        [
            Paragraph("com.driveease.controller", td_code), Paragraph("5", td_bold),
            Paragraph("RESTful WebMVC endpoints dispatching JSON responses, handling HTTP verbs, status codes, and input validation.", td_style)
        ],
        [
            Paragraph("com.driveease.exception", td_code), Paragraph("3", td_bold),
            Paragraph("Custom runtime exceptions and global <code>@RestControllerAdvice</code> interceptor unifying error payloads.", td_style)
        ],
        [
            Paragraph("com.driveease (test)", td_code), Paragraph("1", td_bold),
            Paragraph("Spring Boot context integration test verifying healthy dependency injection container bootstrap.", td_style)
        ]
    ]
    t_pkg = Table(pkg_summary_data, colWidths=[120, 36, 366])
    t_pkg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_BG_LIGHT])
    ]))
    story.append(t_pkg)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: THE 4 PILLARS OF OOP IN DRIVEEASE JAVA CODE
    # =========================================================================
    story.append(Paragraph("2. The Four Pillars of OOP in DriveEase Java Implementation", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "DriveEase avoids 'anemic data containers' by embedding authentic Object-Oriented behaviors directly into its Java classes:",
        body_style
    ))

    # 2.1 Encapsulation
    story.append(Paragraph("2.1 Encapsulation (Information Hiding & Invariant Enforcement)", h2_style))
    story.append(Paragraph(
        "Encapsulation protects internal object state from unauthorized or inconsistent external mutation. In DriveEase:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Private State Declaration:</b> Every instance field in <code>Vehicle</code>, <code>Car</code>, <code>Motorcycle</code>, <code>Booking</code>, and <code>User</code> is declared <code>private</code>. Mutation occurs strictly through validated setter methods or internal domain operations.<br/>"
        "• <b>Rich Domain Calculations (Anti-Anemic Model):</b> In <code>Booking.java</code>, the method <code>calculatePricing()</code> encapsulates days calculation, daily rate extraction, subtotal computation, 10% discount evaluation, tax calculation (10%), and security deposit addition. External callers cannot arbitrarily set the total amount.<br/>"
        "• <b>State Machine Invariant Guard:</b> The method <code>canBeCancelled()</code> encapsulates the business validation rule: cancellations are permitted ONLY if the booking is currently <code>CONFIRMED</code> and the start date is in the future.<br/>"
        "• <b>Atomic State Transition:</b> The method <code>cancel()</code> changes the status to <code>CANCELLED</code>, sets the timestamp, and marks <code>depositRefunded = true</code> in one atomic, encapsulated operation.",
        body_style
    ))

    # Code Box for Encapsulation
    story.append(make_code_box(
        "// Encapsulation in Booking.java: Internalizing business logic and protecting invariants\n"
        "public boolean canBeCancelled() {\n"
        "    if (this.status == BookingStatus.CANCELLED || this.status == BookingStatus.COMPLETED) {\n"
        "        return false;\n"
        "    }\n"
        "    return !startDate.isBefore(LocalDate.now()); // Future bookings only\n"
        "}\n\n"
        "public void cancel() {\n"
        "    if (!canBeCancelled()) {\n"
        "        throw new IllegalStateException(\"Booking cannot be cancelled at this stage\");\n"
        "    }\n"
        "    this.status = BookingStatus.CANCELLED;\n"
        "    this.cancelledAt = LocalDateTime.now();\n"
        "    this.paymentStatus = \"REFUNDED\"; // Encapsulated financial state transition\n"
        "}"
    ))
    story.append(Spacer(1, 6))

    # 2.2 Inheritance
    story.append(Paragraph("2.2 Inheritance & Entity Hierarchies (IS-A Relationship)", h2_style))
    story.append(Paragraph(
        "Inheritance creates specialized abstractions derived from a generalized base class, eliminating redundant schema declarations:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Abstract Base Class (<code>Vehicle.java</code>):</b> Implements 16 shared automotive attributes: <code>id</code>, <code>brand</code>, <code>model</code>, <code>category</code>, <code>fuelType</code>, <code>transmission</code>, <code>dailyRate</code>, <code>securityDeposit</code>, <code>imageUrl</code>, <code>description</code>, <code>available</code>, <code>rating</code>, <code>location</code>, <code>features</code>, <code>isPremium</code>, <code>vehicleOrigin</code>.<br/>"
        "• <b>Derived Class 1 (<code>Car.java</code>):</b> <code>public class Car extends Vehicle</code> introduces automobile-specific state: <code>seatingCapacity</code>, <code>luggageCapacity</code>, <code>bodyType</code>, and <code>hasAirConditioning</code>.<br/>"
        "• <b>Derived Class 2 (<code>Motorcycle.java</code>):</b> <code>public class Motorcycle extends Vehicle</code> introduces two-wheeler state: <code>engineCc</code>, <code>bikeType</code>, and <code>hasHelmetIncluded</code>.<br/>"
        "• <b>JPA Single-Table Inheritance:</b> Mapped with <code>@Inheritance(strategy = InheritanceType.SINGLE_TABLE)</code> and <code>@DiscriminatorColumn(name = \"vehicle_type\")</code>, unifying persistence into a single high-performance SQL table without join penalties.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # 2.3 Polymorphism
    story.append(Paragraph("2.3 Polymorphism (Dynamic Method Dispatch & Interfaces)", h2_style))
    story.append(Paragraph(
        "Polymorphism allows objects of derived classes to be manipulated through base class references, executing specialized behaviors at runtime:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Abstract Polymorphic Methods:</b> <code>Vehicle</code> defines abstract methods:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;1. <code>public abstract String getVehicleSpecificationsSummary();</code><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;2. <code>public abstract BigDecimal calculateBaseInsurance(int days);</code><br/>"
        "• <b>Subclass Overrides:</b> In <code>Car.java</code>, specs format seating and bag capacity; in <code>Motorcycle.java</code>, specs format engine displacement (cc) and helmet inclusion. Insurance in <code>Car</code> incorporates vehicle valuation multipliers, whereas in <code>Motorcycle</code> it charges two-wheeler liability rates.<br/>"
        "• <b>No Type Cascading:</b> The service layer (<code>VehicleServiceImpl</code>) and booking service process <code>Vehicle</code> references polymorphically without needing brittle <code>instanceof</code> or procedural <code>if/else</code> chains.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: ABSTRACTION & DESIGN PATTERNS IN JAVA
    # =========================================================================
    story.append(Paragraph("2.4 Abstraction & Architectural Decoupling", h2_style))
    story.append(Paragraph(
        "Abstraction hides complex implementation mechanics behind clean, contract-driven interfaces:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Service Contracts:</b> Interfaces (<code>VehicleService</code>, <code>BookingService</code>, <code>CurrencyService</code>, <code>UserService</code>, <code>DashboardService</code>) define the business capabilities of the application. Client controllers consume the interface without knowing whether data comes from H2, MySQL, or an external forex API.<br/>"
        "• <b>Persistence Abstraction:</b> Repositories extend <code>org.springframework.data.jpa.repository.JpaRepository</code>, abstracting JDBC connection pooling, prepared statements, and transaction management.<br/>"
        "• <b>DTO Abstraction:</b> Data Transfer Objects prevent internal JPA entity graphs from leaking to REST clients, preventing over-fetching and protecting internal entity fields from mass-assignment vulnerabilities.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3. Design Patterns Implemented in Java", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("3.1 The Strategy Design Pattern (Dynamic Pricing Engine)", h2_style))
    story.append(Paragraph(
        "The Strategy Pattern defines a family of interchangeable algorithms. In DriveEase, rental pricing is governed by the Strategy Pattern:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Strategy Interface (<code>RentalPricingStrategy.java</code>):</b> Declares <code>calculateSubtotal(dailyRate, days)</code>, <code>calculateDiscount(subtotal, days)</code>, and <code>getStrategyName()</code>.<br/>"
        "• <b>Concrete Strategy 1 (<code>StandardPricingStrategy.java</code>):</b> Computes base linear daily pricing (dailyRate * days) with zero discounts.<br/>"
        "• <b>Concrete Strategy 2 (<code>WeeklyDiscountPricingStrategy.java</code>):</b> Evaluates duration and applies an automated 10% saver discount for extended rentals (>= 7 days).<br/>"
        "• <b>Extensibility:</b> New pricing strategies (e.g. <code>WeekendSurgePricingStrategy</code>, <code>CorporateDiscountStrategy</code>) can be added by implementing the interface without modifying existing code (adhering to the Open/Closed Principle).",
        body_style
    ))

    # Code Box for Strategy
    story.append(make_code_box(
        "// Strategy Interface and Concrete Implementation in package com.driveease.strategy\n"
        "public interface RentalPricingStrategy {\n"
        "    BigDecimal calculateSubtotal(BigDecimal dailyRate, int days);\n"
        "    BigDecimal calculateDiscount(BigDecimal subtotal, int days);\n"
        "    String getStrategyName();\n"
        "}\n\n"
        "@Component(\"weeklyDiscountPricingStrategy\")\n"
        "public class WeeklyDiscountPricingStrategy implements RentalPricingStrategy {\n"
        "    private static final BigDecimal DISCOUNT_RATE = new BigDecimal(\"0.10\"); // 10% saver\n"
        "    @Override\n"
        "    public BigDecimal calculateDiscount(BigDecimal subtotal, int days) {\n"
        "        if (days >= 7) {\n"
        "            return subtotal.multiply(DISCOUNT_RATE).setScale(2, RoundingMode.HALF_UP);\n"
        "        }\n"
        "        return BigDecimal.ZERO.setScale(2, RoundingMode.HALF_UP);\n"
        "    }\n"
        "}"
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.2 The Factory Method Pattern (Strategy Factory)", h2_style))
    story.append(Paragraph(
        "<b><code>PricingStrategyFactory.java</code></b> encapsulates the decision logic for strategy instantiation. "
        "It injects all available pricing strategies via Spring Dependency Injection and exposes <code>getStrategy(int days)</code>. "
        "Callers simply pass the rental duration and receive the optimal strategy without procedural branching in caller code.",
        body_style
    ))

    story.append(Paragraph("3.3 Singleton Pattern (Spring Bean Management)", h2_style))
    story.append(Paragraph(
        "Every Spring-managed bean annotated with <code>@Service</code>, <code>@Component</code>, <code>@Repository</code>, or <code>@Configuration</code> "
        "is registered as a thread-safe Singleton within the Spring <code>ApplicationContext</code>, ensuring optimal memory efficiency.",
        body_style
    ))

    story.append(Paragraph("3.4 Repository Pattern & Global Exception Interceptor Pattern", h2_style))
    story.append(Paragraph(
        "• <b>Repository Pattern:</b> Isolates domain logic from data persistence (<code>VehicleRepository</code>, <code>BookingRepository</code>, <code>UserRepository</code>).<br/>"
        "• <b>Controller Advice Pattern:</b> <code>GlobalExceptionHandler.java</code> uses <code>@RestControllerAdvice</code> and <code>@ExceptionHandler</code> to intercept exceptions system-wide, transforming unhandled errors into standardized <code>ApiResponse</code> JSON structures.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: DETAILED BREAKDOWN — ROOT, CONFIG, SECURITY
    # =========================================================================
    story.append(Paragraph("4. Exhaustive File-by-File Java Code Breakdown (All 52 Files)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("4.1 Root Bootstrap Package (<code>com.driveease</code>)", h2_style))
    story.append(make_file_box(
        filename="DriveeaseApplication.java",
        package="com.driveease",
        purpose="The main entry point and bootstrap class of the entire application. Initializes the Spring ApplicationContext, starts the embedded Tomcat server on the configured port, and initiates component scanning.",
        annotations="<code>@SpringBootApplication</code>: Meta-annotation combining <code>@Configuration</code>, <code>@EnableAutoConfiguration</code>, and <code>@ComponentScan</code> across all sub-packages.",
        methods_fields="<code>public static void main(String[] args)</code>: Executes <code>SpringApplication.run(DriveeaseApplication.class, args)</code>.",
        oop_notes="Entry point pattern; kicks off Spring Inversion of Control (IoC) dependency injection container."
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.2 Configuration Package (<code>com.driveease.config</code>)", h2_style))
    story.append(make_file_box(
        filename="SecurityConfig.java",
        package="com.driveease.config",
        purpose="Defines the application's security policy, authentication mechanisms, password hashing, and role-based access control (RBAC). Configures which endpoints are public and which require customer or admin privileges.",
        annotations="<code>@Configuration</code>: Designates the class as a source of bean definitions. <code>@EnableWebSecurity</code>: Activates Spring Security Web filter chain integration. <code>@Bean</code>: Registers managed security beans.",
        methods_fields="<code>passwordEncoder()</code>: Returns <code>new BCryptPasswordEncoder()</code>. <code>userDetailsService()</code>: Implements functional interface lambda querying <code>userRepository.findByEmail()</code>. <code>authenticationProvider()</code>: Configures <code>DaoAuthenticationProvider</code>. <code>securityFilterChain(HttpSecurity)</code>: Configures CSRF, sessions, public routes, and RBAC rules (<code>/api/admin/**</code> restricted to <code>ROLE_ADMIN</code>; <code>/api/bookings/**</code> restricted to authenticated users).",
        oop_notes="Implements the Adapter & Builder patterns (via <code>HttpSecurity</code> builder); utilizes lambda expressions and functional interfaces."
    ))
    story.append(Spacer(1, 6))

    story.append(make_file_box(
        filename="DataInitializer.java",
        package="com.driveease.config",
        purpose="Database seeder that executes upon application startup to populate users, vehicles, and bookings. Ensures that the system is fully operational with realistic data on fresh launch or restart.",
        annotations="<code>@Component</code>: Spring-managed component auto-detected during component scanning. Implements <code>CommandLineRunner</code>: Spring Boot callback interface executed right after the application context loads.",
        methods_fields="<code>run(String... args)</code>: Orchestrates data initialization. <code>seedUsers()</code>: Seeds Admin (<code>admin@driveease.com</code>), John Doe, Arjun Sharma, and Priya Patel with BCrypt hashed passwords. <code>seedVehicles()</code>: Seeds 36 authentic vehicles spanning hatchbacks, sedans, SUVs, electric vehicles, luxury badges, and motorcycles. <code>seedBookings()</code>: Seeds representative confirmed, active, and completed rental contracts. <code>upsertVehicle()</code> & <code>upsertUser()</code>: Helper methods ensuring idempotent database operations.",
        oop_notes="Demonstrates the Template Method Pattern (via <code>CommandLineRunner.run()</code>); polymorphic instantiation of <code>Car</code> and <code>Motorcycle</code> instances."
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: DOMAIN MODELS & ENTITIES (PART 1)
    # =========================================================================
    story.append(Paragraph("4.3 Domain Models & Entity Hierarchy (<code>com.driveease.model</code>)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(make_file_box(
        filename="Vehicle.java",
        package="com.driveease.model",
        purpose="Abstract base class representing any motorized rental vehicle in the fleet. Establishes the foundational attributes and abstract polymorphic contracts for specialized vehicle types.",
        annotations="<code>@Entity</code>, <code>@Table(name = 'vehicles')</code>, <code>@Inheritance(strategy = InheritanceType.SINGLE_TABLE)</code>, <code>@DiscriminatorColumn(name = 'vehicle_type', discriminatorType = DiscriminatorType.STRING)</code>, Jakarta validation annotations (<code>@NotBlank</code>, <code>@NotNull</code>, <code>@DecimalMin</code>).",
        methods_fields="16 private fields: <code>id</code>, <code>brand</code>, <code>model</code>, <code>category</code>, <code>fuelType</code>, <code>transmission</code>, <code>dailyRate</code>, <code>securityDeposit</code>, <code>imageUrl</code>, <code>description</code>, <code>available</code>, <code>rating</code>, <code>location</code>, <code>features</code>, <code>isPremium</code>, <code>vehicleOrigin</code>, <code>baseCurrency</code>. Abstract methods: <code>public abstract String getVehicleSpecificationsSummary()</code> and <code>public abstract BigDecimal calculateBaseInsurance(int days)</code>. Comprehensive getters and setters.",
        oop_notes="Exemplar of Abstraction, Encapsulation, and Polymorphism. Declares abstract contracts overridden by subclasses; protects internal state via private fields."
    ))
    story.append(Spacer(1, 6))

    story.append(make_file_box(
        filename="Car.java",
        package="com.driveease.model",
        purpose="Concrete entity extending <code>Vehicle</code> representing automobiles (sedans, SUVs, hatchbacks, electric cars, luxury saloons). Adds passenger and cargo capacity attributes.",
        annotations="<code>@Entity</code>, <code>@DiscriminatorValue('CAR')</code>: Mapped to discriminator column in single-table schema.",
        methods_fields="Car-specific private fields: <code>seatingCapacity</code> (int), <code>luggageCapacity</code> (int), <code>bodyType</code> (String), <code>hasAirConditioning</code> (boolean). Overridden methods: <code>getVehicleSpecificationsSummary()</code> formats seating, bags, and A/C status. <code>calculateBaseInsurance(int days)</code> calculates car risk insurance.",
        oop_notes="Inheritance (extends <code>Vehicle</code>); Polymorphism (overrides abstract methods with car-specific logic); Constructor chaining using <code>super(...)</code>."
    ))
    story.append(Spacer(1, 6))

    story.append(make_file_box(
        filename="Motorcycle.java",
        package="com.driveease.model",
        purpose="Concrete entity extending <code>Vehicle</code> representing two-wheelers (cruisers, sport bikes, adventure tourers). Adds displacement and safety equipment attributes.",
        annotations="<code>@Entity</code>, <code>@DiscriminatorValue('MOTORCYCLE')</code>: JPA discriminator value for two-wheeler rows.",
        methods_fields="Motorcycle-specific private fields: <code>engineCc</code> (int), <code>bikeType</code> (String), <code>hasHelmetIncluded</code> (boolean). Overridden methods: <code>getVehicleSpecificationsSummary()</code> formats displacement and helmet inclusion. <code>calculateBaseInsurance(int days)</code> calculates motorcycle liability premium.",
        oop_notes="Inheritance; Polymorphism; Encapsulation; Constructor chaining using <code>super(...)</code>."
    ))
    story.append(Spacer(1, 6))

    story.append(make_file_box(
        filename="User.java",
        package="com.driveease.model",
        purpose="Represents registered users in the system (both customers and administrators). Stores authentication credentials, contact details, and role assignments.",
        annotations="<code>@Entity</code>, <code>@Table(name = 'users')</code>, <code>@Column(unique = true)</code> on email, Jakarta validation constraints.",
        methods_fields="Private fields: <code>id</code>, <code>email</code>, <code>password</code> (BCrypt hash), <code>fullName</code>, <code>phoneNumber</code>, <code>role</code> (Role enum), <code>createdAt</code>. Domain methods: <code>isAdmin()</code> returns true if <code>role == Role.ROLE_ADMIN</code>. Complete getters and setters.",
        oop_notes="Encapsulation of identity and credential state; domain business method <code>isAdmin()</code>."
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: DOMAIN MODELS & ENUMS (PART 2)
    # =========================================================================
    story.append(Paragraph("4.3 Domain Models (Cont.) & Model Enums", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(make_file_box(
        filename="Booking.java",
        package="com.driveease.model",
        purpose="Core transactional entity representing a vehicle rental contract between a <code>User</code> and a <code>Vehicle</code>. Encapsulates rental dates, financial breakdowns, deposit tracking, and lifecycle states.",
        annotations="<code>@Entity</code>, <code>@Table(name = 'bookings')</code>, <code>@ManyToOne(fetch = FetchType.EAGER)</code> mappings to <code>User</code> and <code>Vehicle</code>, <code>@Enumerated(EnumType.STRING)</code> for status.",
        methods_fields="Fields: <code>id</code>, <code>bookingNumber</code>, <code>user</code>, <code>vehicle</code>, <code>startDate</code>, <code>endDate</code>, <code>totalDays</code>, <code>dailyRate</code>, <code>subtotal</code>, <code>discountAmount</code>, <code>taxAmount</code>, <code>securityDeposit</code>, <code>totalAmount</code>, <code>status</code>, <code>pickupLocation</code>, <code>dropoffLocation</code>, <code>paymentStatus</code>, <code>createdAt</code>, <code>cancelledAt</code>. Domain methods: <code>calculatePricing()</code> (calculates duration, subtotal, 10% discount for rentals >= 7 days, 10% tax, total). <code>canBeCancelled()</code> (validates cancellation eligibility). <code>cancel()</code> (atomic transition to CANCELLED and refund trigger).",
        oop_notes="Rich Domain Model (Anti-Anemic); Encapsulation of pricing algorithms and reservation lifecycle state machine."
    ))
    story.append(Spacer(1, 6))

    # Table of Domain Enums
    story.append(Paragraph("Domain Enums in Package <code>com.driveease.model</code>:", h2_style))
    story.append(Paragraph(
        "Enums provide type-safe constants preventing invalid state values across the application:",
        body_style
    ))

    enum_data = [
        [Paragraph("Enum File", th_style), Paragraph("Values & Constants", th_style), Paragraph("Domain Meaning & Architectural Usage", th_style)],
        [
            Paragraph("Role.java", td_code),
            Paragraph("<code>ROLE_CUSTOMER</code>, <code>ROLE_ADMIN</code>", td_style),
            Paragraph("Authorities mapped directly to Spring Security's <code>GrantedAuthority</code> for RBAC endpoint protection.", td_style)
        ],
        [
            Paragraph("BookingStatus.java", td_code),
            Paragraph("<code>PENDING</code>, <code>CONFIRMED</code>, <code>ACTIVE</code>, <code>COMPLETED</code>, <code>CANCELLED</code>", td_style),
            Paragraph("Governs the finite state machine of a reservation from draft to return or cancellation.", td_style)
        ],
        [
            Paragraph("VehicleCategory.java", td_code),
            Paragraph("<code>CAR</code>, <code>MOTORCYCLE</code>", td_style),
            Paragraph("High-level classification determining specification pill rendering and rate structures.", td_style)
        ],
        [
            Paragraph("VehicleOrigin.java", td_code),
            Paragraph("<code>INDIAN</code>, <code>INTERNATIONAL</code>", td_style),
            Paragraph("Classifies fleet assets into domestic Indian market models vs. imported international vehicles.", td_style)
        ],
        [
            Paragraph("FuelType.java", td_code),
            Paragraph("<code>PETROL</code>, <code>DIESEL</code>, <code>ELECTRIC</code>, <code>HYBRID</code>", td_style),
            Paragraph("Powertrain specification used in catalog filtering and vehicle detail specifications.", td_style)
        ],
        [
            Paragraph("TransmissionType.java", td_code),
            Paragraph("<code>MANUAL</code>, <code>AUTOMATIC</code>", td_style),
            Paragraph("Gearbox specification filter ensuring customers select suitable driving configurations.", td_style)
        ]
    ]
    t_enum = Table(enum_data, colWidths=[110, 160, 252])
    t_enum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_BG_LIGHT])
    ]))
    story.append(t_enum)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: DATA ACCESS & REPOSITORIES
    # =========================================================================
    story.append(Paragraph("4.4 Data Access Layer (<code>com.driveease.repository</code>)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "Spring Data JPA repositories abstract low-level SQL and JDBC, providing type-safe CRUD operations and JPQL query dispatching:",
        body_style
    ))

    story.append(make_file_box(
        filename="VehicleRepository.java",
        package="com.driveease.repository",
        purpose="Manages persistence and retrieval operations for the <code>Vehicle</code> polymorphic entity hierarchy. Implements custom JPQL queries for multi-criteria fleet filtering.",
        annotations="<code>@Repository</code>, extends <code>JpaRepository<Vehicle, Long></code>.",
        methods_fields="Methods: <code>findByIsAvailableTrue()</code>, <code>findByIsPremiumTrue()</code>, <code>findByCategory(VehicleCategory)</code>, <code>findByVehicleOrigin(VehicleOrigin)</code>, <code>findByRatingGreaterThanEqual(Double)</code>. Custom <code>@Query</code>: <code>findFilteredVehicles(...)</code> handling optional category, origin, premium, search text, fuel type, transmission, and max price in a single query.",
        oop_notes="Repository Pattern; Abstraction of SQL; Polymorphic querying (returns mixed Car and Motorcycle lists)."
    ))
    story.append(Spacer(1, 6))

    story.append(make_file_box(
        filename="BookingRepository.java",
        package="com.driveease.repository",
        purpose="Manages persistence and aggregation operations for <code>Booking</code> records. Executes custom JPQL calculations for dashboard KPIs.",
        annotations="<code>@Repository</code>, extends <code>JpaRepository<Booking, Long></code>.",
        methods_fields="Methods: <code>findByUserOrderByCreatedAtDesc(User)</code>, <code>findByStatus(BookingStatus)</code>, <code>findByBookingNumber(String)</code>. Custom KPI Queries: <code>countByStatus(BookingStatus)</code>, <code>sumTotalRevenue()</code> (aggregates completed/active revenue via <code>COALESCE(SUM(b.totalAmount), 0)</code>), <code>findRecentBookings(Pageable)</code>.",
        oop_notes="Repository Pattern; Information Hiding; Separation of database query logic from business services."
    ))
    story.append(Spacer(1, 6))

    story.append(make_file_box(
        filename="UserRepository.java",
        package="com.driveease.repository",
        purpose="Manages user entity persistence and credential lookups for authentication.",
        annotations="<code>@Repository</code>, extends <code>JpaRepository<User, Long></code>.",
        methods_fields="Methods: <code>findByEmail(String email)</code> (returns <code>Optional<User></code> for safe null handling), <code>existsByEmail(String email)</code> (returns boolean for fast duplicate email verification during registration).",
        oop_notes="Repository Pattern; Functional Java using <code>Optional<T></code> to eliminate <code>NullPointerException</code> risks."
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: PRICING STRATEGY & FACTORY PATTERN
    # =========================================================================
    story.append(Paragraph("4.5 Pricing Strategy & Factory Pattern (<code>com.driveease.strategy</code>)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(make_file_box(
        filename="RentalPricingStrategy.java",
        package="com.driveease.strategy",
        purpose="Strategy interface defining the algorithm contract for calculating vehicle rental charges and duration-based discounts.",
        annotations="Interface declaration (no Spring annotations on interface).",
        methods_fields="<code>BigDecimal calculateSubtotal(BigDecimal dailyRate, int days)</code>: Computes gross rental charges. <code>BigDecimal calculateDiscount(BigDecimal subtotal, int days)</code>: Computes applicable savings. <code>String getStrategyName()</code>: Returns human-readable strategy description.",
        oop_notes="Strategy Pattern; Abstraction; Polymorphism. Enables interchangeable pricing algorithms without modifying client code."
    ))
    story.append(Spacer(1, 6))

    story.append(make_file_box(
        filename="StandardPricingStrategy.java",
        package="com.driveease.strategy",
        purpose="Concrete strategy implementing regular daily pricing with no discounts applied (used for short-term rentals < 7 days).",
        annotations="<code>@Component('standardPricingStrategy')</code>: Registered as a named Spring Bean.",
        methods_fields="<code>calculateSubtotal()</code>: Multiplies dailyRate by days with <code>RoundingMode.HALF_UP</code>. <code>calculateDiscount()</code>: Returns <code>BigDecimal.ZERO</code>. <code>getStrategyName()</code>: Returns 'Standard Daily Rate'.",
        oop_notes="Polymorphic implementation of <code>RentalPricingStrategy</code>; strict financial rounding using <code>BigDecimal</code>."
    ))
    story.append(Spacer(1, 6))

    story.append(make_file_box(
        filename="WeeklyDiscountPricingStrategy.java",
        package="com.driveease.strategy",
        purpose="Concrete strategy offering an automated 10% saver discount for extended rentals lasting 7 days or more.",
        annotations="<code>@Component('weeklyDiscountPricingStrategy')</code>: Registered as a named Spring Bean.",
        methods_fields="Constant: <code>DISCOUNT_RATE = new BigDecimal('0.10')</code>. <code>calculateSubtotal()</code>: Linear calculation. <code>calculateDiscount()</code>: If days >= 7, returns <code>subtotal.multiply(DISCOUNT_RATE)</code>; otherwise returns zero. <code>getStrategyName()</code>: Returns 'Weekly Rental (10% Saver Discount)'.",
        oop_notes="Polymorphism; Strategy Pattern; Encapsulation of promotional pricing rules."
    ))
    story.append(Spacer(1, 6))

    story.append(make_file_box(
        filename="PricingStrategyFactory.java",
        package="com.driveease.strategy",
        purpose="Factory class that dynamically inspects rental duration and returns the optimal <code>RentalPricingStrategy</code> implementation.",
        annotations="<code>@Component</code>: Spring-managed component.",
        methods_fields="Injected dependencies: <code>StandardPricingStrategy</code> and <code>WeeklyDiscountPricingStrategy</code> via constructor injection. Method: <code>public RentalPricingStrategy getStrategy(int days)</code>: Returns <code>weeklyDiscountPricingStrategy</code> if <code>days >= 7</code>, else returns <code>standardPricingStrategy</code>.",
        oop_notes="Factory Method Pattern; Loose Coupling; Inversion of Control (IoC)."
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: SERVICE LAYER (PART 1: VEHICLE, BOOKING, CURRENCY)
    # =========================================================================
    story.append(Paragraph("4.6 Service Layer Architecture (<code>com.driveease.service</code>)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "The Service Layer implements transactional business rules behind clear interface abstractions:",
        body_style
    ))

    story.append(make_file_box(
        filename="VehicleService.java & VehicleServiceImpl.java",
        package="com.driveease.service",
        purpose="Manages the vehicle fleet catalog, CRUD operations, availability toggles, premium classification, and multi-criteria filtering.",
        annotations="<code>@Service</code>, <code>@Transactional(readOnly = true)</code> at class level; <code>@Transactional</code> on mutating methods.",
        methods_fields="Methods: <code>getAllVehicles()</code>, <code>getVehicleById(Long)</code>, <code>getAvailableVehicles()</code>, <code>getFeaturedVehicles()</code>, <code>getPremiumVehicles()</code>, <code>filterVehicles(...)</code>, <code>createVehicle(VehicleRequest)</code>, <code>updateVehicle(Long, VehicleRequest)</code>, <code>deleteVehicle(Long)</code>, <code>toggleAvailability(Long)</code>, <code>togglePremium(Long, boolean)</code>. Helper: <code>mapToDto(Vehicle)</code> converts entities to <code>VehicleDto</code>.",
        oop_notes="Interface-Implementation Abstraction; Encapsulation of fleet state transitions; DTO conversion pattern."
    ))
    story.append(Spacer(1, 6))

    story.append(make_file_box(
        filename="BookingService.java & BookingServiceImpl.java",
        package="com.driveease.service",
        purpose="Coordinates the complete reservation lifecycle, price calculation via Strategy Pattern, reservation creation, customer history, status updates, and cancellations.",
        annotations="<code>@Service</code>, <code>@Transactional</code> on mutation workflows.",
        methods_fields="Injected: <code>BookingRepository</code>, <code>VehicleRepository</code>, <code>UserRepository</code>, <code>PricingStrategyFactory</code>. Methods: <code>createBooking(User, BookingRequest)</code>: Validates dates, retrieves vehicle, generates unique booking number, evaluates duration via <code>PricingStrategyFactory.getStrategy(days)</code>, invokes <code>booking.calculatePricing()</code>, and persists. <code>getUserBookings(User)</code>: Returns customer's bookings. <code>cancelBooking(Long, User)</code>: Verifies ownership, invokes domain method <code>booking.cancel()</code>, restores vehicle availability. <code>updateBookingStatus(Long, BookingStatus)</code>: Admin status transition manager.",
        oop_notes="Orchestrates Strategy and Factory patterns; enforces domain state machine invariants; transactional integrity."
    ))
    story.append(Spacer(1, 6))

    story.append(make_file_box(
        filename="CurrencyService.java & CurrencyServiceImpl.java",
        package="com.driveease.service",
        purpose="High-precision currency conversion engine with thread-safe in-memory caching and automated asynchronous foreign exchange rate fetching.",
        annotations="<code>@Service</code>; Spring <code>@Scheduled(fixedRate = 3600000)</code> for hourly background sync.",
        methods_fields="Constants: <code>BASE_CURRENCY = 'INR'</code>, supported currencies (INR, USD, EUR, GBP, AED). Thread-safe state: <code>ConcurrentHashMap<String, BigDecimal> cachedRates</code>. Methods: <code>getExchangeRates()</code>: Returns <code>CurrencyRatesDto</code> with cached rates and timestamp. <code>convert(BigDecimal, String, String)</code>: High-precision conversion using <code>RoundingMode.HALF_UP</code>. <code>refreshRatesAsync()</code>: Uses modern <code>java.net.http.HttpClient</code> to fetch rates asynchronously from financial API. <code>initFallbackRates()</code>: Seeds real-market fallback exchange rates (USD ≈ ₹86.20, EUR ≈ ₹90.10, GBP ≈ ₹107.50, AED ≈ ₹23.47).",
        oop_notes="Concurrency handling with <code>ConcurrentHashMap</code>; Abstraction via <code>CurrencyService</code> interface; Resilient fault-tolerant design."
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: SERVICE LAYER (PART 2: USER & DASHBOARD)
    # =========================================================================
    story.append(Paragraph("4.6 Service Layer (Cont.: User & Dashboard)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(make_file_box(
        filename="UserService.java & UserServiceImpl.java",
        package="com.driveease.service",
        purpose="Handles user registration, authentication credential validation, profile retrieval, and customer directory listing for administrators.",
        annotations="<code>@Service</code>, <code>@Transactional</code>.",
        methods_fields="Injected: <code>UserRepository</code>, <code>PasswordEncoder</code>. Methods: <code>register(RegisterRequest)</code>: Checks duplicate email via <code>existsByEmail()</code>, encrypts password using <code>passwordEncoder.encode()</code>, creates <code>User</code> entity with <code>ROLE_CUSTOMER</code>, and persists. <code>getUserByEmail(String)</code>: Returns <code>UserDto</code>. <code>getAllCustomers()</code>: Lists registered customers for admin portal. <code>mapToDto(User)</code>: DTO transformation helper.",
        oop_notes="Encapsulation of registration validation and cryptographic password hashing; DTO pattern."
    ))
    story.append(Spacer(1, 6))

    story.append(make_file_box(
        filename="DashboardService.java & DashboardServiceImpl.java",
        package="com.driveease.service",
        purpose="Aggregates platform KPI metrics for the administrative dashboard, including fleet count, active rentals, pending reservations, total revenue, and recent booking activity.",
        annotations="<code>@Service</code>, <code>@Transactional(readOnly = true)</code>.",
        methods_fields="Injected: <code>VehicleRepository</code>, <code>BookingRepository</code>, <code>UserRepository</code>. Method: <code>getDashboardSummary()</code>: Executes parallel repository aggregations (total vehicles, available vehicles, active rentals, total customers, gross revenue via <code>bookingRepository.sumTotalRevenue()</code>, and recent bookings) and packages them into <code>DashboardSummaryDto</code>.",
        oop_notes="Facade Pattern; aggregates complex multi-repository query results into a single consolidated DTO."
    ))
    story.append(Spacer(1, 6))

    # =========================================================================
    # EXCEPTION HANDLING
    # =========================================================================
    story.append(Paragraph("4.7 Exception Handling Subsystem (<code>com.driveease.exception</code>)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(make_file_box(
        filename="GlobalExceptionHandler.java",
        package="com.driveease.exception",
        purpose="Centralized, cross-cutting exception interceptor that catches uncaught exceptions across all REST controllers and translates them into uniform JSON responses.",
        annotations="<code>@RestControllerAdvice</code>: Combines <code>@ControllerAdvice</code> and <code>@ResponseBody</code>. <code>@ExceptionHandler(...)</code>: Maps specific exception types to HTTP status codes.",
        methods_fields="Methods: <code>handleNotFound(ResourceNotFoundException)</code> $\rightarrow$ 404 NOT_FOUND. <code>handleBadRequest(BadRequestException)</code> $\rightarrow$ 400 BAD_REQUEST. <code>handleIllegalState(IllegalStateException)</code> $\rightarrow$ 409 CONFLICT. <code>handleAccessDenied(AccessDeniedException)</code> $\rightarrow$ 403 FORBIDDEN. <code>handleValidationExceptions(MethodArgumentNotValidException)</code> $\rightarrow$ 400 BAD_REQUEST with field-by-field error map. <code>handleGeneralException(Exception)</code> $\rightarrow$ 500 INTERNAL_SERVER_ERROR.",
        oop_notes="Interceptor Pattern; Centralized Error Handling; Uniform Contract Enforcement."
    ))
    story.append(Spacer(1, 6))

    story.append(make_file_box(
        filename="BadRequestException.java & ResourceNotFoundException.java",
        package="com.driveease.exception",
        purpose="Custom unchecked domain runtime exceptions representing invalid user inputs and missing database entities.",
        annotations="No Spring annotations; standard Java subclass of <code>RuntimeException</code>.",
        methods_fields="Constructors: <code>BadRequestException(String message)</code> and <code>ResourceNotFoundException(String message)</code> forwarding message to <code>super(message)</code>.",
        oop_notes="Inheritance (extends <code>RuntimeException</code>); Custom Exception Hierarchy."
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: DATA TRANSFER OBJECTS (DTOs)
    # =========================================================================
    story.append(Paragraph("4.8 Data Transfer Objects (<code>com.driveease.dto</code>)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "The DTO layer decouples the internal relational database schema from external API clients, ensuring contract stability and security:",
        body_style
    ))

    dto_table_data = [
        [Paragraph("DTO Class Name", th_style), Paragraph("Type / Direction", th_style), Paragraph("Core Fields, Purpose & Validation Constraints", th_style)],
        [
            Paragraph("ApiResponse.java", td_code), Paragraph("Response (Generic)", td_bold),
            Paragraph("Universal API envelope: <code>boolean success</code>, <code>String message</code>, <code>T data</code>, <code>LocalDateTime timestamp</code>. Static helpers: <code>ApiResponse.success(data)</code>, <code>ApiResponse.error(msg)</code>.", td_style)
        ],
        [
            Paragraph("AuthResponse.java", td_code), Paragraph("Response", td_bold),
            Paragraph("Returned upon successful sign-in: <code>String token/sessionId</code>, <code>UserDto user</code>, <code>String message</code>.", td_style)
        ],
        [
            Paragraph("LoginRequest.java", td_code), Paragraph("Request", td_bold),
            Paragraph("Credentials payload: <code>@NotBlank String email</code>, <code>@NotBlank String password</code>.", td_style)
        ],
        [
            Paragraph("RegisterRequest.java", td_code), Paragraph("Request", td_bold),
            Paragraph("Customer registration: <code>@NotBlank fullName</code>, <code>@Email email</code>, <code>@Size(min=6) password</code>, <code>phoneNumber</code>.", td_style)
        ],
        [
            Paragraph("UserDto.java", td_code), Paragraph("Response", td_bold),
            Paragraph("Safe user profile without sensitive password hashes: <code>id</code>, <code>fullName</code>, <code>email</code>, <code>phoneNumber</code>, <code>role</code>.", td_style)
        ],
        [
            Paragraph("VehicleDto.java", td_code), Paragraph("Response", td_bold),
            Paragraph("Complete vehicle representation sent to UI: includes brand, model, dailyRate, isPremium, vehicleOrigin, specsSummary, insurance, features.", td_style)
        ],
        [
            Paragraph("VehicleRequest.java", td_code), Paragraph("Request", td_bold),
            Paragraph("Payload for admin creating/updating vehicles: includes category, brand, model, dailyRate, securityDeposit, vehicleOrigin, isPremium, specs.", td_style)
        ],
        [
            Paragraph("BookingRequest.java", td_code), Paragraph("Request", td_bold),
            Paragraph("Checkout submission payload: <code>vehicleId</code>, <code>startDate</code>, <code>endDate</code>, <code>pickupLocation</code>, <code>dropoffLocation</code>, <code>notes</code>.", td_style)
        ],
        [
            Paragraph("BookingStatusRequest.java", td_code), Paragraph("Request", td_bold),
            Paragraph("Admin payload for updating reservation status: <code>@NotNull BookingStatus status</code>.", td_style)
        ],
        [
            Paragraph("BookingDto.java", td_code), Paragraph("Response", td_bold),
            Paragraph("Detailed reservation invoice: includes bookingNumber, vehicle details, user details, totalDays, subtotal, discount, tax, deposit, total, status.", td_style)
        ],
        [
            Paragraph("CurrencyRatesDto.java", td_code), Paragraph("Response", td_bold),
            Paragraph("Multi-currency payload: <code>baseCurrency ('INR')</code>, <code>availableCurrencies</code>, <code>rates Map</code>, <code>lastUpdated</code>, <code>isFallback</code>.", td_style)
        ],
        [
            Paragraph("DashboardSummaryDto.java", td_code), Paragraph("Response", td_bold),
            Paragraph("Consolidated KPI metrics: totalVehicles, activeRentals, pendingBookings, totalCustomers, totalRevenue, recentBookings list.", td_style)
        ]
    ]
    t_dto = Table(dto_table_data, colWidths=[125, 75, 322])
    t_dto.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_BG_LIGHT])
    ]))
    story.append(t_dto)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: REST CONTROLLERS (API LAYER)
    # =========================================================================
    story.append(Paragraph("4.9 RESTful Controllers (<code>com.driveease.controller</code>)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "Controllers expose clean HTTP endpoints, perform DTO binding and validation, and delegate execution to the Service Layer:",
        body_style
    ))

    story.append(make_file_box(
        filename="VehicleController.java",
        package="com.driveease.controller",
        purpose="Public REST controller exposing fleet catalog discovery, details, and filtering endpoints.",
        annotations="<code>@RestController</code>, <code>@RequestMapping('/api/vehicles')</code>, <code>@CrossOrigin</code>.",
        methods_fields="Endpoints: <code>GET /api/vehicles</code> (filters by category, origin, premium, search, fuel, transmission, maxPrice, sortBy). <code>GET /api/vehicles/{id}</code> (returns single vehicle DTO). <code>GET /api/vehicles/available</code> (returns unreserved fleet). <code>GET /api/vehicles/featured</code> (returns top-rated models).",
        oop_notes="Presentation Layer Abstraction; delegates all filtering to <code>VehicleService</code>."
    ))
    story.append(Spacer(1, 6))

    story.append(make_file_box(
        filename="BookingController.java",
        package="com.driveease.controller",
        purpose="Handles customer reservation workflows, checkout submission, booking history retrieval, and reservation cancellations.",
        annotations="<code>@RestController</code>, <code>@RequestMapping('/api/bookings')</code>, <code>@AuthenticationPrincipal</code> injection.",
        methods_fields="Endpoints: <code>POST /api/bookings</code> (creates reservation for authenticated user with <code>@Valid BookingRequest</code>). <code>GET /api/bookings/my</code> (returns customer's reservation history). <code>GET /api/bookings/{id}</code> (retrieves single booking details). <code>PATCH /api/bookings/{id}/cancel</code> (cancels eligible booking and initiates refund).",
        oop_notes="Role-based Security enforcement; Session-based principal injection; Delegation to <code>BookingService</code>."
    ))
    story.append(Spacer(1, 6))

    story.append(make_file_box(
        filename="AuthController.java",
        package="com.driveease.controller",
        purpose="Manages customer registration, authentication sign-in, session invalidation (logout), and active user profile retrieval.",
        annotations="<code>@RestController</code>, <code>@RequestMapping('/api/auth')</code>.",
        methods_fields="Endpoints: <code>POST /api/auth/register</code> (registers customer via <code>userService.register()</code>). <code>POST /api/auth/login</code> (authenticates credentials via <code>AuthenticationManager</code>, establishes HTTP session). <code>POST /api/auth/logout</code> (invalidates session). <code>GET /api/auth/me</code> (returns authenticated user profile).",
        oop_notes="Security adapter; Session state management."
    ))
    story.append(Spacer(1, 6))

    story.append(make_file_box(
        filename="AdminController.java",
        package="com.driveease.controller",
        purpose="Administrative control panel exposing KPI metrics, fleet inventory management (CRUD), availability toggles, and booking status controls.",
        annotations="<code>@RestController</code>, <code>@RequestMapping('/api/admin')</code>; protected by Spring Security <code>ROLE_ADMIN</code>.",
        methods_fields="Endpoints: <code>GET /api/admin/dashboard</code> (returns KPI summary). <code>GET /api/admin/bookings</code> (lists all system bookings). <code>PATCH /api/admin/bookings/{id}/status</code> (updates reservation status). <code>POST /api/admin/vehicles</code> (adds vehicle). <code>PUT /api/admin/vehicles/{id}</code> (updates vehicle). <code>DELETE /api/admin/vehicles/{id}</code> (removes vehicle). <code>PATCH /api/admin/vehicles/{id}/premium</code> (toggles premium flag). <code>PATCH /api/admin/vehicles/{id}/availability</code> (toggles availability). <code>GET /api/admin/customers</code> (lists customer directory).",
        oop_notes="Administrative Facade; Role-Based Access Control (RBAC)."
    ))
    story.append(Spacer(1, 6))

    story.append(make_file_box(
        filename="CurrencyController.java",
        package="com.driveease.controller",
        purpose="Exposes live foreign exchange rates and on-demand conversion calculations to web clients.",
        annotations="<code>@RestController</code>, <code>@RequestMapping('/api/currency')</code>.",
        methods_fields="Endpoints: <code>GET /api/currency/rates</code> (returns base INR currency, supported currencies, and cached forex rates). <code>GET /api/currency/convert?amount=&from=&to=</code> (performs ad-hoc conversion).",
        oop_notes="Presentation layer delegation; stateless REST endpoint."
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: TESTING & CROSS-CUTTING JAVA ANALYSIS
    # =========================================================================
    story.append(Paragraph("4.10 Test Subsystem (<code>src/test/java</code>)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(make_file_box(
        filename="DriveeaseApplicationTests.java",
        package="com.driveease",
        purpose="Integration test verifying that the Spring application context, dependency injection bindings, JPA repositories, and configuration beans load cleanly without configuration errors.",
        annotations="<code>@SpringBootTest</code>: Boots up the complete Spring ApplicationContext in test harness.",
        methods_fields="<code>@Test void contextLoads()</code>: Empty assertion verifying context bootstrapping.",
        oop_notes="Automated Regression Verification; Spring Context Lifecycle Testing."
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("5. Cross-Cutting Java Engineering & Algorithmic Analysis", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("5.1 High-Precision Financial Arithmetic with <code>BigDecimal</code>", h2_style))
    story.append(Paragraph(
        "A critical engineering standard in DriveEase is the complete avoidance of floating-point primitives (<code>double</code>, <code>float</code>) "
        "for monetary calculations. Binary floating-point representation causes catastrophic rounding drift (e.g. <code>0.1 + 0.2 = 0.30000000000000004</code>). "
        "In DriveEase, all prices, daily rates, taxes, discounts, deposits, and exchange rates use Java <code>java.math.BigDecimal</code> with explicit "
        "<code>RoundingMode.HALF_UP</code> and scaled precision, guaranteeing exact accounting reconciliation.",
        body_style
    ))

    story.append(Paragraph("5.2 Thread-Safe Caching & Concurrency Handling", h2_style))
    story.append(Paragraph(
        "In <code>CurrencyServiceImpl.java</code>, exchange rates are shared across concurrent user sessions. To prevent race conditions and locking contention:<br/>"
        "• <b><code>ConcurrentHashMap</code>:</b> The <code>cachedRates</code> map allows lock-free concurrent reads while isolating concurrent writes to hash buckets.<br/>"
        "• <b>Non-Blocking Background Refresh:</b> The <code>refreshRatesAsync()</code> method invokes <code>java.net.http.HttpClient</code> asynchronously, ensuring web requests are never blocked by remote forex network latency.<br/>"
        "• <b>Volatile/Thread-Safe Timestamps:</b> Cache invalidation relies on <code>Duration.between(lastFetchTime, LocalDateTime.now())</code>, refreshing only once per hour.",
        body_style
    ))

    story.append(Paragraph("5.3 Modern Java 21 LTS Features Utilized", h2_style))
    story.append(Paragraph(
        "• <b>Pattern Matching & Type Narrowing:</b> Simplifies instanceof checks and clean conditional casting.<br/>"
        "• <b>Enhanced Switch Expressions:</b> Used in formatting and category selection.<br/>"
        "• <b>Modern HTTP/2 Client (<code>java.net.http.HttpClient</code>):</b> Replaces outdated <code>HttpURLConnection</code> with fluent request builders, asynchronous futures, and timeout resilience.<br/>"
        "• <b>Stream API & Functional Lambdas:</b> Extensive usage of Java 8+ Streams (<code>map()</code>, <code>filter()</code>, <code>collect()</code>) for DTO transformations and security authority mapping.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: MASTER 52-FILE REFERENCE MATRIX (PART A: FILES 1 - 26)
    # =========================================================================
    story.append(Paragraph("6. Master Reference Matrix of All 52 Java Source Files", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "<b>Part A: Infrastructure, Models, Repositories, Strategies & Core Services (Files 1 – 26)</b>",
        h2_style
    ))

    th_row = [Paragraph("#", th_style), Paragraph("Java File Name", th_style), Paragraph("Package", th_style), Paragraph("Role / Layer", th_style), Paragraph("Primary OOP Principle / Design Pattern", th_style)]

    matrix_part1 = [
        th_row,
        [Paragraph("1", td_style), Paragraph("DriveeaseApplication.java", td_code), Paragraph("com.driveease", td_style), Paragraph("Bootstrap", td_style), Paragraph("Application Entry Point", td_style)],
        [Paragraph("2", td_style), Paragraph("SecurityConfig.java", td_code), Paragraph("com.driveease.config", td_style), Paragraph("Configuration", td_style), Paragraph("Adapter & Builder Patterns", td_style)],
        [Paragraph("3", td_style), Paragraph("DataInitializer.java", td_code), Paragraph("com.driveease.config", td_style), Paragraph("Seeder", td_style), Paragraph("Template Method Pattern", td_style)],
        [Paragraph("4", td_style), Paragraph("Vehicle.java", td_code), Paragraph("com.driveease.model", td_style), Paragraph("Entity (Abstract)", td_style), Paragraph("Abstraction, Inheritance, Polymorphism", td_style)],
        [Paragraph("5", td_style), Paragraph("Car.java", td_code), Paragraph("com.driveease.model", td_style), Paragraph("Entity (Concrete)", td_style), Paragraph("Inheritance, Polymorphism", td_style)],
        [Paragraph("6", td_style), Paragraph("Motorcycle.java", td_code), Paragraph("com.driveease.model", td_style), Paragraph("Entity (Concrete)", td_style), Paragraph("Inheritance, Polymorphism", td_style)],
        [Paragraph("7", td_style), Paragraph("Booking.java", td_code), Paragraph("com.driveease.model", td_style), Paragraph("Entity", td_style), Paragraph("Encapsulation (Rich Domain Model)", td_style)],
        [Paragraph("8", td_style), Paragraph("User.java", td_code), Paragraph("com.driveease.model", td_style), Paragraph("Entity", td_style), Paragraph("Encapsulation", td_style)],
        [Paragraph("9", td_style), Paragraph("Role.java", td_code), Paragraph("com.driveease.model", td_style), Paragraph("Enum", td_style), Paragraph("Type-Safe Enum Constants", td_style)],
        [Paragraph("10", td_style), Paragraph("BookingStatus.java", td_code), Paragraph("com.driveease.model", td_style), Paragraph("Enum", td_style), Paragraph("Finite State Machine Modeling", td_style)],
        [Paragraph("11", td_style), Paragraph("VehicleCategory.java", td_code), Paragraph("com.driveease.model", td_style), Paragraph("Enum", td_style), Paragraph("Domain Taxonomy", td_style)],
        [Paragraph("12", td_style), Paragraph("VehicleOrigin.java", td_code), Paragraph("com.driveease.model", td_style), Paragraph("Enum", td_style), Paragraph("Regional Classification", td_style)],
        [Paragraph("13", td_style), Paragraph("FuelType.java", td_code), Paragraph("com.driveease.model", td_style), Paragraph("Enum", td_style), Paragraph("Powertrain Modeling", td_style)],
        [Paragraph("14", td_style), Paragraph("TransmissionType.java", td_code), Paragraph("com.driveease.model", td_style), Paragraph("Enum", td_style), Paragraph("Gearbox Modeling", td_style)],
        [Paragraph("15", td_style), Paragraph("VehicleRepository.java", td_code), Paragraph("com.driveease.repository", td_style), Paragraph("Repository", td_style), Paragraph("Repository Pattern, Abstraction", td_style)],
        [Paragraph("16", td_style), Paragraph("BookingRepository.java", td_code), Paragraph("com.driveease.repository", td_style), Paragraph("Repository", td_style), Paragraph("Repository Pattern, JPQL Queries", td_style)],
        [Paragraph("17", td_style), Paragraph("UserRepository.java", td_code), Paragraph("com.driveease.repository", td_style), Paragraph("Repository", td_style), Paragraph("Repository Pattern, Optional<T>", td_style)],
        [Paragraph("18", td_style), Paragraph("RentalPricingStrategy.java", td_code), Paragraph("com.driveease.strategy", td_style), Paragraph("Strategy Interface", td_style), Paragraph("Strategy Pattern, Abstraction", td_style)],
        [Paragraph("19", td_style), Paragraph("StandardPricingStrategy.java", td_code), Paragraph("com.driveease.strategy", td_style), Paragraph("Strategy Impl", td_style), Paragraph("Strategy Pattern, Polymorphism", td_style)],
        [Paragraph("20", td_style), Paragraph("WeeklyDiscountPricingStrategy.java", td_code), Paragraph("com.driveease.strategy", td_style), Paragraph("Strategy Impl", td_style), Paragraph("Strategy Pattern, Polymorphism", td_style)],
        [Paragraph("21", td_style), Paragraph("PricingStrategyFactory.java", td_code), Paragraph("com.driveease.strategy", td_style), Paragraph("Factory", td_style), Paragraph("Factory Method Pattern", td_style)],
        [Paragraph("22", td_style), Paragraph("VehicleService.java", td_code), Paragraph("com.driveease.service", td_style), Paragraph("Service Interface", td_style), Paragraph("Abstraction", td_style)],
        [Paragraph("23", td_style), Paragraph("VehicleServiceImpl.java", td_code), Paragraph("com.driveease.service", td_style), Paragraph("Service Impl", td_style), Paragraph("Encapsulation, DTO Mapping", td_style)],
        [Paragraph("24", td_style), Paragraph("BookingService.java", td_code), Paragraph("com.driveease.service", td_style), Paragraph("Service Interface", td_style), Paragraph("Abstraction", td_style)],
        [Paragraph("25", td_style), Paragraph("BookingServiceImpl.java", td_code), Paragraph("com.driveease.service", td_style), Paragraph("Service Impl", td_style), Paragraph("Strategy/Factory Integration", td_style)],
        [Paragraph("26", td_style), Paragraph("CurrencyService.java", td_code), Paragraph("com.driveease.service", td_style), Paragraph("Service Interface", td_style), Paragraph("Abstraction", td_style)],
    ]
    t_mat1 = Table(matrix_part1, colWidths=[20, 140, 110, 85, 167])
    t_mat1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_BG_LIGHT])
    ]))
    story.append(t_mat1)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: MASTER 52-FILE REFERENCE MATRIX (PART B: FILES 27 - 52) & CONCLUSION
    # =========================================================================
    story.append(Paragraph(
        "<b>Part B: Services (Cont.), DTOs, REST Controllers, Exceptions & Tests (Files 27 – 52)</b>",
        h2_style
    ))

    matrix_part2 = [
        th_row,
        [Paragraph("27", td_style), Paragraph("CurrencyServiceImpl.java", td_code), Paragraph("com.driveease.service", td_style), Paragraph("Service Impl", td_style), Paragraph("Concurrency, Thread Safety", td_style)],
        [Paragraph("28", td_style), Paragraph("UserService.java", td_code), Paragraph("com.driveease.service", td_style), Paragraph("Service Interface", td_style), Paragraph("Abstraction", td_style)],
        [Paragraph("29", td_style), Paragraph("UserServiceImpl.java", td_code), Paragraph("com.driveease.service", td_style), Paragraph("Service Impl", td_style), Paragraph("Encapsulation, Cryptography", td_style)],
        [Paragraph("30", td_style), Paragraph("DashboardService.java", td_code), Paragraph("com.driveease.service", td_style), Paragraph("Service Interface", td_style), Paragraph("Abstraction", td_style)],
        [Paragraph("31", td_style), Paragraph("DashboardServiceImpl.java", td_code), Paragraph("com.driveease.service", td_style), Paragraph("Service Impl", td_style), Paragraph("Facade Pattern", td_style)],
        [Paragraph("32", td_style), Paragraph("ApiResponse.java", td_code), Paragraph("com.driveease.dto", td_style), Paragraph("Generic DTO", td_style), Paragraph("Generics, Uniform Envelope Pattern", td_style)],
        [Paragraph("33", td_style), Paragraph("AuthResponse.java", td_code), Paragraph("com.driveease.dto", td_style), Paragraph("DTO", td_style), Paragraph("DTO Pattern", td_style)],
        [Paragraph("34", td_style), Paragraph("LoginRequest.java", td_code), Paragraph("com.driveease.dto", td_style), Paragraph("Request DTO", td_style), Paragraph("Encapsulation, Bean Validation", td_style)],
        [Paragraph("35", td_style), Paragraph("RegisterRequest.java", td_code), Paragraph("com.driveease.dto", td_style), Paragraph("Request DTO", td_style), Paragraph("Encapsulation, Bean Validation", td_style)],
        [Paragraph("36", td_style), Paragraph("UserDto.java", td_code), Paragraph("com.driveease.dto", td_style), Paragraph("Response DTO", td_style), Paragraph("Information Hiding (Excludes Password)", td_style)],
        [Paragraph("37", td_style), Paragraph("VehicleDto.java", td_code), Paragraph("com.driveease.dto", td_style), Paragraph("Response DTO", td_style), Paragraph("DTO Pattern, Presentation Mapping", td_style)],
        [Paragraph("38", td_style), Paragraph("VehicleRequest.java", td_code), Paragraph("com.driveease.dto", td_style), Paragraph("Request DTO", td_style), Paragraph("Encapsulation, Validation", td_style)],
        [Paragraph("39", td_style), Paragraph("BookingRequest.java", td_code), Paragraph("com.driveease.dto", td_style), Paragraph("Request DTO", td_style), Paragraph("Encapsulation, Validation", td_style)],
        [Paragraph("40", td_style), Paragraph("BookingStatusRequest.java", td_code), Paragraph("com.driveease.dto", td_style), Paragraph("Request DTO", td_style), Paragraph("Encapsulation", td_style)],
        [Paragraph("41", td_style), Paragraph("BookingDto.java", td_code), Paragraph("com.driveease.dto", td_style), Paragraph("Response DTO", td_style), Paragraph("DTO Pattern", td_style)],
        [Paragraph("42", td_style), Paragraph("CurrencyRatesDto.java", td_code), Paragraph("com.driveease.dto", td_style), Paragraph("Response DTO", td_style), Paragraph("DTO Pattern", td_style)],
        [Paragraph("43", td_style), Paragraph("DashboardSummaryDto.java", td_code), Paragraph("com.driveease.dto", td_style), Paragraph("Response DTO", td_style), Paragraph("Consolidated Aggregation DTO", td_style)],
        [Paragraph("44", td_style), Paragraph("VehicleController.java", td_code), Paragraph("com.driveease.controller", td_style), Paragraph("REST Controller", td_style), Paragraph("Presentation Abstraction", td_style)],
        [Paragraph("45", td_style), Paragraph("BookingController.java", td_code), Paragraph("com.driveease.controller", td_style), Paragraph("REST Controller", td_style), Paragraph("Security, Principal Injection", td_style)],
        [Paragraph("46", td_style), Paragraph("AuthController.java", td_code), Paragraph("com.driveease.controller", td_style), Paragraph("REST Controller", td_style), Paragraph("Session Management", td_style)],
        [Paragraph("47", td_style), Paragraph("AdminController.java", td_code), Paragraph("com.driveease.controller", td_style), Paragraph("REST Controller", td_style), Paragraph("Role-Based Access Control", td_style)],
        [Paragraph("48", td_style), Paragraph("CurrencyController.java", td_code), Paragraph("com.driveease.controller", td_style), Paragraph("REST Controller", td_style), Paragraph("Presentation Abstraction", td_style)],
        [Paragraph("49", td_style), Paragraph("BadRequestException.java", td_code), Paragraph("com.driveease.exception", td_style), Paragraph("Exception", td_style), Paragraph("Inheritance (RuntimeException)", td_style)],
        [Paragraph("50", td_style), Paragraph("ResourceNotFoundException.java", td_code), Paragraph("com.driveease.exception", td_style), Paragraph("Exception", td_style), Paragraph("Inheritance (RuntimeException)", td_style)],
        [Paragraph("51", td_style), Paragraph("GlobalExceptionHandler.java", td_code), Paragraph("com.driveease.exception", td_style), Paragraph("Exception Advice", td_style), Paragraph("Interceptor Pattern", td_style)],
        [Paragraph("52", td_style), Paragraph("DriveeaseApplicationTests.java", td_code), Paragraph("com.driveease (test)", td_style), Paragraph("Test Harness", td_style), Paragraph("Context Bootstrap Verification", td_style)],
    ]
    t_mat2 = Table(matrix_part2, colWidths=[20, 140, 110, 85, 167])
    t_mat2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_BG_LIGHT])
    ]))
    story.append(t_mat2)
    story.append(Spacer(1, 8))

    # Concluding Remarks
    story.append(Paragraph("7. Concluding Engineering Evaluation & Architectural Verdict", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER, spaceBefore=2, spaceAfter=6))
    story.append(Paragraph(
        "The DriveEase Java codebase represents a rigorous, enterprise-caliber application of <b>Object-Oriented Programming (OOP)</b> "
        "and clean architecture in Java 21 LTS. By enforcing strict encapsulation in rich domain entities, leveraging polymorphic "
        "inheritance hierarchies, decoupling presentation and persistence via abstract contracts, and executing extensible "
        "Gang-of-Four design patterns (Strategy, Factory Method, Facade, Singleton, Repository, DTO), DriveEase serves as an "
        "exemplary benchmark for commercial-grade full-stack Java software engineering.",
        body_style
    ))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    build_pdf()
