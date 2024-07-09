from flask import Blueprint
from controllers.user.userAuth import user_login, user_register

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/api/user/login', methods=['POST'])
def login():
    return user_login()

@user_routes.route('/api/user/register', methods=['POST'])
def register():
    return user_register()