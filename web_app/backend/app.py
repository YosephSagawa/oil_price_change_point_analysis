from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load data
data = pd.read_csv('../data/raw/BrentOilPrices.csv')  # Updated path
data['Date'] = pd.to_datetime(data['Date'], format='%d-%b-%y')
events = pd.read_csv('data/events.csv')  # Updated path

# Mock change point data (replace with actual model output)
change_points = [{'date': '2020-03-15', 'mean_before': 50.0, 'mean_after': 30.0}]

@app.route('/prices', methods=['GET'])
def get_prices():
    return jsonify({
        'dates': data['Date'].dt.strftime('%Y-%m-%d').tolist(),
        'prices': data['Price'].tolist()
    })

@app.route('/change_points', methods=['GET'])
def get_change_points():
    return jsonify(change_points)

@app.route('/events', methods=['GET'])
def get_events():
    return jsonify({
        'dates': events['Event_Date'].tolist(),
        'descriptions': events['Event_Description'].tolist()
    })

if __name__ == '__main__':
    app.run(debug=True)