from flask import Blueprint

from app.controllers import UserController


user_routes = Blueprint('user_routes', __name__)
user_controller = UserController()
