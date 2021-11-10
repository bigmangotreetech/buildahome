from flask import Flask, render_template, redirect, request, session, flash, jsonify, send_from_directory
from flask_mysqldb import MySQL
import hashlib

import datetime
import time
from time import mktime
import os
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
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/material'
        return redirect('/material/login')
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        if 'email' in session:
            if 'last_route' in session:
                last_route = session['last_route']
                del session['last_route']
                return redirect(last_route)
            else: return redirect('/material')
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        password = hashlib.sha256(password.encode()).hexdigest()
        cur = mysql.connection.cursor()
        query = "SELECT email, name, role, password FROM App_users WHERE email='"+username+"'"
        cur.execute(query)
        result = cur.fetchone()
        if result is not None:
            if result[3] == password:
                session['email'] = result[0]
                session['role'] = result[2]
                session['name'] = result[1]
                flash('Logged in successfully', 'success')
                return redirect('/material')
            else:
                flash('Incorrect credentials', 'danger')
                return redirect('/material/login')
        else:
            flash('Incorrect credentials. User not found', 'danger')
            return redirect('/material/login')


@app.route('/enter_material', methods=['GET', 'POST'])
def enter_material():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/material/enter_material'
        return redirect('/material/login')
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
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/material/view_inventory'
        return redirect('/material/login')
    cur = mysql.connection.cursor()
    query = "SELECT project_id, project_name FROM projects"
    cur.execute(query)
    projects = cur.fetchall()
    procurements = None
    project = None
    material = None
    if 'project_id' in request.args and 'material' in request.args:
        project_id = request.args['project_id']
        material = request.args['material']
        procurementQuery = 'SELECT * from procurement WHERE project_id='+str(project_id)+' AND material="'+str(material)+'"'
        cur.execute(procurementQuery)
        procurements = cur.fetchall()
        for i in projects:
            if str(i[0]) == str(project_id):
                project = i[1]

    return render_template('view_inventory.html', projects=projects, procurements=procurements, project=project, material=material)

@app.route('/kyp_material', methods=['GET','POST'])
def kyp_material():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/material/kyp_material'
        return redirect('/material/login')
    materialQuantityData = {
        'Cement': '',
        'Concrete': '',
        'Steel': '',
        'M Sand': '',
        'P Sand': '',
        'Aggregates': '',
        'Wall Material': '',
        'Door Window': '',
        'Flooring': '',
        'Sanitary': '',
        'Hardware': ''
    }
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        query = "SELECT project_id, project_name FROM projects"
        cur.execute(query)
        projects = cur.fetchall()

        materialPresent = None;
        project = None
        project_id = None
        if 'project_id' in request.args:
            project_id = request.args['project_id']
            materialQuery = 'SELECT * from kyp_material WHERE project_id='+str(project_id)
            cur.execute(materialQuery)
            result = cur.fetchall()
            for i in result:
                materialName = i[2]
                materialQuantityData[materialName] = i[3]
                materialPresent = True
            for i in projects:
                if str(i[0]) == str(project_id):
                    project = i[1]
        return render_template('kyp_material.html', projects=projects, project_id=project_id, materialPresent=materialPresent, project=project, materialQuantityData=materialQuantityData)
    else:
        cur = mysql.connection.cur()
        project_id = request['project_id']
        deleteOldQuantityChartQuery = 'DELETE from kyp_material WHERE project_id='+str(project_id)
        cur.execute(deleteOldQuantityChartQuery)
        for i in materialQuantityData:
            quantityOfI = request.form[i]

            if len(str(quantityOfI)):
                materialQuantityInsetQuery = 'INSERT into kyp_material (project_id, material, total_quantity) values '+str(project_id)+',"'+i+'","'+quantityOfI+'"'

            cur.execute(materialQuantityInsetQuery)
            mysql.connection.commit()
        flash('Quantity chart updated sucessfully','success')
        return redirect('/material/kyp_material?project_id='+str(project_id))


if __name__ == '__main__':
    app.run(debug=True)