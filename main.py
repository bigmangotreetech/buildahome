from flask import Flask, render_template, redirect, request, session, flash, jsonify, url_for
from werkzeug.datastructures import FileStorage

from flask_mysqldb import MySQL
import hashlib
import boto3, botocore
import requests, json
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy

from datetime import datetime
import pytz
import time
from time import mktime
import os
import time
from werkzeug.utils import secure_filename

from models.projects import projects
from constants.constants import project_fields, roles

from PIL import Image
from io import BytesIO
import random


# Debit note

# Indent audit trail

# Project co ordinator wise order indents

# All Bills Project co ordinator

# Line break check on work order

# Shifting entry to not have edit button on view inventory

# Do not include transportation and laoading unloading in total amount 




# Last labour stage id 412
app = Flask(__name__)
# Sql setup
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'buildahome'
app.config['MYSQL_PASSWORD'] = 'build*2019'
app.config['MYSQL_DB'] = 'buildahome2016'
app.config['UPLOAD_FOLDER'] = '../static/files'
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024
app.config['S3_SECRET'] = os.environ.get('S3_SECRET')
app.config['S3_KEY'] = os.environ.get('S3_KEY')
app.config['S3_BUCKET'] = os.environ.get('S3_BUCKET')
app.config['S3_LOCATION'] = os.environ.get('S3_LOCATION')
app.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://127.0.0.1:6379/0'

mysql = MySQL(app)

s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config['S3_KEY'],
    aws_secret_access_key=app.config['S3_SECRET']
)

app.secret_key = 'bAhSessionKey'
ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpeg', 'jpg']


def send_to_s3(file, bucket_name, filename, acl="public-read", content_type=''):
    try:
        if content_type == '':
            content_type = file.content_type
        s3.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": content_type  # Set appropriate content type as per the file
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return str(e)
    return 'success'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_projects():
    cur = mysql.connection.cursor()
    projects = []
    if len(get_projects_for_current_user()) > 0:
        if session['role'] not in ['Super Admin', 'COO', 'QS Head','Purchase Head', 'Site Engineer', 'Design Head']:
            query = 'SELECT project_id, project_name from projects WHERE is_approved=1 AND archived=0 ' \
                    'AND project_id IN ' + str(get_projects_for_current_user())
            cur.execute(query)
            projects = cur.fetchall()
        else:
            query = 'SELECT project_id, project_name from projects WHERE is_approved=1 AND archived=0'
            cur.execute(query)
            projects = cur.fetchall()
    return projects


def get_projects_for_current_user():
    if 'user_id' in session:
        user_id = session['user_id']
        role = session['role']
        cur = mysql.connection.cursor()
        if role in ['Super Admin', 'COO', 'QS Head', 'Purchase Head', 'Site Engineer', 'Design Head', 'Billing', 'Planning']:
            return ('All')
        elif role == 'Project Coordinator':
            query = 'SELECT project_id from project_operations_team WHERE co_ordinator=' + str(user_id)
            cur.execute(query)
            result = cur.fetchall()
            projects = []
            for i in result:
                projects.append(i[0])
            if len(projects) == 1:
                projects.append(0)
            return tuple(projects)
        elif role == 'Project Manager':
            query = 'SELECT project_id from project_operations_team WHERE project_manager=' + str(user_id)
            cur.execute(query)
            result = cur.fetchall()
            projects = []
            for i in result:
                projects.append(i[0])
            if len(projects) == 1:
                projects.append(0)
            return tuple(projects)
        elif role == 'Purchase Executive':
            query = 'SELECT project_id from project_operations_team WHERE purchase_executive=' + str(user_id)
            cur.execute(query)
            result = cur.fetchall()
            projects = []
            for i in result:
                projects.append(i[0])
            if len(projects) == 1:
                projects.append(0)
            return tuple(projects)
        elif role == 'QS Engineer':
            query = 'SELECT project_id from project_operations_team WHERE qs_engineer=' + str(user_id)
            cur.execute(query)
            result = cur.fetchall()
            projects = []
            for i in result:
                projects.append(i[0])
            if len(projects) == 1:
                projects.append(0)
            return tuple(projects)
        elif role == 'Architect':
            query = 'SELECT project_id from project_design_team WHERE architect=' + str(user_id)
            cur.execute(query)
            result = cur.fetchall()
            projects = []
            for i in result:
                if len(str(i[0])) > 0:
                    projects.append(i[0])
            if len(projects) == 1:
                projects.append(0)
            return tuple(projects)
        elif role == 'Structural Designer':
            query = 'SELECT project_id from project_design_team WHERE structural_designer=' + str(user_id)
            cur.execute(query)
            result = cur.fetchall()
            projects = []
            for i in result:
                projects.append(i[0])
            if len(projects) == 1:
                projects.append(0)
            return tuple(projects)
        elif role == 'Electrical Designer':
            query = 'SELECT project_id from project_design_team WHERE electrical_designer=' + str(user_id)
            cur.execute(query)
            result = cur.fetchall()
            projects = []
            for i in result:
                projects.append(i[0])
            if len(projects) == 1:
                projects.append(0)
            return tuple(projects)
        elif role == 'PHE Designer':
            query = 'SELECT project_id from project_design_team WHERE phe_designer=' + str(user_id)
            cur.execute(query)
            result = cur.fetchall()
            projects = []
            for i in result:
                projects.append(i[0])
            if len(projects) == 1:
                projects.append(0)
            return tuple(projects)
        elif role == 'Senior Architect':
            query = 'SELECT project_id from project_design_team WHERE senior_architect=' + str(user_id)
            cur.execute(query)
            result = cur.fetchall()
            projects = []
            for i in result:
                projects.append(i[0])
            if len(projects) == 1:
                projects.append(0)
            return tuple(projects)
        else:
            return []
@app.route('/delete_old_drawings', methods=['GET'])
def delete_old_drawings():
    cur = mysql.connection.cursor()
    
    f = open('../static/projects_to_delete.txt','r')
    for i in f:
        project_number = i.strip()
        project_id_query = 'SELECT project_id from projects WHERE project_number='+project_number
        cur.execute(project_id_query)
        res = cur.fetchone()
        if res is not None:
            project_id = res[0]
            get_drawings_for_projects = 'SELECT pdf FROM Docs WHERE project_id='+str(project_id)+' AND folder!="RECEIPTS" AND folder!="AGREEMENT "'
            cur.execute(get_drawings_for_projects)
            res = cur.fetchall()
            for d in res:
                try:
                    os.remove('/home/buildahome2016/public_html/app.buildahome.in/team/Drawings/'+d[0])
                except:
                    pass
            delete_drawing_query = 'DELETE from Docs WHERE project_id='+str(project_id)+' AND folder!="RECEIPTS" AND folder!="AGREEMENT "'
            cur.execute(delete_drawing_query)
            
    return 'success'



@app.route('/migrate', methods=['GET'])
def migrate():
    BASE_DIR = '/home/buildahome2016/public_html'
    abs_path = os.path.join(BASE_DIR, '/home/buildahome2016/public_html/app.buildahome.in/api/images')
    files = os.listdir(abs_path)
    im = Image.open(r'/home/buildahome2016/public_html/app.buildahome.in/api/images/' + i)
    width, height = im.size
    while width > 640 and height > 320:
        width = width - 100
        height = height - 100
    im.resize((width, height))
    im.save('/home/buildahome2016/public_html/app.buildahome.in/api/images/' + i)
    try:
        for i in files[0: 10]:
            with open(
                    '/home/buildahome2016/public_html/app.buildahome.in/api/images/' + i,
                    'rb') as fp:
                file = FileStorage(fp, content_type='image/' + i.split('.')[-1])
                send_to_s3(file, app.config["S3_BUCKET"], i)
        return 'success'
    except Exception as e:
        print("Something Happened: ", e)
        return str(e)

@app.route('/files/<filename>', methods=['GET'])
def files(filename):
    response = redirect(app.config['S3_LOCATION'] + filename)
    return response

@app.route('/upload_migrated_image', methods=['GET','POST'])
def upload_migrated_image():
    if 'image' in request.files:
        file = request.files['image']
        if file.filename == '':
            flash('No selected file', 'danger ')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            output = send_to_s3(file, app.config["S3_BUCKET"], 'migrated/'+filename)
            if output != 'success':
                return 'failed'
        return 'success'
    return 'No image'

@app.route('/transfer_image_to_s3', methods=['GET'])
def transfer_image_to_s3():
    last_file_query = 'SELECT image from Daily_images ORDER BY updated_at DESC LIMIT 1'
    cur = mysql.connection.cursor()
    cur.execute(last_file_query)
    res = cur.fetchone()
    last_file = res[0]
    with open(
            '/home/buildahome2016/public_html/app.buildahome.in/api/images/' + last_file,
            'rb') as fp:
        file = FileStorage(fp, content_type='image/' + last_file.split('.')[-1])
        res = send_to_s3(file, os.environ.get('S3_BUCKET'), 'migrated/' + last_file)
        if res == 'success':
            os.remove('/home/buildahome2016/public_html/app.buildahome.in/api/images/' + last_file)
    return ''

@app.route('/', methods=['GET'])
def index():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp'
        return redirect('/erp/login')
    return render_template('index.html')

@app.route('/profile', methods=['GET','POST'])
def profile():
    if request.method == 'GET':
        if 'user_id' in session:
            user_id = session['user_id']
            cur = mysql.connection.cursor()
            view_user_query = 'SELECT user_id, email, name, role, phone, profile_picture FROM App_users WHERE user_id=' + str(user_id)
            cur.execute(view_user_query)
            result = cur.fetchone()
            return render_template('profile.html', user=result)
        else: 
            return redirect('/erp/login')
    else:


        user_id = request.form['user_id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file.filename != '' and file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                picture_filename = 'user_dp_'+str(user_id)+'_'+ filename
                output = send_to_s3(file, app.config["S3_BUCKET"], picture_filename)
                if output != 'success':
                    flash('File upload failed', 'danger')
                    return redirect(request.referrer)
                else:
                    cur = mysql.connection.cursor()
                    update_query = 'UPDATE App_users set profile_picture="'+picture_filename+'" WHERE user_id=' + str(
                        user_id)
                    cur.execute(update_query)
                    mysql.connection.commit()

        if len(password.strip()) > 0:
            old_password = request.form['old_password']
            if old_password.strip() == '':
                flash('Current password field cannot be empty to change password', 'danger')
                return redirect(request.referrer)
            else: 
                c_password = request.form['confirm_password']
                if password != c_password:
                    flash('Passwords did not match. Operation failed', 'danger')
                    return redirect(request.referrer)

                old_password = hashlib.sha256(old_password.encode()).hexdigest()
                cur = mysql.connection.cursor()
                query = "SELECT user_id, password FROM App_users WHERE user_id=" + user_id
                cur.execute(query)
                result = cur.fetchone()
                if result is not None and result[1] == old_password:                           
                    cur = mysql.connection.cursor()
                    password = hashlib.sha256(password.encode()).hexdigest()
                    values = (name, phone, email, password)
                    
                    update_query = 'UPDATE App_users set name=%s, phone=%s, email=%s, password=%s WHERE user_id=' + str(
                        user_id)
                    cur.execute(update_query, values)
                    flash('User details and password updated', 'success')
                    mysql.connection.commit()
                    return redirect(request.referrer)
                else: 
                    flash('Incorrect old password. Operation failed', 'danger')
                    return redirect(request.referrer)
                    
        else:
            cur = mysql.connection.cursor()
            values = (name, phone, email)
            update_query = 'UPDATE App_users set name=%s, phone=%s, email=%s WHERE user_id=' + str(user_id)
            cur.execute(update_query, values)
            flash('Details updated', 'success')
            mysql.connection.commit()
            return redirect(request.referrer)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'email' in session:
            if 'last_route' in session:
                last_route = session['last_route']
                del session['last_route']
                return redirect(last_route)
            else:
                return redirect('/erp')
        else:
            return render_template('login.html')
    else:
        required_fields = ['username', 'password']
        for field in required_fields:
            if field not in list(request.form.keys()):
                flash('Missing fields. Operation failed', 'danger')
                return redirect(request.referrer)

        username = request.form['username']
        password = request.form['password']
        password = hashlib.sha256(password.encode()).hexdigest()
        cur = mysql.connection.cursor()
        query = "SELECT user_id, email, name, role, password, access_level FROM App_users WHERE email='" + username + "'"
        cur.execute(query)
        result = cur.fetchone()
        if result is not None:
            if result[4] == password:
                session['user_id'] = result[0]
                session['email'] = result[1]
                session['role'] = result[3]
                session['name'] = result[2]
                session['access_level'] = result[5]
                session['projects'] = get_projects_for_current_user()
                flash('Logged in successfully', 'success')
                return redirect('/erp')
            else:
                flash('Incorrect credentials', 'danger')
                return redirect('/erp/login')
        else:
            flash('Incorrect credentials. User not found', 'danger')
            return redirect('/erp/login')


@app.route('/mobile_app_banner', methods=['GET', 'POST'])
def mobile_app_banner():
    if request.method == 'GET':
        return render_template('mobile_app_banner.html')
    else:
        if 'banner' in request.files:
            file = request.files['banner']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'mobile_banner.png'))
                flash('Banner updated successfully', 'success')
                return redirect(request.referrer)
            else:
                flash('Invalid file type. Only png images allowed. Operation failed', 'failed')
                return redirect(request.referrer)
        else:
            flash('Missing file. Operation failed', 'failed')
            return redirect(request.referrer)

@app.route('/delete_note', methods=['GET'])
def delete_note():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/enter_material'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO']:
        flash('You do not have permission to delete a note', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        note_id = request.args['id']
        cur = mysql.connection.cursor()
        delete_note_query = 'DELETE from notes_and_comments WHERE id=' + str(note_id)
        cur.execute(delete_note_query)
        mysql.connection.commit()
        flash('Note deleted', 'danger')
        return redirect(request.referrer)

@app.route('/project_notes', methods=['GET','POST'])
def project_notes():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/enter_material'
        return redirect('/erp/login')
    if request.method == 'GET':
        if 'project_id' not in request.args:
            projects = get_projects()
            return render_template('notes_and_comments.html', projects=projects)
        else:
            projects = get_projects()
            project_id = request.args['project_id']
            cur = mysql.connection.cursor()
            get_notes = 'SELECT n.note, n.timestamp, u.name, n.id, n.attachment FROM ' \
                            'notes_and_comments n LEFT OUTER JOIN projects p on p.project_id=n.project_id ' \
                            ' LEFT OUTER JOIN App_users u on u.user_id=n.user_id' \
                            ' WHERE p.project_id =' + str(project_id)
            cur.execute(get_notes)
            res = cur.fetchall()
            return render_template('notes_and_comments.html', projects=projects, notes=res)
    else:
        note = request.form['note']
        IST = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(IST)
        timestamp = current_time.strftime('%d %m %Y at %H %M')
        user_id = session['user_id']
        project_id = request.form['project_id']

        cur = mysql.connection.cursor()
        query = 'INSERT into notes_and_comments(note, timestamp, user_id, project_id) values(%s, %s, %s, %s)'
        cur.execute(query, (note, timestamp, user_id, project_id))

        note_id = cur.lastrowid        
        file = request.files['file']
        if file.filename != '' and file and allowed_file(file.filename):
            filetype = file.filename.split('.')[-1]
            output = send_to_s3(file, app.config["S3_BUCKET"], 'note_'+str(note_id)+'.'+filetype)
            if output != 'success':
                flash('Failed', 'danger')
                return redirect('/erp/project_notes?project_id='+str(project_id))

            cur = mysql.connection.cursor()
            query = 'UPDATE notes_and_comments SET attachment="note_'+str(note_id)+'.'+filetype+'" WHERE id='+str(note_id)
            cur.execute(query)
            mysql.connection.commit()
            

        mysql.connection.commit()
        flash('Note Added', 'success')
        return redirect('/erp/project_notes?project_id='+str(project_id))

@app.route('/enter_material', methods=['GET', 'POST'])
def enter_material():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/enter_material'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'Purchase Head', 'Purchase Executive']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        projects = get_projects()
        vendors = get_vendors()
        return render_template('enter_material.html', projects=projects, vendors=vendors)
    else:
        required_fields = ['material', 'description', 'vendor', 'project', 'po_no', 'invoice_no', 'invoice_date',
                           'quantity', 'unit', 'rate', 'gst', 'total_amount', 'difference_cost', 'photo_date','transportation','loading_unloading']
        for field in required_fields:
            if field not in list(request.form.keys()):
                flash('Missing fields. Operation failed', 'danger')
                return redirect(request.referrer)

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
        photo_date = request.form['photo_date']
        IST = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(IST)
        timestamp = current_time.strftime('%d %m %Y at %H %M')
        
        transportation = request.form['transportation']
        loading_unloading = request.form['loading_unloading']


        cur = mysql.connection.cursor()

        vendor_query = 'SELECT name from vendors WHERE id='+str(vendor)
        cur.execute(vendor_query)
        result = cur.fetchone()
        if result is not None:
            vendor = result[0]

        material_quantity_query = "SELECT total_quantity from kyp_material WHERE project_id=" + str(
            project) + " AND material LIKE '%" + str(material).replace('"','').strip() + "%'"
        cur.execute(material_quantity_query)
        result = cur.fetchone()
        if result is None:
            flash('Total quantity of material has not been specified under KYP material. Entry not recorded', 'danger')
            return redirect('/erp/enter_material')
        if float(result[0]) < (float(quantity)):
            flash('Total quantity of material exceeded limit specified under KYP material. Entry not recorded',
                  'danger')
            return redirect('/erp/enter_material')

        query = "INSERT into procurement (material, description, vendor, project_id, po_no, invoice_no, invoice_date," \
                "quantity, unit, rate, gst, total_amount, difference_cost, photo_date, transportation, loading_unloading, created_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (material, description, vendor, project, po_no, invoice_no, invoice_date, quantity, unit, rate, gst,
                  total_amount, difference_cost, photo_date, transportation, loading_unloading, timestamp)
        cur.execute(query, values)
        mysql.connection.commit()
        flash('Material was inserted successfully', 'success')
        return redirect('/erp/enter_material')


@app.route('/view_inventory', methods=['GET'])
def view_inventory():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_inventory'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'Purchase Head', 'Purchase Executive']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    cur = mysql.connection.cursor()
    projects = get_projects()
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
            procurement_query = 'SELECT * from procurement WHERE project_id=' + str(
                project_id) + ' AND material="' + str(material) + '"'
        cur.execute(procurement_query)
        procurements = cur.fetchall()
        for i in projects:
            if str(i[0]) == str(project_id):
                project = i[1]

        material_quantity_query = "SELECT total_quantity from kyp_material WHERE project_id=" + str(
            project_id) + " AND material LIKE '%" + str(material).replace('"','').strip() + "%'"
        cur.execute(material_quantity_query)
        result = cur.fetchone()
        if result is not None:
            material_total_quantity = result[0]
    return render_template('view_inventory.html', projects=projects, procurements=procurements, project=project,
                           material=material, material_total_quantity=material_total_quantity)

