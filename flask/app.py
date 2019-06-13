from flask import Flask, request
import os
import json
import shutil

app = Flask(__name__)

@app.route("/")
def hello():
    return "Annotation tool"

@app.route('/classification_task', methods=['POST'])
def classification_task():
    return request.form['vott']
    data = request.data
    dataDict = json.loads(data)
    for item in dataDict['items']:
        destPath = os.path.join(dataDict['targetDir'], '/train', item['class'])
        try:
            os.mkdir(destPath)
        except:
            pass
        shutil.copy(item['filename'], os.path.join(destPath, item['filename']))
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/detection_task', methods=['POST'])
def detection_task():
    data = request.data
    dataDict = json.loads(data)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

app.run('0.0.0.0')
