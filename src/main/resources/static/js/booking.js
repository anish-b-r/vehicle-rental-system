/**
 * DriveEase — Booking & Vehicle Details Script
 * Dynamic pricing calculation, Date picker management, Booking submission.
 */

let currentVehicle = null;

async function initVehicleDetailsPage() {
  const params = new URLSearchParams(window.location.search);
  const vehicleId = params.get('id') || params.get('vehicleId');

  if (!vehicleId) {
    showToast('No vehicle selected. Redirecting to fleet catalog.', 'error');
    setTimeout(() => window.location.href = '/vehicles.html', 1500);
    return;
  }

  try {
    const res = await DriveEaseApi.get(`/vehicles/${vehicleId}`);
    currentVehicle = res.data;
    renderVehicleDetails(currentVehicle);
    initDatePickers();
    calculateLiveCost();
  } catch (err) {
    document.getElementById('details-content').innerHTML = `
      <div class="col-12 text-center py-5">
        <div class="alert alert-danger d-inline-block px-4">
          <i class="bi bi-exclamation-triangle me-2"></i>Failed to load vehicle details: ${err.message}
        </div>
        <div>
          <a href="/vehicles.html" class="btn btn-de-outline mt-3">Return to Fleet</a>
        </div>
      </div>
    `;
  }
}

function renderVehicleDetails(v) {
  // Origin & Premium Badges
  const badgesEl = document.getElementById('vehicle-origin-premium-badges');
  if (badgesEl) {
    const originBadge = v.vehicleOrigin === 'INDIAN'
      ? `<span class="badge-origin-indian"><i class="bi bi-flag-fill"></i> Indian Fleet</span>`
      : `<span class="badge-origin-intl"><i class="bi bi-globe"></i> International</span>`;
    const isPrem = v.isPremium || v.premium;
    const premiumBadge = isPrem
      ? `<span class="badge-premium-gold"><i class="bi bi-stars"></i> Premium Fleet</span>`
      : '';
    badgesEl.innerHTML = `${premiumBadge} ${originBadge}`;
  }

  // Title & Brand
  document.getElementById('vehicle-brand').textContent = v.brand;
  document.getElementById('vehicle-model').textContent = v.model;
  document.title = `${v.brand} ${v.model} — DriveEase`;

  // Status & Rating
  const statusBadge = document.getElementById('vehicle-status-badge');
  if (statusBadge) {
    statusBadge.className = `badge ${v.available ? 'badge-available' : 'badge-unavailable'}`;
    statusBadge.textContent = v.available ? 'Available for Rent' : 'Currently Reserved';
  }

  const ratingEl = document.getElementById('vehicle-rating');
  if (ratingEl) {
    ratingEl.innerHTML = `<i class="bi bi-star-fill text-warning me-1"></i>${v.rating ? v.rating.toFixed(1) : '4.8'} (Verified Fleet Review)`;
  }

  // Large Image
  const imgEl = document.getElementById('vehicle-large-image');
  if (imgEl) {
    imgEl.src = v.imageUrl || 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80';
    imgEl.alt = `${v.brand} ${v.model}`;
  }

  // Daily rate
  const rateEl = document.getElementById('vehicle-daily-rate');
  if (rateEl) {
    rateEl.textContent = formatCurrency(v.dailyRate);
  }

  // Description & Location
  const descEl = document.getElementById('vehicle-description');
  if (descEl) descEl.textContent = v.description || 'Premium rental vehicle engineered for comfort, luxury, and unmatched driving excitement.';

  const locEl = document.getElementById('vehicle-location');
  if (locEl) locEl.textContent = v.location || 'Downtown Executive Hub';

  // Specification Badges
  const specsContainer = document.getElementById('vehicle-specs-grid');
  if (specsContainer) {
    let specs = [
      { label: 'Category', value: v.category, icon: 'bi-tag' },
      { label: 'Transmission', value: v.transmission, icon: 'bi-gear' },
      { label: 'Fuel Type', value: v.fuelType, icon: 'bi-fuel-pump' },
      { label: 'Security Deposit', value: formatCurrency(v.securityDeposit), icon: 'bi-shield-check' }
    ];

    if (v.category === 'CAR') {
      specs.push({ label: 'Seating Capacity', value: `${v.seatingCapacity || 5} Persons`, icon: 'bi-people' });
      specs.push({ label: 'Luggage Capacity', value: `${v.luggageCapacity || 2} Bags`, icon: 'bi-briefcase' });
      specs.push({ label: 'Body Type', value: v.bodyType || 'Sedan', icon: 'bi-car-front' });
      specs.push({ label: 'Air Conditioning', value: v.hasAirConditioning ? 'Dual-Zone AC' : 'Standard', icon: 'bi-snow' });
    } else if (v.category === 'BIKE') {
      specs.push({ label: 'Engine Capacity', value: `${v.engineCc || 650} cc`, icon: 'bi-speedometer' });
      specs.push({ label: 'Bike Style', value: v.bikeType || 'Sport', icon: 'bi-bicycle' });
      specs.push({ label: 'Helmet Included', value: v.hasHelmetIncluded ? '2 Premium Helmets' : 'No', icon: 'bi-check-circle' });
    }

    specsContainer.innerHTML = specs.map(s => `
      <div class="col-6 col-md-3 mb-3">
        <div class="p-3 bg-white border rounded-3 text-center h-100">
          <i class="bi ${s.icon} fs-4 text-secondary mb-2 d-block"></i>
          <span class="d-block small text-muted text-uppercase fw-semibold" style="font-size:0.72rem;">${s.label}</span>
          <span class="fw-bold text-dark fs-6">${s.value}</span>
        </div>
      </div>
    `).join('');
  }

  // Features list
  const featuresContainer = document.getElementById('vehicle-features-list');
  if (featuresContainer && v.features) {
    const list = v.features.split(',').map(f => f.trim());
    featuresContainer.innerHTML = list.map(f => `
      <li class="mb-2 d-flex align-items-center gap-2">
        <i class="bi bi-check-circle-fill text-success"></i>
        <span>${f}</span>
      </li>
    `).join('');
  }
}

