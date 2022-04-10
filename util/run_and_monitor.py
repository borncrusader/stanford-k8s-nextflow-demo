#!/usr/bin/env python3

from flask import Flask
import subprocess
import sys
import threading

app = Flask(__name__)

status_txt = 'NOT STARTED'
error_txt = '<nil>'


@app.route('/status')
def status():
    return 'status: {}; error: {}'.format(status_txt, error_txt)


@app.route('/restart')
def restart():
    if status_txt == 'NOT STARTED' or status_txt.startswith('CRASHED') or status_txt == 'DONE':
        x = threading.Thread(target=run)
        x.start()
    else:
        print('Already running')


def run():
    global status_txt
    global error_txt

    if len(sys.argv) < 2:
        error_txt = 'need an argument to start running'
        return
    
    status_txt = 'STARTED'
    
    try:
        for arg in sys.argv[1:]:
            status_txt = 'RUNNING {}'.format(arg)
        
            subprocess.run(arg, shell=True, check=True)

        status_txt = 'DONE'
        error_txt = '<nil>'
    except Exception as e:
        error_txt = str(e)
        status_txt = 'CRASHED: {}'.format(e)


# start the script automatically
if __name__ == '__main__':
    print('Starting thread')

    x = threading.Thread(target=run)
    x.start()

    app.run()
