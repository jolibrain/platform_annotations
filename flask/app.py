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
    """
    Classification task

    Receive HTTP POST request to move an image file to a train folder

    params:
        * targetDir: folder where the file is stored on DeepDetect Platform
            If file is stored in /opt/platform/data/client/images/ then this
            parameter is equal to */client/images/*
        * item: image file to process
            * filename: image filename
            * classname: class associated to this image, this classname will
                determine where the image will be moved. If classname is *dog*,
                then */opt/platform/data/client/images/img,jpg* will be moved
                to */opt/platform/data/client/images/train/dog/img.jpg*
    """
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
    """
    Detection task

    Receive HTTP POST request to create training files for detection purpose.

    params:
        * targetDir: folder where the file is stored on DeepDetect Platform
            If file is stored in /opt/platform/data/client/images/ then this
            parameter is equal to */client/images/*
        * item: image file to process
            * filename: image filename
            * regions: array of regions on the image with various classnames
                * region:
                    * classname: class associated with this region
                    * xmin, ymin, xmax, ymax: coodonates of this region

    A *deepdetect_classes.txt* file will be created to store the region
    classname indexes in order to have the same index for each region classname
    in each image training file.

    When process, each image item will copy itself in *detection/img/[item.filename]*
    and create a new *detection/bbox/[item.filename].txt* file used in training
    with the following format:

        class_idx xmin ymin xmax ymax

    For example, if there is a *dog* region in *client/images/dog.jpg* file with
    the following coordonates [xmin: 0, ymin: 0, xmax: 100, ymax: 100}

    * *client/images/detection/deepdetect_classes.txt* will be created, with the
        following content:

    dog

    * image file will be copied to *client/images/detection/img/dog.jpg*
    * txt training file will be created in *client/images/detection/bbox/dog.txt*
        with the following content:

    1 0 0 100 100
    """
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
            os.utime(classDescriptionFile, times)

    # Get existing classes from class description file
    classDescriptions = [line.rstrip() for line in open(classDescriptionFile)]

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
              f.write("{0} {1} {2} {3} {4}\n".format(
                  int(region['class_number']),
                  int(region['xmin']),
                  int(region['ymin']),
                  int(region['xmax']),
                  int(region['ymax'])
              ))

    # write class description file
    with open(classDescriptionFile, 'w') as f:
        for item in classDescriptions:
            f.write("%s\n" % item)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

app.run(host='0.0.0.0', debug=True)
