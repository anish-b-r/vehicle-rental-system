/**
 * DriveEase — Core Application Script
 * Global API client, Multi-Currency Engine, Authentication State, Toast notifications.
 */

const DriveEaseApi = {
  baseUrl: '/api',

  async request(endpoint, options = {}) {
    const url = endpoint.startsWith('http') ? endpoint : `${this.baseUrl}${endpoint}`;
    const defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };

    const config = {
      ...options,
      credentials: 'include',
      headers: {
        ...defaultHeaders,
        ...options.headers
      }
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || `Request failed with status ${response.status}`);
      }
      return data;
    } catch (err) {
      console.error(`API Error [${endpoint}]:`, err);
      throw err;
    }
  },

  get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  },

  post(endpoint, body) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(body)
    });
  },

  put(endpoint, body) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body)
    });
  },

  patch(endpoint, body) {
    return this.request(endpoint, {
      method: 'PATCH',
      body: body ? JSON.stringify(body) : undefined
    });
  },

  delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
};

const DriveEaseCurrency = {
  current: localStorage.getItem('driveease_currency') || 'INR',
  rates: {
    INR: 1.0,
    USD: 0.010593,
    EUR: 0.009617,
    GBP: 0.008027,
    AED: 0.038904
  },
  symbols: {
    INR: '₹',
    USD: '$',
    EUR: '€',
    GBP: '£',
    AED: 'AED '
  },
  meta: {
    INR: { symbol: '₹', label: 'INR (₹)', name: 'Indian Rupee' },
    USD: { symbol: '$', label: 'USD ($)', name: 'US Dollar' },
    EUR: { symbol: '€', label: 'EUR (€)', name: 'Euro' },
    GBP: { symbol: '£', label: 'GBP (£)', name: 'British Pound' },
    AED: { symbol: 'د.إ', label: 'AED (د.إ)', name: 'UAE Dirham' }
  },

  async init() {
    this.updateDropdownUI();
    try {
      const res = await DriveEaseApi.get('/currency/rates');
      if (res && res.success && res.data && res.data.rates) {
        this.rates = { ...this.rates, ...res.data.rates };
        // If non-default currency, notify pages of fresh live rate
        if (this.current !== 'INR') {
          window.dispatchEvent(new CustomEvent('currencyChanged', {
            detail: { currency: this.current, rate: this.getRate(this.current) }
          }));
        }
      }
    } catch (e) {
      console.warn('Currency rates API fallback in effect:', e);
    }
    this.updateDropdownUI();
  },

  setCurrency(code) {
    if (!this.symbols[code]) return;
    this.current = code;
    localStorage.setItem('driveease_currency', code);
    this.updateDropdownUI();
    window.dispatchEvent(new CustomEvent('currencyChanged', {
      detail: { currency: code, rate: this.getRate(code) }
    }));
  },

  getRate(code = this.current) {
    return this.rates[code] || 1.0;
  },

  convert(amountInInr) {
    if (amountInInr === null || amountInInr === undefined || isNaN(amountInInr)) return 0;
    const rate = this.getRate();
    return Number(amountInInr) * rate;
  },

  format(amountInInr) {
    if (amountInInr === null || amountInInr === undefined || isNaN(amountInInr)) {
      return `${this.symbols[this.current] || '₹'}0`;
    }
    const converted = this.convert(amountInInr);
    const sym = this.symbols[this.current] || '₹';

    if (this.current === 'INR') {
      return sym + Math.round(converted).toLocaleString('en-IN');
    } else if (this.current === 'AED') {
      return 'AED ' + converted.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    } else {
      return sym + converted.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    }
  },

  updateDropdownUI() {
    const flagEl = document.getElementById('active-currency-flag');
    const textEl = document.getElementById('active-currency-text');
    const m = this.meta[this.current] || this.meta['INR'];
    if (flagEl) {
      flagEl.className = 'currency-symbol-badge';
      flagEl.textContent = m.symbol;
    }
    if (textEl) {
      textEl.textContent = m.label;
    }

    // Highlight active selection in all dropdowns
    document.querySelectorAll('#currency-selector-wrapper .dropdown-item').forEach(item => {
      const cur = item.getAttribute('data-currency');
      if (cur === this.current) {
        item.classList.add('active', 'fw-bold');
      } else {
        item.classList.remove('active', 'fw-bold');
      }
    });
  }
};

