import os
import shutil

#Creates necessary file structure for the SQLite databases
#used for replication.  Must be called before starting program.

BASE = './database/dbs/'
FOLDERS = ['primary', 'secondary', 'tertiary']


if __name__ == '__main__':
    if not os.path.exists(BASE):
        os.mkdir(BASE)
        print('created dir: ', BASE)

    #removes existing folders
    print('removing old directories if they exists...')
    for folder in FOLDERS:
        shutil.rmtree(BASE + folder, ignore_errors=True)
    
    #adds folders
    for folder in FOLDERS:
        os.mkdir(BASE + folder)
        print('created dir: ', BASE + folder)
        os.mkdir(BASE + folder + '/mount')
        print('created dir: ', BASE + folder + '/mount')
        os.mkdir(BASE + folder + '/data')
        print('created dir: ', BASE + folder + '/data')

    #adds redis directory to save to disk.
    try:
        os.mkdir(BASE + 'redis')
        print('created dir: ', BASE + 'redis')
    except Exception as e:
        pass