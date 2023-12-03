import dash
from display import StockDisplay
from business import StockBusiness

# Set up the Dash app
app = dash.Dash(__name__)
server = app.server

# Create instances of the classes
display = StockDisplay(app)
business = StockBusiness()

# Run the app
if __name__ == '__main__':
    app.run_server()
