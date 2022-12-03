BEGIN TRANSACTION;
INSERT INTO games(game_id, user_id, username, word) VALUES('g1', '123abc', 'user1', 'abbey'); --double letter example
INSERT INTO games(game_id, user_id, username, word) VALUES('g2', '123abc','user1', 'crane'); --second game added. 
COMMIT;