from quart import Quart, request, Blueprint, abort, g
import random
import dataclasses
import uuid
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