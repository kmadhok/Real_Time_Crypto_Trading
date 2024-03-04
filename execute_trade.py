from configparser import ConfigParser
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import OrderRequest
from alpaca.trading.enums import OrderSide, OrderType, OrderClass, TimeInForce
import csv

# Assume these are your API credentials (you should secure them, not hard-code them!)
api_key = 'PKU420GBAGCAN6XJBV2Q'
secret_key = 'PuYPrkAmxyGLFXfWNylw6CNrn3Exs7JPivT1jZoJ'

# Initialize the TradingClient
trading_client = TradingClient(
    api_key=api_key,
    secret_key=secret_key,
    paper=True
)

def perform_trade(data):
    """
    Perform a trade based on the given data.

    Parameters:
    data (dict): A dictionary containing the trade information, 
                 should include 'symbol', 'qty', 'side', 'type', and 'order_class'.
    """
    # Create the order request based on the data provided
    order_request = OrderRequest(
        symbol=data['symbol'],
        qty=float(data['qty']),
        side=OrderSide[data['side']],
        type=OrderType[data['type']],
        order_class=OrderClass[data['order_class']],
        time_in_force='ioc',  # You can make this dynamic as well based on your data structure
        extended_hours=False  # Same here, adjust as needed
    )

    # Submit the order
    order_submission_response = trading_client.submit_order(order_data=order_request)
    print(order_submission_response)
    return order_submission_response  # Return the response for further processing if needed

