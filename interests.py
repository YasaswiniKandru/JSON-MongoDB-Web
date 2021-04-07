from flask import Flask, json, request
from flask_cors import CORS
import mysql.connector

app = Flask('__name__')
CORS(app)


@app.route('/webforms/insert', methods=['GET', 'POST'])
def insertdata():
	if request.method == 'POST':
		result = request.form.to_dict()
		intiliazedbfile(result)


def intiliazedbfile(data):
	mydb = mysql.connector.connect(
		host="localhost",
		user="raj",
		password="r123",
		database="raj")
	mycursor = mydb.cursor()
	sql = "INSERT INTO main_table (sno,firstname,lastname,status,semester) VALUES (%s,%s,%s,%s,%s)"
	val = (data["sno"], data["firstname"], data["lastname"], data["status"], data["semester"])
	mycursor.execute(sql, val)
	mydb.commit()
	print(mycursor.rowcount, "record inserted")
	sql = "INSERT INTO checkbox (courses,sno) VALUES (%s,%s)"
	val = (data["courses"], data["sno"])
	mycursor.execute(sql, val)
	mydb.commit()
	print(mycursor.rowcount, "record inserted")

@app.route('/webforms/display', methods=['GET', 'POST'])
def displaydata():
	if request.method == 'GET':
		mydb = mysql.connector.connect(
			host="localhost",
			user="raj",
			password="r123",
			database="raj")
		mycursor = mydb.cursor()
		main_dict = {}
		mycursor.execute("SHOW TABLES")
		db_tables = mycursor.fetchall()
		db_tables = [i[0] for i in db_tables]
		main_dict["databases"] = db_tables
		for db_table in db_tables:
			mycursor.execute("DESCRIBE " + db_table)
			db_schema_data = mycursor.fetchall()
			db_schema_data = [i[0] for i in db_schema_data]
			main_dict[db_table] = [db_schema_data]
			y = "SELECT * from " + db_table + ";"
			mycursor.execute(y)
			db_data = mycursor.fetchall()
			for data in db_data:
				main_dict[db_table].append(data)
		return json.dumps(main_dict)



if __name__ == '__main__':
	app.run(host="localhost", port=5000)