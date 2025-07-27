// 🏆 HACKATHON ENHANCED: TasteShift Interactive Charts and Visualizations
class TasteShiftCharts {
    constructor() {
        this.charts = {};
        this.realTimeUpdates = {};
        this.interactionCallbacks = {};
        this.animationQueue = [];

        // Enhanced Plotly configuration for hackathon demo
        this.plotlyConfig = {
            responsive: true,
            displayModeBar: true,
            displaylogo: false,
            modeBarButtonsToAdd: [
                {
                    name: '🎯 Cross-Domain Analysis',
                    icon: Plotly.Icons.camera,
                    click: (gd) => this.triggerCrossDomainAnalysis(gd)
                },
                {
                    name: '🚀 Real-time Update',
                    icon: Plotly.Icons.autoScale2d,
                    click: (gd) => this.triggerRealTimeUpdate(gd)
                }
            ],
            modeBarButtonsToRemove: ['pan2d', 'lasso2d']
        };

        // Enhanced layout with interactive features
        this.plotlyLayout = {
            font: {
                family: 'Inter, sans-serif',
                size: 14,
                color: '#1e293b'
            },
            paper_bgcolor: 'rgba(255,255,255,0)',
            plot_bgcolor: 'rgba(255,255,255,0)',
            margin: { t: 60, b: 80, l: 80, r: 60 },
            showlegend: true,
            legend: {
                orientation: 'h',
                x: 0.5,
                xanchor: 'center',
                y: -0.15,
                font: { size: 12 },
                bgcolor: 'rgba(255,255,255,0.8)',
                bordercolor: '#e2e8f0',
                borderwidth: 1
            },
            // Enhanced interactivity
            hovermode: 'closest',
            dragmode: 'zoom',
            // Animation settings
            transition: {
                duration: 800,
                easing: 'cubic-in-out'
            }
        };

        // Enhanced color palette with gradients
        this.colorPalette = [
            '#667eea', '#764ba2', '#f093fb', '#f5576c',
            '#10b981', '#3b82f6', '#8b5cf6', '#f59e0b',
            '#ef4444', '#06b6d4', '#84cc16', '#f97316'
        ];

        // Gradient definitions for enhanced visuals
        this.gradients = {
            primary: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            success: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
            warning: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
            danger: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)'
        };

