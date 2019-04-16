import smtplib
from email.message import EmailMessage
from app.utils import coffee2history
from app.api.user.models import User, CoffeeHistory
from app.api.system.models import SystemSetting

from celery import shared_task

@shared_task
def create_invoice(user_id, time):
    sysSetting = SystemSetting.query.first()
    user = User.find_by_id(user_id)
    email = EmailMessage()

    email['Subject'] = "Kaffee-Rechnung für {vorname}".format(vorname=user.vorname)
    email['From'] = sysSetting.system_email
    email['To'] = user.email

    betrag = user.coffee_count * sysSetting.coffee_price

    email_body = """
    Hallo lieber {vorname},\n
    \n
    dies ist deine Rechnung für deine getrunkenen Kaffees. \n
    \n
    Anzahl Kaffees: {anzahl_kaffees} \n
    Betrag: {betrag} € \n
    \n
    Ich werde das Geld am {datum} abholen. \n
    \n
    Dein Inkasso-Kaffee

    """.format(
        vorname=user.vorname,
        anzahl_kaffees=user.coffee_count,
        betrag=betrag,
        datum=timedelta(days=time).strftime('%a, %d, %B, %Y')
    )

    email.set_content(email_body)

    s = smtplib.SMTP(host=sysSetting.smtp_host, port=sysSetting.smtp_port)
    if sysSetting.email_tls:
        s.starttls()
        s.login(sysSetting.system_email, sysSetting.email_password)

        try:
            s.send_message(email)
            s.quit()
            if coffee2history(user, betrag):
                user.coffee_count = 0
                user.save()
            else:
                pass

        except:
            print("Es wurde ein Fehler festgestellt. Email konnte nicht gesendet werden.")


    else:
        s.login(sysSetting.system_email, sysSetting.email_password)

        try:
            s.send_message(email)
            s.quit()
            if coffee2history(user, betrag):
                user.coffee_count = 0
                user.save()
        except:
            print("Es wurde ein Fehler festgestellt. Email konnte nicht gesendet werden.")
