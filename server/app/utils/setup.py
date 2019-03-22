import os
import secrets


def create_env_file():
    prompt = "> "

    print("APP_SETTINGS= ? ex. production, development, testing, staging")
    APP_SETTINGS = input(prompt)

    print("FLASK_APP= ? ex. run.py")
    FLASK_APP = input(prompt)

    print("FLASK_ENV= ? ex. development, production")
    FLASK_ENV = input(prompt)

    print("POSTGRES_USER= ?")
    POSTGRES_USER = input(prompt)

    print("POSTGRES_PW= ?")
    POSTGRES_PW = input(prompt)

    print("DATABASE= ?")
    DATABASE = input(prompt)

    print("REDIS_PW= ?")
    REDIS_PW = input(prompt)

    print("BROKER_USER= ?")
    BROKER_USER = input(prompt)
    print("BROKER_PW= ?")
    BROKER_PW = input(prompt)

    SECRET_KEY = secrets.token_hex(32)
    JWT_SECRET = secrets.token_hex(32)

    env_list = [
        "APP_SETTINGS={}".format(APP_SETTINGS),
        "FLASK_ENV={}".format(FLASK_ENV),
        "FLASK_APP={}".format(FLASK_APP),
        "POSTGRES_USER={}".format(POSTGRES_USER),
        "POSTGRES_PW={}".format(POSTGRES_PW),
        "DATABASE={}".format(DATABASE),
        "REDIS_PW={}".format(REDIS_PW),
        "BROKER_USER={}".format(BROKER_USER),
        "BROKER_PW={}".format(BROKER_PW),
        "SECRET_KEY={}".format(SECRET_KEY),
        "JWT_SECRET={}".format(JWT_SECRET)

    ]

    with open(os.path.join('../../..', '.env'), 'a') as f:
        [ f.write(env_var) for env_var in env_list ]
        f.close()


def main():
    create_env_file()


if __name__ == '__main__':
    main()
