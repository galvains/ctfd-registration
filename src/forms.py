from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import InputRequired, Length, Email


class UserRegister(FlaskForm):
    credentials = StringField('ФИО', validators=[InputRequired(), Length(min=3, max=256)],
                              render_kw={"placeholder": "Иванов Иван Иванович"})
    email = EmailField('Почта', validators=[InputRequired(), Email()], render_kw={"placeholder": "example@gmail.com"})
    age = StringField('Возраст', validators=[InputRequired(), Length(min=1, max=4)],
                      render_kw={"placeholder": "18"})

    website = StringField('Тег на ТГ/ВК', validators=[InputRequired(), Length(min=5, max=256)],
                          render_kw={"placeholder": "@name"})
    password = PasswordField('Пароль', validators=[InputRequired(), Length(min=4, max=100)])


class TeamRegister(FlaskForm):
    team_name = StringField('Название команды', validators=[InputRequired(), Length(min=3, max=30)],
                            render_kw={"placeholder": "Название_команды"})
    team_city = StringField('Город', validators=[InputRequired()], render_kw={"placeholder": "Донецк"})
    team_affiliation = StringField('Образовательное учреждение', validators=[InputRequired()],
                                   render_kw={"placeholder": "ДонГУ"})
    password = PasswordField('Пароль', validators=[InputRequired(), Length(min=4, max=100)])


class JoinTeam(FlaskForm):
    team_name = StringField('Название команды', validators=[InputRequired(), Length(min=3, max=30)],
                            render_kw={"placeholder": "Название_команды"})
    password = PasswordField('Пароль', validators=[InputRequired(), Length(min=4, max=100)])


class UsersRegister(FlaskForm):
    username = StringField('Никнейм', validators=[InputRequired(), Length(min=3, max=30)])
    user_email = EmailField('Почта', validators=[InputRequired(), Email()])


class UserLogin(FlaskForm):
    email = EmailField('Почта', validators=[InputRequired(), Email()], render_kw={"placeholder": "example@gmail.com"})
    password = PasswordField('Пароль', validators=[InputRequired(), Length(min=4, max=100)])
