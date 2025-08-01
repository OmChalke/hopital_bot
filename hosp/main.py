from flask import Flask, jsonify, request, session,render_template,redirect,flash
import os
import json
import mysql.connector
import requests
from datetime import datetime, date
from flask import send_file


app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'omchalke2003',
    'database': 'appointment_bot'}

TABLE_NAME = 'new_app'
JSON_FILE_PATH = 'data.json'

def fetch_data_and_update_json():
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)

        query = f"SELECT * FROM {TABLE_NAME} ORDER BY points DESC"
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

latest_data={}

@app.route('/data.json')
def serve_data_json():
    return send_file('data.json', mimetype='application/json')

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('dash.html')
    
@app.route('/signup', methods=['GET'])
def signup_form():
    return render_template('signup.html')        

@app.route('/signup_submit', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not all([username, email, password, confirm_password]):
        return jsonify({"error": "All fields are required"}), 400

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400
    
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()


    cursor.execute(
    "SELECT username, email FROM admin1 WHERE username = %s OR email = %s",
    (username, email))

    existing_user = cursor.fetchone()
    if existing_user:
        if existing_user['username'] == username:
            return jsonify({"error": "Username already exists"}), 409
        else:
            return jsonify({"error": "Email already exists"}), 409


    insert_query = "INSERT INTO admin1 (username, email, password) VALUES (%s, %s, %s)"

    
    data = ( username, email,password)
    cursor.execute(insert_query, data)
    connection.commit()
    connection.close()   

    
    return redirect('/')

@app.route('/entry', methods=['GET'])
def entry_form():
    return render_template('entry.html')  

@app.route('/list', methods=['GET'])
def list_view():
    fetch_data_and_update_json()
    db = mysql.connector.connect(**mysql_config)
    cursor = db.cursor(dictionary=True)


    query = "SELECT * FROM new_app ORDER BY points DESC"
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('list.html', data= rows)

@app.route('/details', methods=['GET'])
def view():
    patient_id = request.args.get('id')

    with open(JSON_FILE_PATH, 'r') as f:
        patients = json.load(f)
  
    patient = None
    for p in patients:
        if str(p['id']) == patient_id:
            patient = p
            break
    
    
    if not patient:
        flash('Patient not found', 'error')
        return redirect('/list')
    
    return render_template('details.html', patient=patient) 

@app.route('/patient', methods=['POST'])
def entry():
    try:
        patient_name = request.form.get('patient_name')
        age = request.form.get('age')
        weight = request.form.get('weight')
        address = request.form.get('address')
        disease = request.form.get('disease')
        assigned_doctor = request.form.get('assigned_doctor')
        doctor_description = request.form.get('doctor_description')

        
        if not all([patient_name, age, assigned_doctor]):
            flash('Please fill all required fields (Name, Age, and Doctor are required)', 'error')
            return redirect(('/'))

        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        insert_query = """INSERT INTO entry1 
                         (patient_name, age, weight, address, disease, assigned_doctor, doctor_description) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        data = (patient_name, age, weight, address, disease, assigned_doctor, doctor_description)
        cursor.execute(insert_query, data)
        connection.commit()

        flash('Patient data successfully entered!', 'success')
        return redirect(('/success'))

    except mysql.connector.Error as err:
        flash(f'Database error: {err}', 'error')
        return redirect(('/'))

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
    
@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')

    
@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

@app.route('/login_submit', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()


    cursor.execute(
    "SELECT username, email FROM student1 WHERE username = %s OR email = %s",
    (username, password))

    existing_user = cursor.fetchone()

    if existing_user:
        session['user'] = username
        return jsonify({'message': 'login successfull'}), 401
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


latest_notification = {'message': '', 'status': False}

@app.route('/popup',methods=['GET'])
def popup():
    if latest_data:
        return render_template('new.html', name=latest_data['name'], date=latest_data['appointment_date'])
    return redirect('/')

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    # Create a more detailed notification message
    risk_level = data.get('risk_level', 'Unknown')
    problem = data.get('problem', 'Not specified')
    
    # Format the notification message with more details
    latest_notification['message'] = f"New {risk_level.lower()} appointment from {data['name']} for {problem}"
    latest_notification['status'] = True
    return jsonify({'success': True})

@app.route('/check_notification', methods=['GET'])
def check_notification():
    if latest_notification['status']:
        latest_notification['status'] = False 
        return jsonify({'notify': True, 'message': latest_notification['message']})
    return jsonify({'notify': False})

@app.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
        return jsonify({'message': 'Logout successful'})
    else:
        return jsonify({'message': 'No user is currently logged in'}), 400 
    


if __name__ == '__main__':
    app.run(debug=True,port=5001)

