from flask import Flask, request
import os
import json
import shutil

app = Flask(__name__)

@app.route("/")
def hello():
    return "Annotation tool"

@app.route('/classification', methods=['POST'])
def classification_task():

    rootPath = '/opt/platform/data/'

    data = request.data
    dataDict = json.loads(data)

    filename = dataDict['item']['filename']
    classname = dataDict['item']['classname']

    destPath = os.path.join(rootPath, dataDict['targetDir'], 'train', classname)

    try:
        os.mkdir(destPath)
    except:
        pass

    shutil.copy(filename, os.path.join(destPath, filename))

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/detection', methods=['POST'])
def detection_task():
    data = request.data
    dataDict = json.loads(data)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

app.run('0.0.0.0')
