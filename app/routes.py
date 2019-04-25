from flask import Flask, render_template, request, flash
from forms import ContactForm
#import Massage and Mail classes from Flask-Mail
from flask_mail import Message, Mail
import sqlite3
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
  if request.method == 'POST': #submitbutton
    entered_comment = request.form['comment'] #collect values in a form with method="post"
    conn =sqlite3.connect('feedback.db') #connect to the database
    cur = conn.cursor()
    cur.execute("INSERT INTO feedbackherman (comment) VALUES ('{}')".format(entered_comment)) #add comment to database
    conn.commit()
    cur.execute('SELECT comment FROM feedbackherman') #take the comment out of the database 
    rows = cur.fetchall()
    return render_template('feedback.html', comments = rows) #display everything
  else:
    conn =sqlite3.connect('feedback.db') #just be on the side without typing in a comment - show all comments
    cur = conn.cursor()
    cur.execute('SELECT comment FROM feedbackherman')
    rows = cur.fetchall()
    return render_template('feedback.html', comments = rows)

if __name__ == '__main__':
  app.run(debug=True)

