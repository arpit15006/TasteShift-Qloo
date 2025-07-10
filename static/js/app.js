// Global state
let currentPersona = null;
let loadingModal = null;

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    
    // Setup form handlers
    document.getElementById('persona-form').addEventListener('submit', handlePersonaGeneration);
    document.getElementById('campaign-form').addEventListener('submit', handleCampaignAnalysis);
    
    // Load existing personas
    loadPersonas();
});

// Show/hide sections
function showHome() {
    document.getElementById('home-section').style.display = 'block';
    document.getElementById('personas-section').style.display = 'none';
}

function showPersonas() {
    document.getElementById('home-section').style.display = 'none';
    document.getElementById('personas-section').style.display = 'block';
    loadPersonas();
}

// Handle persona generation
async function handlePersonaGeneration(e) {
    e.preventDefault();
    
    const region = document.getElementById('region').value;
    const demographic = document.getElementById('demographic').value;
    
    if (!region || !demographic) {
        alert('Please select both region and demographic');
        return;
    }
    
    showLoading('Generating cultural persona...');
    
    try {
        const response = await fetch('/api/generate-persona', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ region, demographic })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentPersona = data.persona;
            displayPersona(data.persona);
            document.getElementById('campaign-section').style.display = 'block';
        } else {
            alert('Error: ' + (data.error || 'Failed to generate persona'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Network error. Please try again.');
    } finally {
        hideLoading();
    }
}

// Handle campaign analysis
async function handleCampaignAnalysis(e) {
    e.preventDefault();
    
    if (!currentPersona) {
        alert('Please generate a persona first');
        return;
    }
    
    const campaignBrief = document.getElementById('campaign-brief').value;
    
    if (!campaignBrief.trim()) {
        alert('Please enter a campaign brief');
        return;
    }
    
    showLoading('Analyzing campaign alignment...');
    
    try {
        const response = await fetch('/api/analyze-campaign', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                persona_id: currentPersona.id,
                campaign_brief: campaignBrief
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayAnalysis(data.analysis);
        } else {
            alert('Error: ' + (data.error || 'Failed to analyze campaign'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Network error. Please try again.');
    } finally {
        hideLoading();
    }
}

// Display persona results
function displayPersona(persona) {
    const personaContent = document.getElementById('persona-content');
    personaContent.innerHTML = `
        <div class="mb-3">
            <h5><i class="fas fa-map-marker-alt me-2"></i>${persona.region} - ${persona.demographic}</h5>
            <small class="text-muted">Generated on ${new Date(persona.created_at).toLocaleDateString()}</small>
        </div>
        <div class="persona-description">
            ${formatText(persona.persona_description)}
        </div>
    `;
    
    document.getElementById('persona-results').style.display = 'block';
    document.getElementById('persona-results').scrollIntoView({ behavior: 'smooth' });
}

// Display analysis results
function displayAnalysis(analysis) {
    const analysisContent = document.getElementById('analysis-content');
    const suggestions = JSON.parse(analysis.creative_suggestions || '[]');
    
    let suggestionsHtml = '';
    if (suggestions.length > 0) {
        suggestionsHtml = `
            <div class="row mt-4">
                <div class="col-12">
                    <h6><i class="fas fa-lightbulb me-2"></i>Creative Suggestions</h6>
                    <div class="row">
                        ${suggestions.map((suggestion, index) => `
                            <div class="col-md-4 mb-3">
                                <div class="card h-100">
                                    <div class="card-body">
                                        <h6 class="card-title text-capitalize">
                                            <i class="fas fa-${getIconForType(suggestion.type)} me-2"></i>
                                            ${suggestion.type}
                                        </h6>
                                        <p class="card-text">${suggestion.suggestion}</p>
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }
    
    analysisContent.innerHTML = `
        <div class="row">
            <div class="col-md-6 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <h3 class="display-4 ${getScoreColor(analysis.taste_shock_score)}">${analysis.taste_shock_score}</h3>
                        <h6>Taste Shock Score</h6>
                        <small class="text-muted">${getScoreDescription(analysis.taste_shock_score)}</small>
                    </div>
                </div>
            </div>
            <div class="col-md-6 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h6><i class="fas fa-clipboard me-2"></i>Campaign Brief</h6>
                        <p class="text-muted">${analysis.campaign_brief.substring(0, 150)}...</p>
                        <small class="text-muted">Analyzed on ${new Date(analysis.created_at).toLocaleDateString()}</small>
                    </div>
                </div>
            </div>
        </div>
        ${suggestionsHtml}
    `;
    
    document.getElementById('analysis-results').style.display = 'block';
    document.getElementById('analysis-results').scrollIntoView({ behavior: 'smooth' });
}

// Load personas list
async function loadPersonas() {
    try {
        const response = await fetch('/api/personas');
        const data = await response.json();
        
        if (data.personas) {
            displayPersonasList(data.personas);
        }
    } catch (error) {
        console.error('Error loading personas:', error);
    }
}

// Display personas list
function displayPersonasList(personas) {
    const personasList = document.getElementById('personas-list');
    
    if (personas.length === 0) {
        personasList.innerHTML = '<div class="col-12"><p class="text-muted">No personas generated yet.</p></div>';
        return;
    }
    
    personasList.innerHTML = personas.map(persona => `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card h-100">
                <div class="card-body">
                    <h6 class="card-title">
                        <i class="fas fa-user me-2"></i>
                        ${persona.region} - ${persona.demographic}
                    </h6>
                    <p class="card-text">${persona.persona_description.substring(0, 100)}...</p>
                    <small class="text-muted">
                        <i class="fas fa-calendar me-1"></i>
                        ${new Date(persona.created_at).toLocaleDateString()}
                    </small>
                </div>
                <div class="card-footer">
                    <button class="btn btn-sm btn-outline-primary" onclick="viewPersona(${persona.id})">
                        <i class="fas fa-eye me-1"></i>View Details
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// View persona details
function viewPersona(personaId) {
    // Switch to home view and populate with selected persona
    showHome();
    // Implementation to load specific persona details would go here
}

// Utility functions
function formatText(text) {
    return text.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
}

function getScoreColor(score) {
    if (score <= 30) return 'text-success';
    if (score <= 60) return 'text-warning';
    return 'text-danger';
}

function getScoreDescription(score) {
    if (score <= 30) return 'Highly aligned with cultural preferences';
    if (score <= 60) return 'Moderately aligned, some cultural disruption';
    return 'Highly disruptive, challenges cultural norms';
}

function getIconForType(type) {
    const icons = {
        'tagline': 'tag',
        'concept': 'lightbulb',
        'visual': 'image',
        'default': 'star'
    };
    return icons[type] || icons.default;
}

function showLoading(text) {
    document.getElementById('loading-text').textContent = text;
    document.getElementById('loading-detail').innerHTML = '<i class="fas fa-info-circle me-1"></i>Fetching cultural data from Qloo API...';
    
    // Simulate progress animation
    const progressBar = document.getElementById('loading-progress');
    progressBar.style.width = '0%';
    
    setTimeout(() => {
        progressBar.style.width = '30%';
        document.getElementById('loading-detail').innerHTML = '<i class="fas fa-brain me-1"></i>Analyzing cultural patterns with AI...';
    }, 1000);
    
    setTimeout(() => {
        progressBar.style.width = '70%';
        document.getElementById('loading-detail').innerHTML = '<i class="fas fa-user me-1"></i>Generating detailed persona...';
    }, 3000);
    
    setTimeout(() => {
        progressBar.style.width = '95%';
        document.getElementById('loading-detail').innerHTML = '<i class="fas fa-check me-1"></i>Finalizing results...';
    }, 8000);
    
    loadingModal.show();
}

function hideLoading() {
    const progressBar = document.getElementById('loading-progress');
    progressBar.style.width = '100%';
    setTimeout(() => {
        loadingModal.hide();
        progressBar.style.width = '0%';
    }, 500);
}
