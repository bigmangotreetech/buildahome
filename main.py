from flask import Flask, render_template, redirect, request, session, flash, jsonify, url_for
from flask_mysqldb import MySQL
import hashlib

import requests, json


from datetime import datetime
import pytz
import time
from time import mktime
import os
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Sql setup
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'buildahome'
app.config['MYSQL_PASSWORD'] = 'build*2019'
app.config['MYSQL_DB'] = 'buildahome2016'
app.config['UPLOAD_FOLDER'] = '../app.buildahome.in/files'
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024

mysql = MySQL(app)


app.secret_key = b'bAhSessionKey'
ALLOWED_EXTENSIONS = ['pdf']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_projects():
    cur = mysql.connection.cursor()
    query = "SELECT project_id, project_name, project_number FROM projects"
    cur.execute(query)
    projects = cur.fetchall()
    return projects

@app.route('/', methods=['GET'])
def index():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/material'
        return redirect('/material/login')
    user_login_data = {
        'email' : session['email'],
        'name': session['name'],
        'access_level': session['access_level'],
        'role': session['role']
    }
    return render_template('index.html', user_login_data=user_login_data)


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
        query = "SELECT email, name, role, password, access_level FROM App_users WHERE email='"+username+"'"
        cur.execute(query)
        result = cur.fetchone()
        if result is not None:
            if result[3] == password:
                session['email'] = result[0]
                session['role'] = result[2]
                session['name'] = result[1]
                session['access_level'] = result[4]
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
        projects = get_projects()
        return render_template('enter_material.html', projects=projects)
    else:
        material = request.form['material']
        description = request.form['description']
        vendor = request.form['vendor']
        project = request.form['project']
        po_no = request.form['po_no']
        invoice_no = request.form['invoice_no']
        invoice_date = request.form['invoice_date']
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
        if float(result[0]) < (float(quantity)):
            flash('Total quantity of material exceeded limit specified under KYP material. Entry not recorded', 'danger')
            return redirect('/material/enter_material')

        query = "INSERT into procurement (material, description, vendor, project_id, po_no, invoice_no, invoice_date," \
                "quantity, unit, rate, gst, total_amount, difference_cost) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (material, description, vendor, project, po_no, invoice_no, invoice_date, quantity, unit, rate, gst, total_amount, difference_cost)
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
        if material == 'All':
            procurement_query = 'SELECT * from procurement WHERE project_id=' + str(
                project_id)
        else:
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
        projects = get_projects()

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
        projects = get_projects()
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
        projects = get_projects()
        return render_template('create_bill.html',projects=projects)
    else:
        project_id = request.form['project_id']
        trade = request.form['trade']
        stage = request.form['stage']
        payment_percentage = request.form['payment_percentage']
        amount = request.form['amount']
        vendor_name = request.form['vendor_name']
        vendor_code = request.form['vendor_code']
        vendor_pan = request.form['vendor_pan']
        total_payable = float(amount)
        check_if_exists_query = 'SELECT id FROM wo_bills WHERE project_id='+str(project_id)+' AND trade="'+str(trade)+'" AND stage="'+str(stage)+'"'
        cur = mysql.connection.cursor()
        cur.execute(check_if_exists_query)
        res = cur.fetchone()
        if res is not None:
            flash("Older bill already exists. Operation failed", 'danger')
            return redirect('/material/create_bill')
        else:
            insert_query = 'INSERT into wo_bills (project_id, trade, stage, payment_percentage, amount, total_payable, vendor_name, vendor_code, vendor_pan) values (%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s)'
            values = (project_id, trade, stage, payment_percentage, amount, total_payable, vendor_name, vendor_code, vendor_pan)
            cur.execute(insert_query, values)
            mysql.connection.commit()
            flash('Bill created successfully', 'success')
            return redirect('/material/create_bill')

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
    work_order_query = 'SELECT value, floors, vendor_name, vendor_code, vendor_pan from work_orders WHERE project_id='+str(project_id)+' AND trade="'+str(trade)+'" ORDER BY id'
    cur = mysql.connection.cursor()
    cur.execute(work_order_query)
    res = cur.fetchone()
    if res is not None:
        work_order_value = res[0]
        floors = res[1]
        vendor_name = res[2]
        vendor_code = res[3]
        vendor_pan = res[4]
        payment_stages_query = 'SELECT stage, payment_percentage from labour_stages WHERE floors="'+str(floors)+'" AND trade="'+trade+'"'
        cur.execute(payment_stages_query)
        result = cur.fetchall()
        stages = {}
        for i in result:
            stages[i[0]] = i[1].replace('%','')

        response = {'work_order_value': work_order_value, 'vendor_name': vendor_name, 'vendor_code': vendor_code, 'vendor_pan': vendor_pan, 'stages' : stages}
        return jsonify(response)