@app.route('/debit_note', methods=['GET','POST'])
def debit_note():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/edit_procurement'
        return redirect('/erp/login')
    if request.method == 'GET':
        projects = get_projects()

        cur = mysql.connection.cursor()
        contractors_query = 'SELECT id, name, trade FROM contractors'
        cur.execute(contractors_query)
        contractors = cur.fetchall()

        return render_template('debit_note.html', contractors=contractors, projects=projects)
    else:
        project = request.form['project']
        contractor = request.form['contractor']
        trade = request.form['trade']
        stage = request.form['stage'] + '(Debit note)'
        value = request.form['value']

        IST = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(IST)
        timestamp = current_time.strftime('%d %m %Y at %H %M')

        cur = mysql.connection.cursor()
        contractor_query = 'SELECT name, code, pan from contractors WHERE id='+str(contractor)
        cur.execute(contractor_query)
        res = cur.fetchone()

        get_wo_query = 'SELECT id from work_orders WHERE trade=%s AND project_id=%s AND contractor_id=%s'
        cur.execute(get_wo_query, (trade, project, contractor))
        wo_res = cur.fetchone()
        if wo_res is None:
            flash('Work order not created for this trade','danger')
            return redirect(request.referrer)    

        
        bill_query = 'INSERT into wo_bills (project_id, contractor_name, contractor_code, contractor_pan, trade, stage, approval_2_amount, approved_on) values (%s,%s,%s,%s,%s,%s,%s,%s)'
        values = (project, res[0], res[1], res[2], trade, stage, str(value).strip(), timestamp)
        cur.execute(bill_query, values)
        mysql.connection.commit()
        flash('Debit note created successfully', 'success')
        return redirect(request.referrer)

@app.route('/edit_procurement', methods=['GET','POST'])
def edit_procurement():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/edit_procurement'
        return redirect('/erp/login')
    if request.method == 'GET':
        if 'procurement_id' not in request.args:
            flash('Something went wrong', 'danger')
            return redirect(request.referrer)
        if 'procurement_id' in request.args:
            procurement_id = request.args['procurement_id']
            procurement_query = 'SELECT * from procurement WHERE id=' + str(procurement_id) 
            cur = mysql.connection.cursor()
            cur.execute(procurement_query)
            result = cur.fetchone()
            return render_template('edit_procurement.html', data=result)
    else:
        procurement_id = request.form['procurement_id']
        material = request.form['material']
        description = request.form['description']
        po_no = request.form['po_no']
        invoice_no = request.form['invoice_no']
        invoice_date = request.form['invoice_date']
        quantity = request.form['quantity']
        unit = request.form['unit']
        rate = request.form['rate']
        gst = request.form['gst']
        total_amount = request.form['total_amount']
        difference_cost = request.form['difference_cost']
        photo_date = request.form['photo_date']
        IST = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(IST)
        project=request.form['project_id']
        timestamp = current_time.strftime('%d %m %Y at %H %M')
        
        transportation = request.form['transportation']
        loading_unloading = request.form['loading_unloading']


        cur = mysql.connection.cursor()

        material_quantity_query = "SELECT total_quantity from kyp_material WHERE project_id=" + str(
            project) + " AND material LIKE '%" + str(material).replace('"','').strip() + "%'"
        cur.execute(material_quantity_query)
        result = cur.fetchone()
        if result is None:
            flash('Total quantity of material has not been specified under KYP material. Entry not recorded', 'danger')
            return redirect('/erp/enter_material')
        if float(result[0]) < (float(quantity)):
            flash('Total quantity of material exceeded limit specified under KYP material. Entry not recorded',
                  'danger')
            return redirect('/erp/enter_material')

        query = 'UPDATE procurement set material=%s, description=%s, po_no=%s, invoice_no=%s, invoice_date=%s, quantity=%s, unit=%s, rate=%s, gst=%s,' \
                  'total_amount=%s, difference_cost=%s, photo_date=%s, transportation=%s, loading_unloading=%s WHERE id='+str(procurement_id)
        values = (material, description, po_no, invoice_no, invoice_date, quantity, unit, rate, gst,
                  total_amount, difference_cost, photo_date, transportation, loading_unloading)
    

        cur.execute(query, values)
        mysql.connection.commit()
        flash('Procurement was updated successfully', 'success')
        return redirect('/erp/view_inventory?project_id='+project+'&material=All')

    

@app.route('/shifting_entry', methods=['GET', 'POST'])
def shifting_entry():
    if request.method == 'GET':
        if 'email' not in session:
            flash('You need to login to continue', 'danger')
            session['last_route'] = '/erp/view_inventory'
            return redirect('/erp/login')
        projects = get_projects()
        material_quantity_data = {
            'PCC M 7.5': '',
            'PCC M 15': '',
            'M 20': '',
            'M 25': '',
            'Red Bricks': '',
            'Exposed Bricks': '',
            'Wirecut bricks': '',
            'Earth Blocks': '',
            'Interlocking Blocks': '',
            'Solid blocks 4"': '',
            'Solid blocks 6"': '',
            'Solid blocks 8"': '',
            'Porotherm Full blocks 8"': '',
            'Porotherm Full blocks 6"': '',
            'Porotherm Full blocks 4"': '',
            'Porotherm End blocks 8"': '',
            'Porotherm End blocks 6"': '',
            'Porotherm End blocks 4"': '',
            'AAC Blocks 8"': '',
            'AAC Blocks 6"': '',
            'AAC Blocks 4"': '',
            'Glass blocks': '',
            'Jaali blocks': '',
            'Door frames': '',
            'Door Beading': '',
            'Door Shutters': '',
            'Windows frames': '',
            'Windows shutters': '',
            'UPVC windows': '',
            'Aluminum windows': '',
            'Window glass': '',
            'Hexagonl Rod': '',
            'Granite': '',
            'Tiles': '',
            'Marble': '',
            'Kota stone': '',
            'HPL Cladding': '',
            'Shera Cladding': '',
            'Floor mat': '',
            'Plumbing': '',
            'Sanitary': '',
            'Aggregates 12mm': '',
            'Aggregates 20mm': '',
            'Aggregates 40mm': '',
            'Cinder': '',
            'Size stone': '',
            'Boulders': '',
            'River sand': '',
            'POP': '',
            'white cement': '',
            'tile adhesive': '',
            'tile grout': '',
            'lime paste': '',
            'Sponge': '',
            'chicken mesh': '',
            'Motor': '',
            'Curing Pipe': '',
            'Helmet': '',
            'Jackets': '',
            'GI sheets': '',
            'Tarpaulin': '',
            'Nails': '',
            'Cement': '',
            'Steel': '',
            'M Sand': '',
            'P Sand': '',
            'Teak wood frame': '',
            'Sal wood frame': '',
            'Honne wood frame': '',
            'Teak wood door': '',
            'Sal wood door': '',
            'Flush door': '',
            'Binding wire': '',
            'Hardwares': '' ,
            'Chamber Covers': '' ,
            'Filler slab material': ''         
        }

        return render_template('shifting_entry.html', projects=projects, material_quantity_data=material_quantity_data)
    else:
        from_project = request.form['from_project']
        to_project = request.form['to_project']
        if from_project == to_project:
            flash('Shifting entry failed. Cannot shift to same project', 'danger')
            return redirect(request.referrer)

        cur = mysql.connection.cursor()

        from_project_name = ''
        from_project_name_query = 'SELECT project_name FROM projects WHERE project_id='+str(from_project)
        cur.execute(from_project_name_query)
        result = cur.fetchone()
        if result is not None:
            from_project_name = result[0]

        
        to_project_name = ''
        to_project_name_query = 'SELECT project_name FROM projects WHERE project_id='+str(to_project)
        cur.execute(to_project_name_query)
        result = cur.fetchone()
        if result is not None:
            to_project_name = result[0]



        material = request.form['material']
        quantity = request.form['quantity']
        unit = request.form['unit']
        difference_cost = request.form['difference_cost']
        description = 'Shifting entry'
        negative_diff = ''
        positive_diff = ''
        if difference_cost != '':
            negative_diff = '-'+str(difference_cost)
            positive_diff = str(difference_cost)

        IST = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(IST)
        timestamp = current_time.strftime('%d %m %Y at %H %M')

        material_quantity_query = "SELECT total_quantity from kyp_material WHERE project_id=" + str(
            from_project) + " AND material LIKE '%" + str(material).replace('"','').strip() + "%'"
        
        cur.execute(material_quantity_query)
        result = cur.fetchone()
        if result is None:
            flash('Total quantity of material has not been specified under KYP material of source project. Entry not recorded', 'danger')
            return redirect('/erp/enter_material')
        if float(result[0]) < (float(quantity)):
            flash('Total quantity of material exceeded limit specified under KYP material of source project. Entry not recorded',
                  'danger')
            return redirect('/erp/enter_material')

        material_quantity_query = "SELECT total_quantity from kyp_material WHERE project_id=" + str(
            from_project) + " AND material LIKE '%" + str(material).replace('"','').strip() + "%'"
        
        cur.execute(material_quantity_query)
        result = cur.fetchone()
        if result is None:
            flash('Total quantity of material has not been specified under KYP material of destination project. Entry not recorded', 'danger')
            return redirect('/erp/enter_material')
        if float(result[0]) < (float(quantity)):
            flash('Total quantity of material exceeded limit specified under KYP material of destination project. Entry not recorded',
                  'danger')
            return redirect('/erp/enter_material')

        check_if_shifting_is_possible = 'SELECT SUM(quantity) from procurement WHERE project_id=%s AND material=%s'
        
        cur.execute(check_if_shifting_is_possible, (from_project, material))
        result = cur.fetchone()

        if result[0] is None or (result is not None and result[0] is not None and int(quantity) < int(result[0])):
            deduction_query = "INSERT into procurement (material, description, project_id," \
                          "quantity, unit, difference_cost) values (%s, %s, %s, %s, %s, %s)"
            values = (material, description+' to '+to_project_name+' on '+timestamp, from_project, int(quantity) * -1, unit, negative_diff)
            cur.execute(deduction_query, values)

            addition_query = "INSERT into procurement (material, description, project_id," \
                            "quantity, unit, difference_cost) values (%s, %s,  %s, %s, %s, %s)"
            values = (material, description+" from "+from_project_name+' on '+timestamp, to_project, quantity, unit, positive_diff)
            cur.execute(addition_query, values)

            mysql.connection.commit()
            flash('Shifting entry successful. Material Shifted!', 'success')
            return redirect(request.referrer)


        else:
            flash('Shifting entry failed. Insufficient quantity in source project', 'danger')
            return redirect(request.referrer)
        

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/create_user'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'Billing']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        return render_template('create_user.html', roles=roles)
    else:
        required_fields = ['name', 'role', 'email', 'phone', 'password', 'confirm_password']
        for field in required_fields:
            if field not in list(request.form.keys()):
                flash('Missing fields. Operation failed', 'danger')
                return redirect(request.referrer)

        name = request.form['name']
        role = request.form['role']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        c_password = request.form['confirm_password']
        if password != c_password:
            flash('Passwords did not match. Operation failed', 'danger')
            return redirect(request.referrer)
        cur = mysql.connection.cursor()
        password = hashlib.sha256(password.encode()).hexdigest()

        check_if_user_exists = 'SELECT user_id from App_users WHERE email="' + str(email) + '"'
        cur.execute(check_if_user_exists)
        res = cur.fetchone()
        if res is not None:
            update_query = 'UPDATE App_users set name=%s, role=%s, phone=%s, password=%s WHERE user_id=' + str(res[0])
            cur.execute(update_query, (name, role, phone, password))
            flash('User with that email already exists. Role updated', 'warning')
        else:
            new_user_query = 'INSERT into App_users (name, role, email, phone, password) values(%s, %s, %s, %s, %s)'
            values = (name, role, email, phone, password)
            cur.execute(new_user_query, values)
            flash('User created successfully', 'success')
        mysql.connection.commit()
        return redirect('/erp/view_users')


@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/edit_user'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'Billing']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        user_id = request.args['user_id']
        cur = mysql.connection.cursor()
        view_user_query = 'SELECT user_id, email, name, role, phone FROM App_users WHERE user_id=' + str(user_id)
        cur.execute(view_user_query)
        result = cur.fetchone()
        return render_template('edit_user.html', user=result, roles=roles)
    else:
        required_fields = ['name', 'role', 'email', 'phone', 'password', 'confirm_password']
        for field in required_fields:
            if field not in list(request.form.keys()):
                flash('Missing fields. Operation failed', 'danger')
                return redirect(request.referrer)

        user_id = request.form['user_id']
        name = request.form['name']
        role = request.form['role']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        if len(password.strip()) > 0:
            c_password = request.form['confirm_password']
            if password != c_password:
                flash('Passwords did not match. Operation failed', 'danger')
                return redirect(request.referrer)
            cur = mysql.connection.cursor()
            password = hashlib.sha256(password.encode()).hexdigest()
            values = (name, role, phone, email, password)
            update_query = 'UPDATE App_users set name=%s, role=%s, phone=%s, email=%s, password=%s WHERE user_id=' + str(
                user_id)
            cur.execute(update_query, values)
            flash('User details and password updated', 'success')
            mysql.connection.commit()
            return redirect('/erp/view_users')
        else:
            cur = mysql.connection.cursor()
            values = (name, role, phone, email)
            update_query = 'UPDATE App_users set name=%s, role=%s, phone=%s, email=%s WHERE user_id=' + str(user_id)
            cur.execute(update_query, values)
            flash('User updated', 'success')
            mysql.connection.commit()
            return redirect('/erp/view_users')


@app.route('/delete_user', methods=['GET'])
def delete_user():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/delete_user'
        return redirect('/erp/login')

    if session['role'] not in ['Super Admin', 'COO', 'Billing']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)

    if 'user_id' not in request.args:
        flash('Missing fields. Operation failed', 'danger')
        return redirect(request.referrer)

    user_id = request.args['user_id']
    cur = mysql.connection.cursor()
    delete_user_query = 'DELETE from App_users WHERE user_id=' + str(user_id)
    cur.execute(delete_user_query)
    mysql.connection.commit()
    flash('User deleted', 'danger')
    return redirect('/erp/view_users')


@app.route('/view_users', methods=['GET'])
def view_users():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_users'
        return redirect('/erp/login')

    if session['role'] not in ['Super Admin', 'COO', 'Billing']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)

    cur = mysql.connection.cursor()
    view_users_query = 'SELECT user_id, email, name, role, phone FROM App_users'
    cur.execute(view_users_query)
    result = cur.fetchall()
    return render_template('view_users.html', users=result)


@app.route('/contractor_registration', methods=['GET', 'POST'])
def contractor_registration():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/vendor_registration'
        return redirect('/erp/login')

    if request.method == 'GET':
        cur = mysql.connection.cursor()
        trades_query = 'SELECT DISTINCT trade from labour_stages'
        cur.execute(trades_query)
        result = cur.fetchall()
        trades = []
        for i in result:
            trades.append(i[0])
        trades.append('NT/NMR')
        return render_template('contractor_registration.html', trades=trades)
    else:
        column_names = list(request.form.keys())
        values = list(request.form.values())
        values[2] = str(request.form.getlist('trade')).replace("'","")

        cur = mysql.connection.cursor()

        check_if_code_exists = 'SELECT id FROM contractors WHERE code="'+request.form['code']+'"'
        cur.execute(check_if_code_exists)
        res = cur.fetchone()
        if res is not None:
            flash('Contractor with that code already exists. Operation failed', 'danger')
            return redirect(request.referrer)

        new_vendor_query = 'INSERT into contractors' + str(tuple(column_names)).replace("'", "") + 'values ' + str(
            tuple(values))
        cur.execute(new_vendor_query)
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file.filename == '':
                flash('No selected file', 'danger ')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                picture_filename = 'contractor_dp_' + str(cur.lastrowid)
                output = send_to_s3(file, app.config["S3_BUCKET"], picture_filename)
                if output != 'success':
                    flash('File upload failed', 'danger')
                    return redirect(request.referrer)
        mysql.connection.commit()
        flash('Contractor registered', 'success')
        return redirect('/erp/view_contractors')


@app.route('/view_contractors', methods=['GET'])
def view_contractors():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_contractors'
        return redirect('/erp/login')

    cur = mysql.connection.cursor()
    contractors_query = 'SELECT id, name, code, pan, phone_number, address, trade, aadhar FROM contractors'
    cur.execute(contractors_query)
    result = cur.fetchall()
    return render_template('view_contractors.html', contractors=result)


@app.route('/edit_contractor', methods=['GET', 'POST'])
def edit_contractor():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/edit_contractor'
        return redirect('/erp/login')
    if request.method == 'GET':
        if 'contractor_id' in request.args:
            cur = mysql.connection.cursor()
            contractor_query = 'SELECT * from contractors WHERE id=' + request.args['contractor_id']
            cur.execute(contractor_query)
            contractor_details = cur.fetchone()
            trades_query = 'SELECT DISTINCT trade from labour_stages'
            cur.execute(trades_query)
            result = cur.fetchall()
            trades = []
            for i in result:
                trades.append(i[0])
            return render_template('edit_contractor.html', trades=trades, contractor_details=contractor_details[1:],
                                   contractor_id=request.args['contractor_id'])
    else:
        cur = mysql.connection.cursor()

        column_names = list(request.form.keys())

        update_string = ""
        for i in column_names[:-1]:
            if i=='trade': 
                update_string += i + '="' + str(request.form.getlist('trade')).replace("'","") + '", '
            else:
                update_string += i + '="' + request.form[i] + '", '
        # Remove the last comma
        update_string = update_string[:-2]
        update_vendor_query = 'UPDATE contractors SET ' + update_string + ' WHERE id=' + str(
            request.form['contractor_id'])
        cur.execute(update_vendor_query)
        mysql.connection.commit()

        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file.filename != '':                
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    picture_filename = 'contractor_dp_' + str(request.form['contractor_id'])
                    output = send_to_s3(file, app.config["S3_BUCKET"], picture_filename)
                    if output != 'success':
                        flash('File upload failed', 'danger')
                        return redirect(request.referrer)
        flash('Contractor updated successfully', 'success')
        return redirect('/erp/view_contractors')


