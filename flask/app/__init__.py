from flask import Flask, request, send_from_directory
import errno
import os
import json
import shutil
import re

def create_app(test_config=None):

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
		* content: image base64 content
		* classname: class associated to this image, this classname will
		    determine where the image will be moved. If classname is *dog*,
		    then */opt/platform/data/client/images/img,jpg* will be moved
		    to */opt/platform/data/client/images/train/dog/img.jpg*
	"""
	data = request.data
	dataDict = json.loads(data)

	dataPath = dataDict['targetDir'].decode('utf-8').lstrip('/')

	item = dataDict['item']
	filename = item['filename'].decode('utf-8')
	classname = item['classname'].decode('utf-8')

	srcPath = os.path.join(u'/opt/platform/data', dataPath)
	dstPath = os.path.join(srcPath, 'train', classname)

	try:
	    os.makedirs(dstPath)
	except OSError as exc:
	    if exc.errno == errno.EEXIST and os.path.isdir(dstPath):
		pass
	    else:
		raise

	# check content attribute in item param from http request
	if 'content' in item and item['content'] is not None:

            # Write new file in classname folder with request content
            g = open(os.path.join(dstPath, filename), "w")
            g.write(item['content'].decode('base64'))
            g.close()

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
		return json.dumps({'success':False}), 200, {'ContentType':'application/json'}

    @app.route('/detection', methods=['POST'])
    def detection_task():
	"""
	Detection task

	Receive HTTP POST request to create training files for detection purpose.

	params:
	    * tags: array of tags, ordered as displayed in vott UI
	    * targetDir: folder where the file is stored on DeepDetect Platform
		If file is stored in /opt/platform/data/client/images/ then this
		parameter is equal to */client/images/*
	    * item: image file to process
		* filename: image filename
		* content: image base64 content
		* regions: array of regions on the image with various classnames
		    * region:
			* classname: class associated with this region
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

	dataPath = dataDict['targetDir'].decode('utf-8').lstrip('/')

	item = dataDict['item']
	filename = item['filename'].decode('utf-8')
	regions = item['regions']

	srcPath = os.path.join(u'/opt/platform/data', dataPath)

	detectionPath = os.path.join(srcPath, 'detection')
	bboxPath = os.path.join(detectionPath, 'bbox')
	imagePath = os.path.join(detectionPath, 'img')

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

	# check content attribute in item param from http request
	if 'content' in item and item['content'] is not None:

	    # Write new file in classname folder with request content
	    g = open(os.path.join(imagePath, filename), "w")
	    g.write(item['content'].decode('base64'))
	    g.close()

	else:

	    # Content was not sent in request, just copy original file
	    # to the training folder
	    shutil.copy(
		os.path.join(srcPath, filename),
		os.path.join(imagePath, filename)
	    )

	classDescriptionFile = os.path.join(detectionPath, 'corresp.txt')

	# create class description file from tags parameter
	if dataDict['tags'] and len(dataDict['tags']) > 0:
	    f = open(classDescriptionFile, 'w')
	    f.write("0 none\n")
	    for counter, item in enumerate(dataDict['tags']):
		f.write("%i %s\n" % (counter + 1, item))
	    f.close()

	# Get existing classes from class description file
	classDescriptions = [re.sub(r'^\d+\s+', '', line.rstrip()) for line in open(classDescriptionFile)]

	# For each region, add class_number attribute
	# that can be found in class description file
	# WARNING: index begins at 1
	for region in regions:
	    region['class_number'] = classDescriptions.index(region['classname'])

	# create bbox file
	basename, file_extension = os.path.splitext(filename)
	bboxFile = os.path.join(bboxPath, basename + '.txt')
	with open(bboxFile, 'w') as f:

	    # write head comment with used tags
	    # avoid issue with un-synchronized corresp.txt file
	    if dataDict['tags'] and len(dataDict['tags']) > 0:
		f.write("# %s\n" % ' '.join(dataDict['tags']))

	    # write regions to file
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

	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    return app
