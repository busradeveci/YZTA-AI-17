// YZTA-AI-17 Medical Prediction System JavaScript

// Global variables
let currentSection = 'cardiovascular';
let currentChart = null;

// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize Application
function initializeApp() {
    setupNavigation();
    setupForms();
    setupModelCards();
    setupTabs();
    setupFormValidation();
    console.log('YZTA-AI-17 Medical Prediction System initialized');
}

// Navigation Setup
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetSection = this.getAttribute('data-section');
            switchSection(targetSection);
            updateActiveNavLink(this);
        });
    });
}

function switchSection(sectionName) {
    // Hide all sections
    const sections = document.querySelectorAll('.prediction-section');
    sections.forEach(section => section.classList.remove('active'));
    
    // Show target section
    const targetSection = document.getElementById(sectionName);
    if (targetSection) {
        targetSection.classList.add('active');
        currentSection = sectionName;
    }
    
    // Hide results if switching sections
    hideResults();
}

function updateActiveNavLink(activeLink) {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => link.classList.remove('active'));
    activeLink.classList.add('active');
}

// Model Cards Setup
function setupModelCards() {
    const modelCards = document.querySelectorAll('.model-card');
    
    modelCards.forEach(card => {
        card.addEventListener('click', function() {
            const modelType = this.getAttribute('data-model');
            switchSection(modelType);
            
            // Update navigation
            const navLink = document.querySelector(`[data-section="${modelType}"]`);
            if (navLink) {
                updateActiveNavLink(navLink);
            }
            
            // Scroll to section
            const section = document.getElementById(modelType);
            if (section) {
                section.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// Forms Setup
function setupForms() {
    const forms = document.querySelectorAll('.prediction-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            handleFormSubmission(this);
        });
    });
}

// Form Submission Handler
async function handleFormSubmission(form) {
    const formId = form.getAttribute('id');
    const modelType = getModelTypeFromFormId(formId);
    
    // Show loading
    showLoading();
    
    try {
        // Collect form data
        const formData = collectFormData(form);
        
        // Validate form data
        if (!validateFormData(formData, modelType)) {
            hideLoading();
            return;
        }
        
        // Make prediction request
        const result = await makePredictionRequest(modelType, formData);
        
        // Display results
        displayResults(result, modelType);
        
    } catch (error) {
        console.error('Prediction error:', error);
        showError('Tahmin yapılamadı. Lütfen tekrar deneyin.');
    } finally {
        hideLoading();
    }
}

function getModelTypeFromFormId(formId) {
    if (formId.includes('cardiovascular')) return 'cardiovascular';
    if (formId.includes('breast-cancer')) return 'breast-cancer';
    if (formId.includes('fetal-health')) return 'fetal-health';
    return 'unknown';
}

function collectFormData(form) {
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        // Convert numeric values
        if (!isNaN(value) && value !== '') {
            data[key] = parseFloat(value);
        } else {
            data[key] = value;
        }
    }
    
    return data;
}

function validateFormData(data, modelType) {
    // Basic validation - check for required fields
    const requiredFields = getRequiredFields(modelType);
    
    for (let field of requiredFields) {
        if (!(field in data) || data[field] === '' || data[field] === null) {
            showError(`Lütfen tüm gerekli alanları doldurun. Eksik: ${field}`);
            return false;
        }
    }
    
    return true;
}

function getRequiredFields(modelType) {
    const fieldMaps = {
        'cardiovascular': [
            'age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
            'serum_cholesterol', 'fasting_blood_sugar', 'resting_electrocardiographic_results',
            'maximum_heart_rate_achieved', 'exercise_induced_angina',
            'st_depression_induced_by_exercise', 'slope_of_the_peak_exercise_st_segment',
            'number_of_major_vessels', 'thal'
        ],
        'breast-cancer': [
            'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
            'smoothness_mean', 'compactness_mean', 'concavity_mean',
            'concave_points_mean', 'symmetry_mean', 'fractal_dimension_mean',
            'radius_se', 'texture_se', 'perimeter_se', 'area_se',
            'smoothness_se', 'compactness_se', 'concavity_se',
            'concave_points_se', 'symmetry_se', 'fractal_dimension_se',
            'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst',
            'smoothness_worst', 'compactness_worst', 'concavity_worst',
            'concave_points_worst', 'symmetry_worst', 'fractal_dimension_worst'
        ],
        'fetal-health': [
            'baseline_value', 'accelerations', 'fetal_movement', 'uterine_contractions',
            'light_decelerations', 'severe_decelerations', 'prolongued_decelerations',
            'abnormal_short_term_variability', 'mean_value_of_short_term_variability',
            'percentage_of_time_with_abnormal_long_term_variability',
            'mean_value_of_long_term_variability', 'histogram_width',
            'histogram_min', 'histogram_max', 'histogram_number_of_peaks',
            'histogram_number_of_zeroes', 'histogram_mode', 'histogram_mean',
            'histogram_median', 'histogram_variance', 'histogram_tendency'
        ]
    };
    
    return fieldMaps[modelType] || [];
}

// API Request Handler
async function makePredictionRequest(modelType, data) {
    const endpoints = {
        'cardiovascular': '/api/predict/cardiovascular',
        'breast-cancer': '/api/predict/breast-cancer',
        'fetal-health': '/api/predict/fetal-health'
    };
    
    const endpoint = endpoints[modelType];
    if (!endpoint) {
        throw new Error('Unknown model type');
    }
    
    const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Prediction request failed');
    }
    
    return await response.json();
}

// Results Display
function displayResults(result, modelType) {
    if (result.error) {
        showError(result.error);
        return;
    }
    
    // Update prediction text
    updatePredictionDisplay(result, modelType);
    
    // Update clinical assessment
    updateClinicalAssessment(result);
    
    // Update key findings
    updateKeyFindings(result);
    
    // Update recommendations
    updateRecommendations(result);
    
    // Create visualization
    createResultsVisualization(result, modelType);
    
    // Show results section
    showResults();
}

function updatePredictionDisplay(result, modelType) {
    const predictionText = document.getElementById('prediction-text');
    const confidenceValue = document.getElementById('confidence-value');
    
    // Set prediction text and badge class
    let prediction = '';
    let badgeClass = '';
    
    if (modelType === 'cardiovascular') {
        prediction = result.risk_level || (result.prediction === 1 ? 'Yüksek Risk' : 'Düşük Risk');
        badgeClass = prediction.toLowerCase().replace(' ', '-');
    } else if (modelType === 'breast-cancer') {
        prediction = result.diagnosis || (result.prediction === 1 ? 'Malign' : 'Benign');
        badgeClass = prediction.toLowerCase();
    } else if (modelType === 'fetal-health') {
        const healthMap = { 1: 'Normal', 2: 'Şüpheli', 3: 'Patolojik' };
        prediction = result.health_status || healthMap[result.prediction] || 'Bilinmeyen';
        badgeClass = prediction.toLowerCase();
    }
    
    predictionText.textContent = prediction;
    predictionText.parentElement.className = `prediction-badge ${badgeClass}`;
    
    // Set confidence
    const confidence = result.confidence || result.max_probability || 0;
    confidenceValue.textContent = `${(confidence * 100).toFixed(1)}%`;
}

function updateClinicalAssessment(result) {
    const assessmentDiv = document.getElementById('clinical-assessment');
    
    let assessmentHTML = '';
    
    if (result.risk_level) {
        assessmentHTML += `<p><strong>Risk Level:</strong> ${result.risk_level}</p>`;
    }
    
    if (result.urgency_level) {
        assessmentHTML += `<p><strong>Urgency:</strong> ${result.urgency_level}</p>`;
    }
    
    if (result.tissue_characteristics) {
        assessmentHTML += '<h4>Tissue Characteristics:</h4><ul>';
        for (let [key, value] of Object.entries(result.tissue_characteristics)) {
            assessmentHTML += `<li><strong>${key}:</strong> ${value}</li>`;
        }
        assessmentHTML += '</ul>';
    }
    
    if (result.fetal_parameters) {
        assessmentHTML += '<h4>Fetal Parameters:</h4><ul>';
        for (let [key, value] of Object.entries(result.fetal_parameters)) {
            assessmentHTML += `<li><strong>${key}:</strong> ${value}</li>`;
        }
        assessmentHTML += '</ul>';
    }
    
    if (!assessmentHTML) {
        assessmentHTML = '<p>No specific clinical assessment available.</p>';
    }
    
    assessmentDiv.innerHTML = assessmentHTML;
}

function updateKeyFindings(result) {
    const findingsDiv = document.getElementById('key-findings');
    
    const findings = result.key_findings || result.clinical_flags || [];
    
    if (findings.length > 0) {
        const findingsHTML = '<ul>' + findings.map(finding => `<li>${finding}</li>`).join('') + '</ul>';
        findingsDiv.innerHTML = findingsHTML;
    } else {
        findingsDiv.innerHTML = '<p>No significant findings detected.</p>';
    }
}

function updateRecommendations(result) {
    const recommendationsDiv = document.getElementById('recommendations');
    
    const recommendations = result.clinical_recommendations || result.recommendations || [];
    const followUp = result.follow_up_suggestions || [];
    
    let recommendationsHTML = '';
    
    if (recommendations.length > 0) {
        recommendationsHTML += '<h4>Clinical Recommendations:</h4><ul>';
        recommendations.forEach(rec => {
            recommendationsHTML += `<li>${rec}</li>`;
        });
        recommendationsHTML += '</ul>';
    }
    
    if (followUp.length > 0) {
        recommendationsHTML += '<h4>Follow-up Suggestions:</h4><ul>';
        followUp.forEach(suggestion => {
            recommendationsHTML += `<li>${suggestion}</li>`;
        });
        recommendationsHTML += '</ul>';
    }
    
    if (!recommendationsHTML) {
        recommendationsHTML = '<p>No specific recommendations available.</p>';
    }
    
    recommendationsDiv.innerHTML = recommendationsHTML;
}

// Results Visualization
function createResultsVisualization(result, modelType) {
    const canvas = document.getElementById('results-chart');
    const ctx = canvas.getContext('2d');
    
    // Destroy existing chart
    if (currentChart) {
        currentChart.destroy();
    }
    
    let chartData = {};
    let chartOptions = {};
    
    if (modelType === 'cardiovascular') {
        chartData = createCardiovascularChart(result);
    } else if (modelType === 'breast-cancer') {
        chartData = createBreastCancerChart(result);
    } else if (modelType === 'fetal-health') {
        chartData = createFetalHealthChart(result);
    }
    
    chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Prediction Confidence'
            }
        }
    };
    
    currentChart = new Chart(ctx, {
        type: 'doughnut',
        data: chartData,
        options: chartOptions
    });
}

