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
app.config['MYSQL_USER'] = 'buildahome'
app.config['MYSQL_PASSWORD'] = 'build*2019'
app.config['MYSQL_DB'] = 'buildahome2016'
app.config['UPLOAD_FOLDER'] = 'images'
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024

mysql = MySQL(app)

app.secret_key = b'bAhSessionKey'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/enter_material', methods=['GET', 'POST'])
def enter_material():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        query = "SELECT project_id, project_name, project_number FROM projects"
        cur.execute(query)
        projects = cur.fetchall()
        return render_template('enter_material.html', projects=projects)
    else:
        material = request.form['material']
        description = request.form['description']
        vendor = request.form['vendor']
        project = request.form['project']
        po_no = request.form['po_no']
        invoice_no = request.form['invoice_no']
        invoice_date = request.form['invoice_date']
        invoice_value = request.form['invoice_value']
        quantity = request.form['quantity']
        unit = request.form['unit']
        rate = request.form['rate']
        amount = request.form['amount']
        gst = request.form['gst']
        total_amount = request.form['total_amount']
        difference_cost = request.form['difference_cost']
        cur = mysql.connection.cursor()
        query = "INSERT into procurement (material, description, vendor, project_id, po_no, invoice_no, invoice_date, invoice_value," \
                "quantity, unit, rate, amount, gst, total_amount, difference_cost) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (material, description, vendor, project, po_no, invoice_no, invoice_date, invoice_value, quantity, unit, rate, amount, gst, total_amount, difference_cost)
        cur.execute(query, values)
        mysql.connection.commit()
        flash('Material was inserted successfully', 'success')
        return redirect('/material/enter_material')


@app.route('/view_inventory', methods=['GET'])
def view_inventory():
    cur = mysql.connection.cursor()
    query = "SELECT project_id, project_name FROM projects"
    cur.execute(query)
    projects = cur.fetchall()
    project_id = request.args['project_id']
    procurements = None
    if project_id:
        procurementQuery = 'SELECT * from procurement WHERE project_id='+str(project_id)
        cur.execute(procurementQuery)
        procurements = cur.fetchall()

    return render_template('view_inventory.html', projects=projects, procurements=procurements)

if __name__ == '__main__':
    app.run(debug=True)