def get_bills_as_json(bills_query):
    cur = mysql.connection.cursor()
    cur.execute(bills_query)
    data = {}
    res = cur.fetchall()
    for i in res:
        project_id = i[0]
        if project_id not in data:
            data[project_id] = {'project_name': i[1], 'bills': []}
        data[project_id]['bills'].append(
            {'bill_id': i[16], 'vendor_name': i[7], 'vendor_pan': i[9], 'vendor_code': i[8], 'trade': i[17],
             'stage': i[3], 'amount': i[5], 'total_payable': i[6],
             'approval_1_amount': i[11], 'approval_1_notes': i[12], 'approval_2_amount': i[14],
             'approval_2_notes': i[15]}
        )
    return data

@app.route('/view_bills', methods=['GET'])
def view_bills():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/material/create_bill'
        return redirect('/material/login')
    if request.method == 'GET':
        bills_query = 'SELECT projects.project_id, projects.project_name, wo_bills.trade, wo_bills.stage, wo_bills.payment_percentage,' \
                         'wo_bills.amount, wo_bills.total_payable, wo_bills.vendor_name, wo_bills.vendor_code, wo_bills.vendor_pan,' \
                         'wo_bills.approval_1_status, wo_bills.approval_1_amount, wo_bills.approval_1_notes,' \
                         'wo_bills.approval_2_status, wo_bills.approval_2_amount, wo_bills.approval_2_notes, wo_bills.id, wo_bills.trade' \
                         ' FROM wo_bills INNER JOIN projects on wo_bills.project_id = projects.project_id AND ( wo_bills.approval_2_amount = 0 OR wo_bills.approval_2_amount IS NULL)'
        data = get_bills_as_json(bills_query)
        access_level = session['access_level']
        return render_template('view_bills.html', data=data, access_level=access_level)

@app.route('/view_approved_bills', methods=['GET'])
def view_approved_bills():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/material/create_bill'
        return redirect('/material/login')
    if request.method == 'GET':
        bills_query = 'SELECT projects.project_id, projects.project_name, wo_bills.trade, wo_bills.stage, wo_bills.payment_percentage,' \
                         'wo_bills.amount, wo_bills.total_payable, wo_bills.vendor_name, wo_bills.vendor_code, wo_bills.vendor_pan,' \
                         'wo_bills.approval_1_status, wo_bills.approval_1_amount, wo_bills.approval_1_notes,' \
                         'wo_bills.approval_2_status, wo_bills.approval_2_amount, wo_bills.approval_2_notes, wo_bills.id, wo_bills.trade' \
                         ' FROM wo_bills INNER JOIN projects on wo_bills.project_id = projects.project_id AND (wo_bills.approval_2_amount != 0 AND wo_bills.approval_2_amount IS NOT NULL)'
        data = get_bills_as_json(bills_query)
        return render_template('view_approved_bills.html', data=data)

def update_work_order_balance(project_id, trade, difference_amount):
    get_wo_query = 'SELECT id, balance from work_orders WHERE project_id=' + str(
        project_id) + ' AND trade="' + trade + '"'
    cur = mysql.connection.cursor()
    cur.execute(get_wo_query)
    res = cur.fetchone()
    if res is not None:
        balance = res[1]
        if str(balance).strip() == '':
            balance = 0
        else:
            balance = float(balance)
        updated_balance = balance + float(difference_amount)
        update_wo_query = 'UPDATE work_orders SET balance='+str(updated_balance)+' WHERE id='+str(res[0])
        cur.execute(update_wo_query)
        mysql.connection.commit()

