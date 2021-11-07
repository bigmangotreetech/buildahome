from flask import Flask, render_template, redirect, request, session, flash, jsonify, send_from_directory
from flask_mysqldb import MySQL
import datetime
import time
from time import mktime
import os
import hashlib
import time
app = Flask(__name__)
# Sql setup
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'ABWorldUser'
app.config['MYSQL_PASSWORD'] = '0XR0MF*&jCKE'
app.config['MYSQL_DB'] = 'ef22yrqyi32q'
app.config['UPLOAD_FOLDER'] = 'images'
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024

mysql = MySQL(app)

app.secret_key = b'bAhSessionKey'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/enter_material', methods=['GET'])
def enter_material():
    return render_template('enter_material.html')

@app.route('/view_inventory', methods=['GET'])
def view_inventory():
    return render_template('view_inventory.html')

if __name__ == '__main__':
    app.run(debug=True)