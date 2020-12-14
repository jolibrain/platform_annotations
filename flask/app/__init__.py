from flask import Flask, request, send_from_directory
import errno
import os
import json
import shutil
import re
import base64

def create_app(test_config=None):

    app = Flask(__name__, static_url_path='')

    @app.route('/classification', methods=['POST'])
    def classification_task():
        """
        Classification task

        Receive HTTP POST request to move an image file to a train folder

        params:
        * targetDir: folder where the file is stored on DeepDetect Platform
        If file is stored in /opt/platform/data/client/images/ then this
        parameter is equal to */client/images/*
        * projectName: project name to use in order to save content in folder
                in use by this project. It avoids issue when same images are used
                in multiple projects
        * item: image file to process
        * filename: image filename
        * content: image base64 content
        * classname: class associated to this image, this classname will
            determine where the image will be moved. If classname is *dog*,
            then */opt/platform/data/client/images/img,jpg* will be moved
            to */opt/platform/data/client/images/train/dog/img.jpg*
        """
        data = request.data
        dataDict = json.loads(data)

        rootPath = dataDict['rootPath'] if 'rootPath' in dataDict else '/opt/platform/data'

        try:
            srcPath = os.path.join(rootPath, dataDict['targetDir'])
        except:
            return json.dumps({'success':False, 'message': 'Invalid targetDir'}), 200, {'ContentType':'application/json'}

        try:
            item = dataDict['item']
        except:
            return json.dumps({'success':False, 'message': 'Invalid item parameter'}), 200, {'ContentType':'application/json'}

        try:
            filename = item['filename']
        except:
            return json.dumps({'success':False, 'message': 'Invalid filename'}), 200, {'ContentType':'application/json'}

        try:
            classname = item['classname']
        except:
            return json.dumps({'success':False, 'message': 'Invalid classname'}), 200, {'ContentType':'application/json'}

        # projectName is an optional attribute in method parameters
        # If it exists, it's added to dstPath
        if 'projectName' in dataDict and len(dataDict['projectName']) > 0:
            projectName = dataDict['projectName']
            dstPath = os.path.join(srcPath, 'train', projectName, classname)
        else:
            dstPath = os.path.join(srcPath, 'train', classname)

        try:
            os.makedirs(dstPath)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(dstPath):
                pass
            else:
                return json.dumps({'success':False, 'message': 'Error while creating targetDir'}), 200, {'ContentType':'application/json'}

        # check content attribute in item param from http request
        if 'content' in item and item['content'] is not None:

            base64_img_bytes = item['content'].encode('utf-8')
            with open(os.path.join(dstPath, filename), 'wb') as file_to_save:
                decoded_image_data = base64.decodebytes(base64_img_bytes)
                file_to_save.write(decoded_image_data)

            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

        else:

            # Content was not sent in request, just copy original file
            # to classname folder
            if os.path.exists(os.path.join(srcPath, filename)):
                shutil.copy(
                    os.path.join(srcPath, filename),
                    os.path.join(dstPath, filename)
                )

                return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
            else:
                # Source file doesn't exist
                return json.dumps({'success':False, 'message': 'Filename doesn\'t exist'}), 200, {'ContentType':'application/json'}

    @app.route('/detection', methods=['POST'])
    def detection_task():
        """
        Detection task

        Receive HTTP POST request to create training files for detection purpose.

        params:
        * targetDir: folder where the file is stored on DeepDetect Platform
        If file is stored in /opt/platform/data/client/images/ then this
        parameter is equal to */client/images/*
        * projectName: project name to use in order to save content in folder
                in use by this project. It avoids issue when same images are used
                in multiple projects
        * item: image file to process
        * filename: image filename
        * content: image base64 content
        * regions: array of regions on the image with various classnames
            * region:
            * classname: class associated with this region
            * class_number: index of the class to be used in corresp.txt
            * xmin, ymin, xmax, ymax: coodonates of this region

        A *detection/corresp.txt* file will be created to store the region
        classname indexes in order to have the same index for each region classname
        in each image training file.

        When process, each image item will copy itself in *detection/img/[item.filename]*
        and create a new *detection/bbox/[item.filename].txt* file used in training
        with the following format:

        class_idx xmin ymin xmax ymax

        A *detection/train.txt* file will be created to store the image path with
        its associated bounding box file.

        For example, if there is a *dog* region in *client/images/dog.jpg* file with
        the following coordonates [xmin: 0, ymin: 0, xmax: 100, ymax: 100}

        * *client/images/detection/corresp.txt* will be created, with the
        following content:

        0 none
        1 dog

        * image file will be copied to *client/images/detection/img/dog.jpg*
        * txt training file will be created in *client/images/detection/bbox/dog.txt*
        with the following content:

        1 0 0 100 100

        * *client/images/detection/train.txt* will be created with the following
        content:

        /opt/platform/data/client/images/detection/img/dog.jpg /opt/platform/data/client/images/detection/bbox/dog.txt
        """
        data = request.data
        dataDict = json.loads(data)

        rootPath = dataDict['rootPath'] if 'rootPath' in dataDict else '/opt/platform/data'

        try:
            srcPath = os.path.join(rootPath, dataDict['targetDir'])
        except:
            return json.dumps({'success':False, 'message': 'Invalid targetDir'}), 200, {'ContentType':'application/json'}

        try:
            item = dataDict['item']
        except:
            return json.dumps({'success':False, 'message': 'Invalid item parameter'}), 200, {'ContentType':'application/json'}

        try:
            filename = item['filename']
        except Exception as err:
            return json.dumps({'success':False, 'message': 'Invalid filename'}), 200, {'ContentType':'application/json'}

        try:
            regions = item['regions']
        except:
            return json.dumps({'success':False, 'message': 'Invalid regions'}), 200, {'ContentType':'application/json'}

        if 'projectName' in dataDict and len(dataDict['projectName']) > 0:
            projectName = dataDict['projectName']
            detectionPath = os.path.join(srcPath, 'detection', projectName)
        else:
            detectionPath = os.path.join(srcPath, 'detection')

        bboxPath = os.path.join(detectionPath, 'bbox')
        imagePath = os.path.join(detectionPath, 'img')

        try:
            os.makedirs(bboxPath)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(bboxPath):
                pass
            else:
                return json.dumps({'success':False, 'message': 'Error while creating bboxPath'}), 200, {'ContentType':'application/json'}

        try:
            os.makedirs(imagePath)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(imagePath):
                pass
            else:
                return json.dumps({'success':False, 'message': 'Error while creating imagePath'}), 200, {'ContentType':'application/json'}

        # check content attribute in item param from http request
        if 'content' in item and item['content'] is not None:

            # Write new file in classname folder with request content
            g = open(os.path.join(imagePath, filename), "w")
            g.write(item['content'].decode('base64'))
            g.close()

        else:

            # Content was not sent in request, just copy original file
            # to the training folder
            if os.path.exists(os.path.join(srcPath, filename)):
                shutil.copy(
                    os.path.join(srcPath, filename),
                    os.path.join(imagePath, filename)
                )
            else:
                # Source file doesn't exist
                return json.dumps({'success':False, 'message': 'Filename doesn\'t exist'}), 200, {'ContentType':'application/json'}

        classDescriptionFile = os.path.join(detectionPath, 'corresp.txt')
        classDescriptions = []

        if os.path.exists(classDescriptionFile):

            # Fill classDescription with content from corresp.txt
            for line in open(classDescriptionFile):
                info = re.search(r"^(\d+)\s+(.*)$", line)
                if info:
                    classDescriptions.append({
                        'index': int(info.groups()[0]),
                        'name': str(info.groups()[1])
                    });
        else:

            # Create new corresp.txt with default 'none' class
            classDescriptions.append({
                'index': 0,
                'name': 'none'
            });
            f = open(classDescriptionFile, 'w')
            f.write("0 none\n")
            f.close()

        print(classDescriptions)

        # For each region, add class_number attribute
        # that can be found in class description file
        # WARNING: index begins at 1
        for region in regions:

            # When not specified, use classDescription to fill class_number
            if 'class_number' not in region:
                try:
                    region['class_number'] = [d['name'] for d in classDescriptions].index(region['classname'])
                except:
                    region['class_number'] = len(classDescriptions)

            # when unknown, append classname to class description
            if region['classname'] not in [d['name'] for d in classDescriptions]:
                classDescriptions.append({
                    'index': region['class_number'],
                    'name': region['classname']
                })
        print(regions)

        # create bbox file
        basename, file_extension = os.path.splitext(filename)
        bboxFile = os.path.join(bboxPath, basename + '.txt')

        # write regions to file
        with open(bboxFile, 'w') as f:
            for region in regions:
                f.write("{0} {1} {2} {3} {4}\n".format(
                    int(region['class_number']),
                    int(region['xmin']),
                    int(region['ymin']),
                    int(region['xmax']),
                    int(region['ymax'])
                ))

        # write train file
        trainFile = os.path.join(detectionPath, 'train.txt')
        line = "%s %s" % (os.path.join(imagePath, filename), bboxFile)
        appendToTrain = False

        # Check if train.txt file exists and if it contains the line to be added
        if os.path.exists(trainFile):
            with open(trainFile, 'r') as f:
                appendToTrain = not line in [l.rstrip() for l in f]

        # Write line to train.txt file
        if not os.path.exists(trainFile) or appendToTrain:
            with open(trainFile, 'a') as f:
                f.write(line + "\n")

        # write class descriptions to corresp.txt
        with open(classDescriptionFile, 'w') as f:
            for description in sorted(classDescriptions, key=lambda item: item['index']):
                f.write("%i %s\n" % (description['index'], description['name']))

        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    return app
