from flask import request, jsonify

from data.conn import mydb, mycursor
from controllers.user.analysis import analyze_company, compare_companies

yfinance_symbols = ['ibm', 'prft', 'nsci', 'ba', 'meta', 'nvda', 'tsla', 'aapl', 'amzn', 'intc']

def oneCompanyAnalysis():
    mycursor.execute('SELECT symbol, name FROM companies')
    companies = {symbol: name for symbol, name in mycursor.fetchall()}
    
    data = request.get_json()
    
    company_symbol = data.get('company_symbol')
    
    if company_symbol in yfinance_symbols:
        analyze_company(company_symbol, companies.get(company_symbol, company_symbol.upper()), True)
    elif company_symbol in companies:
        analyze_company(company_symbol, companies[company_symbol], False)
    else:
        return jsonify({'error': 'Invalid company symbol. Please try again.'})  
    
    return jsonify({'message': "Processing..."}) 

def twoCompaniesAnalysis():
    mycursor.execute('SELECT symbol, name FROM companies')
    companies = {symbol: name for symbol, name in mycursor.fetchall()}
    
    data = request.get_json()
    
    
    symbol1 = data.get('company1')
    symbol2 = data.get('company2')
    
    if (symbol1 in yfinance_symbols or symbol1 in companies) and (symbol2 in yfinance_symbols or symbol2 in companies):
        compare_companies(symbol1, symbol2, companies)
    else:
        if symbol1 not in yfinance_symbols:
            return jsonify({'message' : f"{symbol1} does not exist in the companies data."})
        if symbol2 not in companies:
             return jsonify({'message' : f"{symbol2} does not exist in the companies data."})

        
    return jsonify({'message': "Processing..."}) 