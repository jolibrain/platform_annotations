import pytest
import json
import errno
import os
from shutil import copyfile
import base64
import filecmp

# Test detection task on simple image file
def test_detection(client):

    # Root for detection project
    rootPath = '/tmp/'
    targetDir = 'client/images/'
    dstFolder = os.path.join(rootPath, targetDir)

    # Create root path if not already exist
    try:
        os.makedirs(dstFolder)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dstFolder):
            pass
        else:
            raise

    # Source file
    srcFile = "tests/assets/dog.jpg"

    # Dest file
    dstFile = os.path.join(dstFolder, 'detection', 'img', 'dog.jpg')
    dstBbox = os.path.join(dstFolder, 'detection', 'bbox', 'dog.txt')
    dstCorresp = os.path.join(dstFolder, 'detection', 'corresp.txt')
    dstTrain = os.path.join(dstFolder, 'detection', 'train.txt')

    try:
        os.unlink(dstFile)
    except:
        pass

    try:
        os.unlink(dstBbox)
    except:
        pass

    try:
        os.unlink(dstCorresp)
    except:
        pass

    # verify test file doesn't already exists in project path
    assert not os.path.exists(dstFile)

    # Copy test asset inside project root path
    copyfile(srcFile, os.path.join(dstFolder, 'dog.jpg'))
    assert os.path.exists(os.path.join(dstFolder, 'dog.jpg'))

    # Create detection test parameters
    detection_data = {
        'rootPath': rootPath,
        'targetDir': targetDir,
        'item': {
            'filename': 'dog.jpg',
            'regions': [
                {
                    'classname': 'zone1',
                    'xmin': 0,
                    'xmax': 100,
                    'ymin': 0,
                    'ymax': 100
                },
                {
                    'classname': 'zone2',
                    'xmin': 0,
                    'xmax': 100,
                    'ymin': 0,
                    'ymax': 100
                }
            ]
        }
    }

    # Request flask app on detection task with test parameters
    response = client.post(
        '/detection',
        data=json.dumps(detection_data)
    )

    # Load response json
    data = json.loads(response.get_data(as_text=True))

    # Verify response
    assert data['success']
    assert os.path.exists(dstFile)
    assert os.path.exists(dstBbox)
    assert os.path.exists(dstCorresp)
    assert os.path.exists(dstTrain)

    assert filecmp.cmp(dstBbox, "tests/assets/detection/bbox.txt")
    assert filecmp.cmp(dstCorresp, "tests/assets/detection/corresp.txt")
    assert filecmp.cmp(dstTrain, "tests/assets/detection/train.txt")

    # Clean test data
    os.unlink(dstFile)
    os.unlink(dstBbox)
    os.unlink(dstCorresp)
    os.unlink(dstTrain)



# Test detection task on simple image file
def test_detection_with_project_name(client):

    # Root for detection project
    rootPath = '/tmp/'
    targetDir = 'client/images/'
    dstFolder = os.path.join(rootPath, targetDir)

    # Create root path if not already exist
    try:
        os.makedirs(dstFolder)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dstFolder):
            pass
        else:
            raise

    # Source file
    srcFile = "tests/assets/dog.jpg"

    # Dest file
    dstFile = os.path.join(dstFolder, 'detection', 'custom', 'img', 'dog.jpg')
    dstBbox = os.path.join(dstFolder, 'detection', 'custom', 'bbox', 'dog.txt')
    dstCorresp = os.path.join(dstFolder, 'detection', 'custom', 'corresp.txt')
    dstTrain = os.path.join(dstFolder, 'detection', 'custom', 'train.txt')

    try:
        os.unlink(dstFile)
    except:
        pass

    try:
        os.unlink(dstBbox)
    except:
        pass

    try:
        os.unlink(dstCorresp)
    except:
        pass

    # verify test file doesn't already exists in project path
    assert not os.path.exists(dstFile)

    # Copy test asset inside project root path
    copyfile(srcFile, os.path.join(dstFolder, 'dog.jpg'))
    assert os.path.exists(os.path.join(dstFolder, 'dog.jpg'))

    # Create detection test parameters
    detection_data = {
        'rootPath': rootPath,
        'targetDir': targetDir,
        'projectName': 'custom',
        'item': {
            'filename': 'dog.jpg',
            'regions': [
                {
                    'classname': 'zone1',
                    'xmin': 0,
                    'xmax': 100,
                    'ymin': 0,
                    'ymax': 100
                },
                {
                    'classname': 'zone2',
                    'xmin': 0,
                    'xmax': 100,
                    'ymin': 0,
                    'ymax': 100
                }
            ]
        }
    }

    # Request flask app on detection task with test parameters
    response = client.post(
        '/detection',
        data=json.dumps(detection_data)
    )

    # Load response json
    data = json.loads(response.get_data(as_text=True))

    # Verify response
    assert data['success']
    assert os.path.exists(dstFile)
    assert os.path.exists(dstBbox)
    assert os.path.exists(dstCorresp)

    assert filecmp.cmp(dstBbox, "tests/assets/detection_custom/bbox.txt")
    assert filecmp.cmp(dstCorresp, "tests/assets/detection_custom/corresp.txt")
    assert filecmp.cmp(dstTrain, "tests/assets/detection_custom/train.txt")

    # Clean test data
    os.unlink(dstFile)
    os.unlink(dstBbox)
    os.unlink(dstCorresp)
    os.unlink(dstTrain)



