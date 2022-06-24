from app import mysql

class Testimoni:
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM testimoni")
        return cursor.fetchall()
    def getOne(self, id):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM testimoni WHERE id_testimoni ="+id)
        return cursor.fetchone()
    def store(self, nama, lulusan,pesan, foto):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO testimoni (nama, lulusan,pesan, foto) VALUES (%s, %s, %s, %s)", (nama, lulusan,pesan, foto))
        conn.commit()
        cursor.close()
    def destroy(self,id):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM testimoni WHERE id_testimoni = "+id)
        conn.commit()
        cursor.close()
    def update(self, id, nama, lulusan,pesan, foto):
        conn = mysql.connect()
        cursor = conn.cursor()
        if foto == 'sama':
            cursor.execute("UPDATE testimoni SET nama ='"+nama+"', lulusan = '"+lulusan+"',pesan = '"+pesan+"' WHERE id_testimoni = "+id)
        else:
            cursor.execute("UPDATE testimoni SET nama ='"+nama+"', lulusan = '"+lulusan+"',pesan = '"+pesan+"', foto = '"+foto+"' WHERE id_testimoni = "+id)
        conn.commit()
        cursor.close()
    def getCurrentFile(self, id_testimoni):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT foto FROM testimoni WHERE id_testimoni ="+id_testimoni)
        return cursor.fetchone()