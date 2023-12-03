import yfinance as yf
import numpy as np
import pandas as pd
import plotly.express as px

class StockBusiness:
    @staticmethod
    def calculate_var(stock_name, duration, num_simulations, confidence_level):
        try:
            # Fetch historical stock data
            data = yf.download(stock_name, period=f"{duration}d", interval='1d', progress=False)
            
            if data.empty:
                raise ValueError("No data available for the specified stock symbol.")
            
            # Calculate mean return and standard deviation
            mean_return = np.mean(data['Adj Close'].pct_change().dropna())
            std_dev = np.std(data['Adj Close'].pct_change().dropna())

            # Run Monte Carlo simulation
            simulations = np.random.normal(mean_return, std_dev, num_simulations)

            # Calculate VaR
            var = np.percentile(simulations, confidence_level)
            varval = f"VaR Value: {var}. "
            # Create histogram
            fig = px.histogram(simulations, title='Monte Carlo Simulation - Stock Returns Distribution')

            # Print interpretation for better readability
            interpretation = f"The daily returns for {stock_name} stock won't drop more than {abs(round(var,2))}% on {100-confidence_level} out of 100 days"
            result = varval + " " + interpretation

            return fig, result
        
        except (KeyError, ValueError) as e:
            error_message = f"Error: {str(e)}"
            print(error_message)
            empty_dataframe = pd.DataFrame()  # Create an empty DataFrame
            empty_figure = px.histogram(empty_dataframe)
            return empty_figure, error_message
