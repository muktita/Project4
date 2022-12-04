import os
import shutil

#Creates necessary file structure for the SQLite databases
#used for replication.  Must be called before starting program.

BASE = './database/dbs/'
FOLDERS = ['primary', 'secondary', 'tertiary']


if __name__ == '__main__':
    #makes base path
    if not os.path.exists(BASE):
        os.mkdir(BASE)
        print('created dir: ' + BASE)

    #makes games for database folder
    gamespath = BASE + 'games/'
    if not os.path.exists(gamespath):
        os.mkdir(gamespath)
        print('created dir: ', gamespath)

    #removes existing folders
    print('removing old directories if they exist...')
    for folder in FOLDERS:
        shutil.rmtree(gamespath + folder, ignore_errors=True)
    
    #adds folders
    for folder in FOLDERS:
        os.mkdir(gamespath + folder)
        print('created dir: ', gamespath + folder)
        os.mkdir(gamespath + folder + '/mount')
        print('created dir: ', gamespath + folder + '/mount')
        os.mkdir(gamespath + folder + '/data')
        print('created dir: ', gamespath + folder + '/data')

    #adds the users database folder
    userspath = BASE + 'users/'
    if not os.path.exists(userspath):
        os.mkdir(userspath)
        print('created dir: ', userspath)

    #adds redis directory to save to disk.
    try:
        os.mkdir(BASE + 'redis')
        print('created dir: ', BASE + 'redis')
    except Exception as e:
        pass