# Stage 1: Build the application using Eclipse Temurin JDK 21
FROM eclipse-temurin:21-jdk-jammy AS build
WORKDIR /workspace

# Copy Maven wrapper and POM first to leverage Docker layer caching
COPY pom.xml .
COPY .mvn .mvn
COPY mvnw mvnw
COPY mvnw.cmd mvnw.cmd

# Fix possible Windows CRLF line endings and grant execute permissions
RUN sed -i 's/\r$//' ./mvnw && chmod +x ./mvnw

# Pre-fetch project dependencies
RUN ./mvnw dependency:go-offline -B

# Copy project source code and package application (skip tests for quick build)
COPY src src
RUN ./mvnw clean package -DskipTests -B

# Stage 2: Minimal, secure JRE 21 runtime image
FROM eclipse-temurin:21-jre-jammy
WORKDIR /app

# Run as non-privileged service user for production security
RUN groupadd -r driveease && useradd -r -g driveease driveease
USER driveease:driveease

# Copy compiled JAR from the builder stage
COPY --from=build /workspace/target/*.jar app.jar

# Render supplies dynamic PORT via environment variable (default fallback 8080)
EXPOSE 8080

# Configure memory-efficient container flags suitable for Render 512MB free tier
ENTRYPOINT ["java", "-XX:+UseContainerSupport", "-XX:MaxRAMPercentage=75.0", "-Djava.security.egd=file:/dev/./urandom", "-jar", "app.jar"]
