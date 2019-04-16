# Kaffee-o-bot

## Entwicklungsplan

### Was ist der Kaffee-o-bot?
Beim Kaffee-o-bot handelt es sich um eine App die mit Hilfe des jeweiligen User-Keys, die Kaffee-Liste pflegt und am Ende des Monats eine Mail mit dem zu zahlenden Betrag versendet.

### Was kann ich mir jetzt darunter vorstellen?

1. Der User kann sich mit seinem Key registrieren. 
2. Nach der Registrierung kann der User sich einloggen und sieht seine eigene Übersicht des Monats. Dort hat er auch die Möglichkeit sein Profil zu bearbeiten. 
3. Eine Übersichtstabelle ist auch ohne Einloggen aufrufbar.
4. Der Administrator/Kaffeegeldeintreiber, hat eine komplette Übersicht der User und kann diese Bearbeiten.
5. Der Admin kann das System so einstellen, dass eine Mail am gewünschten/eingestellten Termin versendet wird, personlich für den jeweilgen User mit den getrunkenen Kaffees und dem Betrag der gezahlt werden soll.
6. Der Admin bekommt für die Rechnungsübersicht die Möglichkeit mit einem + und - die zu zahlenden Kaffees einzustellen und ggf welche auf den nächsten Monat zu übertragen.

### Roadmap

1. User
    - User Model
    - __User Resource__
    - UserListApi

        | Methode   | api endpoint          | Beschreibung |
        | --------  | --------              | -------- |
        | GET       | /api/v1/admin/user    | Holt sich die Liste mit allen Users   |
        | POST      | /api/v1/user/register    | Registriert einen User   |  

    - UserApi

        | Methode   | api endpoint          | Beschreibung |
        | --------  | --------              | -------- |
        | GET       | /api/v1/user          | Holt die Daten vom jeweiligen User   |
        | PATCH     | /api/v1/user          | Update der User-Daten   | 
    
    - __User Frontend__
        - *User*
            - Login/Logout
            - Home

2. System
    - SystemEinstellung Model
    - __System Resources__
    - SystemSettingApi
    
        | Methode   | api endpoint          | Beschreibung |
        | --------  | --------              | -------- |
        | GET       | /api/v1/setting       | Holt sich die Systemeinstellungen   |
        | POST      | /api/v1/setting       | Erstellt die Systemeinstellungen   |  
        | PATCH     | /api/v1/setting       | Update der Systemeinstellungen     |

    - __Einstellungen__
        - *Admin*
            - Einstellungen

3. Rechnung
    - Rechnung Model
    - __Rechnung Resources__
    - InvoiceListApi
    
        | Methode   | api endpoint          | Beschreibung |
        | --------  | --------              | -------- |
        | GET       | /api/v1/admin/invoice    | Holt sich alle Rechnungs Daten   |
        | POST      | /api/v1/admin/invoice    | Erstellt eine Task wo der User eine Mail geschickt bekommt   |  
    
    - InvoiceApi
    
        | Methode   | api endpoint          | Beschreibung |
        | --------  | --------              | -------- |
        | GET       | /api/v1/admin/invoice/<string: invoice_id>    | Holt sich Rechnungs Daten für eine Rechnung  |
        | PATCH     | /api/v1/admin/invoice/<string: invoice_id>   | Updatet die Rechnungsdaten für eine spezielle Rechnung (z.b. Bezahlt setztn )   |    
    - __Rechnungen__
        - *Admin*
            - Liste mit allen Users/Kaffee Daten
            - Liste kann bearbeitet werden, Kaffeeanzahl kann verändert werden (+/-)  für die Übernahme in den nächsten Rechnungslauf.
            - Wenn User abwesend(Urlaub), Button um den User aus der Liste zu entfernen

4. Serielle Verbindung zum Key-Reader
    - Compose-Eintrag für den Container der seriellen Verbindung
       - Durchreichen USB Port
    - Pub/Sub mit dem Broker für die Key-Registrierung
    - request.post mit dem jeweiligen Key der gelesen wurde
    - gelesenen Key-Nummern per set(input) auf eine Nummer reduzieren
    
        

## todo

### SerialConnection
- add Container for serial connection
- Durchreichen des USB Ports

### app
- RechnungApi überlegen

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
