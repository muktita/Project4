BEGIN TRANSACTION;
PRAGMA foreign_keys=ON;
DROP TABLE IF EXISTS games;
CREATE TABLE games(
    game_id VARCHAR PRIMARY KEY NOT NULL,
    user_id VARCHAR NOT NULL,
    username VARCHAR NOT NULL,
    guesses_rem INTEGER DEFAULT 6 NOT NULL,
    word VARCHAR NOT NULL,
    finished INTEGER DEFAULT 0 NOT NULL
);

DROP TABLE IF EXISTS guesses;
CREATE TABLE guesses(
    guess_id INTEGER PRIMARY KEY NOT NULL,
    game_id VARCHAR NOT NULL,
    guess VARCHAR NOT NULL,
    guess_num INTEGER NOT NULL,
    FOREIGN KEY(game_id) REFERENCES games(game_id)
);

CREATE INDEX games_idx ON games(finished, user_id COLLATE NOCASE);
CREATE INDEX guess_idx ON guesses(game_id, guess_num);

COMMIT;
