from app import mysql

class Answererror:
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM answer_error")
        return cursor.fetchall()
    def getOne(self, id):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM answer_error WHERE id_answer_error ="+id)
        return cursor.fetchone()
    def store(self, pertanyaan, status):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO answer_error (pertanyaan, status) VALUES (%s, %s)", (pertanyaan, status))
        conn.commit()
        cursor.close()
    def destroy(self,id):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM answer_error WHERE id_answer_error = "+id)
        conn.commit()
        cursor.close()
    def update(self, id, pertanyaan, status):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE answer_error SET pertanyaan ='"+pertanyaan+"', status = '"+status+"' WHERE id_answer_error = "+id)
        conn.commit()
        cursor.close()