# 🧮 MER Contribution Margin Calculator

A professional web application for calculating Marketing Efficiency Ratio (MER) and Contribution Margin with interactive charts and analysis.

## Features

### 🎯 Core Functionality
- **MER Calculation**: Calculate contribution margin based on revenue and MER
- **Interactive Charts**: Professional matplotlib charts showing CM vs Revenue relationship
- **Formula Breakdown**: Step-by-step calculation explanation
- **Goal Tracking**: Check if your contribution margin meets your target goal
- **Additional Analysis**: Minimum revenue calculations and surplus/deficit analysis

### 💼 Professional Interface
- **Modern UI**: Clean, responsive design with Bootstrap 5
- **Interactive Elements**: Real-time form validation and loading indicators
- **Visual Feedback**: Color-coded results (green for success, red for deficits)
- **Mobile Responsive**: Works perfectly on all device sizes
- **Professional Styling**: Gradient backgrounds, smooth animations, and professional typography

### 📊 Chart Features
- **Interactive Visualization**: High-quality matplotlib charts
- **Multiple Data Points**: Revenue range analysis with 20+ data points
- **Clear Annotations**: Target point highlighting and goal line visualization
- **Detailed Explanations**: Color-coded chart legend with explanations

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start
1. **Clone or Download** the project files
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application**:
   ```bash
   python app.py
   ```
4. **Open in Browser**: Navigate to `http://localhost:5000`

## Usage Guide

### 1. Input Configuration
- **Target Revenue**: Your target revenue amount (e.g., €820,000)
- **Target MER**: Marketing Efficiency Ratio (e.g., 7.5 = 750%)
- **Variable Cost**: Cost percentage as decimal (0.65 = 65%)
- **Contribution Margin Goal**: Your target contribution margin (e.g., €176,000)

### 2. Advanced Settings
- **Revenue Increment**: Step size for chart analysis (default: €20,000)

### 3. Calculate Results
- Click "Calculate Contribution Margin" to process your inputs
- View comprehensive results including:
  - Main contribution margin calculation
  - Goal achievement status
  - Additional analysis metrics
  - Interactive chart visualization

### 4. Chart Analysis
The generated chart shows:
- **Blue Line**: How contribution margin changes with revenue
- **Orange Dashed Line**: Your contribution margin goal
- **Red Star**: Your specific target point

## Formula Explanation

### Core Formula
```
Contribution Margin = Revenue × (1 - Variable Cost) - (Revenue ÷ MER)
```

### Example Calculation
With default values:
- Revenue: €820,000
- Variable Cost: 65% (0.65)
- MER: 7.5

```
Gross Profit = €820,000 × (1 - 0.65) = €820,000 × 0.35 = €287,000
Marketing Spend = €820,000 ÷ 7.5 = €109,333
Contribution Margin = €287,000 - €109,333 = €177,667
```

## Technical Details

### Technology Stack
- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **Styling**: Bootstrap 5, Font Awesome icons
- **Charts**: Matplotlib with web integration
- **Data Processing**: Pandas, NumPy

### File Structure
```
mer-calculator/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Main HTML template
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

### Key Features Implementation
- **Session Management**: User preferences persist across page reloads
- **Input Validation**: Comprehensive client and server-side validation
- **Chart Generation**: Dynamic matplotlib charts converted to base64 images
- **Responsive Design**: Mobile-first CSS with modern design patterns
- **Error Handling**: Graceful error handling with user-friendly messages

## Customization

### Styling
The application uses CSS custom properties for easy theming:
```css
:root {
    --primary-color: #2563eb;
    --secondary-color: #f59e0b;
    --success-color: #10b981;
    --danger-color: #ef4444;
}
```

### Default Values
Modify default configuration in `app.py`:
```python
self.default_config = {
    'variable_cost': 0.65,
    'contribution_margin_goal': 176000
}
```

## Browser Compatibility
- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

## Security Features
- Session-based data storage
- Input validation and sanitization
- CSRF protection via Flask's built-in features
- No sensitive data persistence

## Performance
- **Fast Calculation**: Sub-second calculation times
- **Optimized Charts**: Efficient matplotlib rendering
- **Responsive UI**: Smooth animations and transitions
- **Minimal Dependencies**: Lightweight application

## Troubleshooting

### Common Issues
1. **Port Already in Use**: Change port in `app.py` or kill existing process
2. **Missing Dependencies**: Run `pip install -r requirements.txt`
3. **Chart Not Displaying**: Ensure matplotlib backend is properly configured

### Development Mode
For development with auto-reload:
```bash
export FLASK_ENV=development
python app.py
```

## License
This project is open source and available under the MIT License.

## Support
For issues or questions, please check the code comments or create an issue in the project repository.