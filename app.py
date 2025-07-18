from flask import Flask, render_template, request, jsonify, session
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import os
import io
import base64
from datetime import datetime
from typing import Dict, List, Tuple, Optional

app = Flask(__name__)
app.secret_key = 'mer_calculator_secret_key_2024'

class MERCalculator:
    """
    🧮 MER (Marketing Efficiency Ratio) Contribution Margin Calculator
    
    This calculator helps determine contribution margins for different 
    combinations of revenue and MER values.
    """
    
    def __init__(self):
        """Initialize the calculator with default configuration."""
        # Default configuration
        self.default_config = {
            'variable_cost': 0.65,              # 65% variable cost
            'revenue_start_number': 100000,     # €100,000 starting revenue
            'mer_increment': 0.50,              # 50% MER increment
            'revenue_increment': 20000,         # €20,000 revenue increment
            'contribution_margin_goal': 176000  # €176,000 contribution margin goal
        }
        
        # Default user inputs
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
    
    def create_chart(self, revenue_values: List[float], cm_values: List[float], 
                    target_mer: float, target_revenue: float, target_cm: float,
                    cm_goal: float, variable_cost: float) -> str:
        """Create a chart showing contribution margin vs revenue and return as base64 string."""
        plt.figure(figsize=(12, 8))
        plt.style.use('seaborn-v0_8-whitegrid')
        
        # Main line plot - Shows how CM changes with revenue
        plt.plot(revenue_values, cm_values, 'b-', linewidth=3, label='Contribution Margin', marker='o', markersize=4)
        
        # Goal line - Horizontal line showing the CM goal
        plt.axhline(y=cm_goal, color='orange', linestyle='--', 
                   linewidth=3, label=f'CM Goal: €{cm_goal:,.0f}')
        
        # Highlight target point
        plt.scatter([target_revenue], [target_cm], color='red', s=150, zorder=5, 
                   label=f'Your Target: €{target_revenue:,.0f} → €{target_cm:,.0f}', marker='*')
        
        # Add text annotation for the target point
        plt.annotate(f'€{target_cm:,.0f}', 
                    xy=(target_revenue, target_cm), 
                    xytext=(10, 10), 
                    textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.7),
                    color='white', fontweight='bold')
        
        # Formatting
        plt.xlabel('Revenue (€)', fontsize=12, fontweight='bold')
        plt.ylabel('Contribution Margin (€)', fontsize=12, fontweight='bold')
        plt.title(f'Contribution Margin vs Revenue\n(MER: {target_mer*100:.0f}%)', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        # Enhanced legend
        plt.legend(loc='upper left', fontsize=11, frameon=True, fancybox=True, shadow=True)
        
        # Format axes
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'€{x:,.0f}'))
        plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'€{x:,.0f}'))
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        
        # Add explanation text
        plt.figtext(0.02, 0.02, 
                   f"Formula: Revenue × {(1-variable_cost)*100:.0f}% - (Revenue ÷ {target_mer:.1f})",
                   fontsize=10, style='italic', alpha=0.7)
        
        plt.tight_layout()
        
        # Convert plot to base64 string
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=300, bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return plot_url
    
    def validate_inputs(self, config: Dict, user_inputs: Dict) -> List[str]:
        """Validate all inputs and return list of errors."""
        errors = []
        
        # Validate config
        if not config.get('variable_cost') or config['variable_cost'] < 0 or config['variable_cost'] >= 1:
            errors.append('Variable Cost must be between 0 and 1 (e.g., 0.65 for 65%)')
        
        if not config.get('revenue_increment') or config['revenue_increment'] <= 0:
            errors.append('Revenue Increment must be greater than 0')
        
        if not config.get('contribution_margin_goal') or config['contribution_margin_goal'] <= 0:
            errors.append('Contribution Margin Goal must be greater than 0')
        
        # Validate user inputs
        if not user_inputs.get('target_revenue') or user_inputs['target_revenue'] <= 0:
            errors.append('Target Revenue must be greater than 0')
        
        if not user_inputs.get('target_mer') or user_inputs['target_mer'] <= 0:
            errors.append('Target MER must be greater than 0')
        
        return errors