@app.route('/delete_contractor', methods=['GET'])
def delete_contractor():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/delete_contractor'
        return redirect('/erp/login')
    if request.method == 'GET':
        if 'contractor_id' in request.args:
            cur = mysql.connection.cursor()
            contractor_query = 'DELETE from contractors WHERE id=' + request.args['contractor_id']
            cur.execute(contractor_query)
            mysql.connection.commit()
            flash('Contractor deleted', 'danger')
            return redirect('/erp/view_contractors')


@app.route('/vendor_registration', methods=['GET', 'POST'])
def vendor_registration():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/vendor_registration'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'Purchase Head', 'Purchase Executive']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        return render_template('vendor_registration.html')
    else:
        column_names = list(request.form.keys())
        values = list(request.form.values())
        values[2] = str(request.form.getlist('location')).replace("'","")
        values[7] = str(request.form.getlist('material_type')).replace("'","")

        cur = mysql.connection.cursor()

        check_query = 'SELECT id from vendors WHERE code="'+request.form['code']+'"'
        cur.execute(check_query)
        result = cur.fetchone()
        if result is not None:
            flash('Vendor with code '+request.form['code']+' already exists', 'danger')
            return redirect(request.referrer)

        new_vendor_query = 'INSERT into vendors' + str(tuple(column_names)).replace("'", "") + 'values ' + str(
            tuple(values))
        cur.execute(new_vendor_query)
        mysql.connection.commit()

        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file.filename == '':
                flash('No selected file', 'danger ')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                picture_filename = 'vendor_dp_' + str(cur.lastrowid)
                output = send_to_s3(file, app.config["S3_BUCKET"], picture_filename)
                if output != 'success':
                    flash('File upload failed', 'danger')
                    return redirect(request.referrer)
        flash('Vendor registered', 'success')
        return redirect('/erp/view_vendors')


@app.route('/view_vendors', methods=['GET'])
def view_vendors():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_vendors'
        return redirect('/erp/login')

    if session['role'] not in ['Super Admin', 'COO', 'Purchase Head', 'Purchase Executive']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)

    cur = mysql.connection.cursor()
    vendors_query = 'SELECT id, name, code, contact_no FROM vendors ORDER by name'
    cur.execute(vendors_query)
    result = cur.fetchall()
    return render_template('view_vendors.html', vendors=result)


# Field validation for form done till here

@app.route('/view_vendor_details', methods=['GET'])
def view_vendor_details():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_vendor_details'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'Purchase Head', 'Purchase Executive']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    vendor_details = []
    if 'vendor_id' in request.args:
        cur = mysql.connection.cursor()
        vendor_query = 'SELECT * from vendors WHERE id=' + request.args['vendor_id']
        cur.execute(vendor_query)
        vendor_details = cur.fetchone()
    return render_template('view_vendor_details.html', vendor_details=vendor_details[1:])


@app.route('/edit_vendor', methods=['GET', 'POST'])
def edit_vendor():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/edit_vendor'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'Purchase Head', 'Purchase Executive']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        if 'vendor_id' in request.args:
            cur = mysql.connection.cursor()
            vendor_query = 'SELECT * from vendors WHERE id=' + request.args['vendor_id']
            cur.execute(vendor_query)
            vendor_details = cur.fetchone()
            return render_template('edit_vendor.html', vendor_details=vendor_details[1:],
                                   vendor_id=request.args['vendor_id'])
    else:
        cur = mysql.connection.cursor()
        


        column_names = list(request.form.keys())[:-1]

        update_string = ""
        for i in column_names[:-1]:
            if i=='location':
                update_string += i + '="' + str(request.form.getlist('location')).replace("'","''").replace('"','""') + '", '
            elif i=='material_type': 
                update_string += i + '="' + str(request.form.getlist('material_type')).replace("'","''").replace('"','""') + '", '
            else:
                update_string += i + '="' + request.form[i] + '", '
        # Remove the last comma
        update_string = update_string[:-2]
        update_vendor_query = 'UPDATE vendors SET ' + update_string + ' WHERE id=' + str(
            request.form['vendor_id'])
        
        cur.execute(update_vendor_query)
        mysql.connection.commit()
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file.filename == '':
                flash('No selected file', 'danger ')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                picture_filename = 'vendor_dp_' + str(request.form['contractor_id'])
                output = send_to_s3(file, app.config["S3_BUCKET"], picture_filename)
                if output != 'success':
                    flash('File upload failed', 'danger')
                    return redirect(request.referrer)
        flash('Vendor updated successfully', 'success')
        return redirect('/erp/view_vendor_details?vendor_id=' + request.form['vendor_id'])


@app.route('/delete_vendor', methods=['GET'])
def delete_vendor():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/delete_vendor'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'Purchase Head', 'Purchase Executive']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        if 'vendor_id' in request.args:
            cur = mysql.connection.cursor()
            vendor_query = 'DELETE from vendors WHERE id=' + request.args['vendor_id']
            cur.execute(vendor_query)
            mysql.connection.commit()
            flash('Vendor deleted', 'danger')
            return redirect('/erp/view_vendors')


def get_vendors():
    cur = mysql.connection.cursor()
    vendors_query = 'SELECT id, name, code FROM vendors'
    cur.execute(vendors_query)
    result = cur.fetchall()
    vendors = {}
    for i in result:
        vendors[str(i[0])] = str(i[1]) + str(i[2])
    return vendors

@app.route('/get_vendors_for_material', methods=['POST'])
def get_vendors_for_material():
    material_selected = request.form['material_selected']
    cur = mysql.connection.cursor() 
    material_selected = material_selected.replace('"','')
    query = "SELECT id, name from vendors WHERE material_type LIKE '%" + material_selected + "%'"
    cur.execute(query)
    res = cur.fetchall()
    return jsonify(res)


@app.route('/kyp_material', methods=['GET', 'POST'])
def kyp_material():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/kyp_material'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'Purchase Head', 'Purchase Executive']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    material_quantity_data = {
        'PCC M 7.5': '',
        'PCC M 15': '',
        'M 20': '',
        'M 25': '',
        'Red Bricks': '',
        'Exposed Bricks': '',
        'Wirecut bricks': '',
        'Earth Blocks': '',
        'Interlocking Blocks': '',
        'Solid blocks 4"': '',
        'Solid blocks 6"': '',
        'Solid blocks 8"': '',
        'Porotherm Full blocks 8"': '',
        'Porotherm Full blocks 6"': '',
        'Porotherm Full blocks 4"': '',
        'Porotherm End blocks 8"': '',
        'Porotherm End blocks 6"': '',
        'Porotherm End blocks 4"': '',
        'AAC Blocks 8"': '',
        'AAC Blocks 6"': '',
        'AAC Blocks 4"': '',
        'Glass blocks': '',
        'Jaali blocks': '',
        'Door frames': '',
        'Door Beading': '',
        'Door Shutters': '',
        'Windows frames': '',
        'Windows shutters': '',
        'UPVC windows': '',
        'Aluminum windows': '',
        'Window glass': '',
        'Hexagonl Rod': '',
        'Granite': '',
        'Tiles': '',
        'Marble': '',
        'Kota stone': '',
        'HPL Cladding': '',
        'Shera Cladding': '',
        'Floor mat': '',
        'Plumbing': '',
        'Sanitary': '',
        'Aggregates 12mm': '',
        'Aggregates 20mm': '',
        'Aggregates 40mm': '',
        'Cinder': '',
        'Size stone': '',
        'Boulders': '',
        'River sand': '',
        'POP': '',
        'white cement': '',
        'tile adhesive': '',
        'tile grout': '',
        'lime paste': '',
        'Sponge': '',
        'chicken mesh': '',
        'Motor': '',
        'Curing Pipe': '',
        'Helmet': '',
        'Jackets': '',
        'GI sheets': '',
        'Tarpaulin': '',
        'Nails': '',
        'Cement': '',
        'Steel': '',
        'M Sand': '',
        'P Sand': '',
        'Teak wood frame': '',
        'Sal wood frame': '',
        'Honne wood frame': '',
        'Teak wood door': '',
        'Sal wood door': '',
        'Flush door': '' ,
        'Binding wire': '',
        'Hardwares': '' ,
        'Chamber Covers': '' ,
        'Filler slab material': ''      

    }
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        projects = get_projects()

        project = None
        project_id = None
        if 'project_id' in request.args:
            project_id = request.args['project_id']
            material_query = 'SELECT * from kyp_material WHERE project_id=' + str(project_id)
            cur.execute(material_query)
            result = cur.fetchall()
            for i in result:
                material_name = i[2]
                material_quantity_data[material_name] = i[3]
            for i in projects:
                if str(i[0]) == str(project_id):
                    project = i[1]
        return render_template('kyp_material.html', projects=projects, project_id=project_id, project=project,
                               material_quantity_data=material_quantity_data)
    else:
        cur = mysql.connection.cursor()
        project_id = request.form['project_id']
        delete_old_quantity_chart_query = 'DELETE from kyp_material WHERE project_id=' + str(project_id)
        cur.execute(delete_old_quantity_chart_query)
        for i in material_quantity_data:
            quantity_of_i = request.form[i]

            if len(str(quantity_of_i)):
                material_quantity_insert_query = "INSERT into kyp_material (project_id, material, total_quantity) values (" + str(
                    project_id) + ",'" + str(i) + "','" + str(quantity_of_i) + "')"

                cur.execute(material_quantity_insert_query)
                mysql.connection.commit()
        flash('Quantity chart updated successfully', 'success')
        return redirect('/erp/kyp_material?project_id=' + str(project_id))


@app.route('/delete_wo', methods=['GET'])
def delete_wo():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/create_work_order'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin']:
        flash('You do not have permission delete', 'danger')
        return redirect(request.referrer)
    wo_id = request.args['id']
    cur = mysql.connection.cursor()
    query = 'DELETE FROM work_orders WHERE id='+wo_id
    cur.execute(query)
    mysql.connection.commit()
    flash('Work order has been deleted', 'danger')
    return redirect(request.referrer)

@app.route('/create_work_order', methods=['GET', 'POST'])
def create_work_order():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/create_work_order'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'QS Head', 'QS Engineer']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        projects = get_projects()
        floors = ['G + 1', 'G + 2', 'G + 3', 'G + 4']
        trades_query = 'SELECT DISTINCT trade from labour_stages'
        cur.execute(trades_query)
        result = cur.fetchall()
        trades = []
        for i in result:
            trades.append(i[0])
        contractors = []
        contractors_query = 'SELECT id, name, trade FROM contractors'
        cur.execute(contractors_query)
        result = cur.fetchall()
        for i in result:
            contractors.append(i)
        return render_template('create_work_order.html', projects=projects, floors=floors, trades=trades,
                               contractors=contractors)
    else:
        project_id = request.form['project']
        contractor_id = request.form['contractor_id']
        wo_value = request.form['wo_value']
        wo_number = request.form['wo_number']
        cheque_no = request.form['cheque_no']
        comments = request.form['comments']
        total_bua = request.form['total_bua']
        cost_per_sqft = request.form['cost_per_sqft']
        IST = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(IST)
        timestamp = current_time.strftime('%d %m %Y at %H %M')

        milestones = request.form.getlist('milestone[]')
        percentages = request.form.getlist('percentage[]')

        percentage_sum_total = 0
        try:
            for i in percentages:
                percentage_sum_total += float(i)
            if int(percentage_sum_total) != 100:
                flash('Percentages do not add up to 100', 'danger')
                return redirect(request.referrer)
        except:
            flash('Percentages do not add up to 100', 'danger')
            return redirect(request.referrer)

        cur = mysql.connection.cursor()

        trade = request.form['trade']

        check_if_exist_query = 'SELECT id from work_orders WHERE project_id=' + str(project_id) + ' AND trade="' + str(
            trade) + '" AND contractor_id='+str(contractor_id)
        cur.execute(check_if_exist_query)   
        result = cur.fetchone()
        if result is not None:
            flash("Work order already exists. Operation failed", 'danger')
            return redirect('/erp/create_work_order')
        else:
            verification_code = str(random.randint(1000,9999))
            insert_query = 'INSERT into work_orders (project_id, value, trade, wo_number, cheque_no, contractor_id, comments, created_at, total_bua, cost_per_sqft, verification_code) ' \
                           'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            values = (project_id, wo_value, trade, wo_number, cheque_no, contractor_id, comments, timestamp, total_bua, cost_per_sqft, verification_code)
            cur.execute(insert_query, values)

            work_order_id = cur.lastrowid
            for i in range(len(milestones)):
                if milestones[i].strip() != '' and percentages[i].strip() != '':
                    insert_milestones_query = 'INSERT into wo_milestones(work_order_id, stage, percentage) values (%s, %s, %s)'
                    cur.execute(insert_milestones_query, (work_order_id, milestones[i], percentages[i]))

            mysql.connection.commit()
            flash('Work order created successfully', 'success')

            return redirect('/erp/create_work_order')

@app.route('/get_milsetones', methods=['GET', 'POST'])
def get_milsetones():
    work_order_id = request.form['work_order_id']
    cur = mysql.connection.cursor()
    milestones_query = 'SELECT stage, percentage from wo_milestones WHERE work_order_id='+str(work_order_id)
    cur.execute(milestones_query)
    result = cur.fetchall()
    return jsonify(list(result))


@app.route('/create_bill', methods=['GET', 'POST'])
def create_bill():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/create_bill'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'QS Head', 'QS Engineer']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        projects = get_projects()
        cur = mysql.connection.cursor()
        contractors_query = 'SELECT id, name FROM contractors'
        cur.execute(contractors_query)
        result = cur.fetchall()
        return render_template('create_bill.html', projects=projects, contractors=result)
    else:
        project_id = request.form['project_id']
        trade = request.form['trade']
        IST = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(IST)
        timestamp = current_time.strftime('%d %m %Y at %H %M')
        cur = mysql.connection.cursor()
        if trade == 'NT/NMR':
            quantity = request.form['quantity']
            rate = request.form['rate']
            nt_nmr_bill_amount = request.form['nt_nmr_bill_amount']
            description = request.form['description']

            contractor_query = 'SELECT name, code, pan from contractors WHERE id='+request.form['contractor']
            cur.execute(contractor_query)
            res = cur.fetchone()

            insert_query = 'INSERT into wo_bills (project_id, trade, stage, payment_percentage, amount, total_payable, contractor_name, contractor_code, contractor_pan, created_at, quantity, rate) values (%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s,%s ,%s)'
            values = (project_id, trade, description,'', nt_nmr_bill_amount, nt_nmr_bill_amount, res[0], res[1], res[2], timestamp, quantity, rate)
            cur.execute(insert_query, values)
            mysql.connection.commit()
            flash('Bill created successfully', 'success')
            return redirect('/erp/create_bill')


        
        stage = request.form['stage']
        payment_percentage = request.form['payment_percentage']
        amount = request.form['amount']
        contractor_name = request.form['contractor_name']
        contractor_code = request.form['contractor_code']
        contractor_pan = request.form['contractor_pan']


        
        total_payable = float(amount)
        check_if_exists_query = 'SELECT id FROM wo_bills WHERE project_id=' + str(project_id) + ' AND trade="' + str(
            trade) + '" AND stage="' + str(stage) + '"'
        cur.execute(check_if_exists_query)
        res = cur.fetchone()
        if res is not None:
            flash("Older bill already exists. Operation failed", 'danger')
            return redirect('/erp/create_bill')
        else:
            insert_query = 'INSERT into wo_bills (project_id, trade, stage, payment_percentage, amount, total_payable, contractor_name, contractor_code, contractor_pan, created_at) values (%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s)'
            values = (
            project_id, trade, stage, payment_percentage, amount, total_payable, contractor_name, contractor_code,
            contractor_pan, timestamp)
            cur.execute(insert_query, values)
            mysql.connection.commit()
            flash('Bill created successfully', 'success')
            return redirect('/erp/create_bill')


@app.route('/update_trades_for_project', methods=['POST'])
def update_trades_for_project():
    project_id = request.form['project_id']
    trades_query = 'SELECT id, trade from work_orders WHERE signed=1 AND approved=1 AND project_id=' + str(project_id)
    cur = mysql.connection.cursor()
    cur.execute(trades_query)
    result = cur.fetchall()
    return jsonify(list(result))

@app.route('/update_trades_for_contractor', methods=['POST'])
def update_trades_for_contractor():
    contractor_id = request.form['contractor_id']
    trades_query = 'SELECT trade from contractors WHERE id=' + str(contractor_id)
    cur = mysql.connection.cursor()
    cur.execute(trades_query)
    result = cur.fetchone()
    trades = []
    if result is not None:
        contractor_trades = result[0]
        if ',' in contractor_trades or ']' in contractor_trades:
            trades = contractor_trades[1:-1].split(',')
        else:
            trades.append(contractor_trades)
    return jsonify(trades)


@app.route('/update_payment_stages', methods=['POST'])
def update_payment_stages():
    project_id = request.form['project_id']    
    trade = request.form['trade']    
    cur = mysql.connection.cursor()
    
    old_bills_query = 'SELECT stage FROM wo_bills WHERE project_id=' + str(project_id) + ' AND trade="' + str(
            trade) + '"'
    cur.execute(old_bills_query)
    res = cur.fetchall()
    old_bills = []
    for i in res:
        old_bills.append(i[0].strip())

    work_order_id_for_trade = request.form['work_order_id_for_trade']
    work_order_query = 'SELECT wo.value, c.name, c.code, c.pan from work_orders wo INNER JOIN contractors c ON ' \
                       'wo.contractor_id=c.id WHERE wo.id=' + str(work_order_id_for_trade)
    cur.execute(work_order_query)
    res = cur.fetchone()
    if res is not None:
        work_order_value = res[0]
        contractor_name = res[1]
        contractor_code = res[2]
        contractor_pan = res[3]
        payment_stages_query = 'SELECT stage, percentage from wo_milestones WHERE work_order_id=' + str(
            work_order_id_for_trade)
        cur.execute(payment_stages_query)
        result = cur.fetchall()
        stages = {}
        for i in result:
            if i[0].strip() not in old_bills:
                stages[i[0]] = i[1].replace('%', '')

        response = {'work_order_value': work_order_value,
                    'stages': stages,
                    'contractor_name': contractor_name,
                    'contractor_code': contractor_code,
                    'contractor_pan': contractor_pan
                    }
        return jsonify(response)