const DriveEaseAuth = {
  currentUser: null,

  async init() {
    try {
      const res = await DriveEaseApi.get('/auth/me');
      if (res && res.success && res.data) {
        this.currentUser = res.data;
        localStorage.setItem('driveease_user', JSON.stringify(res.data));
      } else {
        this.currentUser = null;
        localStorage.removeItem('driveease_user');
      }
    } catch (e) {
      this.currentUser = null;
      localStorage.removeItem('driveease_user');
    }
    this.updateNavbar();
    return this.currentUser;
  },

  getUser() {
    if (!this.currentUser) {
      const saved = localStorage.getItem('driveease_user');
      if (saved) {
        try { this.currentUser = JSON.parse(saved); } catch (e) {}
      }
    }
    return this.currentUser;
  },

  isLoggedIn() {
    return !!this.getUser();
  },

  isAdmin() {
    const u = this.getUser();
    return u && u.role === 'ROLE_ADMIN';
  },

  async logout() {
    try {
      await DriveEaseApi.post('/auth/logout', {});
    } catch (e) {}
    this.currentUser = null;
    localStorage.removeItem('driveease_user');
    showToast('You have been logged out.', 'info');
    setTimeout(() => {
      window.location.href = '/index.html';
    }, 500);
  },

  updateNavbar() {
    const navAuthContainer = document.getElementById('navbar-auth-actions');
    if (!navAuthContainer) return;

    const user = this.getUser();

    if (user) {
      const isAdminUser = user.role === 'ROLE_ADMIN';
      navAuthContainer.innerHTML = `
        <div class="dropdown">
          <button class="btn btn-de-outline dropdown-toggle d-flex align-items-center gap-2" type="button" data-bs-toggle="dropdown" aria-expanded="false">
            <i class="bi bi-person-circle"></i>
            <span>${user.fullName ? user.fullName.split(' ')[0] : 'Account'}</span>
            ${isAdminUser ? '<span class="badge bg-dark ms-1">Admin</span>' : ''}
          </button>
          <ul class="dropdown-menu dropdown-menu-end shadow-sm border mt-2">
            <li><h6 class="dropdown-header text-truncate" style="max-width: 200px;">${user.email}</h6></li>
            ${isAdminUser ? '<li><a class="dropdown-item" href="/admin.html"><i class="bi bi-speedometer2 me-2"></i>Admin Dashboard</a></li>' : ''}
            <li><a class="dropdown-item" href="/my-bookings.html"><i class="bi bi-calendar-check me-2"></i>My Bookings</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><button class="dropdown-item text-danger" onclick="DriveEaseAuth.logout()"><i class="bi bi-box-arrow-right me-2"></i>Sign Out</button></li>
          </ul>
        </div>
      `;
    } else {
      navAuthContainer.innerHTML = `
        <a href="/login.html" class="nav-link-custom text-dark fw-semibold me-2">Login</a>
        <a href="/register.html" class="btn btn-de-primary">Get Started</a>
      `;
    }
  }
};

// Global Toast helper
function showToast(message, type = 'info', duration = 3500) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `de-toast de-toast-${type}`;

  let icon = 'bi-info-circle-fill text-primary';
  if (type === 'success') icon = 'bi-check-circle-fill text-success';
  if (type === 'error') icon = 'bi-exclamation-triangle-fill text-danger';

  toast.innerHTML = `
    <i class="bi ${icon} fs-5"></i>
    <div class="flex-grow-1 fs-6">${message}</div>
    <button type="button" class="btn-close btn-sm" aria-label="Close"></button>
  `;

  toast.querySelector('.btn-close').addEventListener('click', () => {
    toast.remove();
  });

  container.appendChild(toast);

  setTimeout(() => {
    if (toast.parentNode) {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }
  }, duration);
}

function formatCurrency(amountInInr) {
  return DriveEaseCurrency.format(amountInInr);
}

function formatDate(dateStr) {
  if (!dateStr) return 'N/A';
  const parts = dateStr.split('-');
  if (parts.length === 3) {
    const d = new Date(parts[0], parts[1] - 1, parts[2]);
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  }
  return dateStr;
}