# Initialize calculator
calculator = MERCalculator()

@app.route('/')
def index():
    """Main page route."""
    # Initialize session with default values if not present
    if 'config' not in session:
        session['config'] = calculator.default_config.copy()
    if 'user_inputs' not in session:
        session['user_inputs'] = calculator.default_inputs.copy()
    
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate contribution margin and generate results."""
    try:
        # Get data from request
        data = request.get_json()
        
        # Update session with new values
        config = {
            'variable_cost': float(data.get('variable_cost', 0.65)),
            'revenue_increment': float(data.get('revenue_increment', 20000)),
            'contribution_margin_goal': float(data.get('contribution_margin_goal', 176000))
        }
        
        user_inputs = {
            'target_revenue': float(data.get('target_revenue', 820000)),
            'target_mer': float(data.get('target_mer', 7.50))
        }
        
        # Validate inputs
        errors = calculator.validate_inputs(config, user_inputs)
        if errors:
            return jsonify({'success': False, 'errors': errors})
        
        # Calculate contribution margin
        contribution_margin = calculator.calculate_contribution_margin(
            user_inputs['target_revenue'], 
            user_inputs['target_mer'],
            config['variable_cost']
        )
        
        # Check if goal is met
        meets_goal = contribution_margin >= config['contribution_margin_goal']
        
        # Generate chart data
        revenue_values, cm_values = calculator.generate_revenue_range_data(
            user_inputs['target_mer'], 
            user_inputs['target_revenue'],
            config['variable_cost'],
            config['revenue_increment']
        )
        
        # Create chart
        chart_base64 = calculator.create_chart(
            revenue_values, cm_values, user_inputs['target_mer'], 
            user_inputs['target_revenue'], contribution_margin,
            config['contribution_margin_goal'], config['variable_cost']
        )
        
        # Calculate additional analysis
        coefficient = (1 - config['variable_cost']) - (1 / user_inputs['target_mer'])
        min_revenue = config['contribution_margin_goal'] / coefficient if coefficient > 0 else 0
        
        # Calculate formula components
        gross_profit = user_inputs['target_revenue'] * (1 - config['variable_cost'])
        marketing_spend = user_inputs['target_revenue'] / user_inputs['target_mer']
        
        # Update session
        session['config'] = config
        session['user_inputs'] = user_inputs
        
        # Prepare response
        result = {
            'success': True,
            'contribution_margin': contribution_margin,
            'meets_goal': meets_goal,
            'difference': contribution_margin - config['contribution_margin_goal'],
            'min_revenue': min_revenue,
            'revenue_difference': user_inputs['target_revenue'] - min_revenue,
            'gross_profit': gross_profit,
            'marketing_spend': marketing_spend,
            'chart': chart_base64,
            'chart_explanation': {
                'blue_line': 'Shows how your contribution margin changes as revenue increases',
                'orange_line': f'Your target contribution margin goal (€{config["contribution_margin_goal"]:,.0f})',
                'red_star': f'Your specific revenue/CM combination (€{user_inputs["target_revenue"]:,.0f} → €{contribution_margin:,.0f})'
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'errors': [f'Calculation error: {str(e)}']})

@app.route('/reset', methods=['POST'])
def reset():
    """Reset configuration to defaults."""
    session['config'] = calculator.default_config.copy()
    session['user_inputs'] = calculator.default_inputs.copy()
    return jsonify({'success': True, 'message': 'Configuration reset to defaults'})

@app.route('/get_defaults')
def get_defaults():
    """Get default configuration values."""
    return jsonify({
        'config': session.get('config', calculator.default_config),
        'user_inputs': session.get('user_inputs', calculator.default_inputs)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)