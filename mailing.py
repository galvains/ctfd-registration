import os
import json
import time
import argparse

from mailing_utils import send_email
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


parser = argparse.ArgumentParser()
parser.add_argument("--debug", default=1, type=int, help="Debug mode variable.")
args = parser.parse_args()


def load_from_json() -> dict:
    with open('passwrd.json', 'r') as f:
        data = json.load(f)
    return data


def sender(data: dict) -> None:
    left_users = len(data)
    print(f"===USERS_COUNT: {left_users}===\n====Start mailing====")
    for email, values in data.items():

        username = values[1]
        password = values[2]
        time.sleep(0.3)

        try:
            if args.debug:
                print(f"Left users: {left_users}")
                left_users -= 1
            else:

                context = {'username': username, 'password': password}
                send_email(recipient=email, context=context, selection=False)

                print(f'Left users: {left_users}')
                left_users -= 1

        except Exception as __ex:
            print(__ex)
    print('===Mailing succeeded!===')


def main() -> None:
    from_json = load_from_json()
    sender(from_json)


if __name__ == '__main__':
    main()