@app.route('/get_standard_milestones_and_percentages', methods=['POST'])
def get_standard_milestones_and_percentages():
    trade = request.form['trade']
    project_id = request.form['project_id']
    if str(trade).strip() == '':
        return jsonify({'message': 'Trade field empty'})
    if str(project_id).strip() == '':
        return jsonify({'message': 'Project id field empty'})
    get_floors_for_project_query = 'SELECT no_of_floors from projects WHERE project_id=' + project_id
    cur = mysql.connection.cursor()
    cur.execute(get_floors_for_project_query)
    res = cur.fetchone()
    if res is None or len(res) == 0:
        return jsonify({'message': 'Project not found with id ' + str(project_id)})
    floors = res[0]
    payment_stages_query = 'SELECT stage, payment_percentage from labour_stages WHERE floors="' + str(
        floors) + '" AND trade="' + trade + '"'
    cur.execute(payment_stages_query)
    result = cur.fetchall()
    milestones_and_percentages = {}
    for i in result:
        milestones_and_percentages[i[0]] = i[1].replace('%', '')
    response = {'milestones_and_percentages': milestones_and_percentages, 'message': 'success'}
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
            {'bill_id': i[16], 'contractor_name': i[7], 'contractor_pan': i[9], 'contractor_code': i[8], 'trade': i[2],
             'stage': i[3], 'amount': i[5], 'total_payable': i[6],
             'approval_1_amount': i[11], 'approval_1_notes': i[12], 'approval_2_amount': i[14],
             'approval_2_notes': i[15], 'created_at': i[17],}
        )
    return data


@app.route('/view_bills', methods=['GET'])
def view_bills():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_bills'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'QS Head']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        coordinators_query = 'SELECT pot.project_id, pot.co_ordinator, u.name, p.project_name FROM project_operations_team pot JOIN App_users u ON pot.co_ordinator = u.user_id JOIN projects p on pot.project_id=p.project_id WHERE co_ordinator is not NULL order by pot.co_ordinator'
        cur = mysql.connection.cursor()
        cur.execute(coordinators_query)
        coordinators_res = cur.fetchall()

        data = {}

        for i in coordinators_res:
            data[i[0]] = {'project_name': i[3], 'coordinator': i[2], 'bills': []}
            bills_query = 'SELECT trade, stage, payment_percentage, amount, total_payable, contractor_name, contractor_code, '\
                        'contractor_pan, approval_1_status, approval_1_amount, approval_1_notes,' \
                        'approval_2_status, approval_2_amount, approval_2_notes, id, created_at' \
                        ' FROM wo_bills WHERE wo_bills.project_id='+ str(i[0]) +' wo_bills.approval_2_amount = 0 OR wo_bills.approval_2_amount IS NULL'
            cur.execute(bills_query)
            res = cur.fetchall()
            for i in res:
                data[i[0]]['bills'].append({
                    'trade': i[0],
                    'stage': i[1],
                    'payment_percentage': i[2],
                    'amount': i[3],
                    'total_payable': i[4],
                    'contractor_name': i[5],
                    'contractor_code': i[6],
                    'contractor_pan': i[7],
                    'approval_1_status': i[8],
                    'approval_1_amount': i[9],
                    'approval_1_notes': i[10],
                    'approval_2_status': i[11],
                    'approval_2_amount': i[12],
                    'approval_2_notes': i[13],
                    'id': i[14],
                    'created_at': i[15]
                
                })
                
        access_level = session['access_level']
        return render_template('view_bills.html', data=data, access_level=access_level)


@app.route('/export_bills', methods=['GET'])
def export_bills():
    bills_query = 'SELECT projects.project_id, projects.project_name, wo_bills.trade, wo_bills.stage, wo_bills.payment_percentage,' \
                  'wo_bills.amount, wo_bills.total_payable, wo_bills.contractor_name, wo_bills.contractor_code, wo_bills.contractor_pan,' \
                  'wo_bills.approval_1_status, wo_bills.approval_1_amount, wo_bills.approval_1_notes,' \
                  'wo_bills.approval_2_status, wo_bills.approval_2_amount, wo_bills.approval_2_notes, wo_bills.id, wo_bills.created_at' \
                  ' FROM wo_bills INNER JOIN projects on wo_bills.project_id = projects.project_id AND wo_bills.is_archived=0 AND ' \
                  '(wo_bills.approval_2_amount != 0 AND wo_bills.approval_2_amount IS NOT NULL)'

    data = get_bills_as_json(bills_query)
    cur = mysql.connection.cursor()
    archive_bill = 'UPDATE wo_bills SET is_archived=1 WHERE approval_2_amount != 0 AND approval_2_amount IS NOT NULL'
    cur.execute(archive_bill)
    rb = open_workbook("../static/bills.xls")
    wb = copy(rb)
    IST = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(IST)
    current_time = current_time.strftime('%d %m %Y at %H %M')
    ws = wb.add_sheet('Bills on ' + str(current_time))
    style = xlwt.XFStyle()

    # font
    font = xlwt.Font()
    font.bold = True
    style.font = font

    
    ws.write(1, 0, 'Contractor Name', style=style)
    ws.write(1, 1, 'Contractor PAN', style=style)
    ws.write(1, 2, 'Contractor Code', style=style)
    ws.write(1, 3, 'Trade', style=style)
    ws.write(1, 4, 'Stage', style=style)
    ws.write(1, 5, 'Amount', style=style)
    ws.write(1, 6, 'Created on', style=style)
    row = 2
    column = 0
    read_only = xlwt.easyxf("")
    for project in data:
        column = 0
        cwidth = ws.col(column).width
        if (len(data[project]['project_name']) * 367) > cwidth:
            ws.col(column).width = (len(data[project]['project_name']) * 367)

        ws.write(row, column, data[project]['project_name'], read_only)
        row = row + 1
        for i in data[project]['bills']:

            column = 0
            ws.write(row, column, i['contractor_name'], read_only)
            cwidth = ws.col(column).width
            if (len(i['contractor_name']) * 367) > cwidth:
                ws.col(column).width = (len(i['contractor_name']) * 367)
            column = column + 1

            ws.write(row, column, i['contractor_pan'], read_only)
            cwidth = ws.col(column).width
            if (len(i['contractor_pan']) * 367) > cwidth:
                ws.col(column).width = (len(i['contractor_pan']) * 367)
            column = column + 1

            ws.write(row, column, i['contractor_code'], read_only)
            cwidth = ws.col(column).width
            if (len(i['contractor_code']) * 367) > cwidth:
                ws.col(column).width = (len(i['contractor_code']) * 367)
            column = column + 1

            ws.write(row, column, i['trade'], read_only)
            cwidth = ws.col(column).width
            if (len(i['trade']) * 367) > cwidth:
                ws.col(column).width = (len(i['trade']) * 367)
            column = column + 1

            ws.write(row, column, i['stage'], read_only)
            cwidth = ws.col(column).width
            if (len(i['stage']) * 367) > cwidth:
                if len(i['stage']) * 367 > 65536:
                    ws.col(column).width = 65535
                else: 
                    ws.col(column).width = (len(i['stage']) * 367)
            column = column + 1

            ws.write(row, column, float(i['approval_2_amount']))
            cwidth = ws.col(column).width
            if (len(i['approval_2_amount']) * 367) > cwidth:
                ws.col(column).width = (len(i['approval_2_amount']) * 367)
            column = column + 1

            ws.write(row, column, i['created_at'])
            cwidth = ws.col(column).width
            if (len(i['created_at']) * 367) > cwidth:
                ws.col(column).width = (len(i['created_at']) * 367)
            column = column + 1
            row = row + 1
        row = row + 1
    mysql.connection.commit()
    wb.save('../static/bills.xls')

    flash('Bills exported successfully', 'success')
    return redirect(request.referrer + '?exported=true')


@app.route('/delete_bill', methods=['GET'])
def delete_bill():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/delete_bill'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'Purchase Head', 'Purchase Executive']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        if 'bill_id' in request.args:
            cur = mysql.connection.cursor()
            delete_bill_query = 'DELETE from wo_bills WHERE id=' + request.args['bill_id']
            cur.execute(delete_bill_query)
            mysql.connection.commit()
            flash('Bill deleted', 'danger')
            return redirect('/erp/view_bills')


@app.route('/view_approved_bills', methods=['GET'])
def view_approved_bills():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_approved_bills'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'QS Head', 'QS Engineer']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        bills_query = 'SELECT projects.project_id, projects.project_name, wo_bills.trade, wo_bills.stage, wo_bills.payment_percentage,' \
                      'wo_bills.amount, wo_bills.total_payable, wo_bills.contractor_name, wo_bills.contractor_code, wo_bills.contractor_pan,' \
                      'wo_bills.approval_1_status, wo_bills.approval_1_amount, wo_bills.approval_1_notes,' \
                      'wo_bills.approval_2_status, wo_bills.approval_2_amount, wo_bills.approval_2_notes, wo_bills.id, wo_bills.created_at' \
                      ' FROM wo_bills INNER JOIN projects on wo_bills.project_id = projects.project_id AND wo_bills.is_archived=0 AND ' \
                      '(wo_bills.approval_2_amount != 0 AND wo_bills.approval_2_amount IS NOT NULL)'
        data = get_bills_as_json(bills_query)
        first_bill_id = 0
        for project in data:
            for i in data[project]['bills']:
                first_bill_id = i['bill_id']
                break
            break
        return render_template('view_approved_bills.html', data=data, first_bill_id=first_bill_id)


@app.route('/view_archived_bills', methods=['GET'])
def view_archived_bills():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_approved_bills'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'QS Head', 'QS Engineer']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        bills_query = 'SELECT projects.project_id, projects.project_name, wo_bills.trade, wo_bills.stage, wo_bills.payment_percentage,' \
                      'wo_bills.amount, wo_bills.total_payable, wo_bills.contractor_name, wo_bills.contractor_code, wo_bills.contractor_pan,' \
                      'wo_bills.approval_1_status, wo_bills.approval_1_amount, wo_bills.approval_1_notes,' \
                      'wo_bills.approval_2_status, wo_bills.approval_2_amount, wo_bills.approval_2_notes, wo_bills.id, wo_bills.created_at' \
                      ' FROM wo_bills INNER JOIN projects on wo_bills.project_id = projects.project_id AND wo_bills.is_archived=1 AND (wo_bills.approval_2_amount != 0 AND wo_bills.approval_2_amount IS NOT NULL)'
        data = get_bills_as_json(bills_query)
        first_bill_id = 0
        for project in data:
            for i in data[project]['bills']:
                first_bill_id = i['bill_id']
                break
            break
        return render_template('view_archived_bills.html', data=data, first_bill_id=first_bill_id)


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
        update_wo_query = 'UPDATE work_orders SET balance=' + str(updated_balance) + ' WHERE id=' + str(res[0])
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
        update_bill_query = 'UPDATE wo_bills SET approval_1_amount = "' + str(
            approved_amount) + '" , approval_1_notes = "' + str(notes) + '" WHERE id=' + str(bill_id)
    elif approval_level == 'Level 2':
        IST = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(IST)
        timestamp = current_time.strftime('%d %m %Y at %H %M')

        update_bill_query = 'UPDATE wo_bills SET approved_on="'+ timestamp +'", approval_2_amount = "' + str(
            approved_amount) + '" , approval_2_notes = "' + str(notes) + '" WHERE id=' + str(bill_id)
    cur.execute(update_bill_query)
    if float(difference_amount) > 0 and approval_level == 'Level 2':
        update_work_order_balance(project_id, trade, difference_amount)
    mysql.connection.commit()
    return jsonify({"message": "success"})


@app.route('/project_contractor_info', methods=["GET"])
def project_contractor_info():
    project_id = request.args['project_id']
    contractor_name = request.args['name']
    contractor_code = request.args['code']
    trade = request.args['trade']

    cur = mysql.connection.cursor()
    data = {'name': '', 'code': '', 'pan': '', 'value': '', 'balance': '', 'trade': '', 'contractor_id': ''}

    get_contractor_query = 'SELECT id, name, code, pan from contractors WHERE code="'+contractor_code+'"'
    cur.execute(get_contractor_query)
    res = cur.fetchone()
    contractor_id = 0
    if res is not None:
        contractor_id = res[0]
        data['name'] = res[1]
        data['code'] = res[2]
        data['pan'] = res[3]

    get_wo_query = 'SELECT id, value, balance from work_orders WHERE trade=%s AND project_id=%s AND contractor_id=%s'
    cur.execute(get_wo_query, (trade, project_id, contractor_id))
    res = cur.fetchone()
    if res is not None:
        data['value'] = res[1]
        data['balance'] = res[2]
        data['trade'] = trade
        data['work_order_id'] = res[0]

    get_bills_query = 'SELECT w.stage, w.percentage, b.amount, b.approval_2_amount, b.trade, b.approved_on' \
                        ' FROM wo_milestones w LEFT OUTER JOIN wo_bills b ON b.stage=w.stage AND b.contractor_code=%s AND b.project_id=%s WHERE w.work_order_id=%s'
    cur.execute(get_bills_query, (contractor_code, project_id, str(data['work_order_id'])))
    bills = []
    res = cur.fetchall()
    for i in res:
        bills.append(i)

    get_debit_note_bills = "SELECT stage, approval_2_amount, trade, approved_on from wo_bills WHERE project_id="+str(project_id)+" AND stage LIKE '%Debit note%' AND contractor_code='"+str(contractor_code)+"' AND trade != 'NT/NMR'"
    cur.execute(get_debit_note_bills)
    res = cur.fetchall()
    for i in res:
        bills.append((i[0],'','',i[1],i[2], i[3]))

    get_project_query = 'SELECT project_name, project_number from projects WHERE project_id=' + str(project_id)
    cur.execute(get_project_query)
    project = cur.fetchone()

    return render_template('project_contractor_info.html', bills=bills, project=project, data=data)

@app.route('/clear_nt_nmr_balance', methods=['GET'])
def clear_nt_nmr_balance():
    bill_id = request.args['bill_id']
    cur = mysql.connection.cursor()
    update_old_bill = 'UPDATE wo_bills SET cleared_balance=1 WHERE id='+str(bill_id)
    cur.execute(update_old_bill)
    mysql.connection.commit()
    
    bill_query = 'SELECT quantity, rate, approval_2_amount, stage, project_id, contractor_name, contractor_code, contractor_pan, trade from wo_bills WHERE id='+str(bill_id)
    cur.execute(bill_query)
    res = cur.fetchone()
    if res is not None:
        amount = int(res[0]) * int(res[1])
        payable  = int(res[2])
        difference = amount - payable
        stage = res[3].replace(' (Clear balance)','')+' (Clear balance)'
        project_id = res[4]
        contractor_name = res[5]
        contractor_code = res[6]
        contractor_pan = res[7]
        trade = res[8]


        bills_query = 'INSERT into wo_bills (project_id, trade, stage, contractor_name, contractor_code, contractor_pan, total_payable) values (%s,%s, %s,%s,%s,%s,%s)'
        cur.execute(bills_query, (project_id, trade, stage, contractor_name, contractor_code, contractor_pan, difference))
        mysql.connection.commit()

        flash('Cleared balance','success')
        return redirect(request.referrer)

@app.route('/clear_wo_balance', methods=['POST'])
def clear_wo_balance():
    balance_amnt = request.form['balance_amnt']
    contractor_name = request.form['contractor_name']
    contractor_code = request.form['contractor_code']
    contractor_pan = request.form['contractor_pan']
    project_id = request.form['project_id']
    trade = request.form['trade']
    work_order_id = request.form['work_order_id']
    stage = 'Clearing balance'

    cur = mysql.connection.cursor()
    bills_query = 'INSERT into wo_bills (project_id, trade, stage, contractor_name, contractor_code, contractor_pan, total_payable) values (%s,%s, %s,%s,%s,%s,%s)'
    cur.execute(bills_query, (project_id, trade, stage, contractor_name, contractor_code, contractor_pan, balance_amnt))

    work_order_query = 'UPDATE work_orders SET balance=0 WHERE id=' + work_order_id
    cur.execute(work_order_query)

    mysql.connection.commit()
    return jsonify({'message': 'success'})


def get_work_orders_for_project(project_id):
    cur = mysql.connection.cursor()
    get_wo_query = 'SELECT wo.id, c.name, c.pan, c.code, wo.trade,  wo.value, wo.balance, wo.filename from work_orders wo ' \
                   'INNER JOIN contractors c on wo.approved=1 AND c.id=wo.contractor_id AND wo.project_id=' + str(
        request.args['project_id']) + ' ORDER BY wo.trade'
    cur.execute(get_wo_query)
    res = cur.fetchall()
    return res


@app.route("/view_work_order", methods=['GET'])
def view_work_order():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_work_order'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'QS Head', 'QS Engineer']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        projects = get_projects()
        nt_nmr_bills = None
        work_orders = []
        if 'project_id' in request.args:
            project_id = request.args['project_id']
            work_orders = get_work_orders_for_project(project_id)

            bills_query = 'SELECT wo_bills.id, wo_bills.contractor_name, wo_bills.contractor_code, wo_bills.stage, wo_bills.quantity,' \
                        ' wo_bills.rate, wo_bills.approval_2_amount, wo_bills.cleared_balance FROM wo_bills WHERE project_id='+str(project_id)+' AND trade="NT/NMR"'
            cur = mysql.connection.cursor()
            cur.execute(bills_query)
            nt_nmr_bills = cur.fetchall()

        return render_template('view_work_orders.html', projects=projects, work_orders=work_orders, nt_nmr_bills=nt_nmr_bills)


@app.route("/view_unsigned_work_order", methods=['GET'])
def view_unsigned_work_order():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_unsigned_work_order'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'QS Head', 'QS Engineer']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        work_orders = []

        unsigned_query = 'SELECT p.project_name, p.project_number, wo.id, wo.trade, wo.value, c.name, wo.verification_code FROM work_orders wo ' \
                         'INNER JOIN projects p on p.project_id=wo.project_id AND wo.signed=0 INNER JOIN contractors c on c.id=wo.contractor_id'
        cur = mysql.connection.cursor()
        cur.execute(unsigned_query)
        result = cur.fetchall()
        for i in result:
            work_orders.append({
                'project_name': i[0],
                'project_number': i[1],
                'id': i[2],
                'trade': i[3],
                'value': i[4],
                'contractor_name': i[5],
                'verification_code': i[6],

            })

        return render_template('unsigned_work_orders.html', work_orders=work_orders)


@app.route("/view_unapproved_work_order", methods=['GET'])
def view_unapproved_work_order():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_unapproved_work_order'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'QS Head']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        work_orders = []

        unsigned_query = 'SELECT p.project_name, p.project_number, wo.id, wo.trade, wo.value, c.name FROM work_orders wo ' \
                         'INNER JOIN projects p on p.project_id=wo.project_id AND wo.signed=1 AND wo.approved=0 INNER JOIN contractors c on c.id=wo.contractor_id'
        cur = mysql.connection.cursor()
        cur.execute(unsigned_query)
        result = cur.fetchall()
        for i in result:
            work_orders.append({
                'project_name': i[0],
                'project_number': i[1],
                'id': i[2],
                'trade': i[3],
                'value': str(int(float(i[4].strip().replace(',','')))),
                'contractor_name': i[5],

            })

        return render_template('unapproved_work_order.html', work_orders=work_orders)


