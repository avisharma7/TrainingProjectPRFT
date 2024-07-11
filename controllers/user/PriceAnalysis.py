from flask import request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_prices(price_type):
    try:
        data = request.get_json()
        f1 = data.get('file1').split('_')[0]
        f2 = data.get('file2').split('_')[0]
        file1 = data['file1']
        file2 = data['file2']
        
        if not os.path.exists(file1) or not os.path.exists(file2):
            return jsonify({'error': 'One or both of the files do not exist'}), 404

        # Read CSV files into pandas DataFrames
        df1 = pd.read_csv(file1, parse_dates=['Date'], index_col='Date')
        df2 = pd.read_csv(file2, parse_dates=['Date'], index_col='Date')
        
        # Sort dataframes by Date (if not already sorted)
        df1 = df1.sort_index()
        df2 = df2.sort_index()
        
        # Check if price_type exists in DataFrames
        if price_type not in df1.columns or price_type not in df2.columns:
            return jsonify({'error': f'Price type {price_type} is not a valid column in the data'}), 400

        # Plot daily prices
        plt.figure(figsize=(14, 7))
        plt.plot(df1.index, df1[price_type], label=f1, marker='o')
        plt.plot(df2.index, df2[price_type], label=f2, marker='o')
        
        plt.title(f'Daily {price_type.capitalize()} Prices Comparison')
        plt.xlabel('Date')
        plt.ylabel(f'{price_type.capitalize()} Price ($)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        plt.show()
        
        # Resample to weekly data
        df1_weekly = df1.resample('W').mean()
        df2_weekly = df2.resample('W').mean()
        
        # Plot weekly prices
        plt.figure(figsize=(14, 7))
        plt.plot(df1_weekly.index, df1_weekly[price_type], label=f1, marker='o')
        plt.plot(df2_weekly.index, df2_weekly[price_type], label=f2, marker='o')
        
        plt.title(f'Weekly {price_type.capitalize()} Prices Comparison')
        plt.xlabel('Date')
        plt.ylabel(f'{price_type.capitalize()} Price ($)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        plt.show()
        
        return jsonify({"message": "Processing..."})
    
    except KeyError as e:
        return jsonify({'error': f'Missing key in the data: {str(e)}'}), 400
    except pd.errors.EmptyDataError:
        return jsonify({'error': 'One of the CSV files is empty or cannot be read'}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
