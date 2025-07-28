#!/usr/bin/env python3
"""
Debug script to diagnose environment variable loading issues
"""

import os
from dotenv import load_dotenv

def debug_env():
    print("=== ENVIRONMENT VARIABLES DEBUG ===\n")
    
    # Show working directory and script location
    print("1. Working directory and script location:")
    print(f"   📁 Current working directory: {os.getcwd()}")
    print(f"   📄 Script location: {os.path.abspath(__file__)}")
    
    # Check if config.env exists with different paths
    env_file = 'config.env'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    abs_env_file = os.path.join(base_dir, env_file)
    
    print(f"\n2. Checking config.env file...")
    print(f"   📁 Relative path: {env_file}")
    print(f"   📁 Absolute path: {abs_env_file}")
    
    # Check relative path
    if os.path.exists(env_file):
        print(f"   ✅ Relative path exists")
    else:
        print(f"   ❌ Relative path does not exist")
    
    # Check absolute path
    if os.path.exists(abs_env_file):
        print(f"   ✅ Absolute path exists")
        env_file = abs_env_file  # Use absolute path
    else:
        print(f"   ❌ Absolute path does not exist")
        return
    
    # Show file content
    print(f"\n3. Content of {env_file}:")
    try:
        with open(env_file, 'r') as f:
            content = f.read()
            print("   📄 File content:")
            for i, line in enumerate(content.split('\n'), 1):
                if line.strip() and not line.strip().startswith('#'):
                    print(f"   {i}: {line}")
    except Exception as e:
        print(f"   ❌ Error reading file: {e}")
        return
    
    # Load environment variables
    print(f"\n4. Loading environment variables...")
    try:
        load_dotenv(env_file)
        print("   ✅ load_dotenv() executed successfully")
    except Exception as e:
        print(f"   ❌ Error loading .env file: {e}")
        return
    
    # Check specific variables
    print(f"\n5. Environment variables:")
    variables = ['FLASK_HOST', 'FLASK_PORT', 'DATABASE_PATH', 'DEBUG']
    
    for var in variables:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: {value}")
        else:
            print(f"   ❌ {var}: Not set")
    
    # Check database file
    db_path = os.getenv('DATABASE_PATH')
    if db_path:
        print(f"\n6. Database file check:")
        if os.path.exists(db_path):
            print(f"   ✅ Database exists at: {db_path}")
            print(f"   📁 Size: {os.path.getsize(db_path)} bytes")
        else:
            print(f"   ❌ Database not found at: {db_path}")
    
    print(f"\n=== DEBUG COMPLETE ===")

if __name__ == '__main__':
    debug_env() 