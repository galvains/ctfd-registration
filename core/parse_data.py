import json
from models import engine, session_factory, Base, Pages

Base.metadata.create_all(engine)


def load_from_db() -> dict:
    import_data = dict()

    with session_factory() as session:
        for u in session.query(Pages).all():
            import_data[u.email] = [u.full_name, u.username, u.data]
    return import_data


def write_to_json(import_data: dict) -> None:
    with open('passwrd.json', 'w') as f:
        json.dump(import_data, f, indent=4, ensure_ascii=False)


def main() -> None:
    from_db = load_from_db()
    write_to_json(from_db)


if __name__ == '__main__':
    main()
