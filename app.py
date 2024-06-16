import json
import logging
from flask import Flask, request, render_template_string
from threading import Lock
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Path to the JSON file
JSON_FILE_PATH = 'approval_response.json'
# Lock for thread safety
lock = Lock()

logging.basicConfig(level=logging.DEBUG)

def read_responses():
    try:
        with open(JSON_FILE_PATH, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_responses(responses):
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(responses, file, indent=4)

@app.route('/approve', methods=['GET'])
def approve():
    user_response = request.args.get('response')
    browser = request.args.get('browser')
    ip_address = request.args.get('ip_address')
    logging.debug(f"Received response: {user_response}, browser: {browser}, IP: {ip_address}")
    if user_response in ['yes', 'no']:
        lock.acquire()
        try:
            responses = read_responses()
            responses.append({'response': user_response, 'browser': browser, 'ip_address': ip_address})
            write_responses(responses)
        finally:
            lock.release()
        
        if user_response == 'yes':
            message = "Thank you for your Approval. Your response has been recorded."
        else:
            message = "Thank you for your Response."
        
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background-color: #f9f9f9;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    width: 100%;
                    padding: 20px;
                    background-color: #f9f9f9;
                    display: flex;
                    justify-content: center;
                }
                .content {
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    max-width: 600px;
                    width: 100%;
                }
                .header {
                    text-align: center;
                    margin-bottom: 20px;
                }
                .header h1 {
                    color: #5e0dac;
                }
                .message {
                    text-align: center;
                    margin-bottom: 20px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="content">
                    <div class="header">
                        <h1>Welcome to Easework AI</h1>
                    </div>
                    <div class="message">
                        <p><b>{{ message }}</b></p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """, message=message), 200
    else:
        return "Invalid response", 400

@app.route('/responses', methods=['GET'])
def view_responses():
    responses = read_responses()
    # Format the responses for display
    formatted_responses = '<br>'.join([f"Response: {resp['response']}, Browser: {resp['browser']}, IP: {resp['ip_address']}" for resp in responses])
    return formatted_responses, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
