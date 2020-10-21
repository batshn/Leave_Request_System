from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, length, EqualTo, ValidationError, Regexp, NumberRange

# create new user
class CreateAccount(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), length(min=10, max=20), Regexp(
        '^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{10,20}$', message="wrong password")])
    password_confirm = PasswordField("Confirm password",
                                     validators=[DataRequired(), EqualTo('password'), length(min=10, max=20)])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('manager', 'Manager'), ('staff', 'Staff')])
    submit = SubmitField("Register now")

# change leave allowance 
class ChangeLeaveAllowance(FlaskForm):
    limitLeaveAllowance = IntegerField("Leave Allowance", validators=[DataRequired(), NumberRange(min=1, max=20, message="it must be bewteen 1 and 20")])
    submit = SubmitField("Update")  

# change the password of users
class ChangePassword(FlaskForm):
    pass_old = PasswordField("Old Password", validators=[DataRequired()])
    pass_new = PasswordField("New Password", validators=[DataRequired(), length(min=10, max=20),  Regexp('^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{10,20}$', message="wrong password")])
    pass_confirm = PasswordField("Confirm password", validators=[DataRequired(), EqualTo('pass_new'), length(min=10, max=20)])
    submit = SubmitField("Change")  

# leave request date
class LeaveRequest(FlaskForm):
    leaveRequest = StringField("Select Date", validators=[DataRequired()])


# change user's role
class ChangeUserRole(FlaskForm):
     role = SelectField('Role', choices=[('admin', 'Admin'), ('manager', 'Manager'), ('staff', 'Staff')])
     submit = SubmitField("Change")


# add public holidays
class PublicHolidays(FlaskForm):
    holidayName = StringField("Holiday ")
    startDate = DateField("Start Date ")
    endDate = DateField("End Date ")
    submit = SubmitField("Add")  