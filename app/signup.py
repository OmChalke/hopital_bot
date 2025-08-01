from flask import Flask, render_template, request, redirect, jsonify
import json
import os

app = Flask(__name__)
USERS_FILE = 'file2.json'

def read_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump([], f)

    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def write_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        data = "hello Om"
        return ({'data': data})

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
    
    users = read_users()
    for user in users:
        if not isinstance(user, dict):
            continue

        if user.get('username') == username:
            return jsonify({"error": "Username already exists"}), 409
        
        if user.get('email') == email:
            return jsonify({"error": "Email already exists"}), 409

    new_user = {
        'username': username,
        'email': email,
        'password': password
    }

    users.append(new_user)
    write_users(users)
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

