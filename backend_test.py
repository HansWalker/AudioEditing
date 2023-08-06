from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/send-data', methods=['POST'])
def receive_data():
    data = request.json  # Assuming data is sent as JSON
    # Process the data
    response = {"message": "Data received successfully"}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='localhost', port=5000)