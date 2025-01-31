from flask import Flask, request, jsonify
import gps
from threading import Thread

app = Flask(__name__)
port = 4000

# GPS function to find the current location of the device.
@app.route('/process_signals', methods=['POST'])
def process_signals():
    data = request.get_json()

    # Extract satellite positions and pseudoranges from the request
    satellite_data = data.get('satellite_data', [])
    pseudoranges = data.get('pseudoranges', [])

    # Ensure at least 4 satellites and pseudoranges are provided
    if not satellite_data or not pseudoranges or len(satellite_data) < 4 or len(pseudoranges) < 4:
        return jsonify({"error": "Insufficient data. At least 4 satellites are required."}), 400

    # Extract positions of the satellites
    satellite_positions = [sat['position'] for sat in satellite_data]

    # Perform trilateration to find the device's position
    try:
        # Assuming gps.trilaterate takes positions (lat, lon, alt) and pseudoranges
        device_position = gps.trilaterate(satellite_positions, pseudoranges)
        return jsonify({
            "device_position": {
                "latitude": device_position[0],
                "longitude": device_position[1],
                "altitude": device_position[2]
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Function to run the Flask app
def run_flask():
    print("Running app on port", port)
    app.run(debug=True, port=port)

# Your main function
def main():
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

main()
