from flask import Blueprint, request, jsonify
from app.models.database import DatabaseManager
import os

api = Blueprint('api', __name__)

# Initialize database manager
db_manager = DatabaseManager(os.getenv('DATABASE_PATH', '/Users/lorenzoscaduto/Desktop/wish_data.db'))

@api.route('/api/messages/<message_id>/toggle_maintain', methods=['POST'])
def toggle_message_maintain(message_id):
    """Toggle to_maintain field for a specific message"""
    try:
        data = request.get_json()
        
        # Extract message data from request
        timestamp = data.get('timestamp')
        channel_id = data.get('channel_id')
        user_id = data.get('user_id')
        message = data.get('message')
        to_maintain = data.get('to_maintain', False)
        
        if not all([timestamp, channel_id, user_id, message]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Update the database
        success = db_manager.update_message_maintain(timestamp, channel_id, user_id, message, to_maintain)
        
        if success:
            return jsonify({'success': True, 'to_maintain': to_maintain})
        else:
            return jsonify({'success': False, 'error': 'Failed to update message'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api.route('/api/messages/filter', methods=['GET'])
def filter_messages():
    """Get filtered messages data"""
    try:
        # Get filter parameters
        page = request.args.get('page', 1, type=int)
        channel_id = request.args.get('channel_id', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        user_filter = request.args.get('user_filter', '')
        to_maintain = request.args.get('to_maintain', 'all')
        
        filters = {
            'date_from': date_from,
            'date_to': date_to,
            'user_filter': user_filter,
            'to_maintain': to_maintain
        }
        
        # Get filtered data
        result = db_manager.get_messages_by_channel(channel_id, page, 50, filters)
        
        return jsonify({
            'success': True,
            'data': result['data'],
            'pagination': result
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api.route('/api/channels', methods=['GET'])
def get_channels():
    """Get all channels"""
    try:
        channels = db_manager.get_channels()
        return jsonify({'success': True, 'channels': channels})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        users = db_manager.get_users()
        return jsonify({'success': True, 'users': users})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api.route('/api/table/<table_name>/data', methods=['GET'])
def get_table_data(table_name):
    """Get filtered table data"""
    try:
        page = request.args.get('page', 1, type=int)
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        user_filter = request.args.get('user_filter', '')
        to_maintain = request.args.get('to_maintain', 'all')
        
        filters = {
            'date_from': date_from,
            'date_to': date_to,
            'user_filter': user_filter,
            'to_maintain': to_maintain
        }
        
        result = db_manager.get_table_data(table_name, page, 50, filters)
        
        return jsonify({
            'success': True,
            'data': result['data'],
            'pagination': result
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500 