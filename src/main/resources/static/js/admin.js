/**
 * DriveEase — Administrator Dashboard Script
 * Fleet Management, Origin & Premium Controls, Booking Lifecycle Control, Metrics, Customer Directory.
 */

let adminFleet = [];
let adminBookings = [];
let adminCustomers = [];
let editingVehicleId = null;

let adminOriginFilter = '';
let adminTierFilter = '';

async function initAdminDashboard() {
  const user = DriveEaseAuth.getUser();

  if (!user || user.role !== 'ROLE_ADMIN') {
    try {
      const refreshedUser = await DriveEaseAuth.init();
      if (!refreshedUser || refreshedUser.role !== 'ROLE_ADMIN') {
        showToast('Access restricted: Administrator privilege required.', 'error');
        setTimeout(() => window.location.href = '/login.html?redirect=admin.html', 1000);
        return;
      }
    } catch (e) {
      window.location.href = '/login.html?redirect=admin.html';
      return;
    }
  }

  // Load KPI overview
  await loadDashboardOverview();
  // Load Fleet
  await loadFleetTable();
  // Load Bookings
  await loadBookingsTable();
  // Load Customers
  await loadCustomersTable();

  // Setup category toggle in add vehicle modal
  const categorySelect = document.getElementById('vehicle-category');
  if (categorySelect) {
    categorySelect.addEventListener('change', (e) => {
      toggleVehicleCategoryFields(e.target.value);
    });
  }
}

async function loadDashboardOverview() {
  try {
    const res = await DriveEaseApi.get('/admin/dashboard');
    const data = res.data;

    document.getElementById('metric-total-vehicles').textContent = data.totalVehicles || 0;
    document.getElementById('metric-available-vehicles').textContent = data.availableVehicles || 0;
    document.getElementById('metric-total-customers').textContent = data.totalCustomers || 0;
    const metricTotalBookings = document.getElementById('metric-total-bookings');
    if (metricTotalBookings) metricTotalBookings.textContent = data.totalBookings || 0;
    document.getElementById('metric-active-bookings').textContent = data.activeBookings || 0;
    document.getElementById('metric-total-revenue').textContent = formatCurrency(data.totalRevenue);

    // Recent bookings table in overview
    const recentTbody = document.getElementById('recent-bookings-tbody');
    if (recentTbody && data.recentBookings) {
      if (data.recentBookings.length === 0) {
        recentTbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted py-4">No recent bookings found.</td></tr>`;
      } else {
        recentTbody.innerHTML = data.recentBookings.map(b => `
          <tr>
            <td class="fw-bold">${b.bookingNumber}</td>
            <td>${b.customerName}<br><span class="small text-muted">${b.customerEmail}</span></td>
            <td>${b.vehicleName}</td>
            <td>${formatDate(b.startDate)} → ${formatDate(b.endDate)}</td>
            <td class="fw-bold">${formatCurrency(b.totalAmount)}</td>
            <td><span class="badge ${getStatusBadgeClass(b.status)}">${b.status}</span></td>
          </tr>
        `).join('');
      }
    }
  } catch (err) {
    showToast(`Error fetching dashboard metrics: ${err.message}`, 'error');
  }
}

