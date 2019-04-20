from flask import Flask, render_template, request, flash
from forms import ContactForm
#import Massage and Mail classes from Flask-Mail
from flask_mail import Message, Mail

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
 
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      #We start by composing a new message. The Message class takes a subject line, a "from" address, and a "to" address. We then collect the contact form's subject field data with form.subject.data and set it as the new message's subject line. The email will be sent from the account you configured in app.config["MAIL_USERNAME"], so that's what we used here for the from address. The email will be sent to your personal email address so that you can receive and respond to new messages.
      #Next, we write the email itself. We include the user's name, email and message. I use Python's string formatting operator % to format the email. And finally, we use mail.send(msg) to send the email (line 15).
      msg = Message(form.subject.data, sender='hannah.rau@code.berlin', recipients=['hanahthecoder@gmail.com'])
      msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)

      return render_template('contact.html', success=True)
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form)

 
if __name__ == '__main__':
  app.run(debug=True)

