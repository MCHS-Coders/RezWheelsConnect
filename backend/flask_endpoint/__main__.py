from flask import Flask, request, jsonify
from assets import gps
from assets.p2p import p2p_manager
from threading import Thread

app = Flask(__name__)
port = 4000

# In-memory dictionary for registered clients (UUID → Address)
clients = {}

# GPS function to find the current location of the device.
@app.route('/process_signals', methods=['POST'])
def process_signals():
    data = request.get_json()

    # Debugging output to see the raw data received
    print("Raw data received:", data)

    satellite_data = data.get('satellite_data', [])
    pseudoranges = data.get('pseudoranges', [])

    # Debugging output to check the extracted values
    print("Extracted satellite_data:", satellite_data)
    print("Extracted pseudoranges:", pseudoranges)

    if not satellite_data or not pseudoranges or len(satellite_data) < 4 or len(pseudoranges) < 4:
        return jsonify({"error": "Insufficient data. At least 4 satellites are required."}), 400

    # Reformat satellite data to include time in the correct order (x, y, z, time)
    try:
        reformatted_satellite_data = [
            [sat['position'][0], sat['position'][1], sat['position'][2], sat['time']]  # [x, y, z, time]
            for sat in satellite_data
        ]
    except KeyError as e:
        return jsonify({"error": f"Missing key in satellite data: {str(e)}"}), 400

    # Debugging output for the reformatted satellite data
    print("Reformatted satellite data:", reformatted_satellite_data)

    # Now perform trilateration with the reformatted data
    try:
        # Perform trilateration to find the device's position using all satellite data and pseudoranges
        device_position = gps.trilaterate(reformatted_satellite_data, pseudoranges)
        return jsonify({
            "device_position": {
                "latitude": device_position[0],
                "longitude": device_position[1],
                "altitude": device_position[2]
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/register', methods=['POST'])
def register():
    """Register a new client and assign a UUID."""
    data = request.json
    client_address = data.get('client_address')

    if not client_address:
        return jsonify({"error": "Invalid data. Address is required."}), 400

    client_uuid = p2p_manager.register_user(client_address)
    clients[client_uuid] = client_address  # Store in in-memory dictionary

    return jsonify({"uuid": client_uuid, "message": "Client registered successfully."}), 200


@app.route('/send_message', methods=['POST'])
def send_message():
    """Send a message to a specific client using UUID."""
    data = request.json
    sender_uuid = data.get('sender_uuid')
    receiver_uuid = data.get('receiver_uuid')
    message = data.get('message')

    if not sender_uuid or not receiver_uuid or not message:
        return jsonify({"error": "Invalid data. Missing sender_uuid, receiver_uuid, or message."}), 400

    try:
        response = p2p_manager.send_message(sender_uuid, receiver_uuid, message)
        return jsonify(response), 200
    except Exception as e:
        print(f"[ERROR] Message Sending Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/get_messages', methods=['POST'])
def get_messages():
    """Retrieve all messages for a given UUID."""
    data = request.json
    user_uuid = data.get('user_uuid')

    if not user_uuid:
        return jsonify({"error": "UUID is required."}), 400

    try:
        messages = p2p_manager.get_messages(user_uuid)
        return jsonify({"messages": messages}), 200
    except Exception as e:
        print(f"[ERROR] Message Retrieval Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/clients', methods=['GET'])
def get_clients():
    """Get the list of registered clients."""
    return jsonify(clients), 200


# Function to run the Flask app
def run_flask():
    print(f"[INFO] Running app on port {port}")
    app.run(debug=True, port=port)


if __name__ == "__main__":
    run_flask()
