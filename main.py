import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import yfinance as yf
import numpy as np
import plotly.express as px
import pandas as pd

# Set up the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Stock Analysis Dashboard with Monte Carlo Simulation"),

    # Input components
    html.Div([
        html.Label("Enter Stock Symbol:"),
        dcc.Input(id='stock-input', type='text', value='AAPL'),
    ]),

    html.Div([
        html.Label("Select Historical Data Duration (days):"),
        dcc.Input(id='duration-input', type='number', value=365),
    ]),

    html.Div([
        html.Label("Enter Number of Simulations:"),
        dcc.Input(id='num-simulations-input', type='number', value=1000),
    ]),

    html.Div([
        html.Label("Select Confidence Level (%):"),
        dcc.Input(id='confidence-level-input', type='number', value=5),
    ]),

    # Output components
    dcc.Graph(id='histogram'),
    html.Div(id='var-output')
])

@app.callback(
    [Output('histogram', 'figure'),
     Output('var-output', 'children')],
    [Input('stock-input', 'value'),
     Input('duration-input', 'value'),
     Input('num-simulations-input', 'value'),
     Input('confidence-level-input', 'value')]
)
def update_graph(stock_name, duration, num_simulations, confidence_level):
    print(f"Starting callback with stock_name={stock_name}, duration={duration}, etc.")

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
        print("Callback completed successfully.")

        result = varval + " " + interpretation

        return fig, result
    
    except (KeyError, ValueError) as e:
        error_message = f"Error: {str(e)}"
        print(error_message)
        empty_dataframe = pd.DataFrame()  # Create an empty DataFrame
        empty_figure = px.histogram(empty_dataframe)
        return empty_figure, error_message


#Run the app
if __name__ == '__main__':
   
    server = app.server