import sqlite3
import argparse
import os

#Sqlite3 and Redis Database creation and population script.
#run with argument "-p" to populate database with a few entries.
#view populatedb.sql to see the added user and games.

BASE = './database/'
PRIMARY_BASE = 'dbs/games/primary/mount/'

def setupdb(name:str):
    dbpath = PRIMARY_BASE if name == 'games' else 'dbs/users/'
    dbname = BASE + dbpath + f'{name}.db'
    print('setting up db: ', dbname)
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    with open(BASE +'scripts/' + f'schema_{name}.sql', 'r') as file:
        data = file.read()
        cur.executescript(data)
    con.close()
    print('successfully setup db: ', dbname)

def populatedb(name:str):
    dbpath = PRIMARY_BASE if name == 'games' else 'dbs/users/'
    dbname = BASE + dbpath + f'{name}.db'
    print('populating up db: ', dbname)
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    with open(BASE +'scripts/' + f'populatedb_{name}.sql', 'r') as file:
        data = file.read()
        cur.executescript(data)
    con.close()
    print('successfully populated db: ', dbname)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action='store_true')

    parser = parser.parse_args()

    setupdb('games')
    setupdb('users')

    #deletes the leaderboard redis db on disk to reset it.
    if os.path.exists(BASE + 'dbs/' + 'leaderboard.rdb'):
        os.remove(BASE + 'dbs/' + 'leaderboard.rdb')

    if parser.p:
        populatedb('games')
        populatedb('users')