@app.route('/save_approved_bill', methods=['POST'])
def save_approved_bill():
    bill_id = request.form['bill_id']
    approved_amount = request.form['approved_amount']
    notes = request.form['notes']
    approval_level = request.form['approval_level']
    trade = request.form['trade']
    project_id = request.form['project_id']
    difference_amount = request.form['difference_amount']
    cur = mysql.connection.cursor()
    update_bill_query = ''
    if approval_level == 'Level 1':
        update_bill_query = 'UPDATE wo_bills SET approval_1_amount = "'+str(approved_amount)+'" , approval_1_notes = "'+str(notes)+'" WHERE id='+str(bill_id)
    elif approval_level == 'Level 2':
        update_bill_query = 'UPDATE wo_bills SET approval_2_amount = "'+str(approved_amount)+'" , approval_2_notes = "'+str(notes)+'" WHERE id='+str(bill_id)
    cur.execute(update_bill_query)
    if float(difference_amount) > 0 and  approval_level == 'Level 2':
        update_work_order_balance(project_id, trade, difference_amount)
    mysql.connection.commit()
    return jsonify({"message": "success"})

def get_work_orders_for_project(project_id):
    cur = mysql.connection.cursor()
    get_wo_query = 'SELECT * from work_orders WHERE project_id='+str(project_id)+' ORDER BY trade'
    cur.execute(get_wo_query)
    res = cur.fetchall()
    return res

@app.route("/view_work_order", methods=['GET'])
def view_work_order():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/material/create_bill'
        return redirect('/material/login')
    if request.method == 'GET':
        projects = get_projects()
        work_orders = []
        if 'project_id' in request.args:
            project_id = request.args['project_id']
            work_orders = get_work_orders_for_project(project_id)

        return render_template('view_work_orders.html', projects=projects, work_orders=work_orders)

@app.route('/check_if_floors_updated', methods=['POST'])
def check_if_floors_updated():
    project_id = request.form['project_id']
    query = 'SELECT id, floors from work_orders WHERE project_id='+str(project_id)
    cur = mysql.connection.cursor()
    cur.execute(query)
    result = cur.fetchone()
    if result is not None:
        return jsonify({'floors_updated': True, 'floors': result[1]})
    return jsonify({'floors_updated': False})


@app.route('/view_approved_indents', methods=['GET'])
def view_approved_indents():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/material/create_bill'
        return redirect('/material/login')
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        current_user_role = session['role']
        if current_user_role == 'Admin':
            indents_query = 'SELECT indents.id, projects.project_id, projects.project_name, indents.material, indents.quantity, indents.unit, indents.purpose' \
                            ', App_users.name, indents.timestamp FROM indents INNER JOIN projects on indents.status="approved" AND indents.project_id=projects.project_id ' \
                            ' LEFT OUTER JOIN App_users on indents.created_by_user=App_users.user_id'

            cur.execute(indents_query)
            data = []
            result = cur.fetchall()
            for i in result:
                i = list(i)
                if len(str(i[8]).strip()) > 0:
                    i[8] = str(i[8]).strip()
                    timestamp = datetime.strptime(i[8] + ' 2022 +0530', '%A %d %B %H:%M %Y %z')
                    IST = pytz.timezone('Asia/Kolkata')
                    current_time = datetime.now(IST)
                    time_since_creation = current_time - timestamp
                    difference_in_seconds = time_since_creation.total_seconds()
                    difference_in_hours = difference_in_seconds // 3600
                    if difference_in_hours >= 24:
                        difference_in_days = difference_in_hours // 24
                        hours_remaining = difference_in_hours % 24
                        i[8] = str(int(difference_in_days)) + ' days, ' + str(
                            int(hours_remaining)) + 'hours'
                    else:
                        i[8] = str(int(difference_in_hours)) + ' hours'
                data.append(i)
            return render_template('approved_indents.html', result=data)
        elif current_user_role == 'Purchase Executive':
            current_user_email = session['email']
            access_query = 'SELECT access, role from App_users WHERE email=' + str(current_user_email)
            cur.execute(access_query)
            res = cur.fetchone()
            access = res[0]
            if len(access):
                access = access.split(',')
                access_as_int = [int(i) for i in access]
                access_tuple = tuple(access_as_int)
                indents_query = 'SELECT indents.id, projects.project_id, projects.project_name, indents.material, indents.quantity, indents.unit, indents.purpose' \
                                ', App_users.name, indents.timestamp FROM indents INNER JOIN projects on indents.status="approved" AND indents.project_id=projects.project_id AND indents.project_id IN ' + str(
                                     access_tuple) + '' \
                                    ' LEFT OUTER JOIN App_users on indents.created_by_user=App_users.user_id'
                cur.execute(indents_query)
                data=[]
                result = cur.fetchall()
                for i in result:
                    i = list(i)
                    if len(str(i[8]).strip()) > 0:
                        i[8] = str(i[8]).strip()
                        timestamp = datetime.strptime(i[8]+' 2022 +0530', '%A %d %B %H:%M %Y %z')
                        IST = pytz.timezone('Asia/Kolkata')
                        current_time = datetime.now(IST)
                        time_since_creation = current_time - timestamp
                        difference_in_seconds = time_since_creation.total_seconds()
                        difference_in_hours = difference_in_seconds // 3600
                        if difference_in_hours >= 24:
                            difference_in_days = difference_in_hours // 24
                            hours_remaining = difference_in_hours % 24
                            i[8] = str(int(difference_in_days)) + ' days, ' + str(
                                int(hours_remaining)) + 'hours'
                        else:
                            i[8] = str(int(difference_in_hours)) + ' hours'
                    data.append(i)
                return render_template('approved_indents.html', result=data)
        else:
            return 'You do not have access to view this page'

