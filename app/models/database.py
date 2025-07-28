import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def get_tables(self) -> List[str]:
        """Get all table names from database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            return [row[0] for row in cursor.fetchall()]
    
    def get_table_schema(self, table_name: str) -> List[Dict[str, str]]:
        """Get table schema/columns"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = []
            for row in cursor.fetchall():
                columns.append({
                    'name': row[1],
                    'type': row[2],
                    'notnull': row[3],
                    'default': row[4],
                    'pk': row[5]
                })
            return columns
    
    def get_table_data(self, table_name: str, page: int = 1, per_page: int = 50, 
                      filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get paginated table data with optional filters"""
        offset = (page - 1) * per_page
        
        # Build query with filters
        query = f"SELECT * FROM {table_name}"
        count_query = f"SELECT COUNT(*) FROM {table_name}"
        params = []
        
        if filters:
            where_conditions = []
            for key, value in filters.items():
                if value and value != '':
                    if key == 'date_from' and value:
                        where_conditions.append("timestamp >= ?")
                        params.append(value)
                    elif key == 'date_to' and value:
                        where_conditions.append("timestamp <= ?")
                        params.append(value)
                    elif key == 'user_filter' and value:
                        where_conditions.append("user_name LIKE ?")
                        params.append(f"%{value}%")
                    elif key == 'to_maintain' and value != 'all':
                        where_conditions.append("to_maintain = ?")
                        params.append(value)
            
            if where_conditions:
                query += " WHERE " + " AND ".join(where_conditions)
                count_query += " WHERE " + " AND ".join(where_conditions)
        
        query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
        params.extend([per_page, offset])
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get total count
            cursor.execute(count_query, params[:-2] if params else [])
            total_count = cursor.fetchone()[0]
            
            # Get data
            cursor.execute(query, params)
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            data = []
            for row in rows:
                data.append(dict(zip(columns, row)))
        
        return {
            'data': data,
            'total': total_count,
            'page': page,
            'per_page': per_page,
            'total_pages': (total_count + per_page - 1) // per_page
        }
    
    def get_messages_by_channel(self, channel_id: str = None, page: int = 1, 
                               per_page: int = 50, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get messages filtered by channel with pagination"""
        if not channel_id:
            return self.get_table_data('messages', page, per_page, filters)
        
        offset = (page - 1) * per_page
        
        query = "SELECT * FROM messages WHERE channel_id = ?"
        count_query = "SELECT COUNT(*) FROM messages WHERE channel_id = ?"
        params = [channel_id]
        
        if filters:
            for key, value in filters.items():
                if value and value != '':
                    if key == 'date_from' and value:
                        query += " AND timestamp >= ?"
                        count_query += " AND timestamp >= ?"
                        params.append(value)
                    elif key == 'date_to' and value:
                        query += " AND timestamp <= ?"
                        count_query += " AND timestamp <= ?"
                        params.append(value)
                    elif key == 'user_filter' and value:
                        query += " AND user_name LIKE ?"
                        count_query += " AND user_name LIKE ?"
                        params.append(f"%{value}%")
                    elif key == 'to_maintain' and value != 'all':
                        query += " AND to_maintain = ?"
                        count_query += " AND to_maintain = ?"
                        params.append(value)
        
        query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
        params.extend([per_page, offset])
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get total count
            cursor.execute(count_query, params[:-2])
            total_count = cursor.fetchone()[0]
            
            # Get data
            cursor.execute(query, params)
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            data = []
            for row in rows:
                data.append(dict(zip(columns, row)))
        
        return {
            'data': data,
            'total': total_count,
            'page': page,
            'per_page': per_page,
            'total_pages': (total_count + per_page - 1) // per_page
        }
    
    def get_channels(self) -> List[Dict[str, str]]:
        """Get all unique channels from messages table"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT channel_id, channel_name, COUNT(*) as message_count
                FROM messages 
                GROUP BY channel_id, channel_name
                ORDER BY message_count DESC
            """)
            channels = []
            for row in cursor.fetchall():
                channels.append({
                    'channel_id': row[0],
                    'channel_name': row[1],
                    'message_count': row[2]
                })
            return channels
    
    def get_users(self) -> List[str]:
        """Get all unique user names from messages table"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT user_name FROM messages ORDER BY user_name")
            return [row[0] for row in cursor.fetchall()]
    
    def update_message_maintain(self, timestamp: str, channel_id: str, user_id: str, 
                              message: str, to_maintain: bool) -> bool:
        """Update to_maintain field for a specific message"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE messages 
                    SET to_maintain = ? 
                    WHERE timestamp = ? AND channel_id = ? AND user_id = ? AND message = ?
                """, (str(to_maintain), timestamp, channel_id, user_id, message))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating message: {e}")
            return False
    
    def get_table_stats(self) -> Dict[str, int]:
        """Get record count for all tables"""
        stats = {}
        with self.get_connection() as conn:
            cursor = conn.cursor()
            tables = self.get_tables()
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                stats[table] = cursor.fetchone()[0]
        return stats 