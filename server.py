from flask import Flask, redirect, render_template, flash, request, session
from mysqlconnection import MySQLConnector
import re, datetime, time
app = Flask(__name__)
mysql = MySQLConnector(app,'emails')
app.secret_key = "penguins"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
@app.route('/')
def index():
    # emails = mysql.query_db("SELECT * FROM emails")
    # print emails
    return render_template('index.html')
@app.route('/success', methods=['POST'])
def success():
    check = mysql.query_db("SELECT email from emails WHERE email = '{}'".format(request.form['email']))
    
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!")
        return redirect ('/')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        return redirect ('/')
    elif len(check) > 0:
        flash("Email has already been entered")
        return redirect('/')

    flash("The email address you entered {} is a VALID email address! Thank You".format(request.form['email']))
    query = "INSERT INTO emails(email, created_at, updated_at) VALUES(:email, NOW(), NOW())"
    data = {
        'email': request.form['email']
    }
    
   
    mysql.query_db(query, data)
    emails = mysql.query_db("SELECT * FROM emails")
    return render_template('success.html', all_emails=emails)

@app.route('/delete', methods=['POST'])
def delete():
    mysql.query_db("DELETE FROM emails ORDER BY id desc limit 1")
    return redirect('/success')
app.run(debug=True)