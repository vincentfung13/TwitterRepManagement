from user_hanlde.models import UserEntity
from django.contrib.auth.models import User


# Return true if a username has been registered before and false otherwise
def check_exist(username):
    pass


# Create a new user in the database
def save_user(username, password, email):
    pass


# Add an entity that the user is interested in
def add_interested(username, entity):
    pass
