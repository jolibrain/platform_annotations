import pytest
import json
import errno
import os
from shutil import copyfile
import base64
import filecmp

# Test classification task on simple image file
def test_classification(client):

    # Root for classifciation project
    dstPath = '/opt/platform/data/client/images/'

    # Source file
    srcFile = "tests/assets/dog.jpg"

    # Dest file
    dstFile = os.path.join(dstPath, 'train', 'dog', 'dog.jpg')

    try:
        os.unlink(dstFile)
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
        'targetDir': '/client/images/',
        'item': {
            'filename': 'dog.jpg',
            'classname': 'dog'
        }
    }

    # Request flask app on classification task with test parameters
    response = client.post(
        '/classification',
        data=json.dumps(classif_data)
    )

    # Load response json
    data = json.loads(response.get_data(as_text=True))

    # Verify response
    assert data['success']
    assert os.path.exists(os.path.join(dstPath, 'train', 'dog', 'dog.jpg'))

    # Clean test data
    os.unlink(os.path.join(dstPath, 'dog.jpg'))
    os.unlink(os.path.join(dstPath, 'train', 'dog', 'dog.jpg'))



# Test classification task with base64 content
def test_classification_base64_content(client):

    # Root for classifciation project
    dstPath = '/opt/platform/data/client/images/'

    # Source file
    srcFile = "tests/assets/dog.jpg"

    # Dest file
    dstFile = os.path.join(dstPath, 'train', 'dog', 'dog.jpg')

    try:
        os.unlink(dstFile)
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

    with open(srcFile, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    # Create classification test parameters
    classif_data = {
        'targetDir': '/client/images/',
        'item': {
            'filename': 'dog.jpg',
            'classname': 'dog',
            'content': encoded_string
        }
    }

    # Request flask app on classification task with test parameters
    response = client.post(
        '/classification',
        data=json.dumps(classif_data)
    )

    # Load response json
    data = json.loads(response.get_data(as_text=True))

    # Verify response
    assert data['success']
    assert os.path.exists(dstFile)
    assert filecmp.cmp(srcFile, dstFile)

    # Clean test data
    os.unlink(dstFile)



# Test classification task with invalid filename
def test_classification_invalid_filename(client):

    # Root for classifciation project
    dstPath = '/opt/platform/data/client/images/'

    # Create root path if not already exist
    try:
        os.makedirs(dstPath)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dstPath):
            pass
        else:
            raise

    invalidFile = os.path.join(dstPath, 'invalid_dog.jpg')
    assert not os.path.exists(invalidFile)

    # Create classification test parameters
    classif_data = {
        'targetDir': '/client/images/',
        'item': {
            'filename': 'invalid_dog.jpg',
            'classname': 'dog',
        }
    }

    # Request flask app on classification task with test parameters
    response = client.post(
        '/classification',
        data=json.dumps(classif_data)
    )

    # Load response json
    data = json.loads(response.get_data(as_text=True))

    # Verify response
    assert not data['success']
