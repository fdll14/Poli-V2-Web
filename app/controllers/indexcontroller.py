from flask import render_template
from app import app
import os
from app.models.testimoni import Testimoni

@app.route('/', methods = ['GET'])
def index():
	testimoni = Testimoni()
	
	data = {
		'testimoni': testimoni.get()
	}
	return render_template('index.html', data=data)