from flask import Flask
from flask import redirect, url_for, request, render_template, send_file
from io import BytesIO
import flask
import sqlite3
import database
import dataframe
import datetime

app = Flask(__name__)


@app.route('/')
def index():
    # Clear ip_records table
    database.erase_ips()
    return render_template('login.html')


@app.route('/validate_login', methods=["POST"])
def validate_login():
    username = request.form['username']
    password = request.form['password']
    ip = flask.request.remote_addr
    if database.validate_login(username, password):
        database.insert_new_ip(username, str(ip))
        return render_template('home.html')
    error = "Please enter valid login credentials."
    return render_template('login.html', error=error)


@app.route('/upload_file', methods=["GET", "POST"])
def upload_file_page():
    return render_template('upload_file.html')


@app.route('/upload_file_', methods=["GET", "POST"])
def upload_file():
    ip_address = flask.request.remote_addr
    username = database.get_username_by_ip(str(ip_address))
    # Restrict to upload pending.
    if request.method == "POST":
        file = request.files['user_file']

        file_data = file.read()
        size_of_file = (len(file_data) * 0.000125) * 8
        upload_date = str(datetime.datetime.today())[0:19]
        user_file_name = file.filename.replace("'", "")

        if database.is_user_not_plan_pro(username[0]):
            if database.check_user_space_consumed(username[0]):
                return "You dont have enough space to upload the file."

        database.insert_data(username[0], user_file_name, file_data, size_of_file, upload_date)
        database.update_space_used(username[0], size_of_file)
        return render_template("home.html")

    return render_template("upload_file.html")


@app.route('/view')
def view_files():
    ip_address = flask.request.remote_addr
    username = database.get_username_by_ip(str(ip_address))
    files, file_sizes = database.view_files(username[0])
    return dataframe.dataframe(files, file_sizes)


@app.route('/logout')
def logout():
    database.delete_ip(ip=flask.request.remote_addr)
    return render_template('login.html')


@app.route('/download_file', methods=["GET", "POST"])
def download_file():
    return render_template("download_file.html")


@app.route('/download_file_send', methods=["GET", "POST"])
def send_file():
    ip = flask.request.remote_addr
    username = database.get_username_by_ip(str(ip))
    filename = request.form['filename'].strip()

    if database.check_file_belongs(username[0], filename):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(f""" SELECT data from user_data where name='{filename}' """)

        file = cursor.fetchone()

        conn.commit()
        cursor.close()
        conn.close()
        return flask.send_file(BytesIO(file[0]), attachment_filename=filename, as_attachment=True)

    error = f"No file found as {filename}"
    return render_template('download_file.html', error=error)


@app.route('/signup')
def sigup():
    return render_template('signup.html')


@app.route('/signup_data_valid', methods=["POST"])
def signup_new_user():
    username = request.form['username']
    password = request.form['password']
    plan_details = request.form['plan_details']
    plan_code = request.form['plan_code']
    if database.check_username_available(username):

        if plan_details == "lite":
            database.signup_user(username, password, "lite", 0)
            database.insert_new_ip(username, flask.request.remote_addr)
            return render_template("home.html", message="Thank you! Your account has been created.")

        if plan_details == "pro":
            if database.is_pro_code_valid(plan_code):
                database.signup_user(username, password, "pro", 0)
                database.insert_new_ip(username, flask.request.remote_addr)
                return render_template('home.html', message="Thank you! Your pro account has been created.")
    else:
        return "Username not available please try for a different username."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