@app.route('/update_slab_area', methods=['POST'])
def update_slab_area():
    project_id = request.form['project_id']
    query = 'SELECT basement_slab_area, gf_slab_area, ff_slab_area, sf_slab_area, tf_slab_area, tef_slab_area from projects WHERE project_id=' + str(project_id)
    cur = mysql.connection.cursor()
    cur.execute(query)
    result = cur.fetchone()
    total_bua_sum = 0
    for i in result:
        if i is not None and str(i).strip() != '' and str(i).strip() != 'NIL':
            total_bua_sum = total_bua_sum + int(i)
    return str(total_bua_sum)


@app.route('/check_if_floors_updated', methods=['POST'])
def check_if_floors_updated():
    project_id = request.form['project_id']
    query = 'SELECT id, floors from work_orders WHERE project_id=' + str(project_id)
    cur = mysql.connection.cursor()
    cur.execute(query)
    result = cur.fetchone()
    if result is not None:
        return jsonify({'floors_updated': True, 'floors': result[1]})
    return jsonify({'floors_updated': False})

@app.route('/view_ph_approval_indents', methods=['GET'])
def view_ph_approval_indents():
    cur = mysql.connection.cursor()
    indents_query = 'SELECT indents.id, ' \
                    'projects.project_id, ' \
                    'projects.project_name, ' \
                    'indents.material, ' \
                    'indents.quantity, ' \
                    'indents.unit, ' \
                    'indents.purpose, ' \
                    'App_users.name, ' \
                    'indents.timestamp FROM indents ' \
                    'INNER JOIN projects on ' \
                    'indents.status="po_uploaded" AND ' \
                    'indents.project_id=projects.project_id ' \
                    'LEFT OUTER JOIN App_users on ' \
                    'indents.created_by_user=App_users.user_id'
    cur.execute(indents_query)
    data = []
    projects = {}
    result = cur.fetchall()
    for i in result:
        i = list(i)
        if i[2] not in projects.keys():
            projects[i[2]] = []
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
        
        projects[i[2]].append(i)
        data.append(i)
    return render_template('ph_approval_indents.html', result=data, projects=projects)

@app.route('/view_qs_approval_indents', methods=['GET'])
def view_qs_approval_indents():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_approved_indents'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'QS Head', 'QS Engineer', 'Purchase Executive', 'Purchase Head', 'QS Info']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        current_user_role = session['role']
        indents_query = ''
        if current_user_role in ['Super Admin', 'COO', 'QS Head', 'Purchase Head','QS Info']:
            indents_query = 'SELECT indents.id, ' \
                            'projects.project_id, ' \
                            'projects.project_name, ' \
                            'indents.material, ' \
                            'indents.quantity, ' \
                            'indents.unit, ' \
                            'indents.purpose, ' \
                            'App_users.name, ' \
                            'indents.timestamp FROM indents ' \
                            'INNER JOIN projects on ' \
                            'indents.status="approved" AND ' \
                            'indents.project_id=projects.project_id ' \
                            'LEFT OUTER JOIN App_users on ' \
                            'indents.created_by_user=App_users.user_id'

        elif current_user_role in ['QS Engineer','Purchase Executive']:
            indents_query = 'SELECT indents.id, ' \
                            'projects.project_id, ' \
                            'projects.project_name, ' \
                            'indents.material, ' \
                            'indents.quantity, ' \
                            'indents.unit, ' \
                            'indents.purpose, ' \
                            'App_users.name, ' \
                            'indents.timestamp FROM indents ' \
                            'INNER JOIN projects on ' \
                            'indents.status="approved" AND ' \
                            'indents.project_id=projects.project_id AND ' \
                            'indents.project_id IN ' + str(get_projects_for_current_user()) +' '\
                            'LEFT OUTER JOIN App_users on ' \
                            'indents.created_by_user=App_users.user_id'
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
        return render_template('qs_approval_indents.html', result=data)


@app.route('/view_ph_approved_indents', methods=['GET'])
def view_ph_approved_indents():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_approved_indents'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'QS Head', 'QS Engineer', 'Purchase Executive', 'Purchase Head','Billing']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        current_user_role = session['role']
        indents_query = ''
        if current_user_role in ['Super Admin', 'COO', 'QS Head', 'Purchase Head','Billing']:
            indents_query = 'SELECT indents.id, ' \
                            'projects.project_id, ' \
                            'projects.project_name, ' \
                            'indents.material, ' \
                            'indents.quantity, ' \
                            'indents.unit, ' \
                            'indents.purpose, ' \
                            'App_users.name, ' \
                            'indents.timestamp, indents.billed FROM indents ' \
                            'INNER JOIN projects on ' \
                            'indents.status="approved_by_ph" AND ' \
                            'indents.project_id=projects.project_id ' \
                            'LEFT OUTER JOIN App_users on ' \
                            'indents.created_by_user=App_users.user_id'
        elif current_user_role in ['Purchase Executive']:
            indents_query = 'SELECT indents.id, ' \
                            'projects.project_id, ' \
                            'projects.project_name, ' \
                            'indents.material, ' \
                            'indents.quantity, ' \
                            'indents.unit, ' \
                            'indents.purpose, ' \
                            'App_users.name, ' \
                            'indents.timestamp, indents.billed FROM indents ' \
                            'INNER JOIN projects on ' \
                            'indents.status="approved_by_ph" AND ' \
                            'indents.project_id=projects.project_id AND ' \
                            'indents.project_id IN ' + str(get_projects_for_current_user()) +' '\
                            'LEFT OUTER JOIN App_users on ' \
                            'indents.created_by_user=App_users.user_id'
        
        cur.execute(indents_query)
        data = []
        projects = {}
        result = cur.fetchall()
        for i in result:
            i = list(i)
            if i[2] not in projects.keys():
                projects[i[2]] = []
        
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
            projects[i[2]].append(i)
            data.append(i)
        return render_template('ph_approval_indents.html', result=data, projects=projects)

@app.route('/view_approved_indents', methods=['GET'])
def view_approved_indents():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_approved_indents'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'QS Head', 'QS Engineer', 'Purchase Executive', 'Purchase Head','QS Info']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        current_user_role = session['role']
        if current_user_role in ['Super Admin', 'COO', 'QS Head', 'QS Engineer', 'Purchase Head']:
            indents_query = 'SELECT indents.id, projects.project_id, projects.project_name, indents.material, indents.quantity, indents.unit, indents.purpose' \
                            ', App_users.name, indents.timestamp FROM indents INNER JOIN projects on indents.status="approved_by_qs"' \
                            ' AND indents.project_id=projects.project_id ' \
                            ' LEFT OUTER JOIN App_users on indents.created_by_user=App_users.user_id'

            cur.execute(indents_query)
            data = []
            result = cur.fetchall()
            projects = {}
            for i in result:
                i = list(i)
                if i[2] not in projects.keys():
                    projects[i[2]] = []
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
                projects[i[2]].append(i)
                data.append(i)
            return render_template('approved_indents.html', result=data, projects=projects)
        elif current_user_role == 'Purchase Executive':
            access_tuple = get_projects_for_current_user()
            indents_query = 'SELECT indents.id, projects.project_id, projects.project_name, indents.material, indents.quantity, indents.unit, indents.purpose' \
                            ', App_users.name, indents.timestamp FROM indents INNER JOIN projects on indents.status="approved_by_qs" AND indents.project_id=projects.project_id AND indents.project_id IN ' + str(
                access_tuple) + '' \
                                ' LEFT OUTER JOIN App_users on indents.created_by_user=App_users.user_id'
            cur.execute(indents_query)
            data = []
            projects = {}
            result = cur.fetchall()
            for i in result:
                i = list(i)
                if i[2] not in projects.keys():
                    projects[i[2]] = []
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
                projects[i[2]].append(i)
                data.append(i)
            return render_template('approved_indents.html', result=data, projects=projects)
        else:
            return 'You do not have access to view this page'


@app.route('/view_approved_POs', methods=['GET'])
def view_approved_POs():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_approved_POs'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'QS Head', 'QS Engineer', 'Purchase Executive', 'Purchase Head']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        current_user_role = session['role']
        if current_user_role in ['Super Admin', 'COO', 'QS Head', 'QS Engineer', 'Purchase Head']:
            indents_query = 'SELECT indents.id, projects.project_id, projects.project_name, indents.material, indents.quantity, indents.unit, indents.purpose' \
                            ', App_users.name, indents.timestamp FROM indents INNER JOIN projects on indents.status="po_uploaded" AND indents.project_id=projects.project_id ' \
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
            return render_template('approved_pos.html', result=data)
        elif current_user_role == 'Purchase Executive':
            access_tuple = get_projects_for_current_user()
            indents_query = 'SELECT indents.id, projects.project_id, projects.project_name, indents.material, indents.quantity, indents.unit, indents.purpose' \
                            ', App_users.name, indents.timestamp, indents.purchase_order FROM indents INNER JOIN projects on indents.status="po_uploaded" AND indents.project_id=projects.project_id AND indents.project_id IN ' + str(
                access_tuple) + '' \
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
            return render_template('approved_pos.html', result=data)
        else:
            return 'You do not have access to view this page'

@app.route('/approve_indent_by_qs', methods=['GET'])
def approve_indent_by_qs():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_indent_details'
        return redirect('/erp/login')
    if request.method == 'GET':
        indent_id = request.args['id']
        cur = mysql.connection.cursor()
        query = 'UPDATE indents set status=%s WHERE id=%s'
        cur.execute(query, ('approved_by_qs',indent_id))
        mysql.connection.commit()
        flash('Indent approved','success')
        return redirect('/erp/view_qs_approval_indents')    

@app.route('/mark_as_billed', methods=['GET'])
def mark_as_billed():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/mark_as_billed'
    if request.method == 'GET':
        indent_id = request.args['id']
        cur = mysql.connection.cursor()
        query = 'UPDATE indents set billed=1 WHERE id='+str(indent_id)
        cur.execute(query)
        mysql.connection.commit()
        flash('Indent marked as billed','success')
        return redirect('/erp/view_ph_approved_indents')

@app.route('/rollback_indent_by_ph', methods=['GET'])
def rollback_indent_by_ph():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/rollback_indent_by_ph'
    if request.method == 'GET':
        indent_id = request.args['id']
        cur = mysql.connection.cursor()
        query = 'UPDATE indents set status=%s WHERE id=%s'
        cur.execute(query, ('approved_by_qs',indent_id))
        mysql.connection.commit()
        flash('Indent rolled back','success')
        return redirect('/erp/view_qs_approval_indents')

@app.route('/approve_indent_by_ph', methods=['GET'])
def approve_indent_by_ph():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/approve_indent_by_ph'
        return redirect('/erp/login')
    if request.method == 'GET':
        indent_id = request.args['id']
        cur = mysql.connection.cursor()
        difference_cost = request.args['difference_cost']
        query = 'UPDATE indents set status="approved_by_ph" , difference_cost="'+str(difference_cost)+'" WHERE id='+str(indent_id)
        cur.execute(query)
        mysql.connection.commit()
        get_indent_query = 'SELECT indents.id, projects.project_id, projects.project_name, indents.material, indents.quantity, indents.unit, indents.purpose' \
                                   ', indents.timestamp, indents.created_by_user, indents.acted_by_user FROM indents INNER JOIN projects on indents.project_id=projects.project_id ' \
                                   ' AND indents.id=' + str(indent_id)
        cur.execute(get_indent_query)
        result = cur.fetchone()
        if result is not None:
            notification_body = 'PO uploaded for indent with id ' + str(indent_id) + '. Details: ' + str(
                result[4]) + ' ' + str(result[5]) + ' ' + str(result[3]) + ' For project ' + str(result[2])
            IST = pytz.timezone('Asia/Kolkata')
            datetime_ist = datetime.now(IST)
            timestamp = datetime_ist.strftime('%A %d %B %H:%M')
            send_app_notification('PO Uploaded', notification_body, str(result[8]), str(result[8]),
                                    'PO uploads', timestamp)
            send_app_notification('PO Uploaded', notification_body, str(result[9]), str(result[9]),
                                    'PO uploads', timestamp)
        flash('Indent approved','success')
        return redirect('/erp/view_approved_POs')

@app.route('/view_indent_details', methods=['GET'])
def view_indent_details():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_indent_details'
        return redirect('/erp/login')
    if request.method == 'GET':
        indent_id = request.args['indent_id']
        cur = mysql.connection.cursor()
        indents_query = 'SELECT indents.id, projects.project_id, projects.project_name, indents.material, indents.quantity, indents.unit, indents.purpose' \
                        ', App_users.name, indents.timestamp, indents.purchase_order, indents.status, indents.difference_cost, indents.approval_taken, indents.difference_cost_sheet, indents.comments FROM indents INNER JOIN projects on indents.id=' + str(
            indent_id) + ' AND indents.project_id=projects.project_id ' \
                         ' LEFT OUTER JOIN App_users on indents.created_by_user=App_users.user_id'
        cur.execute(indents_query)
        result = cur.fetchone()
        return render_template('view_indent_details.html', result=result)

@app.route('/edit_indent', methods=['GET','POST'])
def edit_indent():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_indent_details'
        return redirect('/erp/login')
    if request.method == 'GET':
        indent_id = request.args['indent_id']
        cur = mysql.connection.cursor()
        indents_query = 'SELECT indents.id, projects.project_id, projects.project_name, indents.material, indents.quantity, indents.unit, indents.purpose' \
                        ', App_users.name, indents.timestamp, indents.purchase_order, indents.status FROM indents INNER JOIN projects on indents.id=' + str(
            indent_id) + ' AND indents.project_id=projects.project_id ' \
                         ' LEFT OUTER JOIN App_users on indents.created_by_user=App_users.user_id'
        cur.execute(indents_query)
        result = cur.fetchone()
        return render_template('edit_indent.html', result=result)
    else: 
        indent_id = request.form['indent_id']
        material = request.form['material']
        quantity = request.form['quantity']
        unit = request.form['unit']
        purpose = request.form['purpose']
        cur = mysql.connection.cursor()
        query = 'UPDATE indents SET material=%s, quantity=%s, unit=%s, purpose=%s WHERE id=%s'
        values = (material, quantity, unit, purpose, indent_id)
        cur.execute(query, values)
        mysql.connection.commit()
        flash('Indent updated','success')
        return redirect('/erp/view_indent_details?indent_id='+str(indent_id))


@app.route('/delete_indent', methods=['GET'])
def delete_indent():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/view_indent_details'
        return redirect('/erp/login')
    if request.method == 'GET':
        indent_id = request.args['indent_id'] 
        cur = mysql.connection.cursor()
        query = 'DELETE from indents WHERE id='+str(indent_id)
        cur.execute(query)
        mysql.connection.commit()
        flash('Indent deleted','danger')
        return redirect('/erp/view_qs_approval_indents')

@app.route('/close_po_with_comments', methods=['POST'])
def close_po_with_comments():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/create_bill'
        return redirect('/erp/login')
    if request.method == 'POST':
        indent_id = request.form['indent_id']
        comments = request.form['comments'].replace('"', '').replace("'", '')

        cur = mysql.connection.cursor()
        query = 'UPDATE indents set status=%s, comments=%s WHERE id=%s'
        values = ('po_uploaded',comments, indent_id)
        cur.execute(query, values)
        mysql.connection.commit()
        flash('Indent closed with comment successfully', 'success')
        return redirect('/erp/view_approved_indents')



@app.route('/upload_po_for_indent', methods=['POST'])
def upload_po_for_indent():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/create_bill'
        return redirect('/erp/login')
    if request.method == 'POST':
        indent_id = request.form['indent_id']

        difference_cost = request.form['difference_cost']
        cur = mysql.connection.cursor()
        query = 'UPDATE indents set difference_cost=%s WHERE id=%s'
        values = (difference_cost, indent_id)
        cur.execute(query, values)
        mysql.connection.commit()

        if 'difference_cost_sheet' in request.files:
            file = request.files['difference_cost_sheet']
            if file.filename != '':                
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    IST = pytz.timezone('Asia/Kolkata')
                    current_time = time.time()
                    filename = str(current_time)+'_'+filename
                    output = send_to_s3(file, app.config["S3_BUCKET"], str(indent_id) + '_dc_' + filename)
                    if output != 'success':
                        flash('File upload failed', 'danger')
                        return redirect(request.referrer)
                    cur = mysql.connection.cursor()
                    query = 'UPDATE indents set difference_cost_sheet=%s WHERE id=%s'
                    values = (str(indent_id) + '_dc_' + filename, indent_id)
                    cur.execute(query, values)
                    mysql.connection.commit()
                    flash('Difference cost sheet Uploaded successfully', 'success')
                



        if 'purchase_order' in request.files:
            file = request.files['purchase_order']
            if file.filename != '':
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    IST = pytz.timezone('Asia/Kolkata')
                    current_time = time.time()
                    filename = str(current_time)+'_'+filename
                    output = send_to_s3(file, app.config["S3_BUCKET"], str(indent_id) + '_' + filename)
                    if output != 'success':
                        flash('File upload failed', 'danger')
                        return redirect(request.referrer)
                    cur = mysql.connection.cursor()
                    query = 'UPDATE indents set status=%s, purchase_order=%s WHERE id=%s'
                    values = ('po_uploaded', str(indent_id) + '_' + filename, indent_id)
                    cur.execute(query, values)
                    mysql.connection.commit()

                    get_indent_query = 'SELECT indents.id, projects.project_id, projects.project_name, indents.material, indents.quantity, indents.unit, indents.purpose' \
                                    ', indents.timestamp, indents.created_by_user, indents.acted_by_user FROM indents INNER JOIN projects on indents.project_id=projects.project_id ' \
                                    ' AND indents.id=' + str(indent_id)
                    cur.execute(get_indent_query)
                    result = cur.fetchone()
                    if result is not None:
                        notification_body = 'PO uploaded for indent with id ' + str(indent_id) + '. Details: ' + str(
                            result[4]) + ' ' + str(result[5]) + ' ' + str(result[3]) + ' For project ' + str(result[2])
                        IST = pytz.timezone('Asia/Kolkata')
                        datetime_ist = datetime.now(IST)
                        timestamp = datetime_ist.strftime('%A %d %B %H:%M')
                        send_app_notification('PO Uploaded', notification_body, str(result[8]), str(result[8]),
                                            'PO uploads', timestamp)
                        send_app_notification('PO Uploaded', notification_body, str(result[9]), str(result[9]),
                                            'PO uploads', timestamp)
                    flash('PO Uploaded successfully', 'success')
        return redirect('/erp/view_indent_details?indent_id=' + str(indent_id))


