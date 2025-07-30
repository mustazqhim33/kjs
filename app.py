from flask import Flask, request, render_template, redirect, url_for, flash, session
from waitress import serve
from werkzeug.utils import secure_filename
import os
import pymysql
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # ⚠️ Change to environment variable in production
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Function to get a new DB connection
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='root',  # ⚠️ Change to environment variable in production
        database='kjs',
        cursorclass=pymysql.cursors.DictCursor
    )


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/header')
def header():
    active_tab = 'colocate'  # example
    tab_titles = {
        'dashboard': 'Home',
        'operation': 'Operation',
        'colocate': 'Colocate',
        'saq': 'SAQ',
        'projects': 'Projects',
        'users': 'Users Management'
    }
    page_title = tab_titles.get(active_tab, 'KJS Dashboard')
    return render_template('base.html', active_tab=active_tab, page_title=page_title)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM users WHERE users_name = %s AND password = %s"
                cursor.execute(sql, (username, password))
                user = cursor.fetchone()
                if user:
                    session['username'] = user['users_name']
                    session['user_id'] = user['users_id']
                    return redirect(url_for('dashboard'))
                else:
                    error = "Invalid username or password"
        finally:
            conn.close()

    return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', active_tab='dashboard')


@app.route('/colocate')
def colocate():
    colocate = [
        {'id': 1, 'site_name': 'Site A', 'status': 'Pending', 'person': 'Alice'},
        {'id': 2, 'site_name': 'Site B', 'status': 'In-progress', 'person': 'Bob'},
        {'id': 3, 'site_name': 'Site C', 'status': 'Completed', 'person': 'Carol'}
    ]
    return render_template('colocate.html', colocate=colocate)


@app.route('/colocate_detail/<int:colocate_id>', methods=['GET', 'POST'])
def colocate_detail(colocate_id):
    if colocate_id == 0:
        colocate_item = {'id': 0, 'site_name': '', 'status': '', 'person': ''}
    else:
        colocate_list = [
            {'id': 1, 'site_name': 'Site A', 'status': 'Pending', 'person': 'Alice'},
            {'id': 2, 'site_name': 'Site B', 'status': 'In-progress', 'person': 'Bob'},
            {'id': 3, 'site_name': 'Site C', 'status': 'Completed', 'person': 'Carol'}
        ]
        colocate_item = next((item for item in colocate_list if item['id'] == colocate_id), None)

    if not colocate_item:
        return "colocate item not found", 404

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT users_id, users_name FROM users")
            users = cur.fetchall()
    finally:
        conn.close()

    return render_template('colocate_detail.html', colocate=colocate_item, users=users)


@app.route('/colocate_detail')
def colocate_add_new():
    return redirect(url_for('colocate_detail', colocate_id=0))


@app.route('/saq')
def saq():
    saq = [
        {'id': 1, 'site_name': 'Site A', 'status': 'Pending', 'person': 'Alice'},
        {'id': 2, 'site_name': 'Site B', 'status': 'In-progress', 'person': 'Bob'},
        {'id': 3, 'site_name': 'Site C', 'status': 'Completed', 'person': 'Carol'}
    ]
    return render_template('saq.html', active_tab='saq', saq=saq)


@app.route('/saq_detail/<int:saq_id>')
def saq_detail(saq_id):
    if saq_id == 0:
        saq_item = {'id': 0, 'site_name': '', 'status': '', 'person': ''}
    else:
        saq_list = [
            {'id': 1, 'site_name': 'Site A', 'status': 'Pending', 'person': 'Alice'},
            {'id': 2, 'site_name': 'Site B', 'status': 'In-progress', 'person': 'Bob'},
            {'id': 3, 'site_name': 'Site C', 'status': 'Completed', 'person': 'Carol'}
        ]
        saq_item = next((item for item in saq_list if item['id'] == saq_id), None)

    if not saq_item:
        return "saq item not found", 404

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT users_id, users_name FROM users")
            users = cur.fetchall()
    finally:
        conn.close()

    return render_template('saq_detail.html', saq=saq_item, users=users)


@app.route('/saq_detail')
def saq_add_new():
    return redirect(url_for('saq_detail', saq_id=0))


@app.route('/projects')
def projects():
    projects = [
        {'id': 1, 'site_name': 'Site A', 'status': 'Pending', 'person': 'Alice'},
        {'id': 2, 'site_name': 'Site B', 'status': 'In-progress', 'person': 'Bob'},
        {'id': 3, 'site_name': 'Site C', 'status': 'Completed', 'person': 'Carol'}
    ]
    return render_template('projects.html', active_tab='projects', projects=projects)


@app.route('/projects_detail/<int:project_id>')
def projects_detail(project_id):
    if project_id == 0:
        projects_item = {'id': 0, 'site_name': '', 'status': '', 'person': ''}
    else:
        projects_list = [
            {'id': 1, 'site_name': 'Site A', 'status': 'Pending', 'person': 'Alice'},
            {'id': 2, 'site_name': 'Site B', 'status': 'In-progress', 'person': 'Bob'},
            {'id': 3, 'site_name': 'Site C', 'status': 'Completed', 'person': 'Carol'}
        ]
        projects_item = next((item for item in projects_list if item['id'] == project_id), None)

    if not projects_item:
        return "projects item not found", 404

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT users_id, users_name FROM users")
            users = cur.fetchall()
    finally:
        conn.close()

    return render_template('projects_detail.html', projects=projects_item, users=users)


@app.route('/projects_detail')
def projects_add_new():
    return redirect(url_for('projects_detail', project_id=0))


@app.route('/users', methods=['GET', 'POST'])
def users():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            if request.method == 'POST':
                users_name = request.form['users_name']
                email = request.form['email']
                title = request.form['title']
                group = request.form['group']
                cur.execute("INSERT INTO users (users_name, email, title, `group`) VALUES (%s, %s, %s, %s)",
                            (users_name, email, title, group))
                conn.commit()
                return redirect(url_for('users'))

            cur.execute("SELECT users_id, users_name, email, title, `group` FROM users")
            users = cur.fetchall()
    finally:
        conn.close()

    return render_template('users.html', users=users)


@app.route('/operation')
def operation():
    operation_data = [
        {
            'occupant': 'Company X',
            'records': [
                {'tower': 'Tower A', 'frequency': '700 MHz'},
                {'tower': 'Tower B', 'frequency': '800 MHz'},
            ]
        },
        {
            'occupant': 'Company Y',
            'records': [
                {'tower': 'Tower C', 'frequency': '900 MHz'},
            ]
        },
    ]
    return render_template('operation.html', operation=operation_data)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)  # 🟢 Production with waitress
