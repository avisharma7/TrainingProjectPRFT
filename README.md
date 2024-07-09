# Stock Market Analysis Project

## Overview

This project focuses on analyzing stock market data retrieved from an API and stored in CSV format. The primary operations revolve around CRUD (Create, Read, Update, Delete) functionalities applied to stock data. The analysis includes comparing daily, weekly, and monthly stock prices and visualizing them based on user input, specifically the company name.

## Technologies Used

- **Data Retrieval:** yfinance API
- **Data Storage:** MySQL
- **Data Manipulation:** Pandas
- **Backend Development:** Flask (for creating a RESTful API)
- **Visualization:** Matplotlib, Plotly (for graphs and tables)

## Features

- **Data Fetching:** Retrieve stock data using yfinance API and convert it into CSV format.
  
- **CRUD Operations:**
  - **Create:** Insert new stock data into the MySQL database.
  - **Read:** Retrieve stock data from MySQL based on user queries (e.g., company name, date range).
  - **Update:** Update existing stock data (e.g., correct errors, adjust for splits).
  - **Delete:** Remove outdated or irrelevant stock data.

- **Comparative Analysis:**
  - Compare daily, weekly, and monthly stock prices.
  - Calculate and visualize metrics such as moving averages, RSI, and MACD.

- **Visualization:**
  - Generate graphs and tables based on user input (company name).
  - Use Matplotlib and Plotly for interactive and static visualizations.


