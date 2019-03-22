# Kaffee-o-bot

## todo

### SerialConnection
- add Container for serial connection
- Durchreichen des USB Ports

## Notizen

https://www.revsys.com/tidbits/celery-and-django-and-docker-oh-my/

- Docker/docker-compose durchreichen von usb ports


## Installation

.env Datei erstellen

```
APP_SETTINGS=
FLASK_APP=
FLASK_ENV=
POSTGRES_USER=
POSTGRES_PW=
REDIS_PW=
DATABASE=
SECRET_KEY=
JWT_SECRET=

```

<code> mkdir data </code>


- Secret Key herstellen zb. über die python shell

<code>
import secrets

secrets.token_hex(32)
</code>

Anschließend Key rauskopieren und in .env Datei einfügen

- Change Titel in client/public/index.html
