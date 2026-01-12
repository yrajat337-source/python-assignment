// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    
    // Real-time validation
    const username = document.getElementById('username');
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    
    // Username validation
    username.addEventListener('blur', function() {
        const error = document.getElementById('usernameError');
        if (this.value.length < 3) {
            error.textContent = 'Username must be at least 3 characters';
            this.style.borderColor = '#c00';
        } else {
            error.textContent = '';
            this.style.borderColor = '#4caf50';
        }
    });
    
    // Email validation
    email.addEventListener('blur', function() {
        const error = document.getElementById('emailError');
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(this.value)) {
            error.textContent = 'Please enter a valid email address';
            this.style.borderColor = '#c00';
        } else {
            error.textContent = '';
            this.style.borderColor = '#4caf50';
        }
    });
    
    // Password validation
    password.addEventListener('blur', function() {
        const error = document.getElementById('passwordError');
        if (this.value.length < 6) {
            error.textContent = 'Password must be at least 6 characters';
            this.style.borderColor = '#c00';
        } else {
            error.textContent = '';
            this.style.borderColor = '#4caf50';
        }
    });
    
    // Confirm password validation
    confirmPassword.addEventListener('blur', function() {
        const error = document.getElementById('confirmPasswordError');
        if (this.value !== password.value) {
            error.textContent = 'Passwords do not match';
            this.style.borderColor = '#c00';
        } else {
            error.textContent = '';
            this.style.borderColor = '#4caf50';
        }
    });
    
    // Form submission validation
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        // Check all required fields
        if (username.value.length < 3) {
            document.getElementById('usernameError').textContent = 'Username must be at least 3 characters';
            isValid = false;
        }
        
        if (!email.value.includes('@')) {
            document.getElementById('emailError').textContent = 'Please enter a valid email';
            isValid = false;
        }
        
        if (password.value.length < 6) {
            document.getElementById('passwordError').textContent = 'Password must be at least 6 characters';
            isValid = false;
        }
        
        if (password.value !== confirmPassword.value) {
            document.getElementById('confirmPasswordError').textContent = 'Passwords do not match';
            isValid = false;
        }
        
        if (!isValid) {
            e.preventDefault();
        }
    });
});