function createCardiovascularChart(result) {
    const riskProb = result.disease_probability || result.confidence || 0;
    const noRiskProb = 1 - riskProb;
    
    return {
        labels: ['Disease Risk', 'No Risk'],
        datasets: [{
            data: [riskProb * 100, noRiskProb * 100],
            backgroundColor: ['#e74c3c', '#27ae60'],
            borderWidth: 2,
            borderColor: '#ffffff'
        }]
    };
}

function createBreastCancerChart(result) {
    const malignantProb = result.malignancy_probability || result.confidence || 0;
    const benignProb = 1 - malignantProb;
    
    return {
        labels: ['Malignant', 'Benign'],
        datasets: [{
            data: [malignantProb * 100, benignProb * 100],
            backgroundColor: ['#e91e63', '#27ae60'],
            borderWidth: 2,
            borderColor: '#ffffff'
        }]
    };
}

function createFetalHealthChart(result) {
    const probabilities = result.class_probabilities || [0.33, 0.33, 0.34];
    
    return {
        labels: ['Normal', 'Suspect', 'Pathological'],
        datasets: [{
            data: probabilities.map(p => p * 100),
            backgroundColor: ['#27ae60', '#f39c12', '#e74c3c'],
            borderWidth: 2,
            borderColor: '#ffffff'
        }]
    };
}