// ==========================================================================
// Render Free Instance Server Health & Cold-Start Monitor
// ==========================================================================
const RenderServerMonitor = {
  isAwake: false,
  elapsedSeconds: 0,
  timerInterval: null,
  bannerEl: null,

  init() {
    this.createBannerElement();
    this.checkServer();
  },

  createBannerElement() {
    if (document.getElementById('render-server-status-banner')) return;

    const banner = document.createElement('div');
    banner.id = 'render-server-status-banner';
    banner.innerHTML = `
      <div class="render-banner-inner">
        <div class="render-banner-left">
          <div class="render-spinner-ring" id="render-banner-spinner"></div>
          <div>
            <div class="render-banner-title">
              <span id="render-banner-headline">⚡ Waking up Render Cloud Server...</span>
              <span class="render-time-badge" id="render-banner-timer">0s</span>
            </div>
            <div class="render-banner-desc" id="render-banner-sub">
              Free-tier instances spin down after inactivity and take ~30–50s to wake up on cold start. Connecting automatically...
            </div>
          </div>
        </div>
        <div class="d-none d-md-block text-end">
          <span class="badge bg-light text-dark font-monospace" style="font-size: 0.72rem; padding: 4px 8px;">Render Free Tier • Java 21</span>
        </div>
      </div>
    `;
    document.body.prepend(banner);
    this.bannerEl = banner;
  },

  checkServer() {
    if (this.isAwake) return;

    const startTime = Date.now();
    this.timerInterval = setInterval(() => {
      this.elapsedSeconds = Math.floor((Date.now() - startTime) / 1000);
      const timerEl = document.getElementById('render-banner-timer');
      if (timerEl) {
        timerEl.textContent = `${this.elapsedSeconds}s elapsed`;
      }
      // If server took more than 1.8s to respond, show the banner
      if (this.elapsedSeconds >= 2 && !this.isAwake && this.bannerEl) {
        this.bannerEl.classList.add('banner-visible');
      }
    }, 1000);

    this.pollUntilAwake();
  },

  async pollUntilAwake() {
    let attempts = 0;
    while (!this.isAwake) {
      attempts++;
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 6000);
        const res = await fetch('/api/currency/rates', { signal: controller.signal, cache: 'no-store' });
        clearTimeout(timeoutId);

        if (res.ok) {
          const json = await res.json();
          if (json && json.success) {
            this.handleServerAwake();
            return;
          }
        }
      } catch (e) {
        // Cold start in progress, update message
        const headline = document.getElementById('render-banner-headline');
        const sub = document.getElementById('render-banner-sub');
        if (headline && this.elapsedSeconds >= 4) {
          headline.innerHTML = `⚡ Render Server Booting Up (Attempt ${attempts})...`;
        }
        if (sub && this.elapsedSeconds >= 20) {
          sub.textContent = 'Spring Boot container is initializing (~30–50s). Please remain on the page, connecting automatically...';
        }
      }
      await new Promise(r => setTimeout(r, 2500));
    }
  },

  handleServerAwake() {
    this.isAwake = true;
    clearInterval(this.timerInterval);

    this.injectNavbarIndicator();

    if (this.bannerEl && this.bannerEl.classList.contains('banner-visible')) {
      this.bannerEl.classList.remove('banner-error');
      this.bannerEl.classList.add('banner-connected');

      const headline = document.getElementById('render-banner-headline');
      const sub = document.getElementById('render-banner-sub');
      const spinner = document.getElementById('render-banner-spinner');
      const timer = document.getElementById('render-banner-timer');

      if (spinner) {
        spinner.className = 'bi bi-check-circle-fill fs-5 text-white';
        spinner.style.border = 'none';
        spinner.style.animation = 'none';
      }
      if (headline) {
        headline.textContent = '✅ Render Server Connected & Ready!';
      }
      if (timer) {
        timer.textContent = `Awake in ${this.elapsedSeconds}s`;
        timer.style.backgroundColor = 'rgba(255,255,255,0.25)';
        timer.style.color = '#FFFFFF';
      }
      if (sub) {
        sub.textContent = 'Spring Boot backend and database services are online and active.';
      }

      window.dispatchEvent(new CustomEvent('renderServerAwake'));

      setTimeout(() => {
        if (this.bannerEl) {
          this.bannerEl.classList.remove('banner-visible');
          setTimeout(() => {
            this.bannerEl.remove();
          }, 450);
        }
      }, 2500);
    } else {
      window.dispatchEvent(new CustomEvent('renderServerAwake'));
    }
  },

  injectNavbarIndicator() {
    const authActions = document.getElementById('navbar-auth-actions');
    if (authActions && !document.getElementById('render-live-indicator')) {
      const pill = document.createElement('div');
      pill.id = 'render-live-indicator';
      pill.className = 'render-live-indicator d-none d-lg-inline-flex me-2';
      pill.title = 'Render Web Service: Active & Live (Singapore)';
      pill.innerHTML = `<span class="live-dot"></span><span>Server Online</span>`;
      authActions.parentNode.insertBefore(pill, authActions);
    }
  }
};

// Auto-run auth & currency verification on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  RenderServerMonitor.init();
  DriveEaseCurrency.init();
  DriveEaseAuth.init();
});
