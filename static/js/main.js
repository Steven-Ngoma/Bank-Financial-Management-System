// Main JavaScript for SmartLoan Financial System

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// API Helper Functions
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Risk Assessment Functions
function calculateRiskScore(customer, loan) {
    let score = 500; // Base score
    
    // Credit score impact (35% weight)
    const creditImpact = (customer.credit_score - 650) * 0.35;
    score += creditImpact;
    
    // Debt-to-income ratio (25% weight)
    const monthlyIncome = customer.annual_income / 12;
    const estimatedPayment = calculateMonthlyPayment(loan.amount, loan.term_months);
    const dtiRatio = estimatedPayment / monthlyIncome;
    
    if (dtiRatio <= 0.28) score += 100;
    else if (dtiRatio <= 0.36) score += 50;
    else if (dtiRatio > 0.43) score -= 100;
    
    // Employment stability (20% weight)
    if (customer.employment_years >= 5) score += 80;
    else if (customer.employment_years >= 2) score += 40;
    else if (customer.employment_years < 1) score -= 60;
    
    // Loan-to-income ratio (15% weight)
    const ltiRatio = loan.amount / customer.annual_income;
    if (ltiRatio <= 2) score += 60;
    else if (ltiRatio <= 3) score += 30;
    else if (ltiRatio > 4) score -= 60;
    
    return Math.max(300, Math.min(850, Math.round(score)));
}

function calculateMonthlyPayment(principal, termMonths, annualRate = 5.5) {
    const monthlyRate = annualRate / 100 / 12;
    if (monthlyRate === 0) return principal / termMonths;
    
    return (principal * monthlyRate * Math.pow(1 + monthlyRate, termMonths)) / 
           (Math.pow(1 + monthlyRate, termMonths) - 1);
}

function getRiskCategory(score) {
    if (score >= 750) return { category: 'Low Risk', class: 'success' };
    if (score >= 650) return { category: 'Medium Risk', class: 'warning' };
    if (score >= 500) return { category: 'High Risk', class: 'danger' };
    return { category: 'Very High Risk', class: 'danger' };
}

// Form Validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Loading States
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.add('loading');
        element.style.pointerEvents = 'none';
    }
}

function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.remove('loading');
        element.style.pointerEvents = 'auto';
    }
}

// Notification System
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Chart Utilities
function createChart(canvasId, type, data, options = {}) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    
    return new Chart(ctx.getContext('2d'), {
        type: type,
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            ...options
        }
    });
}

// Data Export Functions
function exportToCSV(data, filename) {
    const csv = convertToCSV(data);
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    
    window.URL.revokeObjectURL(url);
}

function convertToCSV(data) {
    if (!data.length) return '';
    
    const headers = Object.keys(data[0]);
    const csvContent = [
        headers.join(','),
        ...data.map(row => headers.map(header => `"${row[header]}"`).join(','))
    ].join('\n');
    
    return csvContent;
}

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 100);
    });
});

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    showNotification('An unexpected error occurred. Please try again.', 'danger');
});

// Export functions for use in other scripts
window.SmartLoan = {
    formatCurrency,
    formatDate,
    apiRequest,
    calculateRiskScore,
    calculateMonthlyPayment,
    getRiskCategory,
    validateForm,
    showLoading,
    hideLoading,
    showNotification,
    createChart,
    exportToCSV
};