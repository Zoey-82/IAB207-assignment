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
    user_name=StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

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
    