// Tabs Setup (for Breast Cancer form)
function setupTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.onclick.toString().match(/showTab\('(.+?)'\)/)[1];
            showTab(tabName);
        });
    });
}

function showTab(tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => content.classList.remove('active'));
    
    // Remove active class from all buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => button.classList.remove('active'));
    
    // Show selected tab content
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Add active class to clicked button
    const clickedButton = event ? event.target : document.querySelector(`[onclick*="${tabName}"]`);
    if (clickedButton) {
        clickedButton.classList.add('active');
    }
}

// Form Validation Setup
function setupFormValidation() {
    const inputs = document.querySelectorAll('input, select');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            clearFieldError(this);
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.getAttribute('name');
    
    // Clear previous errors
    clearFieldError(field);
    
    // Check if required field is empty
    if (field.hasAttribute('required') && !value) {
        showFieldError(field, 'Bu alan gereklidir');
        return false;
    }
    
    // Validate numeric fields
    if (field.type === 'number' && value) {
        const numValue = parseFloat(value);
        const min = parseFloat(field.getAttribute('min'));
        const max = parseFloat(field.getAttribute('max'));
        
        if (isNaN(numValue)) {
            showFieldError(field, 'Lütfen geçerli bir sayı girin');
            return false;
        }
        
        if (!isNaN(min) && numValue < min) {
            showFieldError(field, `Value must be at least ${min}`);
            return false;
        }
        
        if (!isNaN(max) && numValue > max) {
            showFieldError(field, `Value must not exceed ${max}`);
            return false;
        }
    }
    
    return true;
}

