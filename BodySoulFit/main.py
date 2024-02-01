
import datetime as dt
from datetime import date
import smtplib
import requests
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import desc
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_ckeditor import CKEditor
from forms import RegisterForm, LoginForm, PostForm, ScheduleForm
from db import Applications, Programs, Sections, Trainers, Clients, Users, Schedule, Schedule2


app = Flask(__name__)

ckeditor = CKEditor(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

#секретный ключ для данных сессии и шифрования
app.config['SECRET_KEY'] = '8ABYkEfgPQ6O95donz3WlSihXoc7C0sKN7b'


#главаня страница сайта
@app.route('/')
def home():
    return render_template("home.html", title='Body Soul Fitness')


#страница с формой отправки заявки на тренировку
@app.route('/apply', methods=["POST", "GET"])
def apply():
    try:
        new_client = request.form.get('client_name')
        if request.method == 'POST':
            flash('Данные отправлены')
        appl=Applications(client_name=request.form['client_name'], client_phone=request.form['client_phone'], client_email=request.form['client_email'], application_datetime=dt.datetime.now())
        db.session.add(appl)
        db.session.commit()
    except:
        db.session.rollback()
        #flash('Ошибка данных')
    print(request.form)
    #эти данные идут в БД в таблицу applications
    return render_template("apply.html", title='Запись на тренировку')


#страница входа админа
@app.route('/enter_admin', methods=["POST", "GET"])
def enter_admin():
    form= LoginForm()
    if form.validate_on_submit():
        password = form.psw.data
        result = db.session.execute(db.select(Users).where(Users.user_login == form.email.data))
        user = result.scalar()
        #админ не зарегистрировался
        if not user:
            flash("Неправильный логин")
            return redirect(url_for('registration'))
        #хэш пароля не совпадает
        elif not check_password_hash(user.user_password, form.psw.data):
            flash('Неверный пароль')
            return redirect(url_for('enter_admin'))
        else:
            login_user(user)
            return redirect(url_for('admin_menu'))
    print(request.form)
    return render_template("enter_admin.html", title='Вход', form=form)


#страница регистрации админа
@app.route('/reg_admin', methods=["POST", "GET"])
def reg_admin():
    form = RegisterForm()
    if form.validate_on_submit():
        result = db.session.execute(db.select(Users).where(Users.user_login == form.email.data))
        user = result.scalar()
        if user:
            return redirect(url_for('enter_admin'))
        #хэширование пароял
        hash = generate_password_hash(form.psw.data, method='sha256', salt_length=8)
        #создание учетной записи админа
        new_admin = Users(
            user_login=form.email.data,
            user_password=hash,
        )
        db.session.add(new_admin)
        db.session.commit()
        # аутентификация Flask-Login
        login_user(new_admin)
        return redirect(url_for('admin_menu'))

    print(request.form)
    return render_template("reg_admin.html", title='Регистрация', form=form, current_user=current_user)


#страница с инфо об айкидо
@app.route('/aikido')
def aikido():
    a1="/static/assets/img/ai-1.png"
    a2="/static/assets/img/ai-2.jpg"
    a3="/static/assets/img/ai-3.jpg"
    return render_template("aikido.html", img1=a1, img2=a2, img3=a3, title="Айкидо")

#страница с контактами организации
@app.route('/contacts')
def contacts():
    return render_template("contacts.html", title='Контакты')

#страница с инфо о тренажёрном зале
@app.route('/gym')
def gym():
    g1="static/assets/img/gym2.png"
    g2="static/assets/img/gym3.jpg"
    g3="static/assets/img/gym4.jpg"
    return render_template("gym.html", img1=g1, img2=g2, img3=g3, title='Тренажёрный зал')

#страница с инфо о тренерах
@app.route('/instructors')
def instructors():
    return render_template("instructors.html", title='Тренеры')

#страница с инфо о тайском боксе
@app.route('/muay-thai')
def muay_thai():
    m1="static/assets/img/m-thai1.png"
    m2="static/assets/img/m-thai2.jpg"
    m3="static/assets/img/m-thai3.jpeg"
    return render_template("muay-thai.html", img1=m1, img2=m2, img3=m3, title='Тайский бокс')

#страница с инфо об абонементах
@app.route('/prices')
def prices():
    return render_template("prices.html", title='Цены')

#страница с инфо о расписании тренировок/секций
@app.route('/schedule')
def schedule():
    return render_template("schedule.html", title='Расписание')

#страница с инфо о йоге
@app.route('/yoga')
def yoga():
    y1="static/assets/img/yoga-1.png"
    y2="static/assets/img/yoga-2.jpg"
    y3="static/assets/img/yoga-3.jpg"
    return render_template("yoga.html", img1=y1, img2=y2, img3=y3, title='Йога')


#обработчик отсутствующей страницы
@app.errorhandler(404)
def page_not_found(error):
    cat="/static/assets/img/not_found.jpg"
    return render_template('page_404.html', title='Страница не найдена', cat=cat), 404

#отображение новых заявок
@app.route('/clients_applications')
@login_required
def clients_applications():
    new_applications=[]
    #try:
    new_applications=Applications.query.all()
    new_applications=new_applications[::-1]
    #except:
        #flash('Ошибка при получении данных')
    return render_template('clients_applications.html', title='Новые заявки', new_applications=new_applications)


#Добавление новостей
@app.route('/add_news/', methods=["GET", "POST"])
@login_required
def add_news():
	form = PostForm()
	if form.validate_on_submit():
		news = News(news_title=form.title.data, news_body=form.content.data, news_date=dt.datetime.now())
		form.title.data = ''
		form.content.data = ''
		db.session.add(news)
		db.session.commit()
	return render_template("add_news.html", form=form, title="Добавление новости")

#меню действий в админке
@app.route('/admin_menu')

def admin_menu():
    id=current_user.user_id
    if id == 1:
        return render_template("admin_menu.html", title='Для админа')

#список новостей сайта
@app.route('/news/', methods=["GET", "POST"])
def show_news():
    news = News.query.order_by(News.news_date)
    return render_template("news.html", title='Новости', news=news)

#открыть новость
@app.route('/news/<int:news_id>')
def new(news_id):
	new = News.query.get_or_404(news_id)
	return render_template('new.html', new=new)

#редактировать новости
@app.route('/news/edit/<int:news_id>', methods=['GET', 'POST'])
@login_required
def edit_new(news_id):
    new = News.query.get_or_404(news_id)
    form = PostForm()
    if form.validate_on_submit():
        new.news_title = form.title.data
        new.news_body = form.content.data
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('new', news_id=new.news_id))
    form.title.data = new.news_title
    form.content.data = new.news_body
    return render_template('edit_new.html', form=form)

