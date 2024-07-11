from flask import request, jsonify
from data.conn import mydb, mycursor
from controllers.user.analysis import analyze_company, compare_companies

yfinance_symbols = ['ibm', 'prft', 'nsci', 'ba', 'meta', 'nvda', 'tsla', 'aapl', 'amzn', 'intc']

def oneCompanyAnalysis():
    try:
        # Fetch company data from the database
        mycursor.execute('SELECT symbol, name FROM companies')
        companies = {symbol: name for symbol, name in mycursor.fetchall()}
        
        # Get the request data
        data = request.get_json()
        company_symbol = data.get('company_symbol')
        
        # Check if the company symbol is valid and analyze the company
        if company_symbol in yfinance_symbols:
            analyze_company(company_symbol, companies.get(company_symbol, company_symbol.upper()), True)
        elif company_symbol in companies:
            analyze_company(company_symbol, companies[company_symbol], False)
        else:
            return jsonify({'error': 'Invalid company symbol. Please try again.'}), 400
        
        return jsonify({'message': "Processing..."})
    
    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def twoCompaniesAnalysis():
    try:
        # Fetch company data from the database
        mycursor.execute('SELECT symbol, name FROM companies')
        companies = {symbol: name for symbol, name in mycursor.fetchall()}
        
        # Get the request data
        data = request.get_json()
        symbol1 = data.get('company1')
        symbol2 = data.get('company2')
        
        # Validate the symbols and compare the companies
        if (symbol1 in yfinance_symbols or symbol1 in companies) and (symbol2 in yfinance_symbols or symbol2 in companies):
            compare_companies(symbol1, symbol2, companies)
        else:
            if symbol1 not in yfinance_symbols and symbol1 not in companies:
                return jsonify({'message': f"{symbol1} does not exist in the companies data."}), 400
            if symbol2 not in yfinance_symbols and symbol2 not in companies:
                return jsonify({'message': f"{symbol2} does not exist in the companies data."}), 400
        
        return jsonify({'message': "Processing..."})
    
    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
