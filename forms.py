from flask_wtf import FlaskForm
from datetime import date, datetime
import bson
from wtforms import (
    # IntegerField,
    StringField,
    TextAreaField,
    SubmitField,
    DateTimeField,
    DateField,
    PasswordField
)

from wtforms.validators import (
    InputRequired,
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError
    # NumberRange
)

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
        InputRequired(),
        Email()
    ])
    password = PasswordField("Password", validators=[
        InputRequired(),
    ])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[
        InputRequired(),
        Email(),
    ])
    password = PasswordField("Password", validators=[
        InputRequired(),
        Length(min=4,max=20, message="Your password must be between 4 to 20 charecters long.")
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        InputRequired(),
        EqualTo("password",message="This password did not match the one  in the password field.")
    ])

    submit = SubmitField("Register")


def date_validation(form,field):
    submitted_date = field.data
    if submitted_date is None:
        raise ValidationError('Date field cannot be empty.')
    
    current_date = datetime.now()
    if submitted_date < current_date:
        raise ValidationError('Date cannot be in the past.')

def modifyIput(form, field):
    _date = field.data
    # print(_date)
    # print(type(_date))
    # _date = datetime.strptime(_date, '%Y-%m-%d')
    field.data = _date.isoformat()
    print(field.data)

    
class TodoForm(FlaskForm):
    title = StringField("Title", validators=[
        InputRequired(), 
        Length(min=3,max=50)
    ])
    description = TextAreaField("Description", validators=[
        InputRequired(),
        Length(min=3,max=500)
    ])
    due_date = DateTimeField("Due Date", format='%d-%m-%YT%H:%M', validators=[
        # DataRequired(),
        InputRequired(),
        # date_validation
        # modifyIput
    ])
    submit = SubmitField("Add Todo") 


    