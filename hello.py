from flask import Flask
import pickledb
import git, os, shutil
import csv

app = Flask(__name__)

DIR_NAME = "sourcedir"
REMOTE_URL = "ssh://git@git.priv.blablacar.net:7999/android/app-android-v3.git"
BRANCH = "develop"

DB_CLAZZ = pickledb.load('clazz.db', False)
DB_TEST = pickledb.load('test.db', False)


# initial value is old enough
# this acts as a watermark
lastcommit="2df56d7445f"


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/tests/<string:commit>', methods=['GET'])
def tests(commit):
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

    commits = list(repo.iter_commits('%s..%s' %(lastcommit,commit)))
    for item in commits:
        print item 
        print item.hexshi

    # update lastcommit
    lastcommit = commit

    return 'Fetching the tests to run for commit %s' % commit 

@app.route('/add', methods=['GET'])
def provideDBs():
    saveClazz()
    saveTests()
    return "Added"

def saveClazz():
    with open('appClass.csv', 'rb') as csvfile:
        clazzReader = csv.reader(csvfile, delimiter=',')
        for row in clazzReader:
            putClazz(row[0], row[1])

def saveTests():
    with open('testFile.csv', 'rb') as csvfile:
        testReader = csv.reader(csvfile, delimiter=',')
        for row in testReader:
            putTest(row[0], row[1])

def putClazz(k, v):
    values = DB_CLAZZ.get(k)
    if values:
        values.append(v)
        DB_CLAZZ.set(k, values)
    else:
        DB_CLAZZ.set(k, [v])

def putTest(k, v):
    values = DB_TEST.get(k)
    if values:
        values.append(v)
        DB_TEST.set(k, values)
    else:
        DB_TEST.set(k, [v])

