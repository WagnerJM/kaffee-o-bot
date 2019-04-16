
class ResourceMixin(object):

    def check_user(self, role=None, id=None, User_class=None):
        if not User_class.check_role(id):
            return {
                "msg": "Sie haben nicht die nötigen Rechte."
            }, 403
    
    def save_or_except(self, obj_instance):
        try:
            obj_instance.save()
            return {
                "msg": "Das Speichern war erfolgreich."
            }, 200
        except:
            return {
                "msg": "Etwas ist beim Speichern schief gelaufen."
            }, 500
