/**
 * DriveEase — Authentication & Form Validation Script
 */

// Handle Customer / Admin Login
async function handleLoginFormSubmit(event) {
  event.preventDefault();
  const errorAlert = document.getElementById('login-error-alert');
  const submitBtn = document.getElementById('login-submit-btn');

  if (errorAlert) errorAlert.classList.add('d-none');

  const email = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-password').value;

  if (!email || !password) {
    showErrorAlert('Please enter both your email address and password.');
    return;
  }

  submitBtn.disabled = true;
  submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>Signing in...`;

  try {
    const res = await DriveEaseApi.post('/auth/login', { email, password });
    if (res.success && res.data && res.data.user) {
      DriveEaseAuth.currentUser = res.data.user;
      localStorage.setItem('driveease_user', JSON.stringify(res.data.user));

      showToast(`Welcome back, ${res.data.user.fullName}!`, 'success');

      // Check redirect param
      const params = new URLSearchParams(window.location.search);
      const redirect = params.get('redirect');

      setTimeout(() => {
        if (res.data.user.role === 'ROLE_ADMIN' && !redirect) {
          window.location.href = '/admin.html';
        } else if (redirect) {
          window.location.href = redirect;
        } else {
          window.location.href = '/my-bookings.html';
        }
      }, 700);
    }
  } catch (err) {
    showErrorAlert(err.message || 'Invalid email or password. Please verify your credentials.');
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = `Sign In <i class="bi bi-arrow-right ms-1"></i>`;
  }
}

// 1-Click Demo Credentials Filler
function fillDemoCredentials(type) {
  const emailInput = document.getElementById('login-email');
  const passwordInput = document.getElementById('login-password');
  if (!emailInput || !passwordInput) return;

  if (type === 'admin') {
    emailInput.value = 'admin@driveease.com';
    passwordInput.value = 'admin123';
    showToast('Loaded Administrator credentials', 'info');
  } else {
    emailInput.value = 'john@example.com';
    passwordInput.value = 'customer123';
    showToast('Loaded Demo Customer credentials', 'info');
  }
}

// Handle Customer Registration
async function handleRegisterFormSubmit(event) {
  event.preventDefault();
  const errorAlert = document.getElementById('register-error-alert');
  const submitBtn = document.getElementById('register-submit-btn');

  if (errorAlert) errorAlert.classList.add('d-none');

  const fullName = document.getElementById('reg-fullname').value.trim();
  const email = document.getElementById('reg-email').value.trim();
  const phone = document.getElementById('reg-phone').value.trim();
  const password = document.getElementById('reg-password').value;
  const confirmPassword = document.getElementById('reg-confirm-password').value;

  // Validation
  if (fullName.length < 2) {
    showErrorAlert('Full name must be at least 2 characters.');
    return;
  }
  if (!validateEmail(email)) {
    showErrorAlert('Please provide a valid email address.');
    return;
  }
  if (!phone) {
    showErrorAlert('Phone number is required.');
    return;
  }
  if (password.length < 6) {
    showErrorAlert('Password must be at least 6 characters in length.');
    return;
  }
  if (password !== confirmPassword) {
    showErrorAlert('Passwords do not match. Please re-enter.');
    return;
  }

  submitBtn.disabled = true;
  submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>Creating Account...`;

  try {
    const payload = { fullName, email, phone, password, confirmPassword };
    const res = await DriveEaseApi.post('/auth/register', payload);

    showToast('Account registered successfully! Signing you in...', 'success');

    // Auto login immediately
    try {
      const loginRes = await DriveEaseApi.post('/auth/login', { email, password });
      if (loginRes.success && loginRes.data && loginRes.data.user) {
        DriveEaseAuth.currentUser = loginRes.data.user;
        localStorage.setItem('driveease_user', JSON.stringify(loginRes.data.user));

        setTimeout(() => {
          const params = new URLSearchParams(window.location.search);
          const redirect = params.get('redirect') || '/my-bookings.html';
          window.location.href = redirect;
        }, 700);
        return;
      }
    } catch (e) {
      // Fallback redirect to login
      setTimeout(() => {
        window.location.href = '/login.html';
      }, 1000);
    }
  } catch (err) {
    showErrorAlert(err.message || 'Registration failed. Email may already be in use.');
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = `Create Account <i class="bi bi-arrow-right ms-1"></i>`;
  }
}

function showErrorAlert(msg) {
  const alertEl = document.getElementById('login-error-alert') || document.getElementById('register-error-alert');
  if (alertEl) {
    alertEl.innerHTML = `<i class="bi bi-exclamation-circle-fill me-2"></i>${msg}`;
    alertEl.classList.remove('d-none');
  } else {
    showToast(msg, 'error');
  }
}

function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Bind auth form listeners
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', handleLoginFormSubmit);
  }

  const registerForm = document.getElementById('register-form');
  if (registerForm) {
    registerForm.addEventListener('submit', handleRegisterFormSubmit);
  }
});
