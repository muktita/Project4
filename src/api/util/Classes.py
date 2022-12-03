import dataclasses

@dataclasses.dataclass
class Guess:
    game_id: str
    guess: str

@dataclasses.dataclass
class User:
    user_id: str
    username: str

@dataclasses.dataclass
class Game:
    game_id: str
    user_id: str
    guesses_rem: int
    word: str
    guesses: str

@dataclasses.dataclass
class UserAuth:
    username: str
    password: str

@dataclasses.dataclass
class LeaderboardGame:
    username: str
    score: int