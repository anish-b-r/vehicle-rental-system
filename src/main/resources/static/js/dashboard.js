/**
 * DriveEase — Customer Dashboard & My Bookings Script
 */

let myBookingsList = [];
let pendingCancelBookingId = null;

async function initCustomerDashboard() {
  // Ensure authenticated
  const user = DriveEaseAuth.getUser();
  if (!user) {
    // Attempt re-check with API
    try {
      const refreshedUser = await DriveEaseAuth.init();
      if (!refreshedUser) {
        window.location.href = '/login.html?redirect=my-bookings.html';
        return;
      }
    } catch (e) {
      window.location.href = '/login.html?redirect=my-bookings.html';
      return;
    }
  }

  renderUserProfile(DriveEaseAuth.getUser());
  await loadMyBookings();
}

function renderUserProfile(user) {
  if (!user) return;
  const nameEl = document.getElementById('user-profile-name');
  const emailEl = document.getElementById('user-profile-email');
  const phoneEl = document.getElementById('user-profile-phone');
  const avatarEl = document.getElementById('user-profile-avatar');

  if (nameEl) nameEl.textContent = user.fullName;
  if (emailEl) emailEl.textContent = user.email;
  if (phoneEl) phoneEl.textContent = user.phone || 'Phone not set';
  if (avatarEl) {
    const initials = user.fullName ? user.fullName.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase() : 'U';
    avatarEl.textContent = initials;
  }
}

async function loadMyBookings() {
  const activeContainer = document.getElementById('active-bookings-list');
  const pastContainer = document.getElementById('past-bookings-list');

  try {
    const res = await DriveEaseApi.get('/bookings/my');
    myBookingsList = res.data || [];

    // Calculate customer metrics
    const totalCount = myBookingsList.length;
    const activeCount = myBookingsList.filter(b => b.status === 'CONFIRMED' || b.status === 'ACTIVE').length;
    const completedCount = myBookingsList.filter(b => b.status === 'COMPLETED').length;

    const totalEl = document.getElementById('cust-metric-total');
    const activeEl = document.getElementById('cust-metric-active');
    const completedEl = document.getElementById('cust-metric-completed');

    if (totalEl) totalEl.textContent = totalCount;
    if (activeEl) activeEl.textContent = activeCount;
    if (completedEl) completedEl.textContent = completedCount;

    // Filter active and past bookings
    const activeBookings = myBookingsList.filter(b => b.status === 'CONFIRMED' || b.status === 'ACTIVE' || b.status === 'PENDING');
    const pastBookings = myBookingsList.filter(b => b.status === 'COMPLETED' || b.status === 'CANCELLED');

    renderBookingsSection(activeBookings, activeContainer, true);
    renderBookingsSection(pastBookings, pastContainer, false);
  } catch (err) {
    showToast(`Failed to load bookings: ${err.message}`, 'error');
  }
}

function renderBookingsSection(bookings, container, isActiveSection) {
  if (!container) return;

  if (!bookings || bookings.length === 0) {
    container.innerHTML = `
      <div class="empty-state-box py-4">
        <i class="bi bi-calendar2-x empty-state-icon text-muted"></i>
        <h6 class="fw-bold mt-2">No ${isActiveSection ? 'active or upcoming' : 'past'} bookings found</h6>
        ${isActiveSection ? '<a href="/vehicles.html" class="btn btn-de-primary btn-sm-custom mt-2">Explore Fleet & Book</a>' : ''}
      </div>
    `;
    return;
  }

  container.innerHTML = bookings.map(b => createBookingRowHtml(b)).join('');
}

