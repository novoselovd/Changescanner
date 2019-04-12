from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField, validators, TextAreaField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Incorrect email.'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me')


class SignUpForm(FlaskForm):
    name = StringField('Name', [InputRequired(), Length(min=1, max=50)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Incorrect email'), Length(max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current password', validators=[InputRequired()])
    new_password = PasswordField('New password', validators=[InputRequired()])
    new_password_confirm = PasswordField('Confirm new password', validators=[InputRequired()])


class ResetForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Incorrect email'), Length(max=50)])


class AddExchangerForm(FlaskForm):
    name = StringField('Name of the exchanger', [InputRequired(), Length(min=1, max=50)])
    url = StringField('URL', validators=[InputRequired(), Length(max=50)])
    description = TextAreaField('Short description', validators=[InputRequired(), Length(max=350)])
    country = StringField('Country', validators=[InputRequired(), Length(max=50)])
    comments = TextAreaField('Comments(optional)', validators=[Length(max=350)])


class CommentForm(FlaskForm):
    review = TextAreaField('Review', render_kw={"rows": 10, "cols": 11}, validators=[InputRequired()])
    type = SelectField(u'Type', choices=[('Comment', 'Comment'), ('Positive', 'Positive'), ('Complain', 'Complain')],
                       validators=[InputRequired()])


class MainForm(FlaskForm):
    firstCurr = SelectField(u'I have:', choices=[('WMR', 'Webmoney RUB'),
                                                 ('QWRUB', 'QIWI RUB'),
                                                 ('YAMRUB', 'Yandex.Money RUB'),
                                                 ('BTC', 'Bitcoin'),
                                                 ('SBERRUB', 'Sberbank RUB')],
                       validators=[InputRequired()])
    secondCurr = SelectField(u'I want:', choices=[('WMR', 'Webmoney RUB'),
                                                 ('QWRUB', 'QIWI RUB'),
                                                 ('YAMRUB', 'Yandex.Money RUB'),
                                                 ('BTC', 'Bitcoin'),
                                                 ('SBERRUB', 'Sberbank RUB')],
                       validators=[InputRequired()])


class EditForm(FlaskForm):
    name = StringField('Name of the exchanger', validators=[Length(max=50)])
    url = StringField('URL', validators=[Length(max=50)])
    description = TextAreaField('Short description', validators=[Length(max=350)])
    picURL = StringField('URL of a picture')