@app.route('/sign_wo', methods=['GET', 'POST'])
def sign_wo():
    if request.method == 'GET':
        if 'wo_id' in request.args:
            work_order_query = 'SELECT p.project_name, p.project_number, wo.trade, wo.value, c.name,' \
                               'c.pan, c.code, c.address, wo.wo_number, wo.cheque_no, wo.comments, wo.created_at , wo.total_bua, wo.cost_per_sqft, wo.verification_code' \
                               ' FROM work_orders wo ' \
                               'INNER JOIN projects p on p.project_id=wo.project_id AND wo.signed=0 AND wo.id=' + str(
                request.args['wo_id']) + ' INNER JOIN contractors c on c.id=wo.contractor_id'
            cur = mysql.connection.cursor()
            cur.execute(work_order_query)
            result = cur.fetchone()
        return render_template('sign_wo.html', wo=result, wo_id=str(request.args['wo_id']))


@app.route('/upload_signed_wo', methods=['POST'])
def upload_signed_wo():
    # project_name+trade+contractor_name
    wo_id = request.form['wo_id']
    cur = mysql.connection.cursor()
    project_name = request.form['project_name']
    trade = request.form['trade']
    contractor_name = request.form['contractor_name']
    
    project_name = project_name.capitalize().replace(' ', '_').replace('"', '').replace("'", '')
    trade = trade.capitalize().replace(' ', '_').replace('"', '').replace("'", '')
    contractor_name = contractor_name.capitalize().replace(' ', '_').replace('"', '').replace("'", '')

    filename = project_name+'_'+trade+'_'+contractor_name+'_'+ str(wo_id) + '.pdf'

    query = 'UPDATE work_orders SET signed=1, filename="'+filename+'" WHERE id=' + wo_id
    cur.execute(query)
    mysql.connection.commit()


    
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            flash('Work order signed!', 'success')
            output = send_to_s3(file, app.config["S3_BUCKET"], filename, 'public-read','application/pdf')
            if output != 'success':
                flash('File upload failed', 'danger')
                return redirect(request.referrer)
            return 'success'


@app.route('/approve_wo', methods=['GET', 'POST'])
def approve_wo():
    if request.method == 'GET':
        if 'wo_id' in request.args:
            work_order_query = 'SELECT p.project_name, p.project_number, wo.trade, wo.value, c.name,' \
                               'c.pan, c.code, c.address, wo.wo_number, wo.cheque_no, wo.comments, wo.created_at, wo.filename' \
                               ' FROM work_orders wo ' \
                               'INNER JOIN projects p on p.project_id=wo.project_id AND wo.signed=1 AND wo.approved=0 AND wo.id=' + str(
                request.args['wo_id']) + ' ' \
                                         'INNER JOIN contractors c on c.id=wo.contractor_id'
            cur = mysql.connection.cursor()
            cur.execute(work_order_query)
            result = cur.fetchone()
        return render_template('approve_wo.html', wo=result, wo_id=str(request.args['wo_id']))
    else:
        wo_id = request.form['wo_id']
        cur = mysql.connection.cursor()
        query = 'UPDATE work_orders SET approved=1 WHERE id=' + wo_id
        cur.execute(query)
        mysql.connection.commit()
        flash('Work order approved!', 'success')
        return redirect('/erp/view_unapproved_work_order')


@app.route('/archive_project', methods=['GET'])
def archive_project():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/archive_project'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'Sales Executive', 'Billing']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if 'project_id' in request.args:
        cur = mysql.connection.cursor()
        query = 'UPDATE projects set archived=1 WHERE project_id=' + str(request.args['project_id'])
        cur.execute(query)
        mysql.connection.commit()
        flash('Project archived', 'warning')
        return redirect(request.referrer)
    else:
        flash('Missing fields', 'danger')
        return redirect(request.referrer)


@app.route('/unarchive_project', methods=['GET'])
def unarchive_project():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/unarchive_project'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'Sales Executive', 'Billing']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if 'project_id' in request.args:
        cur = mysql.connection.cursor()
        query = 'UPDATE projects set archived=0 WHERE project_id=' + str(request.args['project_id'])
        cur.execute(query)
        mysql.connection.commit()
        flash('Project unarchived', 'success')
        return redirect(request.referrer)
    else:
        flash('Missing fields', 'danger')
        return redirect(request.referrer)


@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/create_project'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'Sales Executive', 'Billing','Planning']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        sales_executives_query = 'SELECT user_id, name from App_users WHERE role="Sales Executive"'
        cur.execute(sales_executives_query)
        result = cur.fetchall()
        return render_template('create_project.html', sales_executives=result)
    else:
        cur = mysql.connection.cursor()

        client_name = request.form['client_name']
        client_phone = request.form['client_phone']

        create_user_query = 'INSERT into App_users (name, phone, role) values (%s, %s, "Client")'
        cur.execute(create_user_query, (client_name, client_phone))    

        column_names = list(request.form.keys())
        values = list(request.form.values())

        column_names.append('created_at')
        IST = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(IST)
        timestamp = current_time.strftime('%d %m %Y at %H %M')
        values.append(timestamp)

        new_project_query = 'INSERT into projects' + str(tuple(column_names)).replace("'", "") + 'values ' + str(
            tuple(values))
        cur.execute(new_project_query)
        project_id = cur.lastrowid
        cost_sheet_filename = ''
        site_inspection_report_filename = ''
        if 'cost_sheet' in request.files:
            file = request.files['cost_sheet']
            if file.filename == '':
                flash('No selected file', 'danger ')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                cost_sheet_filename = 'cost_sheet_' + str(project_id) + '_' + filename
                output = send_to_s3(file, app.config["S3_BUCKET"], cost_sheet_filename)
                if output != 'success':
                    flash('File upload failed', 'danger')
                    return redirect(request.referrer)

        if 'site_inspection_report' in request.files:
            file = request.files['site_inspection_report']
            if file.filename == '':
                flash('No selected file', 'danger ')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                site_inspection_report_filename = 'site_inspection_report_' + str(project_id) + '_' + filename
                output = send_to_s3(file, app.config["S3_BUCKET"], site_inspection_report_filename)
                if output != 'success':
                    flash('File upload failed', 'danger')
                    return redirect(request.referrer)

        update_filename_query = 'UPDATE projects set cost_sheet=%s, site_inspection_report=%s WHERE project_id=%s'
        cur.execute(update_filename_query, (cost_sheet_filename, site_inspection_report_filename, str(project_id)))
        flash('Project created successfully', 'success')
        mysql.connection.commit()
        return redirect(request.referrer)


@app.route('/edit_project', methods=['GET', 'POST'])
def edit_project():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/edit_project'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'COO', 'Sales Executive', 'Billing','Planning']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        fields_as_string = ", ".join(project_fields)
        get_details_query = 'SELECT ' + fields_as_string + ' from projects WHERE project_id=' + str(
            request.args['project_id'])
        cur = mysql.connection.cursor()
        cur.execute(get_details_query)
        result = cur.fetchone()
        project = projects(*result)
        sales_executives_query = 'SELECT user_id, name from App_users WHERE role="Sales Executive"'
        cur.execute(sales_executives_query)
        result = cur.fetchall()
        return render_template('edit_project.html', p=project, sales_executives=result)
    else:

        column_names = list(request.form.keys())

        update_string = ""
        for i in column_names[:-1]:
            if request.form[i].strip() != '':
                update_string += i + '="' + request.form[i].replace('"','""').replace("'","''") + '", '
        # Remove the last comma
        update_string = update_string[:-2]
        update_project_query = 'UPDATE projects SET ' + update_string + ' WHERE project_id=' + str(
            request.form['project_id'])
        cur = mysql.connection.cursor()
        cur.execute(update_project_query)
        mysql.connection.commit()
        cost_sheet_filename = ''
        site_inspection_report_filename = ''
        if 'cost_sheet' in request.files:
            file = request.files['cost_sheet']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                cost_sheet_filename = 'cost_sheet_' + str(request.form['project_id']) + '_' + filename
                output = send_to_s3(file, app.config["S3_BUCKET"], cost_sheet_filename)
                if output == 'success':
                    update_filename_query = 'UPDATE projects set cost_sheet=%s WHERE project_id=%s'
                    cur.execute(update_filename_query,
                                (cost_sheet_filename, str(request.form['project_id'])))

        if 'site_inspection_report' in request.files:
            file = request.files['site_inspection_report']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                site_inspection_report_filename = 'site_inspection_report_' + str(
                    request.form['project_id']) + '_' + filename
                output = send_to_s3(file, app.config["S3_BUCKET"], site_inspection_report_filename)
                if output == 'success':
                    update_filename_query = 'UPDATE projects set site_inspection_report=%s WHERE project_id=%s'
                    cur.execute(update_filename_query,
                                (site_inspection_report_filename, str(request.form['project_id'])))

        mysql.connection.commit()
        flash('Project updated successfully', 'success')
        return redirect('/erp/view_project_details?project_id=' + str(request.form['project_id']))

        # This has to be checked. The if condition is returning false even when everything is okay
        # if cur.rowcount == 1:
        #     flash('Project updated successfully', 'success')
        #     return redirect('/erp/view_project_details?project_id=' + str(request.form['project_id']))
        # else:
        #     flash('Project not updated', 'danger')
        #     return redirect(request.referrer)


@app.route('/unapproved_projects', methods=['GET'])
def unapproved_projects():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/unapproved_projects'
        return redirect('/erp/login')
    if session['role'] not in ['Super Admin', 'Billing']:
        flash('You do not have permission to view that page', 'danger')
        return redirect(request.referrer)
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        unapproved_projects_query = 'SELECT project_id, project_name, project_number from projects WHERE is_approved=0 AND archived=0 ORDER BY project_number'
        cur.execute(unapproved_projects_query)
        result = cur.fetchall()
        return render_template('unapproved_projects.html', projects=result)


@app.route('/projects', methods=['GET'])
def approved_projects():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/projects'
        return redirect('/erp/login')
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        result = []
        if len(get_projects_for_current_user()) > 0:
            if session['role'] not in ['Super Admin', 'COO', 'QS Head','Site Engineer', 'Purchase Head','Planning',
                                       'Sales Executive', 'Billing']:
                approved_projects_query = 'SELECT project_id, project_name, project_number from projects WHERE is_approved=1 AND archived=0 ' \
                                          'AND project_id IN ' + str(get_projects_for_current_user()) + ' ORDER BY project_number'
                cur.execute(approved_projects_query)
                result = cur.fetchall()
            else:
                approved_projects_query = 'SELECT project_id, project_name, project_number from projects WHERE is_approved=1 AND archived=0 ORDER BY project_number'
                cur.execute(approved_projects_query)
                result = cur.fetchall()
        return render_template('approved_projects.html', projects=result)


@app.route('/archived_projects', methods=['GET'])
def archived_projects():
    if 'email' not in session:
        flash('You need to login to continue', 'danger')
        session['last_route'] = '/erp/projects'
        return redirect('/erp/login')
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        result = []
        if len(get_projects_for_current_user()) > 0:
            if session['role'] not in ['Super Admin', 'COO', 'QS Head', 'Site Engineer', 'Purchase Head', 'Billing']:
                archived_projects_query = 'SELECT project_id, project_name, project_number from projects WHERE is_approved=1 AND archived=1 ' \
                                          'AND project_id IN ' + str(get_projects_for_current_user()) + ' ORDER BY project_number'
                cur.execute(archived_projects_query)
                result = cur.fetchall()
            else:
                archived_projects_query = 'SELECT project_id, project_name, project_number from projects WHERE is_approved=1 AND archived=1 ORDER BY project_number'
                cur.execute(archived_projects_query)
                result = cur.fetchall()
        return render_template('archived_projects.html', projects=result)


@app.route('/view_project_details', methods=['GET'])
def view_project_details():
    if request.method == 'GET':
        fields = [
            'project_name', 'project_number', 'project_location', 'package_type', 'no_of_floors', 'project_value',
            'date_of_initial_advance', 'date_of_agreement', 'sales_executive', 'site_area',
            'gf_slab_area', 'ff_slab_area', 'sf_slab_area', 'tf_slab_area', 'tef_slab_area', 'shr_oht',
            'elevation_details', 'additional_cost',
            'paid_percentage', 'comments', 'cost_sheet', 'site_inspection_report', 'is_approved', 'archived', 'created_at','client_name', 'client_phone'
        ]
        fields_as_string = ", ".join(fields)
        get_details_query = 'SELECT ' + fields_as_string + ' from projects WHERE project_id=' + str(
            request.args['project_id'])
        cur = mysql.connection.cursor()
        cur.execute(get_details_query)
        result = cur.fetchone()
        details = {}

        if len(str(result[8])) > 0:
            sales_executive_query = 'SELECT name from App_users WHERE user_id=' + str(result[8])
            cur.execute(sales_executive_query)
            sales_executive_query_result = cur.fetchone()
        for i in range(len(fields)):
            fields_name_to_show = " ".join(fields[i].split('_')).title()
            if fields_name_to_show == 'Sales Executive' and len(
                    str(result[8])) > 0 and sales_executive_query_result is not None:
                details[fields_name_to_show] = sales_executive_query_result[0]
            else:
                details[fields_name_to_show] = result[i]
        return render_template('view_project_details.html', details=details, approved=str(result[-5]),
                               archived=str(result[-4]))


@app.route('/approve_project', methods=['GET'])
def approve_project():
    project_id = request.args['project_id']
    approve_project_query = 'UPDATE projects set is_approved="1" WHERE project_id=' + str(project_id)
    cur = mysql.connection.cursor()
    cur.execute(approve_project_query)
    mysql.connection.commit()
    flash('Project has been approved', 'success')
    return redirect('/erp/view_project_details?project_id=' + str(project_id))


@app.route('/projects_with_no_design_team', methods=['GET'])
def projects_with_no_design_team():
    no_design_team_query = 'SELECT P.project_id, P.project_name from projects P left join project_design_team PDT ' \
                           'on P.project_id = PDT.project_id WHERE P.is_approved=1 AND P.archived=0 AND PDT.project_id is NULL'
    cur = mysql.connection.cursor()
    cur.execute(no_design_team_query)
    result = cur.fetchall()
    return render_template('projects_with_no_design_team.html', projects=result)


@app.route('/projects_with_design_team', methods=['GET'])
def projects_with_design_team():
    design_team_query = 'SELECT P.project_id, P.project_name from projects P left join project_design_team PDT ' \
                        'on P.project_id = PDT.project_id WHERE P.is_approved=1 AND P.archived=0 AND PDT.project_id is NOT NULL'
    cur = mysql.connection.cursor()
    cur.execute(design_team_query)
    result = cur.fetchall()
    return render_template('projects_with_design_team.html', projects=result)


@app.route('/projects_with_no_operations_team', methods=['GET'])
def projects_with_no_operations_team():
    no_ops_team_query = 'SELECT P.project_id, P.project_name from projects P left join project_operations_team POT ' \
                        'on P.project_id = POT.project_id WHERE P.is_approved=1 AND P.archived=0 AND POT.project_id is NULL'
    cur = mysql.connection.cursor()
    cur.execute(no_ops_team_query)
    result = cur.fetchall()
    return render_template('projects_with_no_operations_team.html', projects=result)


@app.route('/projects_with_operations_team', methods=['GET'])
def projects_with_operations_team():
    ops_team_query = 'SELECT P.project_id, P.project_name from projects P left join project_operations_team POT ' \
                     'on P.project_id = POT.project_id WHERE P.is_approved=1 AND P.archived=0 AND POT.project_id is NOT NULL'
    cur = mysql.connection.cursor()
    cur.execute(ops_team_query)
    result = cur.fetchall()
    return render_template('projects_with_operations_team.html', projects=result)


@app.route('/assign_team', methods=['GET', 'POST'])
def assign_team():
    if request.method == 'GET':
        design_team_query = 'SELECT user_id, name, role from App_users WHERE role="Architect" OR role="Senior Architect" OR role="Structural Designer" OR role="Electrical Designer" OR role="PHE Designer"'
        cur = mysql.connection.cursor()
        cur.execute(design_team_query)
        architects = []
        structural_designers = []
        electrical_designers = []
        phe_designers = []
        senior_architects = []
        result = cur.fetchall()
        for i in result:
            if i[2] == 'Architect':
                architects.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Structural Designer':
                structural_designers.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Electrical Designer':
                electrical_designers.append({'id': i[0], 'name': i[1]})
            if i[2] == 'PHE Designer':
                phe_designers.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Senior Architect':
                senior_architects.append({'id': i[0], 'name': i[1]})

        operations_team_query = 'SELECT user_id, name, role from App_users WHERE role="Project Coordinator" OR role="Project Manager" OR role="Purchase Executive" OR role="QS Engineer"'
        cur = mysql.connection.cursor()
        cur.execute(operations_team_query)
        co_ordinators = []
        project_managers = []
        purchase_executives = []
        qs_engineers = []
        result = cur.fetchall()
        for i in result:
            if i[2] == 'Project Coordinator':
                co_ordinators.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Project Manager':
                project_managers.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Purchase Executive':
                purchase_executives.append({'id': i[0], 'name': i[1]})
            if i[2] == 'QS Engineer':
                qs_engineers.append({'id': i[0], 'name': i[1]})

        return render_template('assign_team.html', co_ordinators=co_ordinators,
                                       project_managers=project_managers, purchase_executives=purchase_executives,
                                       qs_engineers=qs_engineers,  senior_architects=senior_architects, architects=architects,
                                       structural_designers=structural_designers, electrical_designers=electrical_designers,
                                       phe_designers=phe_designers)
    else:

        column_names = list(request.form.keys())
        values = list(request.form.values())

        design_team_columns = column_names[:5] + [column_names[-1]]
        design_team_values = values[:5] + [values[-1]]

        cur = mysql.connection.cursor()
        assign_design_team_query = 'INSERT into project_design_team' + str(tuple(design_team_columns)).replace("'","") + 'values ' + str(tuple(design_team_values))
        cur.execute(assign_design_team_query)

        operations_team_columns = column_names[5:]
        operations_team_values = values[5:]

        assign_operations_team_query = 'INSERT into project_operations_team' + str(tuple(operations_team_columns)).replace("'","") + 'values ' + str(tuple(operations_team_values))
        cur.execute(assign_operations_team_query)        

        mysql.connection.commit()
        flash('Team updated successfully', 'success')
        return redirect('/erp/assign_team?project_id='+column_names[-1])