function initDatePickers() {
  const pickupInput = document.getElementById('calc-pickup-date');
  const returnInput = document.getElementById('calc-return-date');

  if (!pickupInput || !returnInput) return;

  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);

  const defaultReturn = new Date(tomorrow);
  defaultReturn.setDate(defaultReturn.getDate() + 3);

  // Format to YYYY-MM-DD
  const formatDateISO = (d) => d.toISOString().split('T')[0];

  pickupInput.min = formatDateISO(today);
  pickupInput.value = formatDateISO(tomorrow);

  returnInput.min = formatDateISO(tomorrow);
  returnInput.value = formatDateISO(defaultReturn);

  pickupInput.addEventListener('change', () => {
    if (new Date(returnInput.value) <= new Date(pickupInput.value)) {
      const nextDay = new Date(pickupInput.value);
      nextDay.setDate(nextDay.getDate() + 1);
      returnInput.value = formatDateISO(nextDay);
    }
    returnInput.min = pickupInput.value;
    calculateLiveCost();
  });

  returnInput.addEventListener('change', calculateLiveCost);
}

function calculateLiveCost() {
  if (!currentVehicle) return;

  const pickupStr = document.getElementById('calc-pickup-date')?.value;
  const returnStr = document.getElementById('calc-return-date')?.value;

  if (!pickupStr || !returnStr) return;

  const pickupDate = new Date(pickupStr);
  const returnDate = new Date(returnStr);

  const diffTime = returnDate - pickupDate;
  let diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  if (diffDays <= 0) diffDays = 1;

  const dailyRate = Number(currentVehicle.dailyRate);
  const subtotal = dailyRate * diffDays;

  // 10% discount for 7+ days (demonstrating Strategy pattern result)
  let discount = 0;
  if (diffDays >= 7) {
    discount = subtotal * 0.10;
  }

  const netSubtotal = subtotal - discount;
  const tax = netSubtotal * 0.10;
  const deposit = Number(currentVehicle.securityDeposit || 200);
  const total = netSubtotal + tax + deposit;

  // Update UI elements
  document.getElementById('calc-days-count').textContent = `${diffDays} Day${diffDays > 1 ? 's' : ''}`;
  document.getElementById('calc-daily-rate-display').textContent = formatCurrency(dailyRate);
  document.getElementById('calc-subtotal').textContent = formatCurrency(subtotal);

  const discountRow = document.getElementById('calc-discount-row');
  if (discountRow) {
    if (discount > 0) {
      discountRow.style.display = 'flex';
      document.getElementById('calc-discount-amount').textContent = `-${formatCurrency(discount)}`;
    } else {
      discountRow.style.display = 'none';
    }
  }

  document.getElementById('calc-tax').textContent = formatCurrency(tax);
  document.getElementById('calc-deposit').textContent = formatCurrency(deposit);
  document.getElementById('calc-total').textContent = formatCurrency(total);
}

async function handleBookNowClick() {
  if (!currentVehicle) return;

  if (!currentVehicle.available) {
    showToast('This vehicle is currently reserved and unavailable for rent.', 'error');
    return;
  }

  const pickupDate = document.getElementById('calc-pickup-date')?.value;
  const returnDate = document.getElementById('calc-return-date')?.value;
  const pickupLocation = currentVehicle.location || 'Downtown Executive Hub';

  const bookingPayload = {
    vehicleId: currentVehicle.id,
    startDate: pickupDate,
    endDate: returnDate,
    pickupLocation: pickupLocation,
    dropoffLocation: pickupLocation,
    paymentMethod: 'CREDIT_CARD',
    customerNotes: 'Online booking via DriveEase platform'
  };

  // Check if authenticated
  if (!DriveEaseAuth.isLoggedIn()) {
    sessionStorage.setItem('pending_booking', JSON.stringify(bookingPayload));
    showToast('Please sign in to confirm your booking.', 'info');
    setTimeout(() => {
      window.location.href = `/login.html?redirect=booking.html?id=${currentVehicle.id}`;
    }, 800);
    return;
  }

  // Redirect to booking checkout confirmation page
  sessionStorage.setItem('active_booking_draft', JSON.stringify({
    ...bookingPayload,
    vehicle: currentVehicle
  }));
  window.location.href = `/booking.html?id=${currentVehicle.id}`;
}

// Re-render prices dynamically on currency change
window.addEventListener('currencyChanged', () => {
  if (currentVehicle) {
    renderVehicleDetails(currentVehicle);
    calculateLiveCost();
  }
});

// Initialize on vehicle details page
document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('vehicle-large-image')) {
    initVehicleDetailsPage();
  }
});