# Test detection task on simple image file
# and use different tags on second request
def test_detection_multi_tags(client):

    # Root for detection project
    rootPath = '/tmp/'
    targetDir = 'client/images/'
    dstFolder = os.path.join(rootPath, targetDir)

    # Create root path if not already exist
    try:
        os.makedirs(dstFolder)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dstFolder):
            pass
        else:
            raise

    # Source file
    srcFileDog = "tests/assets/dog.jpg"
    srcFileCat = "tests/assets/cat.jpg"

    # Dest file
    dstFileDog = os.path.join(dstFolder, 'detection', 'img', 'dog.jpg')
    dstFileCat = os.path.join(dstFolder, 'detection', 'img', 'cat.jpg')
    dstBboxDog = os.path.join(dstFolder, 'detection', 'bbox', 'dog.txt')
    dstBboxCat = os.path.join(dstFolder, 'detection', 'bbox', 'cat.txt')
    dstCorresp = os.path.join(dstFolder, 'detection', 'corresp.txt')
    dstTrain = os.path.join(dstFolder, 'detection', 'train.txt')

    try:
        os.unlink(dstFileDog)
    except:
        pass

    try:
        os.unlink(dstFileCat)
    except:
        pass

    try:
        os.unlink(dstBboxDog)
    except:
        pass

    try:
        os.unlink(dstBboxCat)
    except:
        pass

    try:
        os.unlink(dstCorresp)
    except:
        pass

    try:
        os.unlink(dstTrain)
    except:
        pass

    # Copy test asset inside project root path
    copyfile(srcFileDog, os.path.join(dstFolder, 'dog.jpg'))
    copyfile(srcFileCat, os.path.join(dstFolder, 'cat.jpg'))
    assert os.path.exists(os.path.join(dstFolder, 'dog.jpg'))
    assert os.path.exists(os.path.join(dstFolder, 'cat.jpg'))

    # Create detection test parameters
    detection_data = {
        'rootPath': rootPath,
        'targetDir': targetDir,
        'item': {
            'filename': 'dog.jpg',
            'regions': [
                {
                    'classname': 'zone1',
                    'xmin': 0,
                    'xmax': 100,
                    'ymin': 0,
                    'ymax': 100
                },
                {
                    'classname': 'zone2',
                    'xmin': 0,
                    'xmax': 100,
                    'ymin': 0,
                    'ymax': 100
                }
            ]
        }
    }

    # Request flask app on detection task with test parameters
    response = client.post(
        '/detection',
        data=json.dumps(detection_data)
    )

    # Load response json
    data = json.loads(response.get_data(as_text=True))

    # Verify response
    assert data['success']
    assert os.path.exists(dstFileDog)
    assert os.path.exists(dstBboxDog)
    assert os.path.exists(dstCorresp)
    assert filecmp.cmp(dstBboxDog, "tests/assets/detection_multi_tags/bbox_dog.txt")

    # Create detection test parameters
    detection_data = {
        'rootPath': rootPath,
        'targetDir': targetDir,
        'item': {
            'filename': 'cat.jpg',
            'regions': [
                {
                    'classname': 'zone2',
                    'xmin': 0,
                    'xmax': 100,
                    'ymin': 0,
                    'ymax': 100
                },
                {
                    'classname': 'zone3',
                    'xmin': 0,
                    'xmax': 100,
                    'ymin': 0,
                    'ymax': 100
                }
            ]
        }
    }

    # Request flask app on detection task with test parameters
    response = client.post(
        '/detection',
        data=json.dumps(detection_data)
    )

    # Load response json
    data = json.loads(response.get_data(as_text=True))

    # Verify response
    assert data['success']
    assert os.path.exists(dstFileCat)
    assert os.path.exists(dstBboxCat)
    assert os.path.exists(dstCorresp)
    assert filecmp.cmp(dstBboxCat, "tests/assets/detection_multi_tags/bbox_cat.txt")

    assert filecmp.cmp(dstCorresp, "tests/assets/detection_multi_tags/corresp.txt")
    assert filecmp.cmp(dstTrain, "tests/assets/detection_multi_tags/train.txt")

    # Clean test data
    os.unlink(dstFileDog)
    os.unlink(dstBboxDog)
    os.unlink(dstFileCat)
    os.unlink(dstBboxCat)
    os.unlink(dstCorresp)
    os.unlink(dstTrain)



