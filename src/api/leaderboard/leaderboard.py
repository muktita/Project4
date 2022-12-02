from quart import Quart, request, Blueprint, abort, g
import random
import dataclasses
import uuid
from api.util.util import CORRECT_WORD_BANK, parse_game, process_guess, validate_guess
from api.util.util import _get_db as _getdb
from api.util.Classes import Guess, Game, User
from quart_schema import validate_request, validate_headers
import logging


app_leaderboard = Blueprint('app_leaderboard', __name__)
logger = logging.getLogger('leaderboard')