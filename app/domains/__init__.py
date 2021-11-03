from flask import Blueprint
from app.core.database.models import (
    User,
    Account,
    RunningConfig,
    RunningParticipant,
    Running,
    UserRunningHistory,
)

main_api: Blueprint = Blueprint("main_api", __name__, url_prefix="/api")

from .user.view import *
from .running import socket_handler
from .running.view import *