# Test detection task input validation
def test_detection_validate_input(client):

    # Root for detection project
    rootPath = '/tmp/'
    targetDir = 'client/images/'
    dstFolder = os.path.join(rootPath, targetDir)

    # Create root path if not already exist
    try:
        os.makedirs(dstFolder)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dstFolder):
            pass
        else:
            raise

    #
    # Invalid targetDir
    #
    response = client.post(
        '/detection',
        data=json.dumps({
            'item': {
                'filename': 'dog.jpg',
                'regions': [
                    {
                        'classname': 'zone1',
                        'xmin': 0,
                        'xmax': 100,
                        'ymin': 0,
                        'ymax': 100
                    },
                    {
                        'classname': 'zone2',
                        'xmin': 0,
                        'xmax': 100,
                        'ymin': 0,
                        'ymax': 100
                    }
                ]
            }
        })
    )

    # Load response json
    data = json.loads(response.get_data(as_text=True))

    # Verify response
    assert not data['success']
    assert data['message'] == "Invalid targetDir"

    #
    # Invalid item parameter
    #
    response = client.post(
        '/detection',
        data=json.dumps({
            'rootPath': rootPath,
            'targetDir': targetDir
        })
    )

    # Load response json
    data = json.loads(response.get_data(as_text=True))

    # Verify response
    assert not data['success']
    assert data['message'] == "Invalid item parameter"

    #
    # Invalid filename parameter
    #
    response = client.post(
        '/detection',
        data=json.dumps({
            'rootPath': rootPath,
            'targetDir': targetDir,
            'item': {
                'regions': [
                    {
                        'classname': 'zone1',
                        'xmin': 0,
                        'xmax': 100,
                        'ymin': 0,
                        'ymax': 100
                    },
                    {
                        'classname': 'zone2',
                        'xmin': 0,
                        'xmax': 100,
                        'ymin': 0,
                        'ymax': 100
                    }
                ]
            }
        })
    )

    # Load response json
    data = json.loads(response.get_data(as_text=True))

    # Verify response
    assert not data['success']
    assert data['message'] == "Invalid filename"

    #
    # Missing file
    #
    response = client.post(
        '/detection',
        data=json.dumps({
            'rootPath': rootPath,
            'targetDir': targetDir,
            'item': {
                'filename': 'invalid_dog.jpg',
                'regions': [
                    {
                        'classname': 'zone1',
                        'xmin': 0,
                        'xmax': 100,
                        'ymin': 0,
                        'ymax': 100
                    },
                    {
                        'classname': 'zone2',
                        'xmin': 0,
                        'xmax': 100,
                        'ymin': 0,
                        'ymax': 100
                    }
                ]
            }
        })
    )

    # Load response json
    data = json.loads(response.get_data(as_text=True))

    # Verify response
    assert not data['success']
    assert data['message'] == "Filename doesn't exist"

# Test detection task on simple image file with forced class_number
def test_detection_class_number(client):

    # Root for detection project
    rootPath = '/tmp/'
    targetDir = 'client/images/'
    dstFolder = os.path.join(rootPath, targetDir)

    # Create root path if not already exist
    try:
        os.makedirs(dstFolder)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dstFolder):
            pass
        else:
            raise

    # Source file
    srcFile = "tests/assets/dog.jpg"

    # Dest file
    dstFile = os.path.join(dstFolder, 'detection', 'img', 'dog.jpg')
    dstBbox = os.path.join(dstFolder, 'detection', 'bbox', 'dog.txt')
    dstCorresp = os.path.join(dstFolder, 'detection', 'corresp.txt')

    try:
        os.unlink(dstFile)
    except:
        pass

    try:
        os.unlink(dstBbox)
    except:
        pass

    try:
        os.unlink(dstCorresp)
    except:
        pass

    # verify test file doesn't already exists in project path
    assert not os.path.exists(dstFile)

    # Copy test asset inside project root path
    copyfile(srcFile, os.path.join(dstFolder, 'dog.jpg'))
    assert os.path.exists(os.path.join(dstFolder, 'dog.jpg'))

    # Create detection test parameters
    detection_data = {
        'rootPath': rootPath,
        'targetDir': targetDir,
        'item': {
            'filename': 'dog.jpg',
            'regions': [
                {
                    'classname': 'zone1',
                    'class_number': 2,
                    'xmin': 0,
                    'xmax': 100,
                    'ymin': 0,
                    'ymax': 100
                },
                {
                    'classname': 'zone2',
                    'class_number': 1,
                    'xmin': 0,
                    'xmax': 50,
                    'ymin': 0,
                    'ymax': 100
                }
            ]
        }
    }

    # Request flask app on detection task with test parameters
    response = client.post(
        '/detection',
        data=json.dumps(detection_data)
    )

    # Load response json
    data = json.loads(response.get_data(as_text=True))

    # Verify response
    assert data['success']
    assert os.path.exists(dstFile)
    assert os.path.exists(dstBbox)
    assert os.path.exists(dstCorresp)

    assert filecmp.cmp(dstBbox, "tests/assets/detection_class_number/bbox.txt")
    assert filecmp.cmp(dstCorresp, "tests/assets/detection_class_number/corresp.txt")

    # Clean test data
    os.unlink(dstFile)
    os.unlink(dstBbox)
    os.unlink(dstCorresp)