function showFieldError(field, message) {
    field.classList.add('error');
    
    // Remove existing error message
    const existingError = field.parentElement.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Add new error message
    const errorElement = document.createElement('small');
    errorElement.className = 'error-message';
    errorElement.textContent = message;
    errorElement.style.color = '#e74c3c';
    field.parentElement.appendChild(errorElement);
}

function clearFieldError(field) {
    field.classList.remove('error');
    const errorMessage = field.parentElement.querySelector('.error-message');
    if (errorMessage) {
        errorMessage.remove();
    }
}

// Utility Functions
function showLoading() {
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = 'flex';
    }
}

function hideLoading() {
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = 'none';
    }
}

function showResults() {
    const resultsSection = document.getElementById('results');
    if (resultsSection) {
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
}

function hideResults() {
    const resultsSection = document.getElementById('results');
    if (resultsSection) {
        resultsSection.style.display = 'none';
    }
}

function showError(message) {
    alert('Error: ' + message);
    // TODO: Implement better error display (toast, modal, etc.)
}

function clearForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
        
        // Clear any error messages
        const errorMessages = form.querySelectorAll('.error-message');
        errorMessages.forEach(msg => msg.remove());
        
        // Clear error classes
        const errorFields = form.querySelectorAll('.error');
        errorFields.forEach(field => field.classList.remove('error'));
    }
}

// Sample Data Functions (for testing)
function loadSampleData(modelType) {
    const sampleData = {
        'cardiovascular': {
            'age': 63,
            'gender': 1,
            'chest_pain_type': 3,
            'resting_blood_pressure': 145,
            'serum_cholesterol': 233,
            'fasting_blood_sugar': 1,
            'resting_electrocardiographic_results': 0,
            'maximum_heart_rate_achieved': 150,
            'exercise_induced_angina': 0,
            'st_depression_induced_by_exercise': 2.3,
            'slope_of_the_peak_exercise_st_segment': 0,
            'number_of_major_vessels': 0,
            'thal': 1
        },
        'breast-cancer': {
            'radius_mean': 17.99, 'texture_mean': 10.38, 'perimeter_mean': 122.8,
            'area_mean': 1001, 'smoothness_mean': 0.1184, 'compactness_mean': 0.2776,
            'concavity_mean': 0.3001, 'concave_points_mean': 0.1471, 'symmetry_mean': 0.2419,
            'fractal_dimension_mean': 0.07871, 'radius_se': 1.095, 'texture_se': 0.9053,
            'perimeter_se': 8.589, 'area_se': 153.4, 'smoothness_se': 0.006399,
            'compactness_se': 0.04904, 'concavity_se': 0.05373, 'concave_points_se': 0.01587,
            'symmetry_se': 0.03003, 'fractal_dimension_se': 0.006193, 'radius_worst': 25.38,
            'texture_worst': 17.33, 'perimeter_worst': 184.6, 'area_worst': 2019,
            'smoothness_worst': 0.1622, 'compactness_worst': 0.6656, 'concavity_worst': 0.7119,
            'concave_points_worst': 0.2654, 'symmetry_worst': 0.4601, 'fractal_dimension_worst': 0.1189
        },
        'fetal-health': {
            'baseline_value': 120, 'accelerations': 0.000, 'fetal_movement': 0.0,
            'uterine_contractions': 0.000, 'light_decelerations': 0.000,
            'severe_decelerations': 0.0, 'prolongued_decelerations': 0.0,
            'abnormal_short_term_variability': 73, 'mean_value_of_short_term_variability': 0.5,
            'percentage_of_time_with_abnormal_long_term_variability': 43,
            'mean_value_of_long_term_variability': 2.4, 'histogram_width': 64,
            'histogram_min': 62, 'histogram_max': 126, 'histogram_number_of_peaks': 2,
            'histogram_number_of_zeroes': 0, 'histogram_mode': 120,
            'histogram_mean': 137, 'histogram_median': 121, 'histogram_variance': 73,
            'histogram_tendency': 1
        }
    };
    
    const data = sampleData[modelType];
    if (data) {
        const formId = `${modelType}-form`;
        const form = document.getElementById(formId);
        
        if (form) {
            Object.entries(data).forEach(([key, value]) => {
                const field = form.querySelector(`[name="${key}"]`);
                if (field) {
                    field.value = value;
                }
            });
        }
    }
}

// Export functions for global access
window.showTab = showTab;
window.clearForm = clearForm;
window.hideResults = hideResults;
window.loadSampleData = loadSampleData;
