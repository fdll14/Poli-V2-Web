from app import mysql

class Dataset:
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM question")
        return cursor.fetchall()
    def getOne(self, id):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM question WHERE id_question ="+id)
        return cursor.fetchone()
    def destroy(self,id):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM question WHERE id_question = "+id)
        conn.commit()
        cursor.close()
    def update(self, id, tag, pattern, response,context ):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE question SET tag ='"+tag+"', patterns = '"+pattern+"', responses = '"+response+"',context = '"+context+"' WHERE id_question = "+id)
        conn.commit()
        cursor.close()
    def get_json(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT tag, patterns, responses, context FROM question")
        result = cursor.fetchall()
        num_fields = len(cursor.description)
        thisdict = []
        field_names = [i[0]
            for i in cursor.description
        ]
        for idx, res in enumerate(result):
            thisdict.append( {
                field_names[0] : res[0],
                field_names[1] : res[1].split(','),
                field_names[2] : res[2].split(','),
                field_names[3] : res[3]
            } )
        json_res = { 'intents' : thisdict }

        return json_res

    def store(self, tag, pattern, response, context):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO question (tag, patterns, responses, context) VALUES (%s, %s, %s, %s)", (tag, pattern, response, context))
        conn.commit()
        cursor.close()