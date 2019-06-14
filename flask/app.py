from flask import Flask, request, send_from_directory
import errno
import os
import json
import shutil

app = Flask(__name__, static_url_path='')

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

    dataPath = dataDict['targetDir'].decode('utf-8').lstrip('/')
    filename = dataDict['item']['filename'].decode('utf-8')
    regions = dataDict['item']['regions']

    srcPath = os.path.join(u'/opt/platform/data', dataPath)

    bboxPath = os.path.join(srcPath, 'detection', 'bbox')
    imagePath = os.path.join(srcPath, 'detection', 'img')

    try:
        os.makedirs(bboxPath)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(bboxPath):
            pass
        else:
            raise

    try:
        os.makedirs(imagePath)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(imagePath):
            pass
        else:
            raise

    # copy image to detection image folder
    shutil.copy(
        os.path.join(srcPath, filename),
        os.path.join(imagePath, filename)
    )

    classDescriptionFile = os.path.join(srcPath, 'deepdetect_classes.txt')

    # File doesn't exist, create it
    if os.path.isfile(classDescriptionFile) == False:
        with open(classDescriptionFile, 'a'):
            os.utime(fname, times)

    f = open(classDescriptionFile, 'r')
    classDescriptions = f.readlines()
    f.close()

    # For each region, add class_number attribute
    # that can be found in class description file
    # WARNING: index begins at 1
    for region in regions:
        classname = region['classname']

        if region['classname'] not in classDescriptions:
            classDescriptions.append(classname)

        region['class_number'] = classDescriptions.index(classname) + 1


    # create bbox file
    basename, file_extension = os.path.splitext(filename)
    with open(os.path.join(bboxPath, basename + '.txt'), 'w') as f:
        for region in regions:
              f.write("%s $i %i %i %i\n" % (
                  region['class_number'],
                  int(region['xmin']),
                  int(region['ymin']),
                  int(region['xmax']),
                  int(region['ymax'])
              ))

    # copy image file
    shutil.copy(
        os.path.join(srcPath, filename),
        os.path.join(dstPath, filename)
    )

    # write class description file
    with open(classDescriptionFile, 'w') as f:
        for item in classDescriptions:
            f.write("%s\n" % item)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

app.run(host='0.0.0.0', debug=True)
