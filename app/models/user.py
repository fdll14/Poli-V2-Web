from app import mysql

class User:
	def getOne(self, username):
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM user WHERE username ='"+username+"'")
		return cursor.fetchone()	
	def store(self, username, password, email, nama):
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("INSERT INTO user (username, password, email, nama) VALUES (%s, %s, %s, %s, %s)", (username, password, email, nama))
		conn.commit()
		cursor.close()
	def getOneId(self, id):
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT role FROM user WHERE id_user ='"+id+"'")
		return cursor.fetchone()