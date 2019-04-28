from flask import Flask, render_template, request, flash, redirect, session
from forms import ContactForm
#import Massage and Mail classes from Flask-Mail
from flask_mail import Message, Mail
import sqlite3
from dbconnect import dbconnect #import function from dbconnect.py

#request determines whether the current HTTP method is a GET or a POST
mail = Mail()

app = Flask(__name__)  

app.secret_key = 'supersecretkey' 
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'hannah.rau@code.berlin'
app.config["MAIL_PASSWORD"] = 'password'
 
mail.init_app(app)
@app.route('/')
def home():
  return render_template('home.html')

@app.route('/motion')
def motion():
  return render_template('motion.html')

@app.route('/editorial')
def editorial():
  return render_template('editorial.html')

@app.route('/personal')
def personal():
  return render_template('personal.html')

@app.route('/lifestyle')
def lifestyle():
  return render_template('lifestyle.html')

#If any validation check fails, form.validate() will be False. The error message All fields are required will be sent to contact.html. Otherwise, we'll see the temporary placeholder string Form posted, indicating the form has been successfully submitted.

@app.route('/contact', methods=['GET', 'POST']) 
def contact():
  form = ContactForm()
 
  if request.method == 'POST':  #submitbutton
    if form.validate() == False:
      flash('All fields are required.') #error message 
      return render_template('contact.html', form=form) #still stay at the page
    else:
      #start composing a new message. 
      msg = Message(form.subject.data, sender='hannah.rau@code.berlin', recipients=['hanahthecoder@gmail.com']) #a "from" address, and a "to" address
      msg.body = """
      From: %s <%s> 
      %s
      """ % (form.name.data, form.email.data, form.message.data) #format the mail - we write the email itself. We include the user's name, email and message
      mail.send(msg) #message send

      return render_template('contact.html', success=True)
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
  cur, conn = dbconnect() # connect to database (in a seperated function)
  if request.method == 'POST': #submitbutton
    entered_comment = request.form['comment'] #collect values in a form with method="post"
    cur.execute("INSERT INTO feedbackherman (comment) VALUES ('{}')".format(entered_comment)) #add comment to database
    conn.commit()
  cur.execute('SELECT comment FROM feedbackherman') #take the comment out of the database 
  rows = cur.fetchall()
  return render_template('feedback.html', comments = rows) #display everything
  
@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST': #submitbutton
    entered_username = request.form['username'] #take the username out of the form
    entered_password = request.form['password'] #take the password out of the form
    cur, conn = dbconnect() # connect to database (in a seperated function)
    cur.execute('SELECT username, password FROM logininformation') #read login information out of the database
    rows = cur.fetchall() 
    # username = rows[0][0]
    # password = rows[0][1]
    # -> take data out of the list of tuples
    if rows[0] == (entered_username, entered_password): #if the entered info is equal to the database -> route to editcomment.html
      session['username'] = entered_username #save username in cookie of user if loged in successfully 
      return redirect('/deletecomment') 
  return render_template('login.html') #in case the information is wrong or you just want to view the page the user stays at the login.html

@app.route('/deletecomment', methods=['GET', 'POST'])
def deletecomment():
  if 'username' not in session: #check if user is logged in
    return redirect('/login')  #if he is not go to login.html
  cur, conn = dbconnect() #connection to database
  if request.method == 'POST': #delete button
    entered_id = request.form['id'] #take id out of form
    cur.execute("DELETE FROM feedbackherman WHERE id = {} ".format(entered_id)) #delete the comment out of the table
    conn.commit() #save
  cur.execute('SELECT comment, id FROM feedbackherman') #get all comments
  rows = cur.fetchall() # fetch all comments and save in variable rows
  return render_template('deletecomment.html', comments = rows) #display the comments from the database
 
@app.route('/editcomment', methods=['GET', 'POST'])
def editcomment():
  if 'username' not in session: #check if user is logged in
    return redirect('/login')  #if he is not go to login.html
  cur, conn = dbconnect() #connection to database
  if request.method == 'POST': #delete button
    entered_id = request.form['id'] #take id out of form
    entered_comment = request.form['comment']
    cur.execute("UPDATE feedbackherman SET comment = '{}' WHERE id = {} ".format(entered_comment, entered_id)) #delete the comment out of the table
    conn.commit() #save
  cur.execute('SELECT comment, id FROM feedbackherman') #get all comments
  rows = cur.fetchall() # fetch all comments and save in variable rows
  return render_template('editcomment.html', comments = rows) #display the comments from the database

@app.route('/logout')
def logout():
  session.pop("username", None)
  return redirect('/')

 
if __name__ == '__main__':
  app.run(debug=True)


