from app import mysql

class Gender:
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gender")
        return cursor.fetchall()
    def getOne(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gender WHERE id_gender = 1")
        return cursor.fetchone()
    def update(self, id,gender):
        conn = mysql.connect()
        cursor = conn.cursor()
        id = 1
        cursor.execute("UPDATE gender SET pertanyaan ='"+gender+"' WHERE id_gender = "+id)
        conn.commit()
        cursor.close()