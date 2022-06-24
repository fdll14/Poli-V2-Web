import os
from flask_bcrypt import Bcrypt
from flaskext.mysql import MySQL
from flask_session import Session
import logging
from flask_restful import Api
from flask import Flask


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['AUTOGRAPH_VERBOSITY'] = '0'
logging.getLogger('tensorflow').setLevel(logging.FATAL)


app = Flask(__name__)
mysql = MySQL()
app.config['SECRET_KEY'] = 'super secret key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['UPLOAD_FOLDER'] = os.path.abspath('app/static/upload/fotogender')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
bcrypt = Bcrypt(app)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'poli'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
api = Api(app)

from app.models.gender_detection import gender
api.add_resource(gender, "/api/image", methods=["POST"])

from app.controllers import indexcontroller
from app.controllers import chatbotcontroller
from app.controllers import logincontroller
from app.controllers import admincontroller

if __name__ == '__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')

## cara menjalankan flask run --host=0.0.0.0