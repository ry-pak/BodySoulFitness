#подключение к БД
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/postgres'
db = SQLAlchemy(app)

#создание таблиц в БД
#заявки
class Applications(db.Model):
    __tablename__="applications"
    application_id=db.Column(db.Integer, primary_key=True, index=True)
    client_name=db.Column(db.String(50), nullable=False)
    client_phone=db.Column(db.String(20), nullable=False)
    client_email=db.Column(db.String(20), nullable=False)
    application_datetime=db.Column(db.DateTime, nullable=False)
    rel_clients2=relationship("Clients", back_populates="rel_appl")

#абонементы
class Programs(db.Model):
    __tablename__="programs"
    program_id=db.Column(db.Integer, primary_key=True, index=True)
    program_name=db.Column(db.String(50), nullable=False)
    program_description=db.Column(db.Text, nullable=False)
    program_cost=db.Column(db.Numeric(2), nullable=False)
    rel_clients=relationship("Clients", back_populates="rel_pro")

#секции
class Sections(db.Model):
    __tablename__="sections"
    section_id=db.Column(db.Integer, primary_key=True, index=True)
    section_name=db.Column(db.String(50), nullable=False)
    rel_train=relationship("Trainers", back_populates="rel_sect")
    rel_schedule2=relationship("Schedule", back_populates="rel_sect2")

#тренеры
class Trainers(db.Model):
    __tablename__="trainers"
    trainer_id=db.Column(db.Integer, primary_key=True, index=True)
    trainer_name=db.Column(db.String(50), nullable=False)
    trainer_phone=db.Column(db.String(20), nullable=False)
    trainer_address=db.Column(db.String(100), nullable=False)
    section_id=db.Column(db.Integer, db.ForeignKey('sections.section_id'))
    rel_sect=relationship("Sections", back_populates="rel_train")

#клиенты
class Clients(db.Model):
    __tablename__="clients"
    client_id=db.Column(db.Integer, primary_key=True, index=True)
    program_id=db.Column(db.Integer, db.ForeignKey('programs.program_id'))
    application_id=db.Column(db.Integer, db.ForeignKey('applications.application_id'))
    rel_pro=relationship("Programs", back_populates="rel_clients")
    rel_appl=relationship("Applications", back_populates="rel_clients2")
    #rel_user=relationship("Users", back_populates="rel_client3")
    rel_schedule=relationship("Schedule", back_populates="rel_client4")

#пользователи 
class Users(UserMixin, db.Model):
    __tablename__="users"
    user_id=db.Column(db.Integer, primary_key=True, index=True)
    user_login=db.Column(db.String(50), nullable=False)
    user_password=db.Column(db.String(250), nullable=False)
    #rel_client3=relationship("Clients", back_populates="rel_user")

#расписание секций
class Schedule(db.Model):
    __tablename__="schedule"
    schedule_id=db.Column(db.Integer, primary_key=True, index=True)
    schedule_date=db.Column(db.Date, nullable=False)
    schedule_time=db.Column(db.Time, nullable=False)
    client_id=db.Column(db.Integer, db.ForeignKey('clients.client_id'))
    section_id=db.Column(db.Integer, db.ForeignKey('sections.section_id'))
    rel_client4=relationship("Clients", back_populates="rel_schedule")
    rel_sect2=relationship("Sections", back_populates="rel_schedule2")

#новости
class News (db.Model):
    __tablename__="news"
    news_id=db.Column(db.Integer, primary_key=True, index=True)
    news_date=db.Column(db.Date, nullable=False)
    news_title=db.Column(db.String(50), nullable=False)
    news_body=db.Column(db.Text, nullable=False)


#тестовая таблица с расписанием для текущего функционала
class Schedule2(db.Model):
    __tablename__="schedule2"
    s_id=db.Column(db.Integer, primary_key=True, index=True)
    s_date=db.Column(db.Date, nullable=False)
    s_time=db.Column(db.Time, nullable=False)
    s_name=db.Column(db.String(50), nullable=False)
    s_phone=db.Column(db.String(20), nullable=False)
    s_email=db.Column(db.String(20), nullable=False)
    s_section=db.Column(db.String(50), nullable=False)