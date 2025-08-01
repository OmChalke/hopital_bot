from flask import Flask, jsonify, request, session,render_template,redirect
import os
import json
import mysql.connector


app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'omchalke2003',
    'database': 'om_database'}


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        data = "hello Om"
        return jsonify({'data': data})
    
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
    "SELECT username, email FROM student1 WHERE username = %s OR email = %s",
    (username, email))

    existing_user = cursor.fetchone()
    if existing_user:
        if existing_user['username'] == username:
            return jsonify({"error": "Username already exists"}), 409
        else:
            return jsonify({"error": "Email already exists"}), 409


    insert_query = "INSERT INTO student1 (username, email, password) VALUES (%s, %s, %s)"


    data = ( username, email,password)
    cursor.execute(insert_query, data)
    connection.commit()
    connection.close()   

    
    return redirect('/')

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

@app.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
        return jsonify({'message': 'Logout successful'})
    else:
        return jsonify({'message': 'No user is currently logged in'}), 400 


if __name__ == '__main__':
    app.run(debug=True)