@app.route('/view_indent_details', methods=['GET'])
def view_indent_details():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/material/create_bill'
        return redirect('/material/login')
    if request.method == 'GET':
        indent_id = request.args['indent_id']
        cur = mysql.connection.cursor()
        indents_query = 'SELECT indents.id, projects.project_id, projects.project_name, indents.material, indents.quantity, indents.unit, indents.purpose' \
                        ', App_users.name, indents.timestamp, indents.purchase_order FROM indents INNER JOIN projects on indents.id='+str(indent_id)+' AND indents.project_id=projects.project_id ' \
                        ' LEFT OUTER JOIN App_users on indents.created_by_user=App_users.user_id'
        cur.execute(indents_query)
        result = cur.fetchone()
        return render_template('view_indent_details.html', result=result)


@app.route('/upload_po_for_indent', methods=['POST'])
def upload_po_for_indent():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/material/create_bill'
        return redirect('/material/login')
    if request.method == 'POST':
        indent_id = request.form['indent_id']
        if 'purchase_order' in request.files:
            file = request.files['purchase_order']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(indent_id)+'_'+filename))
                cur = mysql.connection.cursor()
                query = 'UPDATE indents set status=%s, purchase_order=%s WHERE id=%s'
                values = ('po_uploaded', str(indent_id)+'_'+filename, indent_id )
                cur.execute(query, values)
                mysql.connection.commit()

                get_indent_query = 'SELECT indents.id, projects.project_id, projects.project_name, indents.material, indents.quantity, indents.unit, indents.purpose' \
                                ', indents.timestamp, indents.created_by_user, indents.acted_by_user FROM indents INNER JOIN projects on indents.project_id=projects.project_id ' \
                                ' AND indents.id='+str(indent_id)
                cur.execute(get_indent_query)
                result = cur.fetchone()
                if result is not None:
                    notification_body = 'PO uploaded for indent with id '+str(indent_id)+'. Details: '+str(result[4])+' '+str(result[5])+' '+str(result[3])+' For project '+str(result[2])
                    IST = pytz.timezone('Asia/Kolkata')
                    datetime_ist = datetime.now(IST)
                    timestamp = datetime_ist.strftime('%A %d %B %H:%M')
                    send_app_notification('PO Uploaded', notification_body, str(result[8]), str(result[8]), 'PO uploads', timestamp)
                    send_app_notification('PO Uploaded', notification_body, str(result[9]), str(result[9]), 'PO uploads', timestamp)
                flash('PO Uploaded successfully','success')
        return redirect('/material/view_indent_details?indent_id='+str(indent_id))

@app.route('/sign_wo', methods=['GET'])
def sign_wo_order():
    if request.method == 'GET':
        return render_template('sign_wo.html')

@app.route('/create_project', methods=['GET','POST'])
def create_project():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/material/create_project'
        return redirect('/material/login')
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        sales_executives_query = 'SELECT user_id, name from App_users WHERE role="Sales Executive"'
        cur.execute(sales_executives_query)
        result = cur.fetchall()
        return render_template('create_project.html', sales_executives=result)
    else:

        column_names = list(request.form.keys())
        values = list(request.form.values())

        cur = mysql.connection.cursor()
        new_project_query = 'INSERT into projects'+str(tuple(column_names)).replace("'","")+'values '+str(tuple(values))
        cur.execute(new_project_query)
        project_id = cur.lastrowid
        if 'cost_sheet' in request.files:
            file = request.files['cost_sheet']
            if file.filename == '':
                flash('No selected file', 'danger ')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename_on_server = 'cost_sheet_for_project_'+str(project_id)+'_'+filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_on_server))

        flash('Project created successfully', 'success')
        mysql.connection.commit()
        return redirect('/material/create_project')


