/**
 * DriveEase — Vehicles Catalog & Filtering Script
 * Supports Category, Indian/International Origin, Premium Flag, Powertrain, Transmission, Dynamic Currency
 */

let allVehicles = [];
let currentCategory = '';
let currentOrigin = '';
let debounceTimer = null;

async function loadVehicles() {
  const container = document.getElementById('vehicles-grid');
  const countBadge = document.getElementById('vehicle-count-badge');
  if (!container) return;

  container.innerHTML = `
    <div class="col-12 text-center py-5">
      <div class="spinner-border text-dark" role="status">
        <span class="visually-hidden">Loading fleet...</span>
      </div>
      <p class="text-muted mt-2">Curating available vehicles...</p>
    </div>
  `;

  // Build query params
  const searchInput = document.getElementById('search-input')?.value.trim() || '';
  const fuelType = document.getElementById('filter-fuel')?.value || '';
  const transmission = document.getElementById('filter-transmission')?.value || '';
  const availableOnly = document.getElementById('filter-available')?.checked || false;
  const premiumOnly = document.getElementById('filter-premium')?.checked || false;
  const maxPrice = document.getElementById('price-range-slider')?.value || '';
  const sortBy = document.getElementById('sort-by-select')?.value || 'price_asc';

  let query = `/vehicles?sortBy=${sortBy}`;
  if (currentCategory) query += `&category=${currentCategory}`;
  if (currentOrigin) query += `&origin=${currentOrigin}`;
  if (premiumOnly) query += `&premium=true`;
  if (searchInput) query += `&search=${encodeURIComponent(searchInput)}`;
  if (fuelType) query += `&fuelType=${fuelType}`;
  if (transmission) query += `&transmission=${transmission}`;
  if (availableOnly) query += `&availableOnly=true`;
  if (maxPrice && Number(maxPrice) < 30000) query += `&maxPrice=${maxPrice}`;

  try {
    const res = await DriveEaseApi.get(query);
    allVehicles = res.data || [];

    if (countBadge) {
      countBadge.textContent = `${allVehicles.length} vehicles available`;
    }

    renderVehiclesGrid(allVehicles, container);
  } catch (err) {
    container.innerHTML = `
      <div class="col-12 text-center py-5">
        <div class="alert alert-danger d-inline-block px-4">
          <i class="bi bi-exclamation-octagon me-2"></i>Failed to load vehicles. ${err.message}
        </div>
      </div>
    `;
  }
}

function renderVehiclesGrid(vehicles, container) {
  if (!vehicles || vehicles.length === 0) {
    container.innerHTML = `
      <div class="col-12 text-center py-5">
        <div class="empty-state-box">
          <i class="bi bi-car-front empty-state-icon"></i>
          <h4 class="fw-bold">No vehicles match your criteria</h4>
          <p class="text-muted">Try clearing some filters or searching for another brand or model.</p>
          <button class="btn btn-de-outline mt-2" onclick="resetFilters()">Reset All Filters</button>
        </div>
      </div>
    `;
    return;
  }

  container.innerHTML = vehicles.map(v => createVehicleCardHtml(v)).join('');
}

function createVehicleCardHtml(v) {
  const isAvailable = v.available;
  const specPills = [];

  if (v.category === 'CAR') {
    if (v.seatingCapacity) specPills.push(`<span class="spec-pill"><i class="bi bi-people"></i>${v.seatingCapacity} Seats</span>`);
    if (v.bodyType) specPills.push(`<span class="spec-pill"><i class="bi bi-car-front"></i>${v.bodyType}</span>`);
  } else if (v.category === 'BIKE') {
    if (v.engineCc) specPills.push(`<span class="spec-pill"><i class="bi bi-speedometer"></i>${v.engineCc} cc</span>`);
    if (v.bikeType) specPills.push(`<span class="spec-pill"><i class="bi bi-bicycle"></i>${v.bikeType}</span>`);
  }

  specPills.push(`<span class="spec-pill"><i class="bi bi-fuel-pump"></i>${v.fuelType}</span>`);
  specPills.push(`<span class="spec-pill"><i class="bi bi-gear"></i>${v.transmission}</span>`);

  const originBadge = v.vehicleOrigin === 'INDIAN'
    ? `<span class="badge-origin-indian"><i class="bi bi-flag-fill"></i> Indian</span>`
    : `<span class="badge-origin-intl"><i class="bi bi-globe"></i> Intl</span>`;

  const isPremiumVehicle = v.isPremium || v.premium;
  const premiumBadge = isPremiumVehicle
    ? `<span class="badge-premium-gold"><i class="bi bi-stars"></i> Premium</span>`
    : '';

  return `
    <div class="col-md-6 col-lg-4 mb-4">
      <div class="vehicle-card ${isPremiumVehicle ? 'premium-tier' : ''} h-100 d-flex flex-column">
        <div class="vehicle-card-img-wrap">
          <img src="${v.imageUrl || 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80'}" 
               alt="${v.brand} ${v.model}"
               loading="lazy"
               onerror="this.src='https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80'">
          <div class="position-absolute top-0 start-0 m-2.5 d-flex flex-wrap gap-1">
            ${premiumBadge}
            ${originBadge}
          </div>
          <span class="vehicle-badge-status ${isAvailable ? 'badge-available' : 'badge-unavailable'}">
            ${isAvailable ? 'Available' : 'Reserved'}
          </span>
        </div>
        <div class="vehicle-card-body d-flex flex-column flex-grow-1">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <span class="vehicle-card-brand">${v.brand}</span>
            <div class="text-warning small fw-semibold">
              <i class="bi bi-star-fill text-warning"></i> ${v.rating ? v.rating.toFixed(1) : '4.8'}
            </div>
          </div>
          <h3 class="vehicle-card-title">${v.model}</h3>
          
          <div class="vehicle-spec-pills mb-3">
            ${specPills.slice(0, 4).join('')}
          </div>

          <div class="vehicle-card-footer mt-auto pt-3 border-top">
            <div>
              <span class="price-display-amount">${formatCurrency(v.dailyRate)}</span>
              <span class="price-display-unit"> / day</span>
            </div>
            <a href="/vehicle-details.html?id=${v.id}" class="btn btn-de-primary btn-sm-custom">
              View Details <i class="bi bi-arrow-right"></i>
            </a>
          </div>
        </div>
      </div>
    </div>
  `;
}

