import yfinance as yf
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox

def fetch_stock_data(ticker, start_date, end_date):
    """Fetch historical stock data for the given ticker and date range."""
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        if stock_data.empty:
            raise ValueError("No data found for the given ticker and date range.")
        return stock_data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch stock data: {e}")
        return None

def calculate_metrics(stock_data):
    """Calculate financial metrics like daily returns, volatility, and moving averages."""
    stock_data['Daily Return'] = stock_data['Close'].pct_change()
    stock_data['MA_20'] = stock_data['Close'].rolling(window=20).mean()
    stock_data['MA_50'] = stock_data['Close'].rolling(window=50).mean()
    volatility = stock_data['Daily Return'].std()
    return volatility

def plot_stock_data(stock_data, ticker):
    """Plot the stock's closing price and moving averages."""
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data['Close'], label='Closing Price', color='blue')
    plt.plot(stock_data['MA_20'], label='20-Day MA', color='green')
    plt.plot(stock_data['MA_50'], label='50-Day MA', color='red')
    plt.title(f'{ticker} Stock Price and Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.show()

def on_analyze_click():
    """Handle the Analyze button click event."""
    ticker = ticker_entry.get().strip()
    start_date = start_entry.get().strip()
    end_date = end_entry.get().strip()

    if not ticker or not start_date or not end_date:
        messagebox.showerror("Input Error", "Please provide all inputs: Ticker, Start Date, and End Date.")
        return

    stock_data = fetch_stock_data(ticker, start_date, end_date)
    if stock_data is None:
        return

    volatility = calculate_metrics(stock_data)
    messagebox.showinfo("Analysis Complete", f"Volatility: {volatility:.4f}")
    plot_stock_data(stock_data, ticker)

# Create the GUI
root = tk.Tk()
root.title("Stock Screener")

# Input fields
tk.Label(root, text="Ticker:").grid(row=0, column=0, padx=10, pady=5)
ticker_entry = tk.Entry(root)
ticker_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Start Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5)
start_entry = tk.Entry(root)
start_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="End Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
end_entry = tk.Entry(root)
end_entry.grid(row=2, column=1, padx=10, pady=5)

# Analyze button
analyze_button = tk.Button(root, text="Analyze", command=on_analyze_click)
analyze_button.grid(row=3, column=0, columnspan=2, pady=10)

# Run the GUI main loop
root.mainloop()
