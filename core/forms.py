from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.validators import InputRequired, Length, Email, URL


class CaptainRegister(FlaskForm):
    name = StringField('Никнейм', validators=[InputRequired(), Length(min=3, max=30)],
                       render_kw={"placeholder": "username"})
    email = EmailField('Почта', validators=[InputRequired(), Email()], render_kw={"placeholder": "name@gmail.com"})
    website = StringField('ТГ/ВК тег', validators=[InputRequired(), URL()],
                          render_kw={"placeholder": "https://t.me/..."})


class TeamRegister(FlaskForm):
    team_name = StringField('Название команды', validators=[InputRequired(), Length(min=3, max=30)],
                            render_kw={"placeholder": "name_team"})
    team_city = StringField('Город', validators=[InputRequired()], render_kw={"placeholder": "Moscow"})
    team_affiliation = StringField('Образовательное учреждение', render_kw={"placeholder": "DonGU"})


class UsersRegister(FlaskForm):
    user_name = StringField('Никнейм', validators=[InputRequired(), Length(min=3, max=30)])
    user_email = EmailField('Почта', validators=[InputRequired(), Email()])