@app.route('/edit_team', methods=['GET', 'POST'])
def edit_team():
    if request.method == 'GET':
        if 'project_id' not in request.args:
            flash('Missing fields', 'danger')
            return redirect('/erp/projects_with_no_design_team')
        project_id = request.args['project_id']
        design_team_query = 'SELECT user_id, name, role from App_users WHERE role="Architect" OR role="Senior Architect" OR role="Structural Designer" OR role="Electrical Designer" OR role="PHE Designer"'
        cur = mysql.connection.cursor()
        cur.execute(design_team_query)
        architects = []
        structural_designers = []
        electrical_designers = []
        phe_designers = []
        senior_architects = []
        result = cur.fetchall()
        for i in result:
            if i[2] == 'Architect':
                architects.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Structural Designer':
                structural_designers.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Electrical Designer':
                electrical_designers.append({'id': i[0], 'name': i[1]})
            if i[2] == 'PHE Designer':
                phe_designers.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Senior Architect':
                senior_architects.append({'id': i[0], 'name': i[1]})

        existing_team = {
            'Architect': 'None',
            'Structural Designer': 'None',
            'Electrical Designer': 'None',
            'PHE Designer': 'None',
            'Senior Architect': 'None',
            'Project Coordinator': 'None',
            'Project Manager': 'None',
            'Purchase Executive': 'None',
            'QS Engineer': 'None'
        }


        existing_team_query = 'SELECT * FROM project_design_team WHERE project_id=' + str(project_id)
        cur.execute(existing_team_query)
        res = cur.fetchone()
        if res is not None:
            existing_team['Architect'] = res[2]
            existing_team['Structural Designer'] = res[3]
            existing_team['Electrical Designer'] = res[4]
            existing_team['PHE Designer'] = res[5]
            existing_team['Senior Architect'] = res[6]


        operations_team_query = 'SELECT user_id, name, role from App_users WHERE role="Project Coordinator" OR role="Project Manager" OR role="Purchase Executive" OR role="QS Engineer"'
        cur = mysql.connection.cursor()
        cur.execute(operations_team_query)
        co_ordinators = []
        project_managers = []
        purchase_executives = []
        qs_engineers = []
        result = cur.fetchall()
        for i in result:
            if i[2] == 'Project Coordinator':
                co_ordinators.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Project Manager':
                project_managers.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Purchase Executive':
                purchase_executives.append({'id': i[0], 'name': i[1]})
            if i[2] == 'QS Engineer':
                qs_engineers.append({'id': i[0], 'name': i[1]})
        existing_team_query = 'SELECT * FROM project_operations_team WHERE project_id=' + str(project_id)
        cur.execute(existing_team_query)
        res = cur.fetchone()
        if res is not None:
            existing_team['Project Coordinator'] = res[2]
            existing_team['Project Manager'] = res[3]
            existing_team['Purchase Executive'] = res[4]
            existing_team['QS Engineer'] = res[5]


        return render_template('edit_team.html', existing_team=existing_team,
                               senior_architects=senior_architects, architects=architects,
                               structural_designers=structural_designers, electrical_designers=electrical_designers,
                               phe_designers=phe_designers, co_ordinators=co_ordinators,
                               project_managers=project_managers, purchase_executives=purchase_executives,
                               qs_engineers=qs_engineers)

    else:
        cur = mysql.connection.cursor()
        column_names = list(request.form.keys())
        values = list(request.form.values())


        check_if_design_team_exists_query = 'SELECT id from project_design_team WHERE project_id='+str(request.form['project_id'])
        cur.execute(check_if_design_team_exists_query)
        result = cur.fetchone()
        if result is not None:

            update_string = ""
            for i in column_names[:5]:
                update_string += i + '="' + request.form[i] + '", '
            # Remove the last comma
            update_string = update_string[:-2]
            update_project_query = 'UPDATE project_design_team SET ' + update_string + ' WHERE project_id=' + str(
                request.form['project_id'])
            cur.execute(update_project_query)
        
        else :

            design_team_columns = column_names[:5] + [column_names[-1]]
            design_team_values = values[:5] + [values[-1]]

            cur = mysql.connection.cursor()
            assign_design_team_query = 'INSERT into project_design_team' + str(tuple(design_team_columns)).replace("'","") + 'values ' + str(tuple(design_team_values))
            cur.execute(assign_design_team_query)



        check_if_operations_team_exists_query = 'SELECT id from project_operations_team WHERE project_id='+str(request.form['project_id'])
        cur.execute(check_if_operations_team_exists_query)
        result = cur.fetchone()
        if result is not None:

            update_string = ""
            for i in column_names[5:-1]:
                update_string += i + '="' + request.form[i] + '", '
            # Remove the last comma
            update_string = update_string[:-2]
            update_project_query = 'UPDATE project_operations_team SET ' + update_string + ' WHERE project_id=' + str(
                request.form['project_id'])
            cur.execute(update_project_query)
        else : 

            operations_team_columns = column_names[5:]
            operations_team_values = values[5:]

            assign_operations_team_query = 'INSERT into project_operations_team' + str(tuple(operations_team_columns)).replace("'","") + 'values ' + str(tuple(operations_team_values))
            cur.execute(assign_operations_team_query)

        project_id = request.form['project_id']
        
        for i in values[:-1]:
            if str(i).strip() != '':
                access_to_projects = ''
                access_query = 'SELECT access from App_users WHERE user_id='+str(i)
                cur.execute(access_query)
                res = cur.fetchone()
                if res is not None and res[0] is not None:
                    access_to_projects = res[0]
                if str(project_id) not in access_to_projects:
                    access_to_projects = access_to_projects + ',' + str(project_id)
                access_update_query = 'UPDATE App_users SET access="'+access_to_projects+'" WHERE user_id='+str(i)     
                cur.execute(access_update_query)

                
        mysql.connection.commit()
        flash('Team updated successfully', 'success')
        return redirect('/erp/projects')

@app.route('/assign_design_team', methods=['GET', 'POST'])
def assign_design_team():
    if request.method == 'GET':
        design_team_query = 'SELECT user_id, name, role from App_users WHERE role="Architect" OR role="Senior Architect" OR role="Structural Designer" OR role="Electrical Designer" OR role="PHE Designer"'
        cur = mysql.connection.cursor()
        cur.execute(design_team_query)
        architects = []
        structural_designers = []
        electrical_designers = []
        phe_designers = []
        senior_architects = []
        result = cur.fetchall()
        for i in result:
            if i[2] == 'Architect':
                architects.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Structural Designer':
                structural_designers.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Electrical Designer':
                electrical_designers.append({'id': i[0], 'name': i[1]})
            if i[2] == 'PHE Designer':
                phe_designers.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Senior Architect':
                senior_architects.append({'id': i[0], 'name': i[1]})
        return render_template('assign_design_team.html', senior_architects=senior_architects, architects=architects,
                               structural_designers=structural_designers, electrical_designers=electrical_designers,
                               phe_designers=phe_designers)
    else:
        column_names = list(request.form.keys())
        values = list(request.form.values())

        cur = mysql.connection.cursor()
        assign_design_team_query = 'INSERT into project_design_team' + str(tuple(column_names)).replace("'",
                                                                                                        "") + 'values ' + str(
            tuple(values))
        cur.execute(assign_design_team_query)
        mysql.connection.commit()
        flash('Design team has been assigned successfully', 'success')
        return redirect('/erp/projects_with_design_team')


@app.route('/edit_design_team', methods=['GET', 'POST'])
def edit_design_team():
    if request.method == 'GET':
        if 'project_id' not in request.args:
            flash('Missing fields', 'danger')
            return redirect('/erp/projects_with_no_design_team')
        project_id = request.args['project_id']
        design_team_query = 'SELECT user_id, name, role from App_users WHERE role="Architect" OR role="Senior Architect" OR role="Structural Designer" OR role="Electrical Designer" OR role="PHE Designer"'
        cur = mysql.connection.cursor()
        cur.execute(design_team_query)
        architects = []
        structural_designers = []
        electrical_designers = []
        phe_designers = []
        senior_architects = []
        result = cur.fetchall()
        for i in result:
            if i[2] == 'Architect':
                architects.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Structural Designer':
                structural_designers.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Electrical Designer':
                electrical_designers.append({'id': i[0], 'name': i[1]})
            if i[2] == 'PHE Designer':
                phe_designers.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Senior Architect':
                senior_architects.append({'id': i[0], 'name': i[1]})
        existing_team_query = 'SELECT * FROM project_design_team WHERE project_id=' + str(project_id)
        cur.execute(existing_team_query)
        res = cur.fetchone()
        existing_team = {
            'Architect': res[2],
            'Structural Designer': res[3],
            'Electrical Designer': res[4],
            'PHE Designer': res[5],
            'Senior Architect': res[6]
        }

        return render_template('edit_design_team.html', existing_team=existing_team,
                               senior_architects=senior_architects, architects=architects,
                               structural_designers=structural_designers, electrical_designers=electrical_designers,
                               phe_designers=phe_designers)
    else:

        cur = mysql.connection.cursor()
        column_names = list(request.form.keys())

        update_string = ""
        for i in column_names[:-1]:
            if request.form[i].strip() != '':
                update_string += i + '="' + request.form[i] + '", '
        # Remove the last comma
        update_string = update_string[:-2]
        update_project_query = 'UPDATE project_design_team SET ' + update_string + ' WHERE project_id=' + str(
            request.form['project_id'])

        cur.execute(update_project_query)
        mysql.connection.commit()
        flash('Design team has been updated successfully', 'success')
        return redirect('/erp/projects_with_design_team')


@app.route('/assign_operations_team', methods=['GET', 'POST'])
def assign_operations_team():
    if request.method == 'GET':

        operations_team_query = 'SELECT user_id, name, role from App_users WHERE role="Project Coordinator" OR role="Project Manager" OR role="Purchase Executive" OR role="QS Engineer"'
        cur = mysql.connection.cursor()
        cur.execute(operations_team_query)
        co_ordinators = []
        project_managers = []
        purchase_executives = []
        qs_engineers = []
        result = cur.fetchall()
        for i in result:
            if i[2] == 'Project Coordinator':
                co_ordinators.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Project Manager':
                project_managers.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Purchase Executive':
                purchase_executives.append({'id': i[0], 'name': i[1]})
            if i[2] == 'QS Engineer':
                qs_engineers.append({'id': i[0], 'name': i[1]})

        return render_template('assign_operations_team.html', co_ordinators=co_ordinators,
                               project_managers=project_managers, purchase_executives=purchase_executives,
                               qs_engineers=qs_engineers)
    else:
        column_names = list(request.form.keys())
        values = list(request.form.values())

        cur = mysql.connection.cursor()
        assign_operations_team_query = 'INSERT into project_operations_team' + str(tuple(column_names)).replace("'",
                                                                                                                "") + 'values ' + str(
            tuple(values))
        cur.execute(assign_operations_team_query)
        mysql.connection.commit()
        flash('Operations team has been assigned successfully', 'success')
        return redirect('/erp/projects_with_operations_team')


@app.route('/edit_operations_team', methods=['GET', 'POST'])
def edit_operations_team():
    if request.method == 'GET':
        if 'project_id' not in request.args:
            flash('Missing fields', 'danger')
            return redirect('/erp/projects_with_no_operations_team')
        project_id = request.args['project_id']
        operations_team_query = 'SELECT user_id, name, role from App_users WHERE role="Project Coordinator" OR role="Project Manager" OR role="Purchase Executive" OR role="QS Engineer"'
        cur = mysql.connection.cursor()
        cur.execute(operations_team_query)
        co_ordinators = []
        project_managers = []
        purchase_executives = []
        qs_engineers = []
        result = cur.fetchall()
        for i in result:
            if i[2] == 'Project Coordinator':
                co_ordinators.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Project Manager':
                project_managers.append({'id': i[0], 'name': i[1]})
            if i[2] == 'Purchase Executive':
                purchase_executives.append({'id': i[0], 'name': i[1]})
            if i[2] == 'QS Engineer':
                qs_engineers.append({'id': i[0], 'name': i[1]})
        existing_team_query = 'SELECT * FROM project_operations_team WHERE project_id=' + str(project_id)
        cur.execute(existing_team_query)
        res = cur.fetchone()
        existing_team = {
            'Project Coordinator': res[2],
            'Project Manager': res[3],
            'Purchase Executive': res[4],
            'QS Engineer': res[5],
        }
        return render_template('edit_operations_team.html', existing_team=existing_team, co_ordinators=co_ordinators,
                               project_managers=project_managers, purchase_executives=purchase_executives,
                               qs_engineers=qs_engineers)
    else:
        cur = mysql.connection.cursor()
        column_names = list(request.form.keys())

        update_string = ""
        for i in column_names[:-1]:
            if request.form[i].strip() != '':
                update_string += i + '="' + request.form[i] + '", '
        # Remove the last comma
        update_string = update_string[:-2]
        update_project_query = 'UPDATE project_operations_team SET ' + update_string + ' WHERE project_id=' + str(
            request.form['project_id'])

        cur.execute(update_project_query)
        mysql.connection.commit()
        flash('Opeartions team has been updated successfully', 'success')
        return redirect('/erp/projects_with_operations_team')


@app.route('/revised_drawings', methods=['GET', "POST"])
def revised_drawings():
    if request.method == 'GET':
        projects = get_projects()
        drawings = []
        if 'project_id' in request.args:
            cur = mysql.connection.cursor()
            reviewed_drawings_query = 'SELECT id, type, name, file, revision from revised_drawings WHERE project_id=' + str(
                request.args['project_id'])
            cur.execute(reviewed_drawings_query)
            drawings = cur.fetchall()

        return render_template('revised_drawings.html', drawings=drawings, projects=projects)

@app.route('/view_drawings_requests', methods=['GET', "POST"])
def view_drawings_requests():
    if request.method == 'GET':
        projects = get_projects()
        cur = mysql.connection.cursor()

        
        if session['role'] not in ['Super Admin','COO']:
            get_requests = 'SELECT p.project_name, p.project_number, r.category, r.drawing, u.name, r.timestamp, r.purpose, r.id, r.project_id FROM ' \
                            'drawing_requests r LEFT OUTER JOIN projects p on p.project_id=r.project_id ' \
                            ' LEFT OUTER JOIN App_users u on u.user_id=r.created_by_user' \
                            ' WHERE r.status!="closed" AND p.project_id IN ' + str(get_projects_for_current_user())
            cur.execute(get_requests) 
                       
        else: 
            get_requests = 'SELECT p.project_name, p.project_number, r.category, r.drawing, u.name, r.timestamp, r.purpose, r.id, r.project_id FROM ' \
                            'drawing_requests r LEFT OUTER JOIN projects p on p.project_id=r.project_id ' \
                            ' LEFT OUTER JOIN App_users u on u.user_id=r.created_by_user WHERE r.status!="closed"' 
            cur.execute(get_requests) 
        res = cur.fetchall()
            
        return render_template('drawing_requests.html', requests=res)


@app.route('/delete_drawing_request', methods=['GET','POST'])
def delete_drawing_request():
    request_id = request.args['id']
    cur = mysql.connection.cursor()
    query = 'DELETE from drawing_requests WHERE id='+str(request_id)
    cur.execute(query)
    mysql.connection.commit()
    flash("Drawing request has been deleted",'danger')
    return redirect('/erp/view_drawings_requests')

@app.route('/upload_revised_drawing', methods=['GET', "POST"])
def upload_revised_drawing():
    if request.method == 'GET':
        projects = get_projects()
        drawing_types = ['Architect', 'Structural', 'Electrical', 'Plumbing']

        return render_template('upload_revised_drawing.html', projects=projects, drawing_types=drawing_types)
    else:
        cur = mysql.connection.cursor()
        project_id = request.form['project_id']
        type = request.form['drawing_type']
        name = request.form['drawing_name']
        new_drawing_query = 'INSERT into revised_drawings (name, type, project_id) values (%s, %s, %s)'
        cur.execute(new_drawing_query, (name, type, str(project_id)))
        drawing_id = cur.lastrowid
        if 'drawing' in request.files:
            file = request.files['drawing']
            if file.filename == '':
                flash('No selected file', 'danger ')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                drawing_filename = 'rd_' + str(drawing_id) + '.pdf'
                output = send_to_s3(file, app.config["S3_BUCKET"], drawing_filename)
                if output != 'success':
                    flash('File upload failed', 'danger')
                    return redirect(request.referrer)
            mysql.connection.commit()
            flash('Revised drawing uploaded successfully', 'success')
            return redirect('/erp/revised_drawings')


@app.route('/view_drawings', methods=['GET'])
def  view_drawings():            
    return ''


@app.route('/drawings', methods=['GET'])
def drawings():
    table_name = ''
    if 'category' in request.args:
        table_name = request.args['category']
    else:
        table_name = get_drwaings_table_name()
    session['category'] = table_name
    drawings_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'" + table_name + "'"
    cur = mysql.connection.cursor()
    cur.execute(drawings_query)
    result = cur.fetchall()

    query_string = 'p.project_id, p.project_name, p.project_number, '

    drawing_names = []
    for i in result[2:]:
        query_string += 'd.' + i[0] + ', '
        drawing_names.append(i[0].replace('_', ' ').capitalize())

    query_string = query_string[:-2]
    drawings = []
    if len(get_projects_for_current_user()) > 0:
        if session['role'] not in ['Super Admin', 'Purchase Head', 'COO', 'QS Head','QS Engineer', 'Purchase Head', 'Site Engineer',
                                   'Design Head']:
            drawings_info = "SELECT " + query_string + " FROM projects p LEFT OUTER JOIN " + table_name + " d on " \
                            "p.project_id=d.project_id AND p.is_approved=1 AND p.archived=0 " \
                            ' WHERE p.project_id IN ' + str(get_projects_for_current_user()) +' ORDER BY p.project_number'

            cur.execute(drawings_info)
            drawings = cur.fetchall()

        else:
            drawings_info = "SELECT " + query_string + " FROM projects p LEFT OUTER JOIN " + table_name + " d on " \
                            "p.project_id=d.project_id WHERE p.is_approved=1 AND p.archived=0 ORDER BY p.project_number"
            cur.execute(drawings_info)
            drawings = cur.fetchall()

    return render_template('drawings.html', role=session['role'], drawing_names=drawing_names, drawings=drawings)


def get_drwaings_table_name():
    role = session['role']
    if role in ['Super Admin', 'COO', 'Senior Architect', 'Architect', 'Design Head']:
        return 'architect_drawings'
    elif role == 'Structural Designer':
        return 'structural_drawings'
    elif role == 'Electrical Designer':
        return 'electrical_drawings'
    elif role == 'PHE Designer':
        return 'plumbing_drawings'


