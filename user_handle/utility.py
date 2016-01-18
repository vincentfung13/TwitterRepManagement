from user_handle.models import UserEntity
from django.contrib.auth.models import User
from django.http import HttpResponse
import json

# Return true if a username has been registered before and false otherwise
def check_exist(username, email):
    try:
        User.objects.get(username=username)
        User.objects.get(email=email)
        return True
    except User.DoesNotExist:
        return False


# Create a new user in the database
def save_user(username, password, email):
    try:
        user = User.objects.create_user(username, email, password)
    except Exception as e:
        return None, str(e)
    return user


# Add an entity to interest list
# TODO: improve database usage
def add_interested(user, entity):
    # Unique pair issue is handled by DBMS
    UserEntity.objects.create(user=user, entity=entity)


# Remove entity from interest list:
# TODO: improve database usage
def remove_entity(user, entity):
    UserEntity.objects.get(user=user, entity=entity).delete()


def json_response(ret, data="", msg=""):
    resp = {"msg": msg, "ret": ret, "data": data}
    return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")
