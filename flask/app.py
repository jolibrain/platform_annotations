from flask import Flask, request
import errno
import os
import json
import shutil

app = Flask(__name__)

@app.route("/")
def hello():
    return "Annotation tool"

@app.route('/classification', methods=['POST'])
def classification_task():

    data = request.data
    dataDict = json.loads(data)

    dataPath = dataDict['targetDir'].decode('utf-8').lstrip('/')
    filename = dataDict['item']['filename'].decode('utf-8')
    classname = dataDict['item']['classname'].decode('utf-8')

    srcPath = os.path.join(u'/opt/platform/data', dataPath)
    dstPath = os.path.join(srcPath, 'train', classname)

    app.logger.warning(srcPath)
    app.logger.warning(dstPath)
    app.logger.warning(os.path.join(srcPath, filename))
    app.logger.warning(os.path.join(dstPath, filename))

    try:
        os.makedirs(dstPath)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dstPath):
            pass
        else:
            raise

    shutil.copy(
        os.path.join(srcPath, filename),
        os.path.join(dstPath, filename)
    )

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/detection', methods=['POST'])
def detection_task():
    data = request.data
    dataDict = json.loads(data)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

app.run(host='0.0.0.0', debug=True)
