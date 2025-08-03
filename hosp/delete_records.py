import mysql.connector
import json
import os
from datetime import datetime

# Database connection details
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'omchalke2003',
    'database': 'appointment_bot'
}

TABLE_NAME = 'new_app'
JSON_FILE_PATH = 'data.json'

# Names of records to delete
RECORDS_TO_DELETE = [
    "Sita Mehta",
    "Pooja Rao",
    "Ravi Sharma",
    "Amit Joshi",
    "Rahul Kulkarni"
]

def delete_records_from_db_and_json():
    print(f"[{datetime.now()}] Starting deletion process...")
    
    # Connect to the database
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Delete records from database
        for name in RECORDS_TO_DELETE:
            try:
                query = f"DELETE FROM {TABLE_NAME} WHERE name = %s"
                cursor.execute(query, (name,))
                affected_rows = cursor.rowcount
                print(f"[{datetime.now()}] Deleted {affected_rows} record(s) for '{name}' from database")
            except mysql.connector.Error as err:
                print(f"[{datetime.now()}] Error deleting '{name}' from database: {err}")
        
        # Commit the changes
        conn.commit()
        print(f"[{datetime.now()}] Database changes committed successfully")
        
    except mysql.connector.Error as err:
        print(f"[{datetime.now()}] Database connection error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print(f"[{datetime.now()}] Database connection closed")
    
    # Update the JSON file
    try:
        # Read the current JSON file
        with open(JSON_FILE_PATH, 'r') as f:
            records = json.load(f)
        
        # Count records before deletion
        original_count = len(records)
        
        # Filter out the records to delete
        updated_records = [record for record in records if record['name'] not in RECORDS_TO_DELETE]
        
        # Count records after deletion
        new_count = len(updated_records)
        deleted_count = original_count - new_count
        
        # Write the updated records back to the JSON file
        with open(JSON_FILE_PATH, 'w') as f:
            json.dump(updated_records, f, indent=4)
        
        print(f"[{datetime.now()}] Removed {deleted_count} record(s) from JSON file")
        
    except Exception as e:
        print(f"[{datetime.now()}] Error updating JSON file: {e}")
    
    print(f"[{datetime.now()}] Deletion process completed")

if __name__ == "__main__":
    delete_records_from_db_and_json()