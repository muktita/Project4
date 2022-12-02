BEGIN TRANSACTION;
PRAGMA foreign_keys=ON;
DROP TABLE IF EXISTS users;
CREATE TABLE users(
    user_id VARCHAR PRIMARY KEY NOT NULL,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    UNIQUE(username)
);

CREATE INDEX username_idx ON users(username COLLATE NOCASE);

COMMIT;