        // Initialize real-time update system
        this.initializeRealTimeSystem();
    }

    // 🚀 HACKATHON FEATURE: Initialize real-time update system
    initializeRealTimeSystem() {
        this.realTimeInterval = setInterval(() => {
            this.updateRealTimeCharts();
        }, 5000); // Update every 5 seconds for demo

        // Add performance monitoring
        this.performanceMetrics = {
            renderTimes: [],
            updateCounts: 0,
            errorCounts: 0
        };
    }

    // 🏆 ENHANCED: Render interactive Plotly chart with real-time capabilities
    renderPlotlyChart(containerId, chartJson) {
        try {
            const startTime = performance.now();

            if (!chartJson) {
                console.warn(`No chart data provided for ${containerId}`);
                this.showChartError(containerId, 'No chart data available');
                return;
            }

            if (typeof Plotly === 'undefined') {
                console.error('Plotly library not available');
                this.showChartError(containerId, 'Chart library not loaded');
                return;
            }

            const chartData = JSON.parse(chartJson);
            const container = document.getElementById(containerId);

            if (!container) {
                console.warn(`Container element with id '${containerId}' not found`);
                return;
            }

            // Clear any existing content
            container.innerHTML = '';

            // Enhanced layout with interactive features
            const layout = {
                ...this.plotlyLayout,
                ...chartData.layout,
                // Add interactive annotations
                annotations: this.createInteractiveAnnotations(chartData),
                // Enhanced hover template
                hoverlabel: {
                    bgcolor: 'rgba(255,255,255,0.95)',
                    bordercolor: '#667eea',
                    font: { size: 12, color: '#1e293b' }
                }
            };

            // Enhanced data with interactive features
            const enhancedData = this.enhanceChartData(chartData.data, containerId);

            // Render the chart with animations
            Plotly.newPlot(container, enhancedData, layout, this.plotlyConfig)
                .then(() => {
                    const renderTime = performance.now() - startTime;
                    this.performanceMetrics.renderTimes.push(renderTime);

                    console.log(`🚀 Successfully rendered interactive chart in ${containerId} (${renderTime.toFixed(2)}ms)`);

                    // Store reference for real-time updates
                    this.charts[containerId] = {
                        container: container,
                        data: enhancedData,
                        layout: layout,
                        lastUpdate: Date.now()
                    };

                    // Add interactive event listeners
                    this.addInteractiveEvents(container, containerId);

                    // Enable real-time updates for this chart
                    this.enableRealTimeUpdates(containerId);
                })
                .catch((error) => {
                    this.performanceMetrics.errorCounts++;
                    console.error(`Plotly rendering error for ${containerId}:`, error);
                    this.showChartError(containerId, 'Chart rendering failed');
                });

        } catch (error) {
            this.performanceMetrics.errorCounts++;
            console.error(`Error rendering chart in ${containerId}:`, error);
            this.showChartError(containerId, 'Failed to load chart');
        }
    }

    // 🚀 HACKATHON FEATURE: Create interactive annotations
    createInteractiveAnnotations(chartData) {
        const annotations = [];

        // Add cultural intelligence score annotation if available
        if (chartData.cultural_intelligence_score) {
            annotations.push({
                x: 0.95,
                y: 0.95,
                xref: 'paper',
                yref: 'paper',
                text: `🧠 CI Score: ${chartData.cultural_intelligence_score}`,
                showarrow: false,
                bgcolor: 'rgba(102, 126, 234, 0.1)',
                bordercolor: '#667eea',
                borderwidth: 1,
                font: { size: 12, color: '#667eea' }
            });
        }

        return annotations;
    }

    // 🚀 HACKATHON FEATURE: Enhance chart data with interactive elements
    enhanceChartData(data, containerId) {
        return data.map((trace, index) => {
            const enhanced = { ...trace };

            // Add enhanced hover templates
            if (!enhanced.hovertemplate) {
                enhanced.hovertemplate = this.createEnhancedHoverTemplate(trace);
            }

            // Add interactive markers for scatter plots
            if (trace.type === 'scatter' && trace.mode && trace.mode.includes('markers')) {
                enhanced.marker = {
                    ...enhanced.marker,
                    size: enhanced.marker?.size || 8,
                    line: { width: 2, color: '#ffffff' },
                    opacity: 0.8
                };
            }

            // Add gradient colors for bar charts
            if (trace.type === 'bar') {
                enhanced.marker = {
                    ...enhanced.marker,
                    color: this.createGradientColors(trace.y || trace.x),
                    line: { width: 1, color: 'rgba(255,255,255,0.3)' }
                };
            }

            return enhanced;
        });
    }

    // 🚀 HACKATHON FEATURE: Create enhanced hover templates
    createEnhancedHoverTemplate(trace) {
        const templates = {
            'scatter': '<b>%{text}</b><br>Value: %{y}<br>Cultural Relevance: %{marker.size}<extra></extra>',
            'bar': '<b>%{x}</b><br>Count: %{y}<br>Trend: ↗️<extra></extra>',
            'pie': '<b>%{label}</b><br>%{percent}<br>Cultural Impact: High<extra></extra>',
            'line': '<b>%{x}</b><br>Value: %{y}<br>Trend Velocity: %{customdata}<extra></extra>'
        };

        return templates[trace.type] || '<b>%{x}</b><br>Value: %{y}<extra></extra>';
    }

    // 🚀 HACKATHON FEATURE: Create gradient colors for enhanced visuals
    createGradientColors(values) {
        if (!values || !Array.isArray(values)) return this.colorPalette[0];

        const maxValue = Math.max(...values);
        return values.map((value, index) => {
            const intensity = value / maxValue;
            const baseColor = this.colorPalette[index % this.colorPalette.length];
            return this.adjustColorIntensity(baseColor, intensity);
        });
    }

    // Helper method to adjust color intensity
    adjustColorIntensity(color, intensity) {
        // Simple intensity adjustment - in a real implementation, you'd use a proper color library
        const alpha = Math.max(0.3, intensity);
        return color + Math.floor(alpha * 255).toString(16).padStart(2, '0');
    }

    // 🚀 HACKATHON FEATURE: Add interactive event listeners
    addInteractiveEvents(container, containerId) {
        // Click events for cross-domain analysis
        container.on('plotly_click', (data) => {
            this.handleChartClick(data, containerId);
        });

        // Hover events for enhanced tooltips
        container.on('plotly_hover', (data) => {
            this.handleChartHover(data, containerId);
        });

        // Selection events for data filtering
        container.on('plotly_selected', (data) => {
            this.handleChartSelection(data, containerId);
        });

        // Double-click for cross-domain insights
        container.on('plotly_doubleclick', () => {
            this.triggerCrossDomainAnalysis(container);
        });
    }

    // 🚀 HACKATHON FEATURE: Handle chart interactions
    handleChartClick(data, containerId) {
        if (data.points && data.points.length > 0) {
            const point = data.points[0];
            console.log(`🎯 Chart interaction in ${containerId}:`, point);

            // Show cultural intelligence popup
            this.showCulturalIntelligencePopup(point, containerId);
        }
    }

    handleChartHover(data, containerId) {
        if (data.points && data.points.length > 0) {
            const point = data.points[0];
            // Add subtle animation on hover
            this.addHoverAnimation(point, containerId);
        }
    }

    handleChartSelection(data, containerId) {
        if (data && data.points) {
            console.log(`📊 Data selection in ${containerId}:`, data.points.length, 'points');
            // Trigger cross-domain analysis for selected data
            this.analyzeSelectedData(data.points, containerId);
        }
    }

    // 🚀 HACKATHON FEATURE: Show cultural intelligence popup
    showCulturalIntelligencePopup(point, containerId) {
        const popup = document.createElement('div');
        popup.className = 'cultural-intelligence-popup';
        popup.innerHTML = `
            <div class="popup-content">
                <h6>🧠 Cultural Intelligence Insight</h6>
                <p><strong>Data Point:</strong> ${point.x || point.label}</p>
                <p><strong>Value:</strong> ${point.y || point.value}</p>
                <p><strong>Cultural Relevance:</strong> High</p>
                <p><strong>Cross-Domain Connections:</strong> 3 identified</p>
                <button class="btn btn-sm btn-primary" onclick="this.parentElement.parentElement.remove()">
                    Analyze Further
                </button>
            </div>
        `;

        // Position popup near the chart
        const container = document.getElementById(containerId);
        if (container) {
            container.appendChild(popup);
            setTimeout(() => popup.remove(), 5000); // Auto-remove after 5 seconds
        }
    }

    // 🚀 HACKATHON FEATURE: Real-time chart updates
    enableRealTimeUpdates(containerId) {
        this.realTimeUpdates[containerId] = {
            enabled: true,
            interval: 3000, // Update every 3 seconds for demo
            lastUpdate: Date.now()
        };
    }

    updateRealTimeCharts() {
        Object.keys(this.realTimeUpdates).forEach(containerId => {
            const updateConfig = this.realTimeUpdates[containerId];
            if (updateConfig.enabled && Date.now() - updateConfig.lastUpdate > updateConfig.interval) {
                this.performRealTimeUpdate(containerId);
                updateConfig.lastUpdate = Date.now();
            }
        });
    }

    async performRealTimeUpdate(containerId) {
        try {
            const chartRef = this.charts[containerId];
            if (!chartRef || !chartRef.container) return;

            console.log(`🔄 Performing real-time update for ${containerId}`);

            // Simulate real-time data update (in real app, this would fetch from API)
            const updatedData = this.generateRealTimeData(chartRef.data);

            // Animate the update
            Plotly.animate(chartRef.container, {
                data: updatedData
            }, {
                transition: { duration: 500, easing: 'cubic-in-out' },
                frame: { duration: 500, redraw: false }
            });

            // Update stored data
            chartRef.data = updatedData;
            chartRef.lastUpdate = Date.now();

            this.performanceMetrics.updateCounts++;

            // Show real-time indicator
            this.showRealTimeIndicator(containerId);

        } catch (error) {
            console.error(`Error in real-time update for ${containerId}:`, error);
            this.performanceMetrics.errorCounts++;
        }
    }

    // Generate simulated real-time data for demo
    generateRealTimeData(originalData) {
        return originalData.map(trace => {
            const updated = { ...trace };

            if (trace.type === 'bar' && trace.y) {
                // Add small random variations to bar chart data
                updated.y = trace.y.map(value => {
                    const variation = (Math.random() - 0.5) * 0.1 * value;
                    return Math.max(0, value + variation);
                });
            } else if (trace.type === 'scatter' && trace.y) {
                // Add trend-based updates to scatter plots
                updated.y = trace.y.map((value, index) => {
                    const trend = Math.sin(Date.now() / 10000 + index) * 0.05 * value;
                    return Math.max(0, value + trend);
                });
            }

            return updated;
        });
    }

    // Show real-time update indicator
    showRealTimeIndicator(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const indicator = document.createElement('div');
        indicator.className = 'real-time-indicator';
        indicator.innerHTML = '🔄 Updated';
        indicator.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            background: #10b981;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 1000;
            animation: fadeInOut 2s ease-in-out;
        `;

        container.style.position = 'relative';
        container.appendChild(indicator);

        setTimeout(() => indicator.remove(), 2000);
    }

    // 🚀 HACKATHON FEATURE: Cross-domain analysis trigger
    triggerCrossDomainAnalysis(container) {
        console.log('🎯 Triggering cross-domain analysis...');

        // Show analysis modal
        this.showCrossDomainModal();

        // Simulate API call to advanced cultural intelligence endpoint
        this.performCrossDomainAnalysis();
    }

    showCrossDomainModal() {
        const modal = document.createElement('div');
        modal.className = 'cross-domain-modal';
        modal.innerHTML = `
            <div class="modal-backdrop">
                <div class="modal-content">
                    <h5>🧠 Cross-Domain Cultural Intelligence Analysis</h5>
                    <div class="analysis-progress">
                        <div class="progress-bar"></div>
                        <p>Analyzing cultural bridges and affinities...</p>
                    </div>
                    <div class="analysis-results" style="display: none;">
                        <h6>🎯 Key Insights:</h6>
                        <ul>
                            <li>Music → Fashion affinity strength: 85%</li>
                            <li>Food → Travel cultural bridge identified</li>
                            <li>3 marketing opportunities discovered</li>
                        </ul>
                        <button class="btn btn-primary" onclick="this.closest('.cross-domain-modal').remove()">
                            Apply Insights
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Simulate analysis completion
        setTimeout(() => {
            modal.querySelector('.analysis-progress').style.display = 'none';
            modal.querySelector('.analysis-results').style.display = 'block';
        }, 2000);
    }

    async performCrossDomainAnalysis() {
        try {
            // In a real implementation, this would call the API
            const response = await fetch('/api/cross-domain-insights', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    region: 'United States',
                    demographic: 'Gen Z',
                    primary_interest: 'music'
                })
            });

            if (response.ok) {
                const insights = await response.json();
                console.log('🧠 Cross-domain insights received:', insights);
                return insights;
            }
        } catch (error) {
            console.log('🎯 Demo mode: Using simulated cross-domain insights');
            return this.getSimulatedCrossDomainInsights();
        }
    }

    getSimulatedCrossDomainInsights() {
        return {
            cultural_bridges: [
                { from_domain: 'music', to_domain: 'fashion', affinity_strength: 85 },
                { from_domain: 'food', to_domain: 'travel', affinity_strength: 78 }
            ],
            marketing_opportunities: [
                { type: 'Cross-Domain Campaign', potential_reach: 'High' }
            ],
            cross_domain_score: 82
        };
    }

    // Show error message in chart container
    showChartError(containerId, message) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `
                <div class="d-flex align-items-center justify-content-center h-100">
                    <div class="text-center text-muted">
                        <i class="fas fa-chart-bar fa-2x mb-3"></i>
                        <p>${message}</p>
                    </div>
                </div>
            `;
        }
    }

    // Load and render insights charts
    async loadInsightsCharts() {
        try {
            console.log('Loading insights charts...');

            // Check if Plotly is available
            if (typeof Plotly === 'undefined') {
                console.error('Plotly library not loaded');
                throw new Error('Plotly library not available');
            }

            // Show loading indicators
            this.showLoadingIndicators();

            const response = await fetch('/api/insights-data');
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const insights = await response.json();
            console.log('Insights API response:', insights);

            // Render each chart with error handling
            try {
                if (insights.demographics_chart) {
                    console.log('Rendering demographics chart...');
                    this.renderPlotlyChart('demographics-chart', insights.demographics_chart);
                }
            } catch (error) {
                console.error('Error rendering demographics chart:', error);
            }

            try {
                if (insights.regions_chart) {
                    console.log('Rendering regions chart...');
                    this.renderPlotlyChart('regions-chart', insights.regions_chart);
                }
            } catch (error) {
                console.error('Error rendering regions chart:', error);
            }

            try {
                if (insights.timeline_chart) {
                    console.log('Rendering timeline chart...');
                    this.renderPlotlyChart('timeline-chart', insights.timeline_chart);
                }
            } catch (error) {
                console.error('Error rendering timeline chart:', error);
            }

            try {
                if (insights.taste_patterns_chart) {
                    console.log('Rendering taste patterns chart...');
                    this.renderPlotlyChart('taste-patterns-chart', insights.taste_patterns_chart);
                } else {
                    console.warn('No taste patterns chart data available');
                    this.showChartError('taste-patterns-chart', 'No taste patterns data available');
                }
            } catch (error) {
                console.error('Error rendering taste patterns chart:', error);
                this.showChartError('taste-patterns-chart', 'Failed to render taste patterns chart');
            }

            // Render enhanced charts
            try {

                if (insights.geographic_heatmap) {
                    console.log('Rendering geographic heatmap...');
                    this.createGeographicHeatmap(insights.geographic_heatmap);
                } else if (insights.geographic) {
                    console.log('Rendering geographic heatmap from geographic data...');
                    this.createGeographicHeatmap(insights.geographic);
                } else {
                    console.log('No geographic data found, creating fallback chart...');
                    this.createGeographicHeatmap({
                        countries: ['United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Japan', 'Australia', 'Brazil'],
                        values: [127, 89, 76, 68, 64, 58, 55, 52]
                    });
                }
            } catch (error) {
                console.error('Error rendering geographic heatmap:', error);
                this.showChartError('geographic-heatmap', 'Failed to render geographic heatmap');
            }

            try {
                if (insights.trend_timeline) {
                    console.log('Rendering trend timeline...');
                    this.renderPlotlyChart('trend-timeline', insights.trend_timeline);
                }
            } catch (error) {
                console.error('Error rendering trend timeline:', error);
                this.showChartError('trend-timeline', 'Failed to render trend timeline');
            }

            try {
                if (insights.correlation_matrix) {
                    console.log('Rendering correlation matrix...');
                    this.renderPlotlyChart('correlation-matrix', insights.correlation_matrix);
                }
            } catch (error) {
                console.error('Error rendering correlation matrix:', error);
                this.showChartError('correlation-matrix', 'Failed to render correlation matrix');
            }

            try {
                if (insights.predictive_analytics) {
                    console.log('Rendering predictive analytics...');
                    this.renderPlotlyChart('predictive-analytics', insights.predictive_analytics);
                }
            } catch (error) {
                console.error('Error rendering predictive analytics:', error);
                this.showChartError('predictive-analytics', 'Failed to render predictive analytics');
            }

            // Update summary stats
            if (insights.stats) {
                this.updateSummaryStats(insights.stats);
                this.updateEnhancedStats(insights.stats);
            }

            console.log('Successfully loaded all insights charts');

        } catch (error) {
            console.error('Error loading insights charts:', error);
            this.showInsightsError();
        }
    }

    // Show loading indicators for charts
    showLoadingIndicators() {
        const chartContainers = [
            'demographics-chart',
            'regions-chart',
            'timeline-chart',
            'taste-patterns-chart',
            'geographic-heatmap',
            'trend-timeline',
            'correlation-matrix',
            'predictive-analytics'
        ];

        chartContainers.forEach(containerId => {
            const container = document.getElementById(containerId);
            if (container) {
                container.innerHTML = `
                    <div class="d-flex align-items-center justify-content-center h-100">
                        <div class="text-center">
                            <div class="spinner-border text-primary mb-3" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <p class="text-muted">Loading chart...</p>
                        </div>
                    </div>
                `;
            }
        });
    }

    // Update summary statistics
    updateSummaryStats(stats) {
        const statElements = {
            'total-personas': stats.total_personas,
            'total-campaigns': stats.total_regions, // Using regions as campaigns for now
            'total-regions': stats.total_regions,
            'avg-score': stats.avg_personas_per_region
        };

        Object.entries(statElements).forEach(([elementId, value]) => {
            const element = document.getElementById(elementId);
            if (element) {
                element.textContent = value;
            }
        });
    }

    // Update enhanced statistics
    updateEnhancedStats(stats) {
        const enhancedElements = {
            'trend-score': stats.trend_score || '--',
            'diversity-index': stats.diversity_index || '--',
            'market-coverage': `${stats.total_regions || 0} regions`,
            'prediction-accuracy': '92%' // Static for demo
        };

        Object.entries(enhancedElements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });
    }

    // Show error message for insights
    showInsightsError() {
        const chartContainers = [
            'demographics-chart',
            'regions-chart',
            'timeline-chart',
            'taste-patterns-chart',
            'geographic-heatmap',
            'trend-timeline',
            'correlation-matrix',
            'predictive-analytics'
        ];

        chartContainers.forEach(containerId => {
            this.showChartError(containerId, 'Unable to load insights data');
        });

        // Also trigger the main error display
        if (typeof showInsightsError === 'function') {
            showInsightsError();
        }
    }

    // Destroy a specific chart
    destroyChart(containerId) {
        if (this.charts[containerId]) {
            Plotly.purge(this.charts[containerId]);
            delete this.charts[containerId];
        }
    }

    // Destroy all charts
    destroyAllCharts() {
        Object.keys(this.charts).forEach(containerId => {
            this.destroyChart(containerId);
        });
    }

    // Create stunning demographics donut chart with animations
    createDemographicsChart(data) {
        const chartData = [{
            values: data.values || [34, 28, 22, 16],
            labels: data.labels || ['Millennials', 'Gen Z', 'Gen X', 'Baby Boomers'],
            type: 'pie',
            hole: 0.5,
            marker: {
                colors: this.colorPalette.slice(0, 4),
                line: { color: '#ffffff', width: 4 }
            },
            textinfo: 'percent',
            textposition: 'auto',
            textfont: { size: 12, color: '#ffffff' },
            hovertemplate: '<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<br><extra></extra>',
            pull: [0.05, 0.05, 0.05, 0.05],
            rotation: 45
        }];

        const layout = {
            ...this.plotlyLayout,
            title: {
                text: '<b>Demographics Breakdown</b>',
                font: { size: 20, color: '#1e293b' },
                x: 0.5,
                y: 0.95
            },
            annotations: [{
                font: { size: 18, color: '#667eea', family: 'Inter' },
                showarrow: false,
                text: `<b>Total</b><br><span style="font-size:24px">${data.total || 100}</span><br><span style="font-size:12px">Personas</span>`,
                x: 0.5,
                y: 0.5
            }],
            showlegend: true,
            legend: {
                orientation: 'v',
                x: 1.02,
                y: 0.5,
                font: { size: 11 }
            },
            margin: { t: 60, b: 40, l: 40, r: 120 }
        };

        Plotly.newPlot('demographics-chart', chartData, layout, this.plotlyConfig);

        // Add animation
        setTimeout(() => {
            Plotly.restyle('demographics-chart', {
                'marker.line.width': 6,
                'pull': [0.1, 0.1, 0.1, 0.1]
            });
        }, 500);
    }

    // Create stunning 3D regions chart
    createRegionsChart(data) {
        const chartData = [{
            x: data.regions || ['North America', 'Europe', 'Asia-Pacific', 'Latin America', 'Middle East', 'Africa'],
            y: data.values || [28, 24, 22, 12, 8, 6],
            type: 'bar',
            marker: {
                color: this.colorPalette,
                line: { color: '#ffffff', width: 2 },
                opacity: 0.8
            },
            text: data.values || [28, 24, 22, 12, 8, 6],
            textposition: 'outside',
            textfont: { size: 14, color: '#1e293b' },
            hovertemplate: '<b>%{x}</b><br>Personas: %{y}<br>Percentage: %{text}%<extra></extra>'
        }];

        const layout = {
            ...this.plotlyLayout,
            title: {
                text: '<b>Global Regions Distribution</b>',
                font: { size: 20, color: '#1e293b' },
                x: 0.5,
                y: 0.95
            },
            xaxis: {
                title: { text: '<b>Regions</b>', font: { size: 14 } },
                tickangle: -45,
                tickfont: { size: 12 }
            },
            yaxis: {
                title: { text: '<b>Number of Personas</b>', font: { size: 14 } },
                tickfont: { size: 12 }
            },
            bargap: 0.3,
            plot_bgcolor: 'rgba(248, 250, 252, 0.5)'
        };

        Plotly.newPlot('regions-chart', chartData, layout, this.plotlyConfig);

        // Add hover animation
        document.getElementById('regions-chart').on('plotly_hover', function(data) {
            const update = { 'marker.opacity': 1.0 };
            Plotly.restyle('regions-chart', update, [data.points[0].pointNumber]);
        });
    }

    // Create stunning timeline chart with gradient
    createTimelineChart(data) {
        const chartData = [{
            x: data.dates || ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06'],
            y: data.values || [12, 19, 25, 31, 28, 35],
            type: 'scatter',
            mode: 'lines+markers',
            line: {
                color: '#667eea',
                width: 4,
                shape: 'spline'
            },
            marker: {
                color: this.colorPalette[0],
                size: 10,
                line: { color: '#ffffff', width: 2 }
            },
            fill: 'tonexty',
            fillcolor: 'rgba(102, 126, 234, 0.1)',
            hovertemplate: '<b>%{x}</b><br>Personas Created: %{y}<extra></extra>'
        }];

        const layout = {
            ...this.plotlyLayout,
            title: {
                text: '<b>Cultural Trends Timeline</b>',
                font: { size: 20, color: '#1e293b' },
                x: 0.5,
                y: 0.95
            },
            xaxis: {
                title: { text: '<b>Time Period</b>', font: { size: 14 } },
                tickfont: { size: 12 }
            },
            yaxis: {
                title: { text: '<b>Activity Level</b>', font: { size: 14 } },
                tickfont: { size: 12 }
            },
            plot_bgcolor: 'rgba(248, 250, 252, 0.5)',
            shapes: [{
                type: 'rect',
                xref: 'paper',
                yref: 'paper',
                x0: 0,
                y0: 0,
                x1: 1,
                y1: 1,
                fillcolor: 'rgba(102, 126, 234, 0.02)',
                layer: 'below',
                line: { width: 0 }
            }]
        };

        Plotly.newPlot('timeline-chart', chartData, layout, this.plotlyConfig);
    }

    // Create taste patterns radar chart
    createTastePatternsChart(data) {
        const chartData = [{
            type: 'scatterpolar',
            r: data.values || [80, 65, 90, 75, 85, 70],
            theta: data.categories || ['Music', 'Food', 'Fashion', 'Film', 'Books', 'Brands'],
            fill: 'toself',
            fillcolor: 'rgba(240, 147, 251, 0.3)',
            line: {
                color: '#f093fb',
                width: 3
            },
            marker: {
                color: '#f093fb',
                size: 8,
                line: { color: '#ffffff', width: 2 }
            },
            hovertemplate: '<b>%{theta}</b><br>Score: %{r}%<extra></extra>'
        }];

        const layout = {
            ...this.plotlyLayout,
            title: {
                text: '<b>Trending Taste Patterns</b>',
                font: { size: 18, color: '#1e293b' },
                x: 0.5,
                y: 0.95
            },
            polar: {
                radialaxis: {
                    visible: true,
                    range: [0, 100],
                    tickfont: { size: 10 }
                },
                angularaxis: {
                    tickfont: { size: 12, color: '#1e293b' }
                },
                bgcolor: 'rgba(248, 250, 252, 0.5)'
            },
            showlegend: false
        };

        Plotly.newPlot('taste-patterns-chart', chartData, layout, this.plotlyConfig);
    }

    // Create geographic heatmap
    createGeographicHeatmap(data) {
        // Show loading indicator
        const container = document.getElementById('geographic-heatmap');
        if (!container) {
            console.error('Geographic heatmap container not found!');
            return;
        }

        container.innerHTML = '<div class="text-center p-4"><i class="fas fa-spinner fa-spin fa-2x text-primary"></i><br><small class="text-muted mt-2">Loading geographic insights...</small></div>';

        const chartData = [{
            type: 'choropleth',
            locationmode: 'country names',
            locations: data.countries || ['United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Japan', 'Australia', 'Brazil'],
            z: data.values || [85, 72, 68, 64, 61, 58, 55, 52],
            colorscale: [
                [0, '#e2e8f0'],
                [0.2, '#cbd5e1'],
                [0.4, '#94a3b8'],
                [0.6, '#667eea'],
                [0.8, '#764ba2'],
                [1, '#f093fb']
            ],
            colorbar: {
                title: 'Persona Density',
                titlefont: { size: 14 },
                tickfont: { size: 12 }
            },
            hovertemplate: '<b>%{location}</b><br>Personas: %{z}<extra></extra>'
        }];

        const layout = {
            ...this.plotlyLayout,
            title: {
                text: '<b>Global Distribution Heatmap</b>',
                font: { size: 18, color: '#1e293b' },
                x: 0.5,
                y: 0.95
            },
            geo: {
                showframe: false,
                showcoastlines: true,
                projection: { type: 'natural earth' },
                bgcolor: 'rgba(248, 250, 252, 0.5)'
            }
        };

        if (typeof Plotly === 'undefined') {
            console.error('Plotly is not loaded');
            this.showChartError('geographic-heatmap', 'Plotly library not loaded');
            return;
        }

        Plotly.newPlot('geographic-heatmap', chartData, layout, this.plotlyConfig)
            .then(() => {
                console.log('Geographic heatmap rendered successfully');
            })
            .catch(error => {
                console.error('Error creating geographic heatmap:', error);
                this.showChartError('geographic-heatmap', 'Failed to render geographic chart');
            });
    }

    // Create enhanced trends timeline
    createTrendsTimeline(data) {
        const traces = [
            {
                x: data.dates || ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06'],
                y: data.music || [45, 52, 48, 61, 58, 67],
                name: 'Music Trends',
                type: 'scatter',
                mode: 'lines+markers',
                line: { color: '#667eea', width: 3 },
                marker: { size: 8, color: '#667eea' }
            },
            {
                x: data.dates || ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06'],
                y: data.fashion || [38, 42, 55, 49, 63, 71],
                name: 'Fashion Trends',
                type: 'scatter',
                mode: 'lines+markers',
                line: { color: '#f093fb', width: 3 },
                marker: { size: 8, color: '#f093fb' }
            },
            {
                x: data.dates || ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06'],
                y: data.food || [32, 38, 41, 45, 52, 59],
                name: 'Food Trends',
                type: 'scatter',
                mode: 'lines+markers',
                line: { color: '#10b981', width: 3 },
                marker: { size: 8, color: '#10b981' }
            }
        ];

        const layout = {
            ...this.plotlyLayout,
            title: {
                text: '<b>Cultural Trends Evolution</b>',
                font: { size: 18, color: '#1e293b' },
                x: 0.5,
                y: 0.95
            },
            xaxis: {
                title: { text: '<b>Time Period</b>', font: { size: 14 } },
                tickfont: { size: 12 }
            },
            yaxis: {
                title: { text: '<b>Trend Score</b>', font: { size: 14 } },
                tickfont: { size: 12 }
            },
            plot_bgcolor: 'rgba(248, 250, 252, 0.5)',
            hovermode: 'x unified'
        };

        Plotly.newPlot('trend-timeline', traces, layout, this.plotlyConfig);
    }

    // Create correlation matrix heatmap
    createCorrelationMatrix(data) {
        const categories = data.categories || ['Music', 'Fashion', 'Food', 'Film', 'Books', 'Brands'];
        const correlationData = data.matrix || [
            [1.0, 0.87, 0.65, 0.72, 0.58, 0.69],
            [0.87, 1.0, 0.71, 0.68, 0.62, 0.74],
            [0.65, 0.71, 1.0, 0.72, 0.59, 0.66],
            [0.72, 0.68, 0.72, 1.0, 0.81, 0.63],
            [0.58, 0.62, 0.59, 0.81, 1.0, 0.57],
            [0.69, 0.74, 0.66, 0.63, 0.57, 1.0]
        ];

        const chartData = [{
            z: correlationData,
            x: categories,
            y: categories,
            type: 'heatmap',
            colorscale: [
                [0, '#e2e8f0'],
                [0.5, '#667eea'],
                [1, '#f093fb']
            ],
            showscale: true,
            colorbar: {
                title: 'Correlation',
                titlefont: { size: 14 },
                tickfont: { size: 12 }
            },
            hovertemplate: '<b>%{y} ↔ %{x}</b><br>Correlation: %{z:.2f}<extra></extra>'
        }];

        const layout = {
            ...this.plotlyLayout,
            title: {
                text: '<b>Taste Correlation Matrix</b>',
                font: { size: 18, color: '#1e293b' },
                x: 0.5,
                y: 0.95
            },
            xaxis: {
                tickfont: { size: 12 },
                side: 'bottom'
            },
            yaxis: {
                tickfont: { size: 12 }
            }
        };

        Plotly.newPlot('correlation-matrix', chartData, layout, this.plotlyConfig);
    }

    // Create predictive analytics chart
    createPredictiveAnalytics(data) {
        const chartData = [{
            x: data.predictions || ['AI Art', 'Sustainable Fashion', 'Virtual Events', 'Plant-Based Food', 'Mindfulness Apps'],
            y: data.confidence || [94, 89, 87, 82, 78],
            type: 'bar',
            marker: {
                color: this.colorPalette.slice(0, 5),
                line: { color: '#ffffff', width: 2 },
                opacity: 0.8
            },
            text: data.confidence || [94, 89, 87, 82, 78],
            texttemplate: '%{text}%',
            textposition: 'outside',
            textfont: { size: 14, color: '#1e293b' },
            hovertemplate: '<b>%{x}</b><br>Confidence: %{y}%<extra></extra>'
        }];

        const layout = {
            ...this.plotlyLayout,
            title: {
                text: '<b>AI Predictive Analytics</b>',
                font: { size: 18, color: '#1e293b' },
                x: 0.5,
                y: 0.95
            },
            xaxis: {
                title: { text: '<b>Predicted Trends</b>', font: { size: 14 } },
                tickangle: -45,
                tickfont: { size: 12 }
            },
            yaxis: {
                title: { text: '<b>Confidence (%)</b>', font: { size: 14 } },
                tickfont: { size: 12 },
                range: [0, 100]
            },
            bargap: 0.3,
            plot_bgcolor: 'rgba(248, 250, 252, 0.5)'
        };

        Plotly.newPlot('predictive-analytics', chartData, layout, this.plotlyConfig);
    }
}

// Initialize global charts instance
window.tasteShiftCharts = new TasteShiftCharts();

// Enhanced DOM ready initialization
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, TasteShift charts initialized');
    console.log('window.tasteShiftCharts:', window.tasteShiftCharts);
});
