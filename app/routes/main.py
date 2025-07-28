from flask import Blueprint, render_template, request, jsonify
from app.models.database import DatabaseManager
import os

main = Blueprint('main', __name__)

# Initialize database manager
db_manager = DatabaseManager(os.getenv('DATABASE_PATH', '/path/to/wish_data.db'))

@main.route('/')
def index():
    """Dashboard with table overview"""
    try:
        tables = db_manager.get_tables()
        stats = db_manager.get_table_stats()
        
        table_info = []
        for table in tables:
            table_info.append({
                'name': table,
                'count': stats.get(table, 0),
                'url': f'/table/{table}'
            })
        
        return render_template('index.html', tables=table_info)
    except Exception as e:
        return render_template('error.html', error=str(e))

@main.route('/table/<table_name>')
def table_view(table_name):
    """View for specific table with filters"""
    try:
        # Get filters from request
        page = request.args.get('page', 1, type=int)
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        user_filter = request.args.get('user_filter', '')
        to_maintain = request.args.get('to_maintain', 'all')
        type_filter = request.args.get('type_filter', 'all')
        status_filter = request.args.get('status_filter', 'all')
        command_filter = request.args.get('command_filter', 'all')
        
        filters = {
            'date_from': date_from,
            'date_to': date_to,
            'user_filter': user_filter,
            'to_maintain': to_maintain,
            'type_filter': type_filter,
            'status_filter': status_filter,
            'command_filter': command_filter
        }
        
        # Get table data
        result = db_manager.get_table_data(table_name, page, 50, filters)
        
        # Get table schema for column names
        schema = db_manager.get_table_schema(table_name)
        
        # Get unique type values if type column exists
        type_values = []
        if any(col['name'] == 'type' for col in schema):
            type_values = db_manager.get_unique_values(table_name, 'type')
        
        # Get unique status values if status column exists
        status_values = []
        if any(col['name'] == 'status' for col in schema):
            status_values = db_manager.get_unique_values(table_name, 'status')
        
        # Get unique command values if command column exists
        command_values = []
        if any(col['name'] == 'command' for col in schema):
            command_values = db_manager.get_unique_values(table_name, 'command')
        
        return render_template('table_view.html', 
                             table_name=table_name,
                             data=result['data'],
                             pagination=result,
                             schema=schema,
                             filters=filters,
                             type_values=type_values,
                             status_values=status_values,
                             command_values=command_values)
    except Exception as e:
        return render_template('error.html', error=str(e))

@main.route('/messages')
def messages_view():
    """Special messages view with chat interface"""
    try:
        # Get filters from request
        page = request.args.get('page', 1, type=int)
        channel_id = request.args.get('channel_id', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        user_filter = request.args.get('user_filter', '')
        to_maintain = request.args.get('to_maintain', 'all')
        text_filter = request.args.get('text_filter', '')
        
        filters = {
            'date_from': date_from,
            'date_to': date_to,
            'user_filter': user_filter,
            'to_maintain': to_maintain,
            'text_filter': text_filter
        }
        
        # Get channels for sidebar
        channels = db_manager.get_channels()
        
        # Get users for filter dropdown
        users = db_manager.get_users()
        
        # Get messages data
        if channel_id:
            result = db_manager.get_messages_by_channel(channel_id, page, 50, filters)
        else:
            result = db_manager.get_messages_by_channel(None, page, 50, filters)
        
        return render_template('messages.html',
                             messages=result['data'],
                             channels=channels,
                             users=users,
                             selected_channel=channel_id,
                             pagination=result,
                             filters=filters)
    except Exception as e:
        return render_template('error.html', error=str(e)) 