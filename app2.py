from flask import Flask, jsonify, request
import logging
from datetime import datetime
import random
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

MESSAGES = [
    "Hello World from API2! 🌍",
    "Greetings from the backend service! 👋",
    "API2 is working perfectly! ✅",
    "Hello from the microservice architecture! 🏗️",
    "API2 responding with enthusiasm! 🚀"
]

@app.route('/api/hello', methods=['GET'])
def get_hello():
    try:
        logger.info(f"=== API2 REQUEST RECEIVED ===")
        logger.info(f"Timestamp: {datetime.now()}")
        logger.info(f"Source IP: {request.remote_addr}")
        logger.info(f"Request Method: {request.method}")
        logger.info(f"Request Path: {request.path}")
        logger.info(f"User Agent: {request.headers.get('User-Agent', 'Unknown')}")
        
        processing_time = random.uniform(0.1, 0.5)
        logger.info(f"Simulating processing time: {processing_time:.2f} seconds")
        time.sleep(processing_time)
        
        selected_message = random.choice(MESSAGES)
        
        response_data = {
            "message": selected_message,
            "timestamp": datetime.now().isoformat(),
            "service": "API2",
            "port": 5001,
            "processing_time_seconds": round(processing_time, 2),
            "request_id": f"req_{int(time.time())}_{random.randint(1000, 9999)}",
            "server_info": {
                "version": "1.0.0",
                "environment": "docker",
                "status": "operational"
            },
            "additional_data": {
                "random_number": random.randint(1, 100),
                "server_uptime": "Container started recently",
                "api_version": "v1"
            }
        }
        
        logger.info(f"=== SENDING RESPONSE TO API1 ===")
        logger.info(f"Response Message: {selected_message}")
        logger.info(f"Processing completed in {processing_time:.2f} seconds")
        logger.info(f"Request ID: {response_data['request_id']}")
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error in API2: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal server error in API2",
            "service": "API2",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    logger.info("Health check requested for API2")
    return jsonify({
        "status": "healthy", 
        "service": "API2",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/api/status', methods=['GET'])
def get_status():
    logger.info("Status check requested")
    return jsonify({
        "service": "API2",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "endpoints": ["/api/hello", "/health", "/api/status"]
    }), 200

if __name__ == '__main__':
    logger.info("Starting API2 service on port 5001")
    app.run(host='0.0.0.0', port=5001, debug=True)