@app.route('/unapproved_projects', methods=['GET'])
def unapproved_projects():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        unapproved_projects_query = 'SELECT project_id, project_name from projects WHERE is_approved=0'
        cur.execute(unapproved_projects_query)
        result = cur.fetchall()
        return render_template('unapproved_projects.html', projects=result)

@app.route('/view_project_details',methods=['GET'])
def view_project_details():
    if request.method == 'GET':
        fields = [
            'project_name', 'project_location', 'no_of_floors', 'project_value', 'sales_executive', 'site_area',
            'gf_slab_area', 'ff_slab_area', 'tf_slab_area', 'tef_slab_area', 'shr_oht', 'elevation_details',
            'paid_percentage', 'comments'
        ]
        fields_as_string = " ".join(fields)
        get_details_query = 'SELECT ('+fields_as_string+') from projects WHERE project_id='+str(request.args['project_id'])
        cur = mysql.connection.cursor()
        cur.execute(get_details_query)
        result = cur.fetchone()
        details = {}
        for i in range (len(fields)) :
            fields_name_to_show = " ".join(fields[i].split('_')).title()
            details[fields_name_to_show] = result[i]
        return render_template('view_project_details.html', details=details)

@app.route('/logout', methods=['GET'])
def logout():
    del session['email']
    del session['name']
    del session['role']
    return redirect('/material/login')



# APIs for mobile app
@app.route('/API/create_indent', methods=['POST'])
def create_indent():
    if request.method == 'POST':
        project_id = request.form['project_id']
        material = request.form['material']
        quantity = request.form['quantity']
        unit = request.form['unit']
        purpose = request.form['purpose']
        timestamp = request.form['timestamp']
        status = 'unapproved'
        cur = mysql.connection.cursor()
        user_id = request.form['user_id']
        query = 'INSERT into indents(project_id, material, quantity, unit, purpose, status, created_by_user, timestamp) values (%s, %s, %s, %s, %s, %s, %s, %s)'
        values = (project_id, material, quantity, unit, purpose, status, user_id, timestamp)
        cur.execute(query, values)
        mysql.connection.commit()
        return jsonify({'message':'success'})

def save_notification_to_db(title, body, user_id, role, category, timestamp):
    cur = mysql.connection.cursor()
    notification_query = 'INSERT into app_notifications(title, body, user_id, role, category, timestamp) values (%s, %s, %s, %s, %s, %s)'
    values = (title, body, user_id, role, category, timestamp)
    cur.execute(notification_query, values)
    mysql.connection.commit()
    return

def send_app_notification(title, body, user_id, role, category, timestamp):
    save_notification_to_db(title, body, user_id, role, category, timestamp)
    recipient = ''
    if str(user_id).strip() == '':
        recipient = role
    else:
        recipient = user_id
    url = 'https://fcm.googleapis.com/fcm/send'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=AAAAlQ1Lrfw:APA91bHvI2-qFZNCf-oFfeZgM0JUDxxbuykH_ffka9hPUE0xBpiza4uHF0LmItT_SfMZ1Zl5amGUfAXigaR_VcMsEArqpOwHNup4oRTQ24htJ_GWYH0OWZzFrH2lRY24mnQ-uiHgLyln'
    }
    data = {
        "notification": {"title": title, "body": body, 'data': {'category': 'team_notifications'}},
        "to": "/topics/" + recipient,
    }
    requests.post(url, headers=headers, data=json.dumps(data))
    return

@app.route('/API/change_indent_status', methods=['POST'])
def change_indent_status():
    indent_id = request.form['indent_id']
    status = request.form['status']

    cur = mysql.connection.cursor()
    query = 'UPDATE indents SET status="'+status+'", acted_by_user='+str(request.form['acted_by_user'])+' WHERE id='+str(indent_id)
    cur.execute(query)
    mysql.connection.commit()

    if status == 'approved':
        send_app_notification(
            'Indent Approved',
            request.form['notification_body'],
            request.form['user_id'],
            request.form['user_id'],
            'Indent Approval',
            request.form['timestamp']
        )
    elif status == 'rejected':
        send_app_notification(
            'Indent Rejected',
            request.form['notification_body'],
            request.form['user_id'],
            request.form['user_id'],
            'Indent Rejection',
            request.form['timestamp']
        )
    return jsonify({'message': 'success'})

