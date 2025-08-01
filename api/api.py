from flask import Flask, jsonify, request, session,render_template,redirect
import requests
import os
import json
import mysql.connector


app = Flask(__name__)

def users():
    url="https://jsonplaceholder.typicode.com/users"
    print("data:",url)

    response= requests.get(url)
    json= response.json()
    
    all_users = []
    for i in json:
        user_info = {
            'name': i['name'],
            'username': i['username'],
            'email': i['email']
        }
        all_users.append(user_info)
        

    return all_users

@app.route('/info', methods=['GET'])
def user_information():
    user_data= users()

    return render_template('index.html',users=user_data)

if __name__ == '__main__':
    app.run(debug=True)