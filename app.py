from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

class FactorsTableLookup:
    _df = None  # Cache the dataframe
    
    @classmethod
    def load_factors_table(cls):
        """Load the factors table CSV once and cache it"""
        if cls._df is None:
            csv_path = os.path.join(os.path.dirname(__file__), 'factors_table.xlsx.csv')
            try:
                cls._df = pd.read_csv(csv_path)
                # Ensure column names are clean
                cls._df.columns = cls._df.columns.str.strip()
            except FileNotFoundError:
                raise FileNotFoundError(f"factors_table.xlsx.csv not found at {csv_path}")
        return cls._df
    
    @classmethod
    def get_available_rates(cls):
        """Get all available interest rates from the table"""
        df = cls.load_factors_table()
        rates = sorted(df['interest_rate'].unique())
        return rates
    
    @classmethod
    def lookup_factor(cls, rate, factor_type, period):
        """
        Lookup a specific factor value from the table
        
        Args:
            rate: Interest rate (e.g., 0.25 for 0.25%)
            factor_type: Factor acronym ('F/P', 'P/F', 'A/F', 'A/P', 'F/A', 'P/A', 'A/G', 'P/G')
            period: Period number (n)
        
        Returns:
            dict with factor value and metadata
        """
        try:
            df = cls.load_factors_table()
            
            # Filter for the specific rate and period
            row = df[(df['interest_rate'] == rate) & (df['n'] == period)]
            
            if row.empty:
                return {'error': f'No data found for rate {rate}% and period {period}'}
            
            # Get the factor value
            if factor_type not in row.columns:
                return {'error': f'Factor type {factor_type} not found in table'}
            
            factor_value = row[factor_type].iloc[0]
            
            # Get factor descriptions
            factor_descriptions = {
                'F/P': {'name': '(F/P) - Future Worth of Present Sum', 'formula': 'F = P × (F/P,i%,n)'},
                'P/F': {'name': '(P/F) - Present Worth of Future Sum', 'formula': 'P = F × (P/F,i%,n)'},
                'A/F': {'name': '(A/F) - Sinking Fund Factor', 'formula': 'A = F × (A/F,i%,n)'},
                'A/P': {'name': '(A/P) - Capital Recovery Factor', 'formula': 'A = P × (A/P,i%,n)'},
                'F/A': {'name': '(F/A) - Future Worth of Uniform Series', 'formula': 'F = A × (F/A,i%,n)'},
                'P/A': {'name': '(P/A) - Present Worth of Uniform Series', 'formula': 'P = A × (P/A,i%,n)'},
                'A/G': {'name': '(A/G) - Arithmetic Gradient Uniform Series Factor', 'formula': 'A = G × (A/G,i%,n)'},
                'P/G': {'name': '(P/G) - Arithmetic Gradient Present Worth Factor', 'formula': 'P = G × (P/G,i%,n)'}
            }
            
            return {
                'rate': rate,
                'factor_type': factor_type,
                'period': period,
                'factor_value': factor_value,
                'factor_info': factor_descriptions.get(factor_type, {'name': factor_type, 'formula': 'N/A'}),
                'lookup_success': True
            }
            
        except Exception as e:
            return {'error': f'Lookup error: {str(e)}'}

@app.route('/')
def index():
    return render_template('simple_lookup.html')

@app.route('/api/rates')
def get_available_rates():
    """Get all available interest rates from the factors table CSV"""
    try:
        rates = FactorsTableLookup.get_available_rates()
        return jsonify({
            'rates': rates,
            'total_rates': len(rates)
        })
    except Exception as e:
        return jsonify({'error': f'Error loading rates: {str(e)}'}), 500

@app.route('/api/lookup', methods=['POST'])
def lookup_factor():
    """Lookup a specific factor value from the CSV table"""
    try:
        data = request.get_json()
        
        # Validate input
        required_fields = ['rate', 'factor_type', 'period']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        rate = float(data['rate'])
        factor_type = data['factor_type']
        period = int(data['period'])
        
        # Lookup the factor
        result = FactorsTableLookup.lookup_factor(rate, factor_type, period)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
        
    except ValueError:
        return jsonify({'error': 'Invalid input format. Please enter numeric values.'}), 400
    except Exception as e:
        return jsonify({'error': f'Lookup error: {str(e)}'}), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Bind to 0.0.0.0 to allow external connections in Docker
    app.run(debug=True, host='0.0.0.0', port=port)