#удалить новости
@app.route('/news/delete/<news_id>')
@login_required
def delete_new(news_id):
    new_to_delete = News.query.get_or_404(news_id)
    db.session.delete(new_to_delete)
    db.session.commit()
    news = News.query.order_by(News.news_date)
    return render_template("news.html", news=news)

#добавить клиентов в расписание
@app.route('/change_schedule/', methods=["GET", "POST"])
@login_required
def change_schedule():
    form = ScheduleForm()
    if form.validate_on_submit():
        schedule = Schedule2(s_date=form.date.data, s_time=form.time.data, s_name=form.name.data, s_phone=form.phone.data, s_email=form.email.data, s_section=form.section.data)
        #очистить поля ввода
        form.date.data=''
        form.time.data=''
        form.name.data=''
        form.phone.data=''
        form.email.data=''
        form.section.data=''
        db.session.add(schedule)
        db.session.commit()
    return render_template("change_schedule.html", form=form, title="Изменение расписания")

#просмотр списка тренировок клиентов
@app.route('/list_schedule', methods=["GET", "POST"])
@login_required
def list_schedule():
    list_schedule=Schedule2.query.order_by(Schedule2.s_date)
    return render_template('list_schedule.html', list_schedule=list_schedule)

#посмотреть запись в списке тренировок
@app.route('/list_schedule/<int:s_id>')
@login_required
def schedule_item(s_id):
    schedule_item = Schedule2.query.get_or_404(s_id)
    return render_template("schedule_item.html", schedule=schedule_item)

#редактировать запись о тренировке
@app.route('/list_schedule/edit/<int:s_id>', methods=['GET', 'POST'])
@login_required
def edit_schedule_item(s_id):
    schedule_item = Schedule2.query.get_or_404(s_id)
    form = ScheduleForm()
    if form.validate_on_submit():
        schedule_item.s_date = form.date.data
        schedule_item.s_time = form.time.data
        schedule_item.s_name = form.name.data
        schedule_item.s_phone = form.phone.data
        schedule_item.s_email = form.email.data
        schedule_item.s_section = form.section.data
        db.session.add(schedule_item)
        db.session.commit()
        return redirect(url_for('schedule_item', s_id=schedule_item.s_id))
    form.date.data=schedule_item.s_date
    form.time.data=schedule_item.s_time
    form.name.data=schedule_item.s_name
    form.phone.data=schedule_item.s_phone
    form.email.data=schedule_item.s_email
    form.section.data=schedule_item.s_section
    return render_template('edit_schedule_item.html', form=form)

#удалить запись о тренировке
@app.route('/list_schedule/delete/<s_id>')
@login_required
def delete_schedule_item(s_id):
    schedule_item_to_delete = Schedule2.query.get_or_404(s_id)
    db.session.delete(schedule_item_to_delete)
    db.session.commit()
    list_schedule = Schedule2.query.order_by(Schedule2.s_date)
    return render_template("list_schedule.html", list_schedule=list_schedule)


#отправка email с напоминанием о тренировке осуществляется за 1 день до тренировки
#в переменную from_email вводится адрес корпоративной почты
#для корректной работы прописывается smtp-строка для подключения к почте, например: smtp.gmail.com для почты gmail
#в переменную from_password вводится код безопасности для почты, который находится в настройках безопасности акаунта
from_email="bodysoul@gmail.com"
from_password="fwt12stc27"
list_schedule = Shedule2.query.all()
for s in list_schedule:
    if (dt.date.today() + dt.timedelta(days=1)) == list_schedule.s_date:
        to_email=list_schedule.s_email
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(from_email, from_password)
            connection.sendmail(from_addr=from_email, to_addrs=to_email, msg=f"Subject: Напоминание о тренировке\n\nНапоминаем, что {list_shedule.s_date} в {list_schedule.s_time} состоится тренировка по {list_schedule.s_section}")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)

