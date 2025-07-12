from flask import Flask, jsonify, request
import requests
import logging
from datetime import datetime
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

API2_URL = os.getenv('API2_URL', 'http://api2:5001')

@app.route('/api/message', methods=['GET'])
def get_message():
    try:
        logger.info(f"=== API1 REQUEST RECEIVED ===")
        logger.info(f"Timestamp: {datetime.now()}")
        logger.info(f"Client IP: {request.remote_addr}")
        logger.info(f"Request Method: {request.method}")
        logger.info(f"Request Path: {request.path}")
        
        logger.info(f"Forwarding request to API2 at: {API2_URL}")
        
        response = requests.get(f"{API2_URL}/api/hello", timeout=10)
        
        logger.info(f"=== API2 RESPONSE RECEIVED ===")
        logger.info(f"Status Code: {response.status_code}")
        logger.info(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            api2_data = response.json()
            
            result = {
                "status": "success",
                "message": "Request processed successfully",
                "api1_timestamp": datetime.now().isoformat(),
                "api2_response": api2_data,
                "request_flow": "User -> API1 -> API2 -> API1 -> User"
            }
            
            logger.info(f"=== SENDING RESPONSE TO USER ===")
            logger.info(f"Final Response: {result}")
            
            return jsonify(result), 200
        else:
            logger.error(f"API2 returned error: {response.status_code}")
            return jsonify({
                "status": "error",
                "message": f"API2 returned status {response.status_code}"
            }), 500
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to connect to API2: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to connect to API2"
        }), 503
    except Exception as e:
        logger.error(f"Unexpected error in API1: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    logger.info("Health check requested")
    return jsonify({"status": "healthy", "service": "API1"}), 200

if __name__ == '__main__':
    logger.info("Starting API1 service on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=True)