// Navigation toggle for mobile
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        }, 5000);
    });
    
    // Payment mode selection
    const paymentModes = document.querySelectorAll('.payment-mode');
    const paymentModeInput = document.querySelector('input[name="payment_mode"]');
    
    paymentModes.forEach(mode => {
        mode.addEventListener('click', function() {
            // Remove selected class from all modes
            paymentModes.forEach(m => m.classList.remove('selected'));
            
            // Add selected class to clicked mode
            this.classList.add('selected');
            
            // Update hidden input value
            if (paymentModeInput) {
                paymentModeInput.value = this.dataset.mode;
            }
        });
    });
    
    // Card number formatting
    const cardNumberInput = document.querySelector('input[name="card_number"]');
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', function() {
            let value = this.value.replace(/\s/g, '').replace(/[^0-9]/gi, '');
            let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
            this.value = formattedValue;
        });
    }
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let hasErrors = false;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = '#dc3545';
                    hasErrors = true;
                } else {
                    field.style.borderColor = '#e1e5e9';
                }
            });
            
            if (hasErrors) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });
    
    // Table row click handlers
    const tableRows = document.querySelectorAll('tr[data-href]');
    tableRows.forEach(row => {
        row.addEventListener('click', function() {
            window.location.href = this.dataset.href;
        });
        row.style.cursor = 'pointer';
    });
    
    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('.btn-danger[href*="delete"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });
    
    // Auto-refresh for dashboard
    if (window.location.pathname.includes('dashboard')) {
        setInterval(() => {
            // Refresh page every 5 minutes
            window.location.reload();
        }, 300000);
    }
    
    // Search functionality
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('tbody tr');
            
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
    
    // Amount validation for payments
    const amountInputs = document.querySelectorAll('input[name="amount"]');
    amountInputs.forEach(input => {
        input.addEventListener('input', function() {
            const value = parseFloat(this.value);
            const max = parseFloat(this.getAttribute('max'));
            
            if (value > max) {
                this.setCustomValidity(`Amount cannot exceed $${max}`);
            } else if (value <= 0) {
                this.setCustomValidity('Amount must be greater than 0');
            } else {
                this.setCustomValidity('');
            }
        });
    });
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Export functions for use in templates
window.MyFeeStatus = {
    formatCurrency,
    formatDate
};
