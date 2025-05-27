import time
import datetime
import os
import sys
import uuid
import traceback

global logDir, name
logDir = os.path.join(os.path.expanduser('~'), 'mlogs')
name = 'log'

MAXOUTPUTLENGTH = 500

def setName(newname):
    global name
    name = newname

def mdate():
    return datetime.datetime.now().strftime("%Y%m%d")

def mnow():
    return datetime.datetime.now().strftime("%H:%M:%S")

def mlogPath():
    global name
    return os.path.join(logDir, '{}_{}.log'.format(name, mdate()))

def generateHelperFile():
    helperPath = os.path.join(mlogPath(), '{}.log'.format(uuid.uuid4()))
    with open(helperPath, 'w') as f:
        pass
    return helperPath

def checkAndSetLog():
    global name
    path = mlogPath()
    if not os.path.exists(logDir):
        os.mkdir(logDir)
    if not os.path.exists(path):
        with open(path, 'w') as f:
            print('Starting {}! check logs at:\n\t{}'.format(name, path))
    return path

def logJob(func, *args, **kwargs):
    path = checkAndSetLog()
    retVal = "Failure...? -> check diagnoser.py > logJob()"
    try:
        retVal = func(*args, **kwargs)
    except Exception as e:
        retVal = 'An exception occured:\n{}'.format(traceback.format_exc())
    with open(path, 'a') as f:
        f.write('|{}|\tRan {}\n'.format(mnow(), func.__name__))
        retVal = repr(retVal)
        if len(retVal) > MAXOUTPUTLENGTH:
            toShow = retVal[:MAXOUTPUTLENGTH]
            f.write('\t\t-> {}\n'.format(toShow))
            helperPath = generateHelperFile()
            with open(helperPath, 'a') as hf:
                hf.write(retVal)
                hf.write('\n')
            f.write('...Output truncated. Full output at {}'.format(helperPath))
        else:
            f.write('\t\t-> {}\n'.format(retVal))

def logDuration(func, *args, **kwargs):
    path = checkAndSetLog()
    retVal = "Failure...? -> check diagnoser.py > logDuration() [retVal not set]"
    timeElapsed = -1
    try:
        startTime = time.time()
        retVal = func(*args, **kwargs)
        timeElapsed = time.time() - startTime
    except Exception as e:
        retVal = 'An exception occured:\n{}'.format(traceback.format_exc())
    with open(path, 'a') as f:
        f.write('|{}|\tRan {}\n'.format(mnow(), func.__name__))
        retVal = repr(retVal)
        if len(retVal) > MAXOUTPUTLENGTH:
            toShow = retVal[:MAXOUTPUTLENGTH]
            f.write('\t\t-> {}\n'.format(toShow))
            helperPath = generateHelperFile()
            with open(helperPath, 'a') as hf:
                hf.write(retVal)
                hf.write('\n')
            f.write('...Output truncated. Full output at {}'.format(helperPath))
        else:
            f.write('\t\t-> {}\n'.format(retVal))
        if timeElapsed == -1:
            f.write('Failure...? -> check diagnoser.py > logDuration() [timeElapsed = -1?]\n')
        else:
            f.write('|{}|\t Process took {}s\n'.format(mnow(), timeElapsed))
            f.write('\t\t>> which is {}min\n'.format(timeElapsed/60))
            f.write('\t\t>> which is {}hrs\n'.format(timeElapsed/60/60))

def CrashWithLog(textToShow):
    path = checkAndSetLog()
    with open(path, 'a') as f:
        f.write('|{}| We got a crash. here is the text\n')
        f.write('>>')
        f.write(textToShow)
        f.write('\n')
    sys.exit(1)