async function loadFleetTable() {
  const tbody = document.getElementById('fleet-tbody');
  if (!tbody) return;

  try {
    const res = await DriveEaseApi.get('/vehicles?sortBy=price_asc');
    adminFleet = res.data || [];
    filterAdminFleet();
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="8" class="text-center text-danger py-4">Failed to load fleet: ${err.message}</td></tr>`;
  }
}

function setAdminOriginFilter(origin) {
  adminOriginFilter = origin;
  document.getElementById('admin-origin-all')?.classList.toggle('active', origin === '');
  document.getElementById('admin-origin-in')?.classList.toggle('active', origin === 'INDIAN');
  document.getElementById('admin-origin-intl')?.classList.toggle('active', origin === 'INTERNATIONAL');
  filterAdminFleet();
}

function setAdminTierFilter(tier) {
  adminTierFilter = tier;
  document.getElementById('admin-tier-all')?.classList.toggle('active', tier === '');
  document.getElementById('admin-tier-prem')?.classList.toggle('active', tier === 'PREMIUM');
  document.getElementById('admin-tier-std')?.classList.toggle('active', tier === 'STANDARD');
  filterAdminFleet();
}

function filterAdminFleet() {
  const tbody = document.getElementById('fleet-tbody');
  if (!tbody) return;

  const query = document.getElementById('admin-fleet-search')?.value.toLowerCase().trim() || '';

  const filtered = adminFleet.filter(v => {
    const isPrem = v.isPremium || v.premium;
    if (adminOriginFilter && v.vehicleOrigin !== adminOriginFilter) return false;
    if (adminTierFilter === 'PREMIUM' && !isPrem) return false;
    if (adminTierFilter === 'STANDARD' && isPrem) return false;
    if (query) {
      const match = `${v.brand} ${v.model} ${v.location || ''}`.toLowerCase();
      if (!match.includes(query)) return false;
    }
    return true;
  });

  if (filtered.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" class="text-center text-muted py-4">No matching fleet vehicles found.</td></tr>`;
    return;
  }

  tbody.innerHTML = filtered.map(v => {
    const isPrem = v.isPremium || v.premium;
    const originBadge = v.vehicleOrigin === 'INDIAN'
      ? `<span class="badge-origin-indian"><i class="bi bi-flag-fill"></i> Indian</span>`
      : `<span class="badge-origin-intl"><i class="bi bi-globe"></i> Intl</span>`;

    return `
      <tr>
        <td>
          <img src="${v.imageUrl || 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=120&q=80'}"
               alt="${v.brand} ${v.model}"
               class="table-img-thumb"
               onerror="this.src='https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=120&q=80'">
        </td>
        <td>
          <div class="fw-bold text-dark">${v.brand} ${v.model}</div>
          <span class="small text-muted">${v.transmission} · ${v.fuelType}</span>
        </td>
        <td>
          <div>${originBadge}</div>
          <span class="badge bg-light text-dark border mt-1">${v.category}</span>
        </td>
        <td>${v.location || 'Downtown Hub'}</td>
        <td class="fw-bold">${formatCurrency(v.dailyRate)} <span class="small text-muted">/day</span></td>
        <td>
          <div class="form-check form-switch">
            <input class="form-check-input" type="checkbox" role="switch"
                   ${isPrem ? 'checked' : ''}
                   onchange="toggleVehiclePremium(${v.id}, this.checked)">
            <label class="form-check-label small ${isPrem ? 'text-warning fw-bold' : 'text-muted'}">
              ${isPrem ? '⭐ Premium' : 'Standard'}
            </label>
          </div>
        </td>
        <td>
          <div class="form-check form-switch">
            <input class="form-check-input" type="checkbox" role="switch" 
                   ${v.available ? 'checked' : ''} 
                   onchange="toggleVehicleAvailability(${v.id}, this.checked)">
            <label class="form-check-label small ${v.available ? 'text-success fw-semibold' : 'text-danger'}">
              ${v.available ? 'Available' : 'Reserved'}
            </label>
          </div>
        </td>
        <td class="text-end">
          <button class="btn btn-sm btn-outline-secondary me-1" onclick="openEditVehicleModal(${v.id})" title="Edit Vehicle">
            <i class="bi bi-pencil"></i>
          </button>
          <button class="btn btn-sm btn-outline-danger" onclick="confirmDeleteVehicle(${v.id}, '${v.brand} ${v.model}')" title="Delete Vehicle">
            <i class="bi bi-trash"></i>
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

async function loadBookingsTable() {
  const tbody = document.getElementById('bookings-tbody');
  if (!tbody) return;

  try {
    const res = await DriveEaseApi.get('/admin/bookings');
    adminBookings = res.data || [];

    if (adminBookings.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" class="text-center text-muted py-4">No bookings found in the system.</td></tr>`;
      return;
    }

    tbody.innerHTML = adminBookings.map(b => `
      <tr>
        <td class="fw-bold">${b.bookingNumber}</td>
        <td>
          <div class="fw-semibold text-dark">${b.customerName}</div>
          <span class="small text-muted">${b.customerEmail}</span>
        </td>
        <td>${b.vehicleName}</td>
        <td>${formatDate(b.startDate)} → ${formatDate(b.endDate)}<br><span class="small text-muted">${b.totalDays} Days</span></td>
        <td class="fw-bold">${formatCurrency(b.totalAmount)}</td>
        <td><span class="badge ${getStatusBadgeClass(b.status)}">${b.status}</span></td>
        <td>
          <select class="form-select form-select-sm" style="width: 140px;" onchange="updateBookingStatus(${b.id}, this.value)">
            <option value="CONFIRMED" ${b.status === 'CONFIRMED' ? 'selected' : ''}>Confirmed</option>
            <option value="ACTIVE" ${b.status === 'ACTIVE' ? 'selected' : ''}>Active</option>
            <option value="COMPLETED" ${b.status === 'COMPLETED' ? 'selected' : ''}>Completed</option>
            <option value="CANCELLED" ${b.status === 'CANCELLED' ? 'selected' : ''}>Cancelled</option>
          </select>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="7" class="text-center text-danger py-4">Failed to load bookings: ${err.message}</td></tr>`;
  }
}

async function loadCustomersTable() {
  const tbody = document.getElementById('customers-tbody');
  if (!tbody) return;

  try {
    const res = await DriveEaseApi.get('/admin/customers');
    adminCustomers = res.data || [];

    if (adminCustomers.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" class="text-center text-muted py-4">No customers registered yet.</td></tr>`;
      return;
    }

    tbody.innerHTML = adminCustomers.map(c => `
      <tr>
        <td class="fw-bold text-dark">${c.fullName}</td>
        <td>${c.email}</td>
        <td>${c.phone || 'N/A'}</td>
        <td><span class="badge bg-secondary">${c.role}</span></td>
        <td>${formatDate(c.createdAt ? c.createdAt.split('T')[0] : '')}</td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="5" class="text-center text-danger py-4">Failed to load customer directory: ${err.message}</td></tr>`;
  }
}

function showAdminTab(tabName) {
  document.querySelectorAll('.sidebar-nav-link').forEach(link => {
    link.classList.toggle('active', link.dataset.tab === tabName);
  });

  ['overview', 'vehicles', 'bookings', 'customers'].forEach(sec => {
    const secEl = document.getElementById(`section-${sec}`);
    if (secEl) {
      secEl.classList.toggle('d-none', sec !== tabName);
    }
  });
}

function toggleVehicleCategoryFields(category) {
  const carFields = document.getElementById('car-specific-fields');
  const bikeFields = document.getElementById('bike-specific-fields');

  if (category === 'BIKE') {
    if (carFields) carFields.classList.add('d-none');
    if (bikeFields) bikeFields.classList.remove('d-none');
  } else {
    if (carFields) carFields.classList.remove('d-none');
    if (bikeFields) bikeFields.classList.add('d-none');
  }
}

function openAddVehicleModal() {
  editingVehicleId = null;
  document.getElementById('vehicle-modal-title').textContent = 'Add New Fleet Vehicle';
  document.getElementById('vehicle-form').reset();
  document.getElementById('vehicle-origin').value = 'INDIAN';
  document.getElementById('vehicle-is-premium').checked = false;
  toggleVehicleCategoryFields('CAR');

  const modal = new bootstrap.Modal(document.getElementById('vehicleModal'));
  modal.show();
}

function openEditVehicleModal(id) {
  const v = adminFleet.find(item => item.id === id);
  if (!v) return;

  editingVehicleId = id;
  document.getElementById('vehicle-modal-title').textContent = `Edit ${v.brand} ${v.model}`;

  document.getElementById('vehicle-brand').value = v.brand;
  document.getElementById('vehicle-model').value = v.model;
  document.getElementById('vehicle-category').value = v.category;
  document.getElementById('vehicle-fuel').value = v.fuelType;
  document.getElementById('vehicle-transmission').value = v.transmission;
  document.getElementById('vehicle-origin').value = v.vehicleOrigin || 'INDIAN';
  document.getElementById('vehicle-is-premium').checked = !!(v.isPremium !== undefined ? v.isPremium : v.premium);
  document.getElementById('vehicle-rate').value = v.dailyRate;
  document.getElementById('vehicle-deposit').value = v.securityDeposit || 3000;
  document.getElementById('vehicle-image').value = v.imageUrl || '';
  document.getElementById('vehicle-location').value = v.location || 'Connaught Place Hub';
  document.getElementById('vehicle-desc').value = v.description || '';
  document.getElementById('vehicle-features').value = v.features || '';

  toggleVehicleCategoryFields(v.category);

  if (v.category === 'CAR') {
    document.getElementById('car-seats').value = v.seatingCapacity || 5;
    document.getElementById('car-luggage').value = v.luggageCapacity || 2;
    document.getElementById('car-body').value = v.bodyType || 'Sedan';
    document.getElementById('car-ac').checked = v.hasAirConditioning !== false;
  } else if (v.category === 'BIKE') {
    document.getElementById('bike-cc').value = v.engineCc || 650;
    document.getElementById('bike-type').value = v.bikeType || 'Sport';
    document.getElementById('bike-helmet').checked = v.hasHelmetIncluded !== false;
  }

  const modal = new bootstrap.Modal(document.getElementById('vehicleModal'));
  modal.show();
}

async function handleVehicleFormSubmit(event) {
  event.preventDefault();
  const btn = document.getElementById('save-vehicle-btn');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span>Saving...`;

  const category = document.getElementById('vehicle-category').value;

  const payload = {
    brand: document.getElementById('vehicle-brand').value.trim(),
    model: document.getElementById('vehicle-model').value.trim(),
    category: category,
    fuelType: document.getElementById('vehicle-fuel').value,
    transmission: document.getElementById('vehicle-transmission').value,
    vehicleOrigin: document.getElementById('vehicle-origin').value,
    isPremium: document.getElementById('vehicle-is-premium').checked,
    dailyRate: Number(document.getElementById('vehicle-rate').value),
    securityDeposit: Number(document.getElementById('vehicle-deposit').value || 3000),
    imageUrl: document.getElementById('vehicle-image').value.trim(),
    location: document.getElementById('vehicle-location').value.trim(),
    description: document.getElementById('vehicle-desc').value.trim(),
    features: document.getElementById('vehicle-features').value.trim(),
    available: true
  };

  if (category === 'CAR') {
    payload.seatingCapacity = Number(document.getElementById('car-seats').value || 5);
    payload.luggageCapacity = Number(document.getElementById('car-luggage').value || 2);
    payload.bodyType = document.getElementById('car-body').value;
    payload.hasAirConditioning = document.getElementById('car-ac').checked;
  } else if (category === 'BIKE') {
    payload.engineCc = Number(document.getElementById('bike-cc').value || 650);
    payload.bikeType = document.getElementById('bike-type').value;
    payload.hasHelmetIncluded = document.getElementById('bike-helmet').checked;
  }

  try {
    if (editingVehicleId) {
      await DriveEaseApi.put(`/admin/vehicles/${editingVehicleId}`, payload);
      showToast('Vehicle updated successfully', 'success');
    } else {
      await DriveEaseApi.post('/admin/vehicles', payload);
      showToast('Vehicle added to fleet successfully', 'success');
    }

    const modalEl = document.getElementById('vehicleModal');
    const modal = bootstrap.Modal.getInstance(modalEl);
    if (modal) modal.hide();

    await loadFleetTable();
    await loadDashboardOverview();
  } catch (err) {
    showToast(`Error saving vehicle: ${err.message}`, 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = 'Save Vehicle';
  }
}

async function toggleVehicleAvailability(id, isAvailable) {
  try {
    await DriveEaseApi.patch(`/admin/vehicles/${id}/availability?available=${isAvailable}`);
    showToast(`Vehicle availability updated to ${isAvailable ? 'Available' : 'Reserved'}`, 'info');
    const v = adminFleet.find(item => item.id === id);
    if (v) v.available = isAvailable;
    await loadDashboardOverview();
  } catch (err) {
    showToast(`Failed to update status: ${err.message}`, 'error');
    loadFleetTable();
  }
}

async function toggleVehiclePremium(id, isPremium) {
  try {
    await DriveEaseApi.patch(`/admin/vehicles/${id}/premium?premium=${isPremium}`);
    showToast(`Vehicle classified as ${isPremium ? 'Premium Fleet' : 'Standard Fleet'}`, 'info');
    const v = adminFleet.find(item => item.id === id);
    if (v) {
      v.isPremium = isPremium;
      v.premium = isPremium;
    }
    filterAdminFleet();
  } catch (err) {
    showToast(`Failed to update premium classification: ${err.message}`, 'error');
    loadFleetTable();
  }
}

async function confirmDeleteVehicle(id, name) {
  if (confirm(`Are you sure you want to permanently delete ${name} from the fleet?`)) {
    try {
      await DriveEaseApi.delete(`/admin/vehicles/${id}`);
      showToast('Vehicle removed from fleet', 'success');
      await loadFleetTable();
      await loadDashboardOverview();
    } catch (err) {
      showToast(`Delete failed: ${err.message}`, 'error');
    }
  }
}

async function updateBookingStatus(id, newStatus) {
  try {
    await DriveEaseApi.patch(`/admin/bookings/${id}/status`, { status: newStatus });
    showToast(`Booking #${id} status updated to ${newStatus}`, 'success');
    await loadBookingsTable();
    await loadDashboardOverview();
  } catch (err) {
    showToast(`Failed to update booking status: ${err.message}`, 'error');
    loadBookingsTable();
  }
}

function getStatusBadgeClass(status) {
  switch (status) {
    case 'CONFIRMED': return 'badge-status-confirmed';
    case 'ACTIVE': return 'badge-status-active';
    case 'COMPLETED': return 'badge-status-completed';
    case 'CANCELLED': return 'badge-status-cancelled';
    default: return 'badge-status-pending';
  }
}

// Re-render prices dynamically on currency change
window.addEventListener('currencyChanged', () => {
  loadDashboardOverview();
  filterAdminFleet();
  if (adminBookings.length > 0) loadBookingsTable();
});

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('metric-total-vehicles')) {
    initAdminDashboard();
  }

  const vehicleForm = document.getElementById('vehicle-form');
  if (vehicleForm) {
    vehicleForm.addEventListener('submit', handleVehicleFormSubmit);
  }
});
