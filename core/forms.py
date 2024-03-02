from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.validators import InputRequired, Length, Email, URL


class CaptainRegister(FlaskForm):
    username = StringField('Никнейм', validators=[InputRequired(), Length(min=3, max=128)],
                       render_kw={"placeholder": "Никнейм"})
    full_name = StringField('ФИО', validators=[InputRequired(), Length(min=3, max=256)],
                       render_kw={"placeholder": "Иванов Иван Иванович"})
    email = EmailField('Почта', validators=[InputRequired(), Email()], render_kw={"placeholder": "name@gmail.com"})
    website = StringField('Ссылка на ТГ/ВК', validators=[InputRequired(), URL()],
                          render_kw={"placeholder": "https://t.me/..."})


class TeamRegister(FlaskForm):
    team_name = StringField('Название команды', validators=[InputRequired(), Length(min=3, max=30)],
                            render_kw={"placeholder": "Название_команды"})
    team_city = StringField('Город', validators=[InputRequired()], render_kw={"placeholder": "Донецк"})
    team_affiliation = StringField('Образовательное учреждение', validators=[InputRequired()],
                                   render_kw={"placeholder": "ДонГУ"})


class UsersRegister(FlaskForm):
    username = StringField('Никнейм', validators=[InputRequired(), Length(min=3, max=30)])
    user_email = EmailField('Почта', validators=[InputRequired(), Email()])
