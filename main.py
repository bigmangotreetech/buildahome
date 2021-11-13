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

labourTradeStageMap = {

}

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
        gst = request.form['gst']
        total_amount = request.form['total_amount']
        difference_cost = request.form['difference_cost']
        cur = mysql.connection.cursor()

        material_quantity_query = 'SELECT total_quantity from kyp_material WHERE project_id='+str(project)+' AND material="'+str(material)+'"'
        cur.execute(material_quantity_query)
        result = cur.fetchone()
        if result is None:
            flash('Total quantity of material has not been specified under KYP material. Entry not recorded', 'danger')
            return redirect('/material/enter_material')
        if float(result[0]) < (float(quantity) + float(result[0])):
            flash('Total quantity of material exceeded limii specified under KYP material. Entry not recorded', 'danger')
            return redirect('/material/enter_material')

        query = "INSERT into procurement (material, description, vendor, project_id, po_no, invoice_no, invoice_date, invoice_value," \
                "quantity, unit, rate, gst, total_amount, difference_cost) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (material, description, vendor, project, po_no, invoice_no, invoice_date, invoice_value, quantity, unit, rate, gst, total_amount, difference_cost)
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
    material_total_quantity = None
    if 'project_id' in request.args and 'material' in request.args:
        project_id = request.args['project_id']
        material = request.args['material']
        procurement_query = 'SELECT * from procurement WHERE project_id='+str(project_id)+' AND material="'+str(material)+'"'
        cur.execute(procurement_query)
        procurements = cur.fetchall()
        for i in projects:
            if str(i[0]) == str(project_id):
                project = i[1]

        material_quantity_query = 'SELECT total_quantity from kyp_material WHERE project_id='+str(project_id)+' AND material="'+str(material)+'"'
        cur.execute(material_quantity_query)
        result = cur.fetchone()
        if result is not None:
            material_total_quantity = result[0]
    return render_template('view_inventory.html', projects=projects, procurements=procurements, project=project, material=material, material_total_quantity=material_total_quantity)

@app.route('/kyp_material', methods=['GET','POST'])
def kyp_material():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/material/kyp_material'
        return redirect('/material/login')
    material_quantity_data = {
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

        project = None
        project_id = None
        if 'project_id' in request.args:
            project_id = request.args['project_id']
            material_query = 'SELECT * from kyp_material WHERE project_id='+str(project_id)
            cur.execute(material_query)
            result = cur.fetchall()
            for i in result:
                material_name = i[2]
                material_quantity_data[material_name] = i[3]
            for i in projects:
                if str(i[0]) == str(project_id):
                    project = i[1]
        return render_template('kyp_material.html', projects=projects, project_id=project_id, project=project, material_quantity_data=material_quantity_data)
    else:
        cur = mysql.connection.cursor()
        project_id = request.form['project_id']
        delete_old_quantity_chart_query = 'DELETE from kyp_material WHERE project_id='+str(project_id)
        cur.execute(delete_old_quantity_chart_query)
        for i in material_quantity_data:
            quantity_of_i = request.form[i]

            if len(str(quantity_of_i)):
                material_quantity_insert_query = "INSERT into kyp_material (project_id, material, total_quantity) values ("+str(project_id)+",'"+str(i)+"','"+str(quantity_of_i)+"')"

                cur.execute(material_quantity_insert_query)
                mysql.connection.commit()
        flash('Quantity chart updated successfully','success')
        return redirect('/material/kyp_material?project_id='+str(project_id))

@app.route('/create_work_order', methods=['GET', 'POST'])
def create_work_order():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/material/create_work_order'
        return redirect('/material/login')
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        query = "SELECT project_id, project_name FROM projects"
        cur.execute(query)
        projects = cur.fetchall()
        floors = ['G + 1','G + 2','G + 3','G + 4']
        trades_query = 'SELECT DISTINCT trade from labour_stages'
        cur.execute(trades_query)
        result = cur.fetchall()
        trades = []
        for i in result:
            trades.append(i[0])
        return render_template('create_work_order.html', projects=projects, floors=floors, trades=trades)
    else:
        project_id = request.form['project']
        trade = request.form['trade']
        floors = request.form['floors']
        wo_value = request.form['wo_value']
        vendor_name = request.form['vendor_name']
        vendor_pan = request.form['vendor_pan']
        vendor_code = request.form['vendor_code']
        check_if_exist_query = 'SELECT id from work_orders WHERE project_id='+str(project_id)+' AND floors="'+str(floors)+'" AND trade="'+str(trade)+'"'
        cur = mysql.connection.cursor()
        cur.execute(check_if_exist_query)
        result = cur.fetchone()
        if result is not None:
            flash("Work order already exists. Operation failed",'danger')
            return redirect('/material/create_work_order')
        else:
            insert_query = 'INSERT into work_orders (project_id, value, trade, floors, vendor_name, vendor_code, vendor_pan) values (%s, %s, %s, %s, %s, %s, %s)'
            values = (project_id, wo_value, trade, floors, vendor_name, vendor_code, vendor_pan)
            cur.execute(insert_query, values)
            mysql.connection.commit()
            flash('Work order created successfully', 'success')
            return redirect('/material/create_work_order')


@app.route('/create_bill', methods=['GET', 'POST'])
def create_bill():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/material/create_bill'
        return redirect('/material/login')
    if request.method == 'GET':
        projects_query = 'SELECT projects.project_id, projects.project_name FROM work_orders INNER JOIN projects on work_orders.project_id = projects.project_id'
        cur = mysql.connection.cursor()
        cur.execute(projects_query)
        projects = cur.fetchall()
        return render_template('create_bill.html',projects=projects)

@app.route('/update_trades_for_project', methods=['POST'])
def update_trades_for_project():
    project_id = request.form['project_id']
    trades_query = 'SELECT DISTINCT trade from work_orders WHERE project_id='+str(project_id)
    cur = mysql.connection.cursor()
    cur.execute(trades_query)
    trades = []
    result = cur.fetchall()
    for i in result:
        trades.append(i[0])
    return jsonify(trades)

@app.route('/update_payment_stages', methods=['POST'])
def update_payment_stages():
    project_id = request.form['project_id']
    trade = request.form['trade']
    work_order_query = 'SELECT value, floors, vendor_name, vendor_code, vendor_pan from work_orders WHERE project_id='+str(project_id)+' AND trade="'+str(trade)+'"'
    cur = mysql.connection.cursor()
    cur.execute(work_order_query)
    res = cur.fetchone()
    if res is not None:
        work_order_value = res[0]
        floors = res[1]
        vendor_name = res[2]
        vendor_code = res[3]
        vendor_pan = res[4]
        payment_stages_query = 'SELECT stage, payment_percentage from labour_stages WHERE floor="'+str(floors)+'" AND trade="'+trade+'"'
        cur.execute(payment_stages_query)
        result = cur.fetchall()
        stages = {}
        for i in result:
            stages[i[0]] = i[1]

        response = {'work_order_value': work_order_value, 'vendor_name': vendor_name, 'vendor_code': vendor_code, 'vendor_pan': vendor_pan, 'stages' : stages}
        return jsonify(response)


@app.route('/logout', methods=['GET'])
def logout():
    del session['email']
    del session['name']
    del session['role']
    return redirect('/material/login')

if __name__ == '__main__':
    app.run(debug=True)