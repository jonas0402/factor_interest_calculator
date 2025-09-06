# Engineering Economics Factors Lookup

A clean, simple web application for looking up engineering economics factors from standard factor tables. Built with Flask and Bootstrap for a modern, responsive user experience.

## 🔍 What This Does

This application provides a streamlined interface to lookup engineering economics factors from CSV data tables. Simply:
- Select an interest rate from the dropdown
- Choose a factor type (F/P, P/F, A/F, etc.)
- Enter the period number (n)
- Get the exact factor value from your data

## ✨ Features

- **Simple Lookup Interface**: Clean, intuitive design with dropdowns and input fields
- **CSV Data Integration**: Loads factor data directly from `factors_table.xlsx.csv`
- **All Standard Factors**: Supports F/P, P/F, A/F, A/P, F/A, P/A, A/G, P/G factors
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Validation**: Input validation with helpful error messages
- **Professional UI**: Bootstrap-powered interface with gradients and animations

## 🛠️ Technology Stack

- **Backend**: Python 3.10+ with Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5.3.0
- **Data Processing**: pandas for CSV handling
- **Dependencies**: Flask-CORS for API access

## 📁 Project Structure

```
Calculator/
├── app.py                      # Flask application with lookup endpoints
├── factors_table.xlsx.csv      # Engineering economics factors data
├── requirements.txt            # Python dependencies
├── templates/
│   ├── simple_lookup.html      # Main lookup interface
│   ├── index.html             # (Legacy compound interest calculator)
│   └── lookup.html            # (Alternative lookup interface)
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd Calculator
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## 📊 CSV Data Format

Your `factors_table.xlsx.csv` should have the following structure:

| interest_rate | n | F/P | P/F | A/F | A/P | F/A | P/A | A/G | P/G |
|---------------|---|-----|-----|-----|-----|-----|-----|-----|-----|
| 0.25 | 1 | 1.0025 | 0.9975 | ... | ... | ... | ... | ... | ... |
| 0.25 | 2 | 1.0050 | 0.9950 | ... | ... | ... | ... | ... | ... |

## 🔧 API Endpoints

### GET `/api/rates`
Returns all available interest rates from the CSV data.

**Response:**
```json
{
    "rates": [0.25, 0.5, 0.75, 1.0, 1.25, ...],
    "total_rates": 50
}
```

### POST `/api/lookup`
Lookup a specific factor value.

**Request:**
```json
{
    "rate": 1.0,
    "factor_type": "F/P",
    "period": 10
}
```

**Response:**
```json
{
    "rate": 1.0,
    "factor_type": "F/P",
    "period": 10,
    "factor_value": 1.104622,
    "factor_info": {
        "name": "(F/P) - Future Worth of Present Sum",
        "formula": "F = P × (F/P,i%,n)"
    },
    "lookup_success": true
}
```

## 💡 Factor Types Supported

| Factor | Name | Formula | Purpose |
|--------|------|---------|---------|
| **F/P** | Future Worth of Present Sum | F = P × (F/P,i%,n) | Find future value from present value |
| **P/F** | Present Worth of Future Sum | P = F × (P/F,i%,n) | Find present value from future value |
| **A/F** | Sinking Fund Factor | A = F × (A/F,i%,n) | Find annual payment from future value |
| **A/P** | Capital Recovery Factor | A = P × (A/P,i%,n) | Find annual payment from present value |
| **F/A** | Future Worth of Uniform Series | F = A × (F/A,i%,n) | Find future value from annual payments |
| **P/A** | Present Worth of Uniform Series | P = A × (P/A,i%,n) | Find present value from annual payments |
| **A/G** | Arithmetic Gradient Uniform Series | A = G × (A/G,i%,n) | Find uniform series from gradient |
| **P/G** | Arithmetic Gradient Present Worth | P = G × (P/G,i%,n) | Find present value from gradient |

## 🎯 Use Cases

- **Engineering Economics Students**: Quick factor lookups for homework and exams
- **Professional Engineers**: Factor verification for project calculations  
- **Financial Analysis**: Engineering economics calculations for project evaluation
- **Academic Research**: Standardized factor table access for consistent calculations

## 🔧 Development

### Running in Development Mode
The Flask app runs in debug mode by default for development:
```bash
python app.py
```

### Adding New Data
To update the factor tables, simply replace the `factors_table.xlsx.csv` file with your new data, ensuring the column names match the expected format.

### Customizing the UI
The interface uses Bootstrap 5.3.0. You can customize the styling by modifying the CSS in `simple_lookup.html`.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Disclaimer

This tool is for educational and professional reference purposes. Always verify critical calculations independently for important engineering and financial decisions.

## 🐛 Issues & Support

If you encounter any issues or have suggestions for improvements, please [open an issue](../../issues) on GitHub.

---

*Built with ❤️ for engineering economics calculations*