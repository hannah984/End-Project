from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError

class ContactForm(Form):
  name = TextField("Name",  [validators.Required()])
  email = TextField("Email",  [validators.Required(), validators.Email()])
  subject = TextField("Subject",  [validators.Required()])
  message = TextAreaField("Message",  [validators.Required()])
  submit = SubmitField("Send")

#We just created a form. What did we do? First, we imported a few useful classes from Flask-WTF — the base Form class, a text field, a textarea field for multi-line text input, and a submit button. Next, we created a new class named ContactForm, inheriting from the base Form class. Then we created each field that we want to see in the contact form. Instead of writing <input type="text">Name</input> in an HTML file, you write name = TextField("Name").
#We start by importing validators and ValidationError from Flask-WTF. This gives us access to Flask-WTF's built-in validators. Next we add [validators.Required()] to each form field in order to validate its presence. Notice that this validator is inside a Python list, meaning that we can easily add more validators to this list.