from allauthdjango.apps.authentication.models import User
import random


class Utils:
    @staticmethod
    def create_username(first_name="", last_name=""):
        username = f"{first_name}.{last_name}"
        user = User.objects.filter(username=username).first()
        if user:
            return user.username+str(random.randrange(1, 1000))
        else:
            return username
