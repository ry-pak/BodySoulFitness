from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, URL
from flask_ckeditor import CKEditorField
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

#вход для админа 
class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email()])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField("Войти")

#регистрация админа
class RegisterForm(FlaskForm):
    email = StringField("Логин", validators=[Email()])
    psw = PasswordField("Пароль", validators=[DataRequired(),  Length(min=8, max=20)])
    submit = SubmitField("Зарегистрироваться")
    remember = BooleanField("Запомнить", default = False)

#добавить новость
class PostForm(FlaskForm):
	title = StringField("Название", validators=[DataRequired()])
	content = CKEditorField('Содержание', validators=[DataRequired()])
	submit = SubmitField("Отправить")

#внести данные в расписание
class ScheduleForm(FlaskForm):
    date = StringField("Дата", validators=[DataRequired()])
    time = StringField("Время", validators=[DataRequired()])
    name = StringField("ФИО", validators=[DataRequired()])
    phone = StringField("Телефон", validators=[DataRequired()])
    email = StringField("Email", validators=[Email()])
    section = StringField("Секция", validators=[DataRequired()])
    submit = SubmitField("Отправить")
