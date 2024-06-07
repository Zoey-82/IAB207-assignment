from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    contact_number = StringField('Contact Number', validators=[InputRequired()])
    street_address = StringField('Street Address', validators=[InputRequired()])
    submit = SubmitField('Register')

     # submit button
    submit = SubmitField("Register")
    
    # ticket form 
class TicketForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[InputRequired(), NumberRange(min=1)])
    submit = SubmitField('Book Tickets')

#comment form
class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[InputRequired()])
    submit = SubmitField('Post Comment')

# event form
class EventForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    date = DateTimeField('Date', format='%Y-%m-%d %H:%M:%S', validators=[InputRequired()])
    submit = SubmitField('Create Event')
