import pytest
import json
import errno
import os
from shutil import copyfile
import base64
import filecmp

# Test detection task on simple image file
def test_detection(client):

    # Root for classifciation project
    dstPath = '/opt/platform/data/client/images/'

    # Source file
    srcFile = "tests/assets/dog.jpg"

    # Dest file
    dstFile = os.path.join(dstPath, 'detection', 'img', 'dog.jpg')
    dstBbox = os.path.join(dstPath, 'detection', 'bbox', 'dog.txt')
    dstCorresp = os.path.join(dstPath, 'detection', 'corresp.txt')
    dstTrain = os.path.join(dstPath, 'detection', 'train.txt')

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

    # Create root path if not already exist
    try:
        os.makedirs(dstPath)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dstPath):
            pass
        else:
            raise

    # verify test file doesn't already exists in project path
    assert not os.path.exists(dstFile)

    # Copy test asset inside project root path
    copyfile(srcFile, os.path.join(dstPath, 'dog.jpg'))
    assert os.path.exists(os.path.join(dstPath, 'dog.jpg'))

    # Create classification test parameters
    classif_data = {
        'tags': ['zone1', 'zone2'],
        'targetDir': '/client/images/',
        'item': {
            'filename': 'dog.jpg',
            'classname': 'dog',
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

    # Request flask app on classification task with test parameters
    response = client.post(
        '/detection',
        data=json.dumps(classif_data)
    )

    # Load response json
    data = json.loads(response.get_data(as_text=True))

    # Verify response
    assert data['success']
    assert os.path.exists(dstFile)
    assert os.path.exists(dstBbox)
    assert os.path.exists(dstCorresp)

    assert filecmp.cmp(dstBbox, "tests/assets/detection/bbox.txt")
    assert filecmp.cmp(dstCorresp, "tests/assets/detection/corresp.txt")
    assert filecmp.cmp(dstTrain, "tests/assets/detection/train.txt")

    # Clean test data
    os.unlink(dstFile)
    os.unlink(dstBbox)
    os.unlink(dstCorresp)
