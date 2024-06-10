from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pickle
import numpy as np
import os

app = Flask(__name__)

app.secret_key = 'xyzsdfg'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sistemair'

mysql = MySQL(app)

picFolder = os.path.join('static', 'pics')

app.config['UPLOUD_FOLDER'] = picFolder

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
        name = request.form['name']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Cek apakah akun adalah akun admin
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (name, password,))
        admin = cursor.fetchone()
        if admin:
            session['loggedin'] = True
            session['admin'] = True
            session['username'] = name
            mesage = 'Admin logged in successfully!'
            return render_template('admin.html', mesage=mesage)
        
        # Jika bukan akun admin, cek apakah akun adalah akun pengguna biasa
        cursor.execute('SELECT * FROM user WHERE nama = %s AND password = %s', (name, password,))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['id']
            session['name'] = user['nama']
            mesage = 'Logged in successfully!'

            pic1 = os.path.join(app.config["UPLOUD_FOLDER"], 'water.png')
            pic2 = os.path.join(app.config["UPLOUD_FOLDER"], 'water2.png')
            pic3 = os.path.join(app.config["UPLOUD_FOLDER"], 'contact.png')
            return render_template('user.html', mesage=mesage, user_image = pic1, user_image2 = pic2, user_image3 = pic3)

        mesage = 'Please enter correct name / password!'
    return render_template('login.html', mesage=mesage)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('name', None)
    session.pop('admin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
        name = request.form['name']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE nama = %s', (name,))
        account = cursor.fetchone()
        if account:
            mesage = 'User account already exists!'
        else:
            cursor.execute('INSERT INTO user (nama, password) VALUES (%s, %s)', (name, password,))
            mysql.connection.commit()
            mesage = 'User account registered successfully!'
    elif request.method == 'POST':
        mesage = 'Please fill out the form!'
    return render_template('register.html', mesage=mesage)

# Muat model SVM dari file
with open('svm_model.pkl', 'rb') as model_file:
    svm_model = pickle.load(model_file)

@app.route('/testing', methods=['GET', 'POST'])
def testing():
    prediction_text = ''
    if request.method == 'POST':
        ph = request.form['ph']
        solids = request.form['solids']
        conductivity = request.form['Conductivity']
        
        # Simpan data ke dalam basis data MySQL
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO kualitasair (ph, solids, conductivity) VALUES (%s, %s, %s)', (ph, solids, conductivity,))
        mysql.connection.commit()
        
        # Siapkan data untuk prediksi
        input_data = np.array([[ph, solids, conductivity]], dtype=float)
        
        # Lakukan prediksi dengan model SVM
        prediction = svm_model.predict(input_data)

         # Interpretasi hasil prediksi
        if prediction[0] == 1:
            prediction_result = "Air dapat diminum."
        else:
            prediction_result = "Air tidak dapat diminum."
        
        prediction_text = f"Prediksi: {prediction_result}"
    
    return render_template('testing.html', prediction_text=prediction_text)

@app.route('/user')
def user():
    if 'loggedin' in session and session['loggedin']:
        return render_template('user.html', name=session.get('name'))
    else:
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
