from app import mysql

class History:
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history_mobile")
        return cursor.fetchall()
    def getOne(self, id):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history_mobile WHERE id_history ="+id)
        return cursor.fetchone()
    def store(self, hasil_gender, foto):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO history_mobile (hasil_gender, foto) VALUES (%s, %s, %s, %s)", (hasil_gender, foto))
        conn.commit()
        cursor.close()
    def update(self, id, hasil_gender, foto):
        conn = mysql.connect()
        cursor = conn.cursor()
        if foto == 'sama':
            cursor.execute("UPDATE history_mobile SET nama ='"+hasil_gender+"' WHERE id_history = "+id)
        else:
            cursor.execute("UPDATE history_mobile SET gender ='"+hasil_gender+"', foto = '"+foto+"' WHERE id_history = "+id)
        conn.commit()
        cursor.close()
    def getCurrentFile(self, id_history):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT foto FROM history_mobile WHERE id_history ="+id_history)
        return cursor.fetchone()