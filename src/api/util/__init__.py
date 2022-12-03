from asyncio import base_events
from itertools import cycle
from api.util.util import CORRECT_WORD_BANK, VALID_WORD_BANK, _read_jsonfile

_base_path = './api/util/'

CORRECT_WORD_BANK += _read_jsonfile(_base_path + 'correct.json')
VALID_WORD_BANK += _read_jsonfile(_base_path + 'valid.json')

