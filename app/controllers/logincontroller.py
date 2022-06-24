from flask import ( render_template, url_for, request, redirect, session, flash)
from app import app
from app.models.user import User

import hashlib


@app.route('/login', methods=['GET'])
def login():
    if not session.get('id'):
        return render_template('login.html')
    else:
        return redirect(url_for('admin'))


@app.route('/login/proses', methods=['POST'])
def proses():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        user = User()
        account = user.getOne(username)
        
        if account:
            if account[2] == hashlib.md5(password.encode()).hexdigest():
                session['id'] = account[0]
                user = User()
                session['user'] = account
                session['login'] = True
                flash("Selamat Datang")
                return redirect(url_for('admin'))
            else:
                flash("Password salah")
                return redirect(url_for('login'))
        else:
            flash("Pengguna tidak ditemukan")
            return redirect(url_for('login'))
            
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