function createBookingRowHtml(b) {
  const statusClass = getStatusBadgeClass(b.status);

  return `
    <div class="card mb-3 border rounded-3 p-3 shadow-sm">
      <div class="row align-items-center">
        <div class="col-md-2 col-4 mb-2 mb-md-0">
          <img src="${b.vehicleImageUrl || 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=400&q=80'}" 
               alt="${b.vehicleName}"
               class="rounded-3 w-100" 
               style="height: 75px; object-fit: cover;">
        </div>
        <div class="col-md-4 col-8 mb-2 mb-md-0">
          <span class="badge ${statusClass} mb-1">${b.status}</span>
          <h5 class="fw-bold mb-1 fs-6">${b.vehicleName}</h5>
          <div class="small text-muted">
            <span class="fw-semibold text-dark">${b.bookingNumber}</span> · ${b.vehicleCategory}
          </div>
        </div>
        <div class="col-md-3 col-6 small">
          <div class="text-muted"><i class="bi bi-calendar-event me-1"></i>Duration:</div>
          <div class="fw-semibold text-dark">${formatDate(b.startDate)} → ${formatDate(b.endDate)} (${b.totalDays} Days)</div>
          <div class="text-muted mt-1"><i class="bi bi-geo-alt me-1"></i>${b.pickupLocation || 'Downtown Hub'}</div>
        </div>
        <div class="col-md-3 col-6 text-md-end text-start mt-2 mt-md-0">
          <div class="fs-5 fw-bold text-dark">${formatCurrency(b.totalAmount)}</div>
          <div class="small text-muted mb-2">Total Paid</div>
          <div class="d-flex gap-2 justify-content-md-end">
            <button class="btn btn-de-outline btn-sm-custom" onclick="openReceiptModal('${b.bookingNumber}')">
              <i class="bi bi-receipt"></i> Details
            </button>
            ${b.canBeCancelled ? `
              <button class="btn btn-outline-danger btn-sm-custom" onclick="promptCancelBooking(${b.id}, '${b.vehicleName}')">
                <i class="bi bi-x-circle"></i> Cancel
              </button>
            ` : ''}
          </div>
        </div>
      </div>
    </div>
  `;
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

function openReceiptModal(bookingNumber) {
  const booking = myBookingsList.find(b => b.bookingNumber === bookingNumber);
  if (!booking) return;

  document.getElementById('receipt-number').textContent = booking.bookingNumber;
  document.getElementById('receipt-status').textContent = booking.status;
  document.getElementById('receipt-status').className = `badge ${getStatusBadgeClass(booking.status)}`;
  document.getElementById('receipt-vehicle').textContent = booking.vehicleName;
  document.getElementById('receipt-dates').textContent = `${formatDate(booking.startDate)} — ${formatDate(booking.endDate)} (${booking.totalDays} Days)`;
  document.getElementById('receipt-pickup').textContent = booking.pickupLocation || 'Downtown Executive Hub';
  document.getElementById('receipt-rate').textContent = `${formatCurrency(booking.dailyRate)} / day`;
  document.getElementById('receipt-subtotal').textContent = formatCurrency(booking.subtotal);

  const discountRow = document.getElementById('receipt-discount-row');
  if (booking.discountAmount && Number(booking.discountAmount) > 0) {
    discountRow.style.display = 'flex';
    document.getElementById('receipt-discount').textContent = `-${formatCurrency(booking.discountAmount)}`;
  } else {
    discountRow.style.display = 'none';
  }

  document.getElementById('receipt-tax').textContent = formatCurrency(booking.taxAmount);
  document.getElementById('receipt-deposit').textContent = formatCurrency(booking.securityDeposit);
  document.getElementById('receipt-total').textContent = formatCurrency(booking.totalAmount);
  document.getElementById('receipt-payment-method').textContent = booking.paymentMethod || 'Credit Card';

  const modal = new bootstrap.Modal(document.getElementById('receiptModal'));
  modal.show();
}

function promptCancelBooking(bookingId, vehicleName) {
  pendingCancelBookingId = bookingId;
  const modalText = document.getElementById('cancel-modal-vehicle-text');
  if (modalText) {
    modalText.textContent = `Are you sure you want to cancel your rental booking for ${vehicleName}? The security deposit will be fully refunded to your payment method.`;
  }
  const modal = new bootstrap.Modal(document.getElementById('cancelConfirmModal'));
  modal.show();
}

async function confirmCancelBooking() {
  if (!pendingCancelBookingId) return;

  const btn = document.getElementById('confirm-cancel-btn');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span>Cancelling...`;

  try {
    await DriveEaseApi.patch(`/bookings/${pendingCancelBookingId}/cancel`);
    showToast('Your booking has been cancelled and deposit marked for refund.', 'success');

    // Close modal
    const modalEl = document.getElementById('cancelConfirmModal');
    const modal = bootstrap.Modal.getInstance(modalEl);
    if (modal) modal.hide();

    // Reload list
    await loadMyBookings();
  } catch (err) {
    showToast(`Cancellation error: ${err.message}`, 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = 'Yes, Cancel Booking';
    pendingCancelBookingId = null;
  }
}

// Re-render dynamically on currency change
window.addEventListener('currencyChanged', () => {
  if (myBookingsList.length > 0) {
    const activeContainer = document.getElementById('active-bookings-list');
    const pastContainer = document.getElementById('past-bookings-list');
    const activeBookings = myBookingsList.filter(b => b.status === 'CONFIRMED' || b.status === 'ACTIVE' || b.status === 'PENDING');
    const pastBookings = myBookingsList.filter(b => b.status === 'COMPLETED' || b.status === 'CANCELLED');
    renderBookingsSection(activeBookings, activeContainer, true);
    renderBookingsSection(pastBookings, pastContainer, false);
  }
});

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('active-bookings-list')) {
    initCustomerDashboard();
  }
});
