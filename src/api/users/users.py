import dataclasses
import sqlite3
from quart import request, abort, Blueprint
from quart_schema import validate_request
import uuid
from api.util.util import _get_db as _getdb
from api.util.Classes import UserAuth
import dataclasses
import logging


app_users = Blueprint('app_users', __name__)
logger = logging.getLogger('users')

async def _get_db():
    db, _ = await _getdb('users')
    return db


@app_users.route("/register", methods=['POST'])
@validate_request(UserAuth)
async def register(data:UserAuth):
    form = dataclasses.asdict(data)
    user = {}
    user["user_id"] = str(uuid.uuid1())
    user["password"] = form['password']
    user['username'] = form['username']

    #aborts if the password or username is too short
    if len(form['password']) < 5 or len(form['username']) < 5:
        abort(406, 'invalid parameter length')
    db = await _get_db()
    try:
        res = await db.execute(
            """
            INSERT INTO users(user_id, username, password)
            VALUES(:user_id,:username,:password)
            """,user
        )
    except sqlite3.IntegrityError as e:
        abort(409, "user already exists.")

    return {'user_id': user['user_id'], 'username': user['username']},201

@app_users.route("/checkPassword", methods=['GET'])
async def check():
    '''Performs simple auth to authenticate a user.'''
    username = ''
    password = ''
    if request.authorization:
        username = request.authorization.username
        password = request.authorization.password
        
    db = await _get_db()

    sql = f'SELECT * FROM users WHERE username LIKE "{username}" AND password LIKE "{password}"'
    logger.info('/checkPassword SQL: ' + sql)
    users = await db.fetch_one(sql)
    
    #if user is not None, that means a valid user was found with same credentials
    if users is not None:
        return {"authenticated" : True}
    else:
        return "invalid login", 401, {'WWW-Authenticate' : 'Basic Realm = "Login Required"'}
    

