from uuid import UUID
#from app.api.models.user import User
#from app.api.models.coffee_hist import CoffeeHistory
from datetime import datetime

def str2uuid(string):
    return UUID(string)

"""def coffee2history(user, betrag):

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
"""
