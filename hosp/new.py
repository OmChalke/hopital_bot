@app.route('/patient', methods=['POST'])
def signup():
    patient_name = request.form.get('patient_name')
    age = request.form.get('age')
    weight = request.form.get('weight')
    address = request.form.get('address')
    disease = request.form.get('disease')
    assigned_doctor = request.form.get('assigned_doctor')
    doctor_description = request.form.get('doctor_description')

    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    insert_query = "INSERT INTO entry (patient_name,age,weight,address,disease,assigned_doctor,doctor_description) VALUES (%s, %s, %s)"


    data = (patient_name,age,weight,address,disease,assigned_doctor,doctor_description )
    cursor.execute(insert_query, data)
    connection.commit()
    connection.close()