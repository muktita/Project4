from quart import Quart, request, Blueprint, abort, g
import random
import dataclasses
import uuid
from api.util.util import CORRECT_WORD_BANK, parse_game, process_guess, validate_guess
from api.util.util import _get_db as _getdb
from api.util.Classes import Guess, Game, User
from quart_schema import validate_request, validate_headers
import logging


app_create = Blueprint('app_create', __name__)
logger = logging.getLogger('games')

def _get_db():
    return _getdb('games')

@app_create.route('/game/create', methods=['POST'])
@validate_headers(User)
async def create(headers:User):
    '''creates a new game for a given user.  Returns 401 if they are unauthoized to.'''
    headers = dataclasses.asdict(headers)

    user_id = str(headers['user_id'])
    username = request.authorization.username

    #gets user and validates userid
    primary, replica = await _get_db()
   
    #generates a random word and creates a new game entry in the database
    random_word = random.choice(CORRECT_WORD_BANK)
    game_id = str(uuid.uuid1())
    query = f'INSERT INTO games(game_id, user_id, username, word) VALUES("{game_id}", "{user_id}", "{username}", "{random_word}")'
    id = await primary.execute(query)    #id = gameid
    
    if id == -1:
        return abort(500)

    return {'game_id': game_id}, 201


@app_create.route('/game/list', methods=['GET'])
@validate_headers(User)
async def get_all_games(headers: User):
    '''gets a list of all the active games for a given user. If no user found, returns empty list for the games'''
    headers = dataclasses.asdict(headers)
    user_id = headers['user_id']

    username = request.authorization.username

    primary, replica = await _get_db()
    sql = f'SELECT game_id FROM games WHERE user_id LIKE "{user_id}" AND finished=0 AND username LIKE "{username}"'
    logger.info('/game/list SQL: ' + sql)
    games = await replica.fetch_all(sql)

    #converts the games found into a list of ints for the game_id
    games = [g.game_id for g in games]

    return {'game_ids': games}



@app_create.route('/game/<string:id>', methods=['GET'])
@validate_headers(User)
async def get_game(id:str, headers:User):
#async def get_game(id:int):
    '''Gets a single game give the game_id and returns the state of the game.'''
    headers = dataclasses.asdict(headers)
    game_id = id    
    user_id = headers['user_id']
    #verifies correct user is logged in and accessing resources
    username = request.authorization.username
   

    #gets db and searches for game
    primary, replica = await _get_db()
    sql = f'SELECT * FROM games WHERE game_id="{game_id}" AND user_id="{user_id}" AND username="{username}"'
    logger.info('/game/' + str(game_id) + ' get game SQL: ' + sql)
    game = await replica.fetch_one(sql)

    if not game:
        return abort(401, 'Game Not Found')
    
    #gets guesses from table
    sql = f'SELECT guess, guess_num FROM guesses WHERE game_id="{game_id}" ORDER BY guess_num ASC'
    logger.info('/game/' + str(game_id) + ' get guesses SQL: ' + sql)
    guesses = await replica.fetch_all(sql)
    if guesses:
        guesses = [g.guess for g in guesses]
    else:
        guesses = []
    
    game = Game(game.game_id, game.user_id, game.guesses_rem, game.word, guesses)
    return parse_game(game)
    


@app_create.route('/game/guess', methods=['POST'])
@validate_request(Guess)
@validate_headers(User)
async def make_guess(data:Guess, headers:User):
    '''checks and verifies that a user gives a valid guess and if so, returns the results of the guess'''
    
    #gets necessary info from the json body and headers
    headers = dataclasses.asdict(headers)
    data = dataclasses.asdict(data)
    guess = data['guess']
    game_id = str(data['game_id'])
    user_id = headers['user_id']

    username = request.authorization.username

    primary, replica = await _get_db()
    
    #gets the status of the game and returns if the game is not found
    sql = f'SELECT * FROM games WHERE game_id="{game_id}" AND user_id="{user_id}" AND finished=0 AND username="{username}"'
    logger.info('/game/guess get game SQL: ' + sql)
    game = await replica.fetch_one(sql)

    if game is None:
        return abort(401, "No game found")

    valid, correct = validate_guess(guess, game.word)
    guesses_rem = game.guesses_rem
    #if valid guess was made, decrements guesses_remaining and adds to guesses database
    if valid:
        guesses_rem -= 1
        guess_num = 6 - guesses_rem
        finished = (guesses_rem == 0 or correct)
        #updates the number of guesses remaining
        sql = f'UPDATE games SET guesses_rem={guesses_rem}, finished={finished} WHERE game_id="{game_id}"'
        logger.info('/game/guess update game state SQL: ' + sql)
        r = await primary.execute(sql)
        #adds the guess to the guesses database.
        sql = f'INSERT INTO guesses(game_id, guess, guess_num) VALUES("{game_id}", "{guess}", {guess_num})'
        logger.info('/game/guess add guess SQL: ' + sql)
        g_id = await primary.execute(sql)
        if r == -1:
            return abort(500)   #error with updating table

    result = {'game_id': game_id, 'valid': valid, 'guesses_remaining': guesses_rem}
    
    #adds optional parameters if a valid guess was made
    c_letters, m_letters = process_guess(data['guess'], game.word)
    if valid and not correct:
        result['correct_guess'] = correct
        result['correct'] = c_letters
        result['misplaced'] = m_letters
    elif valid and correct:
        result['correct_guess'] = correct
    
    return result


    