function setCategoryFilter(category) {
  currentCategory = category;
  document.querySelectorAll('.category-tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.category === category);
  });
  loadVehicles();
}

function setOriginFilter(origin) {
  currentOrigin = origin;
  const allBtn = document.getElementById('origin-btn-all');
  const inBtn = document.getElementById('origin-btn-indian');
  const intlBtn = document.getElementById('origin-btn-intl');
  if (allBtn) allBtn.classList.toggle('active', origin === '');
  if (inBtn) inBtn.classList.toggle('active', origin === 'INDIAN');
  if (intlBtn) intlBtn.classList.toggle('active', origin === 'INTERNATIONAL');
  loadVehicles();
}

function resetFilters() {
  currentCategory = '';
  currentOrigin = '';
  document.querySelectorAll('.category-tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.category === '');
  });
  setOriginFilter('');

  const searchInput = document.getElementById('search-input');
  if (searchInput) searchInput.value = '';

  const fuelSelect = document.getElementById('filter-fuel');
  if (fuelSelect) fuelSelect.value = '';

  const transSelect = document.getElementById('filter-transmission');
  if (transSelect) transSelect.value = '';

  const availCheck = document.getElementById('filter-available');
  if (availCheck) availCheck.checked = false;

  const premCheck = document.getElementById('filter-premium');
  if (premCheck) premCheck.checked = false;

  const slider = document.getElementById('price-range-slider');
  const sliderVal = document.getElementById('price-slider-value');
  if (slider) {
    slider.value = 30000;
    if (sliderVal) sliderVal.textContent = 'Any Rate';
  }

  const sortSelect = document.getElementById('sort-by-select');
  if (sortSelect) sortSelect.value = 'price_asc';

  loadVehicles();
}

// Initial setup for vehicles page
document.addEventListener('DOMContentLoaded', () => {
  // Check URL params for initial filters
  const params = new URLSearchParams(window.location.search);
  const initialCategory = params.get('category');
  const initialSearch = params.get('search');
  const initialOrigin = params.get('origin');
  const initialPremium = params.get('premium');

  if (initialCategory) {
    currentCategory = initialCategory.toUpperCase();
    document.querySelectorAll('.category-tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.category === currentCategory);
    });
  }

  if (initialOrigin) {
    setOriginFilter(initialOrigin.toUpperCase());
  }

  if (initialPremium === 'true') {
    const premCheck = document.getElementById('filter-premium');
    if (premCheck) premCheck.checked = true;
  }

  if (initialSearch && document.getElementById('search-input')) {
    document.getElementById('search-input').value = initialSearch;
  }

  // Price slider listener
  const priceSlider = document.getElementById('price-range-slider');
  const priceValue = document.getElementById('price-slider-value');
  if (priceSlider && priceValue) {
    priceSlider.addEventListener('input', (e) => {
      const val = Number(e.target.value);
      if (val >= 30000) {
        priceValue.textContent = 'Any Rate';
      } else {
        priceValue.textContent = `${formatCurrency(val)} / day`;
      }
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(loadVehicles, 300);
    });
  }

  // Search input debouncer
  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(loadVehicles, 350);
    });
  }

  // Dropdown & Checkbox changes
  ['filter-fuel', 'filter-transmission', 'filter-available', 'sort-by-select'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('change', loadVehicles);
    }
  });

  // Re-render prices dynamically when currency changes
  window.addEventListener('currencyChanged', () => {
    const container = document.getElementById('vehicles-grid');
    if (allVehicles.length > 0 && container) {
      renderVehiclesGrid(allVehicles, container);
    }
    const slider = document.getElementById('price-range-slider');
    const sliderVal = document.getElementById('price-slider-value');
    if (slider && sliderVal && Number(slider.value) < 30000) {
      sliderVal.textContent = `${formatCurrency(slider.value)} / day`;
    }
  });

  // Only run if on vehicles page
  if (document.getElementById('vehicles-grid')) {
    loadVehicles();
  }
});
