# -*- coding: utf-8 --
import pytest
import json
import errno
import os
from shutil import copyfile
import base64
import filecmp

# Test classification task on simple image file
def test_classification(client):

    # Root for classification project
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
    dstFile = os.path.join(dstFolder, 'train', 'dog', 'dog.jpg')

    try:
        os.unlink(dstFile)
    except:
        pass

    # verify test file doesn't already exists in project path
    assert not os.path.exists(dstFile)

    # Copy test asset inside project root path
    copyfile(srcFile, os.path.join(dstFolder, 'dog.jpg'))
    assert os.path.exists(os.path.join(dstFolder, 'dog.jpg'))

    # Create classification test parameters
    classif_data = {
        'rootPath': rootPath,
        'targetDir': targetDir,
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
    assert os.path.exists(os.path.join(dstFolder, 'train', 'dog', 'dog.jpg'))

    # Clean test data
    os.unlink(os.path.join(dstFolder, 'dog.jpg'))
    os.unlink(os.path.join(dstFolder, 'train', 'dog', 'dog.jpg'))



# Test classification task with base64 content
def test_classification_base64_content(client):

    # Root for classification project
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
    dstFile = os.path.join(dstFolder, 'train', 'dog', 'dog.jpg')

    try:
        os.unlink(dstFile)
    except:
        pass

    # verify test file doesn't already exists in project path
    assert not os.path.exists(dstFile)

    with open(srcFile, "rb") as image_file:
        binary_file_data = image_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        encoded_string = base64_encoded_data.decode('utf-8')

    # Create classification test parameters
    classif_data = {
        'rootPath': rootPath,
        'targetDir': targetDir,
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

    # Root for classification project
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

    invalidFile = os.path.join(dstFolder, 'invalid_dog.jpg')
    assert not os.path.exists(invalidFile)

    # Create classification test parameters
    classif_data = {
        'rootPath': rootPath,
        'targetDir': targetDir,
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
    assert data['message'] == "Filename doesn't exist"

# Test classification parameters validation
def test_classification_validate_parameters(client):

    # Root for classification project
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
    # invalid targetDir
    #

    response = client.post(
        '/classification',
        data=json.dumps({
            'item': {
                'filename': 'image_construction_siège_lille2.jpg',
                'classname': 'dog'
            }
        })
    )

    # Load response json
    data = json.loads(response.get_data(as_text=True))

    # Verify response
    assert not data['success']
    assert data['message'] == 'Invalid targetDir'

    #
    # invalid item
    #

    response = client.post(
        '/classification',
        data=json.dumps({
            'rootPath': rootPath,
            'targetDir': targetDir
        })
    )

    # Load response json
    data = json.loads(response.get_data(as_text=True))

    # Verify response
    assert not data['success']
    assert data['message'] == 'Invalid item parameter'

    #
    # invalid filename
    #

    response = client.post(
        '/classification',
        data=json.dumps({
            'rootPath': rootPath,
            'targetDir': targetDir,
            'item': {
                'classname': 'dog'
            }
        })
    )

    # Load response json
    data = json.loads(response.get_data(as_text=True))

    # Verify response
    assert not data['success']
    assert data['message'] == 'Invalid filename'

    #
    # Filename doesn't exist
    #

    response = client.post(
        '/classification',
        data=json.dumps({
            'rootPath': rootPath,
            'targetDir': targetDir,
            'item': {
                'filename': 'image_construction_siège_lille2.jpg',
                'classname': 'dog'
            }
        })
    )

    # Load response json
    data = json.loads(response.get_data(as_text=True))

    # Verify response
    assert not data['success']
    assert data['message'] == "Filename doesn't exist"

    #
    # invalid classname
    #

    response = client.post(
        '/classification',
        data=json.dumps({
            'rootPath': rootPath,
            'targetDir': targetDir,
            'item': {
                'filename': 'dog.jpg',
            }
        })
    )

    # Load response json
    data = json.loads(response.get_data(as_text=True))

    # Verify response
    assert not data['success']
    assert data['message'] == 'Invalid classname'

# Test classification task with project name parameter
def test_classification_with_project_name(client):

    # Root for classification project
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
    dstFile = os.path.join(dstFolder, 'train', 'dog', 'dog.jpg')

    try:
        os.unlink(dstFile)
    except:
        pass

    # verify test file doesn't already exists in project path
    assert not os.path.exists(dstFile)

    # Copy test asset inside project root path
    copyfile(srcFile, os.path.join(dstFolder, 'dog.jpg'))
    assert os.path.exists(os.path.join(dstFolder, 'dog.jpg'))

    # Create classification test parameters
    classif_data = {
        'rootPath': rootPath,
        'targetDir': targetDir,
        'projectName': 'custom',
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
    print(data)
    assert data['success']
    assert os.path.exists(os.path.join(dstFolder, 'train', 'custom', 'dog', 'dog.jpg'))

    # Clean test data
    os.unlink(os.path.join(dstFolder, 'dog.jpg'))
    os.unlink(os.path.join(dstFolder, 'train', 'custom', 'dog', 'dog.jpg'))
