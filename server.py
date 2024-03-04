from flask import Flask, jsonify, request, Response, stream_with_context, redirect, url_for
import pandas as pd
import time
from flask_cors import CORS
from execute_trade import perform_trade  
from trade_strategy import tradestrategy  
app = Flask(__name__)
CORS(app, resources={r"/stream": {"origins": "*"}}, supports_credentials=True)

api_key = 'PKU420GBAGCAN6XJBV2Q'
secret_key = 'PuYPrkAmxyGLFXfWNylw6CNrn3Exs7JPivT1jZoJ'


tradestrategy()

@app.route('/')
def home():
    return redirect(url_for('static', filename='index.html'))

def stream_data():
    data = pd.read_csv('signals.csv', chunksize=1)  # Stream one row at a time
    for chunk in data:
        json_data = chunk.to_json(orient='records')
        print(json_data)  # Add this line to debug
        chunk_dict = chunk.iloc[0].to_dict()  # Convert the first (and only) row of the chunk to a dictionary
        print(chunk_dict)  # Debug print to see the actual data structure
        perform_trade(chunk_dict)  # Pass the dictionary, not the JSON string
        yield f"data:{json_data}\n\n"
        time.sleep(1)  

@app.route('/stream')
def stream_csv_data():
    response = Response(stream_with_context(stream_data()), mimetype='text/event-stream')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