@app.route('/upload_drawing', methods=['POST'])
def upload_drawing():
    project_id = request.form['project_id']
    drawing_name = request.form['drawing_name']
    drawing_name = drawing_name.lower().replace(' ', '_')
    if request.method == 'POST':
        drawing_filenames = []
        drawing_filename = ''
        files = request.files.getlist("drawings[]")
        index = 1
        for file in files:
            if file.filename == '':
                flash('No selected file', 'danger ')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                drawing_filename = 'd_'+str(project_id) + '_' + str(drawing_name) + '_' + str(index) + '_' + str(int(time.time())) + '.pdf'
                output = send_to_s3(file, app.config["S3_BUCKET"], drawing_filename)
                drawing_filenames.append(drawing_filename)
                index = index + 1
                if output != 'success':
                    flash('File upload failed', 'danger')
                    return redirect(request.referrer)
        

        cur = mysql.connection.cursor()
        table_name = ''
        if 'category' in request.form:
            table_name = request.form['category']
        elif 'category' in session:
            table_name = session['category']
        else:
            table_name = get_drwaings_table_name()
        check_if_drawing_exists_query = 'SELECT id, '+ drawing_name +' FROM ' + table_name + ' WHERE project_id=' + str(project_id)
        cur.execute(check_if_drawing_exists_query)
        result = cur.fetchone()
        if result is not None:
            update_drawing_query = 'UPDATE ' + table_name + ' set ' + drawing_name + '="' + '||'.join(drawing_filenames) + '" WHERE id=' + str(
                result[0])
            cur.execute(update_drawing_query)
            drawing_name = drawing_name.replace('_', ' ').capitalize()
            if str(result[1]).strip() != '':
                revision = 1
                revised_drawing_no_query = 'SELECT id from revised_drawings WHERE name="'+drawing_name+'" AND ' \
                                            'type="'+table_name+'" AND project_id='+str(project_id)
                cur.execute(revised_drawing_no_query)
                res = cur.fetchall()
                if res is not None: 
                    revision = len(res) + 1
                revised_drawing_query = 'INSERT into revised_drawings (name, type, project_id, file, revision) values (%s, %s, %s, %s, %s)'
                cur.execute(revised_drawing_query, (drawing_name, table_name, str(project_id), result[1], revision))


            flash(drawing_name + ' Drawing uploaded to project ' + request.form['project_name'], 'success')
        else:
            insert_drawing_query = 'INSERT into ' + table_name + ' (project_id, ' + drawing_name + ') values (%s, %s)'
            cur.execute(insert_drawing_query, (str(project_id), '||'.join(drawing_filenames)))
            drawing_name = drawing_name.replace('_', ' ').capitalize()
            flash(drawing_name + ' Drawing uploaded to project ' + request.form['project_name'], 'success')

        if 'drawing_request_id' in request.form:
            IST = pytz.timezone('Asia/Kolkata')
            current_time = datetime.now(IST)
            timestamp = current_time.strftime('%d %m %Y at %H %M')
            query = 'UPDATE drawing_requests SET status="closed" ' \
                    'WHERE id='+str(request.form['drawing_request_id'])
            cur.execute(query)

            mysql.connection.commit()
            return redirect('/erp/view_drawings_requests')

        mysql.connection.commit()            
        return redirect('/erp/drawings')

@app.route('/change_drawing_status', methods=['POST'])
def change_drawing_status():
    project_id = request.form['project_id']
    drawing_name = request.form['drawing_name']
    action = request.form['action']
    drawing_name = drawing_name.lower().replace(' ', '_')
    
    cur = mysql.connection.cursor()
    table_name = ''
    if 'category' in session:
        table_name = session['category']
    else:
        table_name = get_drwaings_table_name()

    cur = mysql.connection.cursor()
    check_if_drawing_exists_query = 'SELECT id FROM ' + table_name + '  WHERE project_id=' + str(project_id)
    cur.execute(check_if_drawing_exists_query)
    result = cur.fetchone()
    if result is not None:
        if action == 'pending':
            update_drawing_query = 'UPDATE ' + table_name + ' set ' + drawing_name + '="" WHERE id=' + str(
                result[0])
            cur.execute(update_drawing_query)
        elif action == 'not_applicable':
            update_drawing_query = 'UPDATE ' + table_name + ' set ' + drawing_name + '="-1" WHERE id=' + str(
                result[0])
            cur.execute(update_drawing_query)
        mysql.connection.commit()
        flash('Drawing marked as in progress!', 'success')
        return redirect('/erp/drawings')
    else:
        insert_drawing_query = 'INSERT into ' + table_name + ' (project_id, ' + drawing_name + ') values (%s, %s)'
        if action == 'pending':
            cur.execute(insert_drawing_query, (str(project_id), ''))
        if action == 'not_applicable':    
            cur.execute(insert_drawing_query, (str(project_id), '-1'))
        mysql.connection.commit()
        flash('Drawing marked as in progress!', 'success')
        return redirect('/erp/drawings')



@app.route('/mark_drawing_in_progress', methods=['POST'])
def mark_drawing_in_progress():
    project_id = request.form['project_id']
    drawing_name = request.form['drawing_name']
    drawing_name = drawing_name.lower().replace(' ', '_')

    cur = mysql.connection.cursor()
    table_name = ''
    if 'category' in session:
        table_name = session['category']
    else:
        table_name = get_drwaings_table_name()

    cur = mysql.connection.cursor()
    check_if_drawing_exists_query = 'SELECT id FROM ' + table_name + '  WHERE project_id=' + str(project_id)
    cur.execute(check_if_drawing_exists_query)
    result = cur.fetchone()
    if result is not None:
        update_drawing_query = 'UPDATE ' + table_name + ' set ' + drawing_name + '="0" WHERE id=' + str(
            result[0])
        cur.execute(update_drawing_query)
        mysql.connection.commit()
        flash('Drawing marked as in progress!', 'success')
        return redirect('/erp/drawings')
    else:
        insert_drawing_query = 'INSERT into ' + table_name + ' (project_id, ' + drawing_name + ') values (%s, %s)'
        cur.execute(insert_drawing_query, (str(project_id), '0'))
        mysql.connection.commit()
        flash('Drawing marked as in progress!', 'success')
        return redirect('/erp/drawings')


@app.route('/logout', methods=['GET'])
def logout():
    del session['email']
    del session['name']
    del session['role']
    return redirect('/erp/login')


# APIs for mobile app
@app.route('/API/nt_nmr', methods=['GET'])
def api_nt_nmr():
    if request.method == 'GET':
        project_id=request.args['project_id']
        bills_query = 'SELECT wo_bills.id, wo_bills.contractor_name, wo_bills.contractor_code, wo_bills.stage, wo_bills.quantity,' \
                        ' wo_bills.rate, wo_bills.approval_2_amount FROM wo_bills WHERE project_id='+str(project_id)+' AND trade="NT/NMR"'
        cur = mysql.connection.cursor()
        cur.execute(bills_query)
        nt_nmr_bills = cur.fetchall()

        return jsonify(nt_nmr_bills)


@app.route('/API/view_bills', methods=['GET'])
def api_view_bills():
    if request.method == 'GET':
        project_id = request.args['project_id']
        contractor_name = request.args['name']
        contractor_code = request.args['code']
        trade = request.args['trade']

        cur = mysql.connection.cursor()
        data = {'name': '', 'code': '', 'pan': '', 'value': '', 'balance': '', 'trade': '', 'contractor_id': ''}

        get_contractor_query = 'SELECT id, name, code, pan from contractors WHERE code="'+contractor_code+'"'
        cur.execute(get_contractor_query)
        res = cur.fetchone()
        if res is not None:
            data['name'] = res[0]
            data['code'] = res[1]
            data['pan'] = res[2]

        get_wo_query = 'SELECT id, value, balance from work_orders WHERE trade=%s AND project_id=%s'
        cur.execute(get_wo_query, (trade, project_id))
        res = cur.fetchone()
        if res is not None:
            data['value'] = res[1]
            data['balance'] = res[2]
            data['trade'] = trade
            data['work_order_id'] = res[0]

        get_bills_query = 'SELECT w.stage, w.percentage, b.amount, b.approval_2_amount, b.trade, b.approved_on' \
                            ' FROM wo_milestones w LEFT OUTER JOIN wo_bills b ON b.stage=w.stage AND b.contractor_code=%s AND b.project_id=%s WHERE w.work_order_id=%s'
        cur.execute(get_bills_query, (contractor_code, project_id, str(data['work_order_id'])))
        bills = cur.fetchall()

        get_project_query = 'SELECT project_name, project_number from projects WHERE project_id=' + str(project_id)
        cur.execute(get_project_query)
        project = cur.fetchone()
        return jsonify(bills)

@app.route('/API/post_comment', methods=['GET','POST'])
def post_comment():
    if request.method == 'POST':
        user_id = request.form['user_id']
        project_id = request.form['project_id']
        note = request.form['note']


        IST = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(IST)
        timestamp = current_time.strftime('%d %m %Y at %H %M')

        cur = mysql.connection.cursor()
        query = 'INSERT into notes_and_comments(note, timestamp, user_id, project_id) values(%s, %s, %s, %s)'
        cur.execute(query, (note, timestamp, user_id, project_id))
        mysql.connection.commit()
        return jsonify({'message':'success', 'note_id': str(cur.lastrowid) })

@app.route('/API/notes_picture_uplpoad', methods=['GET','POST'])
def notes_picture_uplpoad():
    if request.method == 'POST':
        note_id = request.form['note_id']
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger ')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filetype = file.filename.split('.')[-1]
            output = send_to_s3(file, app.config["S3_BUCKET"], 'note_'+str(note_id)+'.'+filetype)
            if output != 'success':
                return jsonify({'message':'failed'})

            cur = mysql.connection.cursor()
            query = 'UPDATE notes_and_comments SET attachment="note_'+str(note_id)+'.'+filetype+'" WHERE id='+str(note_id)
            cur.execute(query)
            mysql.connection.commit()
            return jsonify({'message':'success'})

@app.route('/API/mark_notifications_as_read', methods=['GET','POST'])
def mark_notifications_as_read():
    if request.method == 'GET':
        if 'user_id' not in request.args:
            return 'No user'
        else:
            user_id = request.args['user_id']
            cur = mysql.connection.cursor()
            query = 'UPDATE app_notifications SET unread=0 WHERE user_id='+str(user_id)

            cur.execute(query)
            mysql.connection.commit()
            return 'success'

@app.route('/API/get_POs', methods=['GET','POST'])
def get_POs():
    if request.method == 'GET':
        if 'project_id' not in request.args:
            return 'No project'
        else:
            project_id = request.args['project_id']
            cur = mysql.connection.cursor()
            get_POs ='SELECT id, material, quantity, unit, purchase_order FROM indents' \
                            ' WHERE status="approved_by_ph" AND project_id =' + str(project_id)
            cur.execute(get_POs)
            res = cur.fetchall()
            return jsonify(res)

@app.route('/API/get_work_orders', methods=['GET','POST'])
def get_work_orders():
    if request.method == 'GET':
        if 'project_id' not in request.args:
            return 'No project'
        else:
            project_id = request.args['project_id']
            work_orders = get_work_orders_for_project(project_id)
            return jsonify(work_orders)

@app.route('/API/get_notes', methods=['GET','POST'])
def get_notes():
    if request.method == 'GET':
        if 'project_id' not in request.args:
            return 'No project'
        else:
            project_id = request.args['project_id']
            cur = mysql.connection.cursor()
            get_notes = 'SELECT n.note, n.timestamp, u.name, n.id , n.attachment FROM ' \
                            'notes_and_comments n LEFT OUTER JOIN projects p on p.project_id=n.project_id ' \
                            ' LEFT OUTER JOIN App_users u on u.user_id=n.user_id' \
                            ' WHERE p.project_id =' + str(project_id)
            cur.execute(get_notes)
            res = cur.fetchall()
            return jsonify(res)

@app.route('/API/dpr_image_upload', methods=['POST'])
def dpr_image_upload():
    if request.method == 'POST':
        file = request.files['image']
        if file.filename == '':
            flash('No selected file', 'danger ')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            content_type = file.content_type
            in_mem_file = BytesIO(file.read())
            im = Image.open(in_mem_file)
            im.thumbnail((600, 1000))
            in_mem_file = BytesIO()
            im.save(in_mem_file, format=im.format)
            in_mem_file.seek(0)
            
            filename = secure_filename(file.filename)
            output = send_to_s3(in_mem_file, app.config["S3_BUCKET"], 'migrated/'+filename, "public-read", content_type)
            if output != 'success':
                return output
        return 'success'

@app.route('/API/create_indent', methods=['POST'])
def create_indent():
    if request.method == 'POST':
        project_id = request.form['project_id']
        material = request.form['material']
        quantity = request.form['quantity']
        unit = request.form['unit']
        purpose = request.form['purpose']
        timestamp = request.form['timestamp']
        user_id = request.form['user_id']
        status = 'unapproved'
        cur = mysql.connection.cursor()


        if 'approvalTaken' in request.form and 'differenceCost' in request.form:
            

            approval_taken = request.form['approvalTaken']
            difference_cost = request.form['differenceCost']
            
            query = 'INSERT into indents(project_id, material, quantity, unit, purpose, status, created_by_user, timestamp, approval_taken, difference_cost) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            values = (project_id, material, quantity, unit, purpose, status, user_id, timestamp, approval_taken, difference_cost)
        else: 
            query = 'INSERT into indents(project_id, material, quantity, unit, purpose, status, created_by_user, timestamp) values (%s, %s, %s, %s, %s, %s, %s, %s)'
            values = (project_id, material, quantity, unit, purpose, status, user_id, timestamp)

        cur.execute(query, values)
        mysql.connection.commit()
        return jsonify({'message': 'success'})

@app.route('/API/create_drawing_request', methods=['POST'])
def create_drawing_request():
    if request.method == 'POST':
        project_id = request.form['project_id']
        category = request.form['category']
        drawing = request.form['drawing']
        purpose = request.form['purpose']
        timestamp = request.form['timestamp']
        user_id = request.form['user_id']

        cur = mysql.connection.cursor()
        query = 'INSERT into drawing_requests(project_id, category, drawing, purpose, created_by_user, timestamp) values (%s, %s, %s, %s, %s, %s)'
        values = (project_id, category, drawing, purpose, user_id, timestamp)
        cur.execute(query, values)
        mysql.connection.commit()
        return jsonify({'message': 'success'})

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
    query = 'UPDATE indents SET status="' + status + '", acted_by_user=' + str(
        request.form['acted_by_user']) + ' WHERE id=' + str(indent_id)
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

@app.route('/API/get_my_indents', methods=['GET'])
def get_my_indents():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        user_id = request.args['user_id']
        access_query = 'SELECT access, role from App_users WHERE user_id=' + str(user_id)
        cur.execute(access_query)
        res = cur.fetchone()
        access = res[0]
        role = res[1]
        if role == 'Admin':
            indents_query = 'SELECT indents.id, projects.project_id, projects.project_name, indents.material, indents.quantity, indents.unit, indents.purpose' \
                            ', App_users.name, indents.timestamp, indents.created_by_user, indents.status , indents.difference_cost, indents.approval_taken FROM indents INNER JOIN projects on indents.project_id=projects.project_id ' \
                            ' LEFT OUTER JOIN App_users on indents.created_by_user=App_users.user_id AND indents.created_by_user='+str(user_id)+' ORDER by indents.id DESC'
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
                indent_entry['status'] = i[10].replace('_',' ').title()
                indent_entry['difference_cost'] = i[11]
                indent_entry['approval_taken'] = i[12]
                data.append(indent_entry)

            return jsonify(data)
        elif len(access):
            access = access.split(',')
            access_as_int = [int(i) for i in access]
            access_tuple = tuple(access_as_int)
            indents_query = 'SELECT indents.id, projects.project_id, projects.project_name, indents.material, indents.quantity, indents.unit, indents.purpose' \
                            ', App_users.name, indents.timestamp, indents.created_by_user, indents.status , indents.difference_cost, indents.approval_taken FROM indents INNER JOIN projects on indents.project_id=projects.project_id AND indents.project_id IN ' + str(
                access_tuple) + '' \
                                ' LEFT OUTER JOIN App_users on indents.created_by_user=App_users.user_id AND indents.created_by_user='+str(user_id)+' ORDER by indents.id DESC'
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
                indent_entry['status'] = i[10].replace('_',' ').title()
                indent_entry['difference_cost'] = i[11]
                indent_entry['approval_taken'] = i[12]
                data.append(indent_entry)

            return jsonify(data)
        else:
            return jsonify([])


@app.route('/API/get_unapproved_indents', methods=['GET'])
def get_unapproved_indents():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        user_id = request.args['user_id']
        access_query = 'SELECT access, role from App_users WHERE user_id=' + str(user_id)
        cur.execute(access_query)
        res = cur.fetchone()
        access = res[0]
        role = res[1]
        if role == 'Admin':
            indents_query = 'SELECT indents.id, projects.project_id, projects.project_name, indents.material, indents.quantity, indents.unit, indents.purpose' \
                            ', App_users.name, indents.timestamp, indents.created_by_user , indents.difference_cost, indents.approval_taken FROM indents INNER JOIN projects on indents.status="unapproved" AND indents.project_id=projects.project_id ' \
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
                indent_entry['difference_cost'] = i[10]
                indent_entry['approval_taken'] = i[11]
                data.append(indent_entry)

            return jsonify(data)
        elif len(access):
            access = access.split(',')
            access_as_int = [int(i) for i in access]
            access_tuple = tuple(access_as_int)
            indents_query = 'SELECT indents.id, projects.project_id, projects.project_name, indents.material, indents.quantity, indents.unit, indents.purpose' \
                            ', App_users.name, indents.timestamp, indents.created_by_user , indents.difference_cost, indents.approval_taken FROM indents INNER JOIN projects on indents.status="unapproved" AND indents.project_id=projects.project_id AND indents.project_id IN ' + str(
                access_tuple) + '' \
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
                indent_entry['difference_cost'] = i[10]
                indent_entry['approval_taken'] = i[11]
                data.append(indent_entry)

            return jsonify(data)
        else:
            return jsonify([])


@app.route('/API/get_notifications', methods=['GET'])
def get_notifications():
    recipient = request.args['recipient']
    cur = mysql.connection.cursor()
    notifications_query = 'SELECT title, body, timestamp, unread from app_notifications WHERE user_id=' + str(recipient)
    cur.execute(notifications_query)
    data = []
    result = cur.fetchall()
    for i in result:
        data.append({'title': i[0], 'body': i[1], 'timestamp': i[2], 'unread': i[3]})
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
