from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/process_text', methods=['POST'])
def process_text():
    time.sleep(0.1)
    data = request.get_json()
    text = data.get('text', '')
    response_text = text + 'です。'
    app.logger.info(f"Received text: {text}")
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