@app.route('/API/edit_and_approve_indent', methods=['POST'])
def edit_and_approve_indent():
    indent_id = request.form['indent_id']
    status = 'approved'
    project_id = request.form['project_id']
    material = request.form['material']
    quantity = request.form['quantity']
    user_id = request.form['acted_by_user']
    unit = request.form['unit']
    purpose = request.form['purpose']
    cur = mysql.connection.cursor()
    query = 'UPDATE indents SET status=%s, project_id=%s, material=%s, quantity=%s, unit=%s, purpose=%s, acted_by_user=%s WHERE id=%s'
    values = (status, project_id, material, quantity, unit, purpose, user_id, indent_id)
    cur.execute(query, values)
    mysql.connection.commit()
    send_app_notification(
        'Indent Approved',
        request.form['notification_body'],
        request.form['user_id'],
        request.form['user_id'],
        'Indent Approval',
        request.form['timestamp']
    )
    return jsonify({'message': 'success'})

@app.route('/API/get_unapproved_indents', methods=['GET'])
def get_unapproved_indents():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        user_id = request.args['user_id']
        access_query = 'SELECT access, role from App_users WHERE user_id='+str(user_id)
        cur.execute(access_query)
        res = cur.fetchone()
        access = res[0]
        role = res[1]
        if role == 'Admin':
            indents_query = 'SELECT indents.id, projects.project_id, projects.project_name, indents.material, indents.quantity, indents.unit, indents.purpose' \
                            ', App_users.name, indents.timestamp, indents.created_by_user FROM indents INNER JOIN projects on indents.status="unapproved" AND indents.project_id=projects.project_id '\
                                ' LEFT OUTER JOIN App_users on indents.created_by_user=App_users.user_id'
            cur.execute(indents_query)
            res = cur.fetchall()
            data = []
            for i in res:
                indent_entry = {}
                indent_entry['id'] = i[0]
                indent_entry['project_id'] = i[1]
                indent_entry['project_name'] = i[2]
                indent_entry['material'] = i[3]
                indent_entry['quantity'] = i[4]
                indent_entry['unit'] = i[5]
                indent_entry['purpose'] = i[6]
                indent_entry['created_by_user'] = i[7]
                indent_entry['timestamp'] = i[8]
                indent_entry['created_by_user_id'] = i[9]
                data.append(indent_entry)

            return jsonify(data)
        elif len(access):
            access = access.split(',')
            access_as_int = [int(i) for i in access]
            access_tuple = tuple(access_as_int)
            indents_query = 'SELECT indents.id, projects.project_id, projects.project_name, indents.material, indents.quantity, indents.unit, indents.purpose' \
                            ', App_users.name, indents.timestamp, indents.created_by_user FROM indents INNER JOIN projects on indents.status="unapproved" AND indents.project_id=projects.project_id AND indents.project_id IN '+str(access_tuple)+'' \
                            ' LEFT OUTER JOIN App_users on indents.created_by_user=App_users.user_id'
            cur.execute(indents_query)
            res = cur.fetchall()
            data = []
            for i in res:
                indent_entry = {}
                indent_entry['id'] = i[0]
                indent_entry['project_id'] = i[1]
                indent_entry['project_name'] = i[2]
                indent_entry['material'] = i[3]
                indent_entry['quantity'] = i[4]
                indent_entry['unit'] = i[5]
                indent_entry['purpose'] = i[6]
                indent_entry['created_by_user'] = i[7]
                indent_entry['timestamp'] = i[8]
                indent_entry['created_by_user_id'] = i[9]
                data.append(indent_entry)

            return jsonify(data)
        else: return jsonify([])

@app.route('/API/get_notifications', methods = ['GET'])
def get_notifications():
    recipient = request.args['recipient']
    cur = mysql.connection.cursor()
    notifications_query = 'SELECT title, body, timestamp from app_notifications WHERE user_id='+str(recipient)
    cur.execute(notifications_query)
    data = []
    result = cur.fetchall()
    for i in result:
        data.append({'title': i[0], 'body': i[1], 'timestamp': i[2]})
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)