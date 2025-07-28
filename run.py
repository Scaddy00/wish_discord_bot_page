from app import create_app
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('config.env')

app = create_app()

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"Starting Flask app on {host}:{port}")
    print(f"Database path: {os.getenv('DATABASE_PATH')}")
    
    app.run(host=host, port=port, debug=debug) 