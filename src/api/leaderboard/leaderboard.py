import socket
import time
import httpx
from quart import Quart, request, Blueprint, abort, g
import random
import dataclasses
import uuid

import redis
from api.util.util import CORRECT_WORD_BANK, parse_game, process_guess, validate_guess
from api.util.util import _get_redis
from api.util.Classes import Guess, Game, User, LeaderboardGame
from quart_schema import validate_request, validate_headers
import logging


app_leaderboard = Blueprint('app_leaderboard', __name__)
logger = logging.getLogger('leaderboard')

@app_leaderboard.route('/leaderboard/update', methods=['POST'])
@validate_request(LeaderboardGame)
def update_leaderboard(data:LeaderboardGame):
    '''
    Updates the leaderboard with a given user and the given result of the game.
    '''
    
    db = _get_redis()
    data = dataclasses.asdict(data)

    score = data['score']
    user = data['username']
    key = 'scores:' + user  #gets the key for the user's score
    try:
        db.lpush(key, score)    #adds to redis list of scores for user

        #finds average for user
        avgs = db.lrange(key, 0, -1)
        avgs = [int(x) for x in list(avgs)]

        avg = sum(avgs) / db.llen(key)

        db.zadd('leaderboard:average', {user: avg})
    
    except (redis.exceptions.RedisError, Exception) as e:
        logger.logging(e)
        return abort(500)

    return {'username': user, 'average': avg}



@app_leaderboard.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    '''
    Gets and returns the top 10 players in wordle sorted.
    '''
    db = _get_redis()
    
    try:
        top10 = db.zrevrange('leaderboard:average', 0, 9, withscores=True)

    except (redis.exceptions.RedisError, Exception) as e:
        logger.logging(e)
        abort(500)

    return {'top10': top10}

@app_leaderboard.before_serving
def register_callback():
    hostname = socket.getfqdn()
    # port = os.environ["PORT"] # unnused for now? not sure where it would be useful
    callbackURL = f"http://{hostname}/leaderboard/payload"

    data = {"url": callbackURL, "client": "leaderboard"}

    try:
        r = httpx.post(f"http://{hostname}/webhook", json=data)
        r.raise_for_status()
    except httpx.HTTPStatusError as exc:
        app_leaderboard.logger.critical(exc)
        app_leaderboard.logger.critical("Failure to Register")
        if exc.response.status_code == 502:
            app_leaderboard.logger.critical("Retrying again in 1 second")
            time.sleep(1)
            register_callback()
        else:
            app_leaderboard.logger.critical(
                f"unknown error found. response code: {exc.response.status_code}"
            )
            return
        return
    except Exception as e:
        app_leaderboard.logger.critical(e)
        app_leaderboard.logger.critical("Failure to Register")
        return

    app_leaderboard.logger.info("Successfully Registered Leaderboard Service")
    return