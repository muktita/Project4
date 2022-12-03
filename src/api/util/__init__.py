from asyncio import base_events
from itertools import cycle
from api.util.util import CORRECT_WORD_BANK, VALID_WORD_BANK, _read_jsonfile, _load_toml_dbs

_base_path = './api/util/'

CORRECT_WORD_BANK += _read_jsonfile(_base_path + 'correct.json')
VALID_WORD_BANK += _read_jsonfile(_base_path + 'valid.json')

#GAME_REPLICAS = cycle(_load_toml_dbs('./config/config.toml')['DATABASE']['URL_GAMES_REPLICAS'])
#USER_REPLICAS = cycle(_load_toml_dbs('./config/config.toml')['DATABASE']['URL_USERS_REPLICAS'])