import mysql.connector


mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'omchalke2003',
    'database': 'appointment_bot'
}


db = mysql.connector.connect(**mysql_config)
cursor = db.cursor()


query = "SELECT * FROM new_app ORDER BY points DESC"
cursor.execute(query)
rows = cursor.fetchall()

cursor.close()
db.close()
