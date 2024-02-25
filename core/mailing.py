import json
import time

from utils import send_email
from models import engine, session_factory, Base, Pages

Base.metadata.create_all(engine)


def load_from_db() -> dict:
    import_data = dict()

    with session_factory() as session:
        for u in session.query(Pages).all():
            import_data[u.email] = [u.username, u.data]
    return import_data


def write_to_json(import_data: dict) -> None:
    with open('passwrd.json', 'w') as f:
        json.dump(import_data, f, indent=4)


def load_from_json() -> dict:
    with open('passwrd.json', 'r') as f:
        data = json.load(f)
    return data


def sender(data: dict) -> None:
    for email, values in data.items():
        username = values[0]
        password = values[1]
        time.sleep(0.3)

        try:
            print(f"Данные от вашего аккаунта Quzmine:\n\n"
                  f"Username: {username}\n"
                  f"Password: {password}\n"
                  f"Ссылка для входа: https://...\n\n"
                  f"С уважением, Quizmine team.")

            # send_email(email,
            #            "Логин Quizmine",
            #            f"Данные от вашего аккаунта Quzmine:\n\n"
            #            f"Username: {username}\n"
            #            f"Password: {password}\n"
            #            f"Ссылка для входа: https://...\n\n"
            #            f"С уважением, Quizmine team."
            #            )

        except Exception as __ex:
            print(__ex)


def main() -> None:
    from_db = load_from_db()
    write_to_json(from_db)
    from_json = load_from_json()
    sender(from_json)


if __name__ == '__main__':
    main()
