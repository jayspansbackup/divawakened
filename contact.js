// Contact form validation and enhancement
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    const submitBtn = document.getElementById('submitBtn');
    const descriptionField = document.getElementById('description');
    const descriptionCount = document.getElementById('descriptionCount');
    const flashMessages = document.getElementById('flash-messages');
    
    // Email validation regex
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    
    // Character counter for description field
    if (descriptionField && descriptionCount) {
        descriptionField.addEventListener('input', function() {
            const currentLength = this.value.length;
            descriptionCount.textContent = currentLength;
            
            if (currentLength > 1800) {
                descriptionCount.style.color = 'var(--bs-warning)';
            } else if (currentLength > 1900) {
                descriptionCount.style.color = 'var(--bs-danger)';
            } else {
                descriptionCount.style.color = '';
            }
        });
        
        // Initialize counter
        descriptionCount.textContent = descriptionField.value.length;
    }
    
    // Real-time validation
    function validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        
        // Remove existing validation classes
        field.classList.remove('is-valid', 'is-invalid');
        
        switch(field.type) {
            case 'email':
                isValid = value && emailRegex.test(value);
                break;
            case 'tel':
                isValid = value.length > 0;
                break;
            case 'radio':
                // For radio buttons, check if any in the group is selected
                const radioGroup = document.querySelectorAll(`input[name="${field.name}"]`);
                isValid = Array.from(radioGroup).some(radio => radio.checked);
                // Apply validation to all radio buttons in the group
                radioGroup.forEach(radio => {
                    radio.classList.remove('is-valid', 'is-invalid');
                    radio.classList.add(isValid ? 'is-valid' : 'is-invalid');
                });
                return isValid;
            case 'text':
            case 'textarea':
                isValid = value.length > 0;
                break;
            default:
                isValid = value.length > 0;
        }
        
        // Check length limits
        if (field.hasAttribute('maxlength')) {
            const maxLength = parseInt(field.getAttribute('maxlength'));
            if (value.length > maxLength) {
                isValid = false;
            }
        }
        
        // Add validation class
        field.classList.add(isValid ? 'is-valid' : 'is-invalid');
        
        return isValid;
    }
    
    // Add real-time validation to all required fields
    const requiredFields = form.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        field.addEventListener('blur', function() {
            validateField(this);
        });
        
        field.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                validateField(this);
            }
        });
    });
    
    // Form submission handling
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate all required fields
        let isFormValid = true;
        requiredFields.forEach(field => {
            if (!validateField(field)) {
                isFormValid = false;
            }
        });
        
        if (!isFormValid) {
            // Focus on first invalid field
            const firstInvalid = form.querySelector('.is-invalid');
            if (firstInvalid) {
                firstInvalid.focus();
                firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
            return;
        }
        
        // Show loading state
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
        
        // Submit form
        this.submit();
        
        // Reset form after a short delay (in case of same-page redirect)
        setTimeout(() => {
            if (!document.querySelector('.alert-success')) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        }, 5000);
    });
    
    // Auto-hide flash messages after 5 seconds
    if (flashMessages) {
        const alerts = flashMessages.querySelectorAll('.alert');
        alerts.forEach(alert => {
            // Only auto-hide success messages
            if (alert.classList.contains('alert-success')) {
                setTimeout(() => {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                }, 5000);
            }
        });
    }
    
    // Reset form if submission was successful
    if (document.querySelector('.alert-success')) {
        // Clear form fields
        form.reset();
        
        // Remove validation classes
        requiredFields.forEach(field => {
            field.classList.remove('is-valid', 'is-invalid');
        });
        
        // Reset description counter
        if (descriptionCount) {
            descriptionCount.textContent = '0';
            descriptionCount.style.color = '';
        }
        
        // Scroll to top to show success message
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    // Smooth scroll for form errors
    if (document.querySelector('.alert-danger')) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
});

// Utility function to sanitize input (prevent XSS)
function sanitizeInput(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// Add input sanitization on form fields
document.addEventListener('input', function(e) {
    if (e.target.matches('input[type="text"], input[type="email"], textarea')) {
        // Basic sanitization - remove any HTML tags
        const sanitized = sanitizeInput(e.target.value);
        if (sanitized !== e.target.value) {
            e.target.value = sanitized;
        }
    }
});
