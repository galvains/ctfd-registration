import os

from flask import Flask, flash, render_template, send_from_directory, request, url_for, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from src.database import Base, engine
from src.forms import UserRegister, TeamRegister, JoinTeam, UserLogin
from src.teams.dao import db_create_team, db_join_team, db_team_exists
from src.users.dao import db_register_user, db_get_user
from src.users.models import UserLogin as Auth
from src.utils import verify_hcaptcha, valid_symbols, verify_password, valid_telegram_tag, valid_age, send_email
from src.config import get_secret_key

SECRET_KEY = get_secret_key()

app = Flask("tournament", template_folder="src/templates", static_folder="src/static")
app.secret_key = SECRET_KEY

login_manager = LoginManager(app)
login_manager.login_view = "login"

Base.metadata.create_all(engine)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/success')
@login_required
def success():
    context = {
        'subject': 'Успех',
        'title': 'Успех'
    }
    return render_template('success.html',
                           message=f'Ты в команде! Письмо с инструкцией отправлено на почту.', context=context)


@app.errorhandler(404)
def page_not_found(e):
    context = {
        'subject': '',
        'title': '404'
    }
    return render_template('error.html', message='Страница не найдена', context=context), 404


@app.errorhandler(403)
def page_not_found(e):
    context = {
        'subject': 'Ошибка',
        'title': '403'
    }
    return render_template('error.html', message='Доступ запрещен', context=context), 403


@app.errorhandler(500)
def page_not_found(e):
    context = {
        'subject': 'Ошибка',
        'title': '500'
    }
    return render_template('error.html', message='Ошибка сервера', context=context), 500


@app.route('/', methods=['GET', 'POST'])
def home():
    context = {
        'subject': 'Название события',
        'title': 'Событие'
    }
    return render_template('home.html', message=f"Описание события", context=context)


@login_manager.user_loader
def load_user(user_id):
    user_login = Auth()
    return user_login.fromDB(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    logout_user()

    form = UserLogin()
    context = {
        'subject': 'Вход',
        'title': 'Логин'
    }
    if request.method == "POST":
        user = db_get_user(email=form.email.data)

        if user and verify_password(form.password.data, user.password):
            user_login = Auth().create(user)
            login_user(user_login)
            return redirect(url_for('home'))
        flash("Неверный логин или пароль.")
    return render_template("login.html", form=form, context=context)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    logout_user()

    form = UserRegister()
    context = {
        'subject': 'Регистрация',
        'title': 'Регистрация',
    }

    captcha = request.form.get("g-recaptcha-response")

    if form.validate_on_submit():

        if not valid_telegram_tag(form.website.data):
            flash('Неверный формат тега.')
            return render_template('register.html', form=form, context=context)

        if not valid_symbols(form.credentials.data):
            flash("Введите корректные символы (поле ввода может содержать только буквы, цифры, и символы @.+-_)")
            return render_template('register.html', form=form, context=context)

        if not valid_age(form.age.data):
            flash('Неверный формат возраста.')
            return render_template('register.html', form=form, context=context)

        if not verify_hcaptcha(captcha):
            flash("Пройдите капчу.")
            return render_template('register.html', form=form, context=context)

        else:
            new_user = db_register_user(
                credentials=form.credentials.data,
                email=form.email.data,
                website=form.website.data,
                age=form.age.data,
                password=form.password.data
            )

            if new_user:
                user_login = Auth().create(new_user)
                login_user(user_login)
                return redirect(url_for('change_team'))

    return render_template('register.html', form=form, context=context)


@app.route('/team', methods=['GET'])
@login_required
def change_team():
    context = {
        'subject': 'Команда',
        'title': 'Команда'
    }

    return render_template('change_team.html',
                           message=f"Чтобы принять участие в событии, вы должны присоединиться к команде или создать ее.",
                           context=context)


@app.route('/team/join', methods=["GET", "POST"])
@login_required
def join_team():
    form = JoinTeam()

    context = {
        'subject': 'Команда',
        'title': 'Команда'
    }

    if form.validate_on_submit():
        success_join_team = db_join_team(
            current_user_id=current_user.get_id(),
            team_name=form.team_name.data,
            team_pwd=form.password.data
        )
        if success_join_team is True:
            context = {
                "username": current_user.get_username(),
                "team_name": form.team_name.data
            }
            send_email(recipient=current_user.get_email(), context=context)

            return redirect(url_for('success'))
        elif success_join_team is False:
            flash("Неверное имя команды или пароль.")
        elif success_join_team == "size_error":
            flash("Максимальное кол-во участников достигнуто.")

    return render_template('join_team.html', form=form, context=context)


@app.route('/team/create', methods=['GET', 'POST'])
@login_required
def create_team():
    form = TeamRegister()

    context = {
        'subject': 'Команда',
        'title': 'Команда'
    }

    captcha = request.form.get("g-recaptcha-response")

    if form.validate_on_submit():
        result_team_name = valid_symbols(form.team_name.data)
        result_team_city = valid_symbols(form.team_city.data)
        result_team_affiliation = valid_symbols(form.team_affiliation.data)

        if not (result_team_city and result_team_name and result_team_affiliation):
            flash("Введите корректные символы (поле ввода может содержать только буквы, цифры, и символы @.+-_)")
            return render_template('create_team.html', form=form, context=context)

        if not verify_hcaptcha(captcha):
            flash("Пройдите капчу.")
            return render_template('create_team.html', form=form, context=context)

        if db_team_exists(form.team_name.data):
            flash("Команда с таким именем уже существует.")
            return render_template('create_team.html', form=form, context=context)

        new_team = db_create_team(
            team_name=form.team_name.data,
            team_city=form.team_city.data,
            team_affiliation=form.team_affiliation.data,
            password=form.password.data,
            current_user_id=current_user.get_id()
        )

        if new_team:

            context = {
                "username": current_user.get_username(),
                "team_name": form.team_name.data
            }
            send_email(recipient=current_user.get_email(), context=context)

            return redirect(url_for('success'))
        else:
            flash("Ошибка при создании команды. Пожалуйста, попробуйте снова.")

    return render_template('create_team.html', form=form, context=context)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
