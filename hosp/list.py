import mysql.connector
import json
import os
from datetime import datetime, date # Import date as well

# Database connection details
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'omchalke2003',
    'database': 'appointment_bot'
}

TABLE_NAME = 'new_app'
JSON_FILE_PATH = 'data.json'

def fetch_data_and_update_json():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = query = f"SELECT * FROM {TABLE_NAME} ORDER BY points DESC"
        cursor.execute(query)
        records = cursor.fetchall()

        processed_records = []
        for record in records:
            processed_record = {}
            for key, value in record.items():
                if isinstance(value, (datetime, date)):
                    processed_record[key] = value.isoformat()
                else:
                    processed_record[key] = value
            processed_records.append(processed_record)

        with open(JSON_FILE_PATH, 'w') as f:
            json.dump(processed_records, f, indent=4) 

        print(f"[{datetime.now()}] Data successfully written to {JSON_FILE_PATH}")

    except mysql.connector.Error as err:
        print(f"[{datetime.now()}] Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    fetch_data_and_update_json()