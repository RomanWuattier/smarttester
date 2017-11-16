from flask import Flask
import pickledb
import git, os, shutil
import csv

app = Flask(__name__)

DIR_NAME = "sourcedir"
REMOTE_URL = "ssh://git@git.priv.blablacar.net:7999/android/app-android-v3.git"
BRANCH = "develop"

# initial value is old enough
# this acts as a watermark
lastcommit="2df56d7445f"

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/tests/<string:commit>', methods=['GET'])
def tests(commit):
    # save the commit to diff against later
    lastcommit = commit

    # first, clone the project
    print 'Fetching the AndroidV3 code base'
    if os.path.isdir(DIR_NAME): 
        shutil.rmtree(DIR_NAME)

    os.mkdir(DIR_NAME) 
   
    repo = git.Repo
    repo.clone_from(REMOTE_URL, DIR_NAME, branch='develop')
        
    #repo = git.Repo.init(DIR_NAME)
    #origin = repo.create_remote('origin', REMOTE_URL)
    #origin.fetch()
    #origin.pull(origin.refs[0].remote_head)
    
    # get the diff for a given commit hash
    for commit in repo.iter_commits('develop'):
        print commit
        
    
    db = pickledb.load('test.db', False)
    db.set('key', commit) 
    value = db.get('key')

    
    # update lastcommit
    lastcommit = commit

    return 'Fetching the tests to run for commit %s' % commit 

def saveClazz():
    with open('appClass.csv', newline='') as csvfile:
        clazzReader = csv.reader(csvfile, delimiter=',')
        for row in clazzReader:
            db.set(row[1], row[2])

def saveTests():
    with open('testFile.csv', newline='') as csvfile:
        testReader = csv.reader(csvfile, delimiter=',')
        for row in testReader:
            db.set(row[1], row[2])

