from uuid import UUID
from datetime import datetime

from app.api.user.models import CoffeeHistory

def str2uuid(string):
    return UUID(string)

def coffee2history(user, betrag):

    user_hist = user.coffee_hist

    hist = CoffeeHistory(user.coffee_count, betrag)
    user_hist.append(hist)

    try:
        user.save()
        print("CoffeeHistory wurde geupdatet.")
        return True
    except:
        print("Es ist ein Fehler festgestellt worden.")
        return False
