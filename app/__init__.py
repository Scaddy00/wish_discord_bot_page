from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    """Application factory for Flask app"""
    # Load environment variables
    load_dotenv('config.env')
    
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['DATABASE_PATH'] = os.getenv('DATABASE_PATH', '/Users/lorenzoscaduto/Desktop/wish_data.db')
    
    # Register blueprints
    from app.routes import main, api
    app.register_blueprint(main)
    app.register_blueprint(api)
    
    return app 