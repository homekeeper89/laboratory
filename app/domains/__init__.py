from flask import Blueprint

main_api: Blueprint = Blueprint("main_api", __name__, url_prefix="/api")

from .user.view import *
from .running import socket_handler
