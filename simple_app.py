#!/usr/bin/env python3
"""
🧮 MER Contribution Margin Calculator - Simplified Version
A professional web application for calculating Marketing Efficiency Ratio (MER) 
and Contribution Margin with basic visualization.
"""

import math
import json
import io
import base64
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Simple Flask-like web server using only built-in modules
import http.server
import socketserver
import urllib.parse
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

class MERCalculator:
    """MER (Marketing Efficiency Ratio) Contribution Margin Calculator"""
    
    def __init__(self):
        """Initialize the calculator with default configuration."""
        self.default_config = {
            'variable_cost': 0.65,              # 65% variable cost
            'revenue_increment': 20000,         # €20,000 revenue increment
            'contribution_margin_goal': 176000  # €176,000 contribution margin goal
        }
        
        self.default_inputs = {
            'target_revenue': 820000,           # €820,000 - Target revenue
            'target_mer': 7.50                  # 750% MER (7.50 as decimal)
        }
    
    def calculate_contribution_margin(self, revenue: float, mer: float, variable_cost: float) -> float:
        """Calculate contribution margin for given revenue and MER."""
        gross_profit = revenue * (1 - variable_cost)
        marketing_spend = revenue / mer
        return gross_profit - marketing_spend
    
    def generate_revenue_range_data(self, target_mer: float, target_revenue: float, 
                                   variable_cost: float, revenue_increment: float,
                                   points_before: int = 10, points_after: int = 10) -> Tuple[List[float], List[float]]:
        """Generate data points for revenue range analysis."""
        start_revenue = target_revenue - (points_before * revenue_increment)
        end_revenue = target_revenue + (points_after * revenue_increment)
        
        revenue_values = []
        cm_values = []
        
        current_revenue = start_revenue
        while current_revenue <= end_revenue:
            revenue_values.append(current_revenue)
            cm_values.append(self.calculate_contribution_margin(current_revenue, target_mer, variable_cost))
            current_revenue += revenue_increment
        
        return revenue_values, cm_values
    
    def create_simple_chart_data(self, revenue_values: List[float], cm_values: List[float], 
                                target_revenue: float, target_cm: float, cm_goal: float) -> Dict:
        """Create chart data for simple visualization."""
        return {
            'revenue_values': revenue_values,
            'cm_values': cm_values,
            'target_revenue': target_revenue,
            'target_cm': target_cm,
            'cm_goal': cm_goal,
            'min_revenue': min(revenue_values),
            'max_revenue': max(revenue_values),
            'min_cm': min(cm_values),
            'max_cm': max(cm_values)
        }
    
    def validate_inputs(self, config: Dict, user_inputs: Dict) -> List[str]:
        """Validate all inputs and return list of errors."""
        errors = []
        
        if not config.get('variable_cost') or config['variable_cost'] < 0 or config['variable_cost'] >= 1:
            errors.append('Variable Cost must be between 0 and 1 (e.g., 0.65 for 65%)')
        
        if not config.get('revenue_increment') or config['revenue_increment'] <= 0:
            errors.append('Revenue Increment must be greater than 0')
        
        if not config.get('contribution_margin_goal') or config['contribution_margin_goal'] <= 0:
            errors.append('Contribution Margin Goal must be greater than 0')
        
        if not user_inputs.get('target_revenue') or user_inputs['target_revenue'] <= 0:
            errors.append('Target Revenue must be greater than 0')
        
        if not user_inputs.get('target_mer') or user_inputs['target_mer'] <= 0:
            errors.append('Target MER must be greater than 0')
        
        return errors

# Initialize calculator
calculator = MERCalculator()

# Global session storage (simplified)
sessions = {}

class MERRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the MER calculator."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/' or self.path == '/index.html':
            self.serve_index()
        elif self.path == '/api/defaults':
            self.serve_defaults()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/api/calculate':
            self.handle_calculate()
        elif self.path == '/api/reset':
            self.handle_reset()
        else:
            self.send_error(404)
    
    def serve_index(self):
        """Serve the main HTML page."""
        html_content = self.get_html_template()
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-length', len(html_content.encode()))
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def serve_defaults(self):
        """Serve default configuration values."""
        response = {
            'config': calculator.default_config,
            'user_inputs': calculator.default_inputs
        }
        
        self.send_json_response(response)
    
    def handle_calculate(self):
        """Handle calculation requests."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            config = {
                'variable_cost': float(data.get('variable_cost', 0.65)),
                'revenue_increment': float(data.get('revenue_increment', 20000)),
                'contribution_margin_goal': float(data.get('contribution_margin_goal', 176000))
            }
            
            user_inputs = {
                'target_revenue': float(data.get('target_revenue', 820000)),
                'target_mer': float(data.get('target_mer', 7.50))
            }
            
            errors = calculator.validate_inputs(config, user_inputs)
            if errors:
                self.send_json_response({'success': False, 'errors': errors})
                return
            
            contribution_margin = calculator.calculate_contribution_margin(
                user_inputs['target_revenue'], 
                user_inputs['target_mer'],
                config['variable_cost']
            )
            
            meets_goal = contribution_margin >= config['contribution_margin_goal']
            
            revenue_values, cm_values = calculator.generate_revenue_range_data(
                user_inputs['target_mer'], 
                user_inputs['target_revenue'],
                config['variable_cost'],
                config['revenue_increment']
            )
            
            chart_data = calculator.create_simple_chart_data(
                revenue_values, cm_values, user_inputs['target_revenue'], 
                contribution_margin, config['contribution_margin_goal']
            )
            
            coefficient = (1 - config['variable_cost']) - (1 / user_inputs['target_mer'])
            min_revenue = config['contribution_margin_goal'] / coefficient if coefficient > 0 else 0
            
            gross_profit = user_inputs['target_revenue'] * (1 - config['variable_cost'])
            marketing_spend = user_inputs['target_revenue'] / user_inputs['target_mer']
            
            result = {
                'success': True,
                'contribution_margin': contribution_margin,
                'meets_goal': meets_goal,
                'difference': contribution_margin - config['contribution_margin_goal'],
                'min_revenue': min_revenue,
                'revenue_difference': user_inputs['target_revenue'] - min_revenue,
                'gross_profit': gross_profit,
                'marketing_spend': marketing_spend,
                'chart_data': chart_data,
                'chart_explanation': {
                    'blue_line': 'Shows how your contribution margin changes as revenue increases',
                    'orange_line': f'Your target contribution margin goal (€{config["contribution_margin_goal"]:,.0f})',
                    'red_star': f'Your specific revenue/CM combination (€{user_inputs["target_revenue"]:,.0f} → €{contribution_margin:,.0f})'
                }
            }
            
            self.send_json_response(result)
            
        except Exception as e:
            self.send_json_response({'success': False, 'errors': [f'Calculation error: {str(e)}']})
    
    def handle_reset(self):
        """Handle reset requests."""
        response = {'success': True, 'message': 'Configuration reset to defaults'}
        self.send_json_response(response)
    
    def send_json_response(self, data):
        """Send a JSON response."""
        json_data = json.dumps(data).encode()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-length', len(json_data))
        self.end_headers()
        self.wfile.write(json_data)
    
    def get_html_template(self):
        """Return the HTML template."""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧮 MER Contribution Margin Calculator</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        :root {
            --primary-color: #2563eb;
            --success-color: #10b981;
            --danger-color: #ef4444;
            --dark-color: #1f2937;
            --light-gray: #f8fafc;
            --border-color: #e5e7eb;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .main-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            margin: 2rem auto;
            max-width: 1200px;
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, var(--primary-color), #3b82f6);
            color: white;
            padding: 2rem;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .content-area {
            padding: 2rem;
        }

        .input-section {
            background: var(--light-gray);
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 2rem;
        }

        .form-control {
            border: 2px solid var(--border-color);
            border-radius: 8px;
            padding: 0.75rem;
            transition: all 0.3s ease;
        }

        .form-control:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 0.2rem rgba(37, 99, 235, 0.25);
        }

        .btn-primary {
            background: var(--primary-color);
            border: none;
            padding: 0.75rem 2rem;
            font-weight: 600;
            border-radius: 8px;
            transition: all 0.3s ease;
        }

        .btn-primary:hover {
            background: #1d4ed8;
            transform: translateY(-2px);
        }

        .results-section {
            background: white;
            border: 2px solid var(--border-color);
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 2rem;
            display: none;
        }

        .results-section.show {
            display: block;
            animation: slideIn 0.5s ease-out;
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .result-card {
            background: var(--light-gray);
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border-left: 4px solid var(--primary-color);
        }

        .result-card.success {
            border-left-color: var(--success-color);
            background: #f0fdf4;
        }

        .result-card.danger {
            border-left-color: var(--danger-color);
            background: #fef2f2;
        }

        .metric {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }

        .metric-value.success { color: var(--success-color); }
        .metric-value.danger { color: var(--danger-color); }

        .chart-container {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 2rem;
            border: 2px solid var(--border-color);
        }

        @media (max-width: 768px) {
            .main-container { margin: 1rem; }
            .header h1 { font-size: 2rem; }
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="main-container">
            <div class="header">
                <h1><i class="fas fa-calculator"></i> MER Calculator</h1>
                <p>Professional Marketing Efficiency Ratio & Contribution Margin Calculator</p>
            </div>

            <div class="content-area">
                <div class="input-section">
                    <h2><i class="fas fa-cog"></i> Configuration & Target Values</h2>
                    
                    <form id="calculatorForm">
                        <div class="row">
                            <div class="col-md-6">
                                <h5><i class="fas fa-bullseye"></i> Target Values</h5>
                                
                                <div class="mb-3">
                                    <label for="target_revenue" class="form-label">Target Revenue (€)</label>
                                    <input type="number" class="form-control" id="target_revenue" value="820000" step="1000" min="1">
                                </div>

                                <div class="mb-3">
                                    <label for="target_mer" class="form-label">Target MER</label>
                                    <input type="number" class="form-control" id="target_mer" value="7.50" step="0.1" min="0.1">
                                </div>
                            </div>

                            <div class="col-md-6">
                                <h5><i class="fas fa-sliders-h"></i> Configuration</h5>
                                
                                <div class="mb-3">
                                    <label for="variable_cost" class="form-label">Variable Cost (decimal)</label>
                                    <input type="number" class="form-control" id="variable_cost" value="0.65" step="0.01" min="0" max="0.99">
                                </div>

                                <div class="mb-3">
                                    <label for="contribution_margin_goal" class="form-label">Contribution Margin Goal (€)</label>
                                    <input type="number" class="form-control" id="contribution_margin_goal" value="176000" step="1000" min="1">
                                </div>
                            </div>
                        </div>

                        <div class="text-center mt-4">
                            <button type="submit" class="btn btn-primary btn-lg me-3">
                                <i class="fas fa-calculator"></i> Calculate Contribution Margin
                            </button>
                            <button type="button" class="btn btn-secondary" onclick="resetForm()">
                                <i class="fas fa-undo"></i> Reset
                            </button>
                        </div>
                    </form>
                </div>

                <div id="errorMessages"></div>

                <div class="results-section" id="resultsSection">
                    <h2><i class="fas fa-chart-line"></i> Results & Analysis</h2>

                    <div class="row">
                        <div class="col-md-6">
                            <div class="result-card" id="mainResultCard">
                                <h5><i class="fas fa-target"></i> Main Results</h5>
                                <div class="metric">
                                    <span>Target Revenue:</span>
                                    <span id="displayTargetRevenue">€0</span>
                                </div>
                                <div class="metric">
                                    <span>Target MER:</span>
                                    <span id="displayTargetMer">0%</span>
                                </div>
                                <div class="metric">
                                    <span>Contribution Margin:</span>
                                    <span id="displayContributionMargin">€0</span>
                                </div>
                                <div class="metric">
                                    <span>Goal Amount:</span>
                                    <span id="displayGoalAmount">€0</span>
                                </div>
                                <div class="metric">
                                    <span>Meets Goal:</span>
                                    <span id="displayMeetsGoal">-</span>
                                </div>
                                <div class="metric">
                                    <span>Difference:</span>
                                    <span id="displayDifference">€0</span>
                                </div>
                            </div>
                        </div>

                        <div class="col-md-6">
                            <div class="result-card">
                                <h5><i class="fas fa-microscope"></i> Additional Analysis</h5>
                                <div class="metric">
                                    <span>Minimum Revenue for Goal:</span>
                                    <span id="displayMinRevenue">€0</span>
                                </div>
                                <div class="metric">
                                    <span>Revenue vs Minimum:</span>
                                    <span id="displayRevenueDiff">€0</span>
                                </div>
                                <div class="metric">
                                    <span>Gross Profit:</span>
                                    <span id="displayGrossProfit">€0</span>
                                </div>
                                <div class="metric">
                                    <span>Marketing Spend:</span>
                                    <span id="displayMarketingSpend">€0</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="row mt-4">
                        <div class="col-12">
                            <div class="result-card">
                                <h5><i class="fas fa-calculator"></i> Formula Breakdown</h5>
                                <p><strong>Formula:</strong> Contribution Margin = Revenue × (1 - Variable Cost) - (Revenue ÷ MER)</p>
                                <p id="formulaBreakdown">-</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="chart-container" id="chartContainer" style="display: none;">
                    <h2><i class="fas fa-chart-area"></i> Contribution Margin vs Revenue Chart</h2>
                    <canvas id="merChart" width="800" height="400"></canvas>
                </div>
            </div>
        </div>
    </div>

    <script>
        let chart = null;

        document.addEventListener('DOMContentLoaded', function() {
            loadDefaults();
        });

        async function loadDefaults() {
            try {
                const response = await fetch('/api/defaults');
                const data = await response.json();
                
                if (data.config && data.user_inputs) {
                    document.getElementById('target_revenue').value = data.user_inputs.target_revenue;
                    document.getElementById('target_mer').value = data.user_inputs.target_mer;
                    document.getElementById('variable_cost').value = data.config.variable_cost;
                    document.getElementById('contribution_margin_goal').value = data.config.contribution_margin_goal;
                }
            } catch (error) {
                console.error('Error loading defaults:', error);
            }
        }

        async function resetForm() {
            try {
                await fetch('/api/reset', { method: 'POST' });
                loadDefaults();
                hideResults();
            } catch (error) {
                console.error('Error resetting:', error);
            }
        }

        document.getElementById('calculatorForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = {
                target_revenue: parseFloat(document.getElementById('target_revenue').value),
                target_mer: parseFloat(document.getElementById('target_mer').value),
                variable_cost: parseFloat(document.getElementById('variable_cost').value),
                contribution_margin_goal: parseFloat(document.getElementById('contribution_margin_goal').value),
                revenue_increment: 20000
            };
            
            try {
                const response = await fetch('/api/calculate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    displayResults(result, formData);
                } else {
                    showErrors(result.errors);
                }
            } catch (error) {
                showError('Error calculating results. Please try again.');
            }
        });

        function displayResults(result, formData) {
            const mainCard = document.getElementById('mainResultCard');
            mainCard.className = result.meets_goal ? 'result-card success' : 'result-card danger';
            
            document.getElementById('displayTargetRevenue').textContent = formatCurrency(formData.target_revenue);
            document.getElementById('displayTargetMer').textContent = (formData.target_mer * 100).toFixed(0) + '%';
            document.getElementById('displayContributionMargin').textContent = formatCurrency(result.contribution_margin);
            document.getElementById('displayGoalAmount').textContent = formatCurrency(formData.contribution_margin_goal);
            
            const meetsGoalEl = document.getElementById('displayMeetsGoal');
            meetsGoalEl.textContent = result.meets_goal ? 'YES ✅' : 'NO ❌';
            meetsGoalEl.className = result.meets_goal ? 'metric-value success' : 'metric-value danger';
            
            const differenceEl = document.getElementById('displayDifference');
            differenceEl.textContent = formatCurrency(result.difference) + (result.difference >= 0 ? ' (Surplus)' : ' (Deficit)');
            differenceEl.className = result.difference >= 0 ? 'metric-value success' : 'metric-value danger';
            
            document.getElementById('displayMinRevenue').textContent = formatCurrency(result.min_revenue);
            
            const revenueDiffEl = document.getElementById('displayRevenueDiff');
            revenueDiffEl.textContent = formatCurrency(result.revenue_difference) + (result.revenue_difference >= 0 ? ' (Surplus)' : ' (Deficit)');
            revenueDiffEl.className = result.revenue_difference >= 0 ? 'metric-value success' : 'metric-value danger';
            
            document.getElementById('displayGrossProfit').textContent = formatCurrency(result.gross_profit);
            document.getElementById('displayMarketingSpend').textContent = formatCurrency(result.marketing_spend);
            
            const grossProfitPercent = ((1 - formData.variable_cost) * 100).toFixed(0);
            document.getElementById('formulaBreakdown').innerHTML = 
                `€${formatNumber(formData.target_revenue)} × ${grossProfitPercent}% - (€${formatNumber(formData.target_revenue)} ÷ ${formData.target_mer}) = €${formatNumber(result.gross_profit)} - €${formatNumber(result.marketing_spend)} = <strong>€${formatNumber(result.contribution_margin)}</strong>`;
            
            createChart(result.chart_data);
            
            document.getElementById('resultsSection').classList.add('show');
            document.getElementById('chartContainer').style.display = 'block';
        }

        function createChart(chartData) {
            const ctx = document.getElementById('merChart').getContext('2d');
            
            if (chart) {
                chart.destroy();
            }
            
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: chartData.revenue_values.map(r => formatCurrency(r)),
                    datasets: [{
                        label: 'Contribution Margin',
                        data: chartData.cm_values,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        borderWidth: 3,
                        fill: true
                    }, {
                        label: 'CM Goal',
                        data: Array(chartData.revenue_values.length).fill(chartData.cm_goal),
                        borderColor: '#f59e0b',
                        borderDash: [10, 5],
                        borderWidth: 3,
                        pointRadius: 0
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Contribution Margin vs Revenue'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            ticks: {
                                callback: function(value) {
                                    return formatCurrency(value);
                                }
                            }
                        }
                    }
                }
            });
        }

        function formatCurrency(value) {
            return '€' + formatNumber(value);
        }

        function formatNumber(value) {
            return new Intl.NumberFormat('en-US').format(Math.round(value));
        }

        function hideResults() {
            document.getElementById('resultsSection').classList.remove('show');
            document.getElementById('chartContainer').style.display = 'none';
        }

        function showErrors(errors) {
            const errorDiv = document.getElementById('errorMessages');
            errorDiv.innerHTML = `
                <div class="alert alert-danger">
                    <h5><i class="fas fa-exclamation-triangle"></i> Validation Errors:</h5>
                    <ul class="mb-0">
                        ${errors.map(error => `<li>${error}</li>`).join('')}
                    </ul>
                </div>
            `;
        }

        function showError(message) {
            const errorDiv = document.getElementById('errorMessages');
            errorDiv.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle"></i> ${message}
                </div>
            `;
        }
    </script>
</body>
</html>'''

def main():
    """Run the MER Calculator web server."""
    port = 8000
    
    try:
        server = HTTPServer(('0.0.0.0', port), MERRequestHandler)
        print(f"🧮 MER Calculator Server Starting...")
        print(f"🌐 Server running at: http://localhost:{port}")
        print(f"📱 Access from any device on your network")
        print(f"🔗 Open your browser and navigate to the URL above")
        print(f"⭐ Features: Professional UI, Interactive Charts, Real-time Calculations")
        print(f"🛑 Press Ctrl+C to stop the server")
        print("="*60)
        
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Thank you for using MER Calculator!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Try changing the port if 8000 is already in use")

if __name__ == "__main__":
    main()