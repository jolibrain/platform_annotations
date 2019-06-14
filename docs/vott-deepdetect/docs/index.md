# Classification

DeepDetect Annotation Tool helps tagging images for a classification job.

## Create Connection

Visit DeepDetect Annotation Tool homepage:

![VoTT](img/vott_home.png)

Select the connections icons to visit Connection tab:

![VoTT - Select Connection](img/vott_home_select_connector.png)

You are now on Connection tab:

![VoTT Connection](img/vott_connector_home.png)

Now, click on the "+" icon to create a new connection:

![VoTT Connection - Select Add Connection](img/vott_connector_home_select_add.png)

This form appears, fill it to create a new connection:

![VoTT Connection Add](img/vott_add_connector.png)

You must select "DeepDetect Platform Storage" inside the Provider menu:

![VoTT Connection Add - Select Provider](img/vott_add_connector_select_provider.png)

You will find the following options for the DeepDetect Platform Storage provider:

![VoTT Connection Add - DeepDetect Platform Storage](img/vott_add_connector_deepdetect.png)

* **Best Practive** : you should name your connection with a reference to the data path you're using so it'll be easier to find the right connection when you'll be creating a new project.
* **Data Storage Location** : where your images are stored on DeepDetect Platform. If your images are stored in */opt/platform/data/client/images/*, you must fill */client/images/* in this input;
* **Model Type** : for a classification job, please select *classification* in this menu.

## Create Project

If a DeepDetect Platform Storage connection is ready, you can now create a new Project.

Visit *Annotation Tool* home and click on *New Project*:

![VoTT - Select New Project](img/vott_home_select_new_project.png)

This *New Project* form appears:

![VoTT New Project](img/vott_new_project.png)

Fill the details, and select the connection you've created before as Source and Target connection:

![VoTT New Project - Connections](img/vott_new_project_select_connector.png)

## Tag Editor

When the project has been created, the *Tag Editor* tab will be available, with images from the connection

![VoTT Tag Editor](img/vott_tag_editor.png)

Now you must create new Tags in the tag section of the page,  click on the "+" icon:

![VoTT Tag Editor - New Tags](img/vott_tag_editor_select_new_tag.png)

Here is an example of created tags:

![VoTT Tag Editor - Tags](img/vott_tag_editor_select_tags.png)

You can now tag each image from the Tag Editor.

The workflow is optimised for fast keyboard manipulation:

1. press key "F" to add a rectangle on the full image
2. press the tag shortcut number to apply a tab on this rectangle. In our example, "1" for "Cat" and "2" for "dog"
3. press down arrow key to navigate to the next image

![VoTT Tag Editor - Tagging](img/vott_tag_editor_tagging.png)

![VoTT Tag Editor - Tagging](img/vott_tag_editor_tagging_bis.png)

## Result Folder

Results are avaible on the DeepDetect Platform Filebrowser.

You can navigate to your connection data path:

![Filebrowser - Connector Home](img/filebrowser_images.png)

You'll find a new "**train**" folder:

![Filebrowser - Select Train Folder](img/filebrowser_images_select_train.png)

Inside this train folder, you will find a folder for each tag, containing the images you've tagged from the Tag Editor.

![Filebrowser - Train Folder](img/filebrowser_images_train.png)

# Detection

DeepDetect Annotation Tool helps tagging images for a detection job.

## Create Connection

Visit DeepDetect Annotation Tool homepage:

![VoTT](img/vott_home.png)

Select the connections icons to visit Connection tab:

![VoTT - Select Connection](img/vott_home_select_connector.png)

You are now on Connection tab:

![VoTT Connection](img/vott_connector_home.png)

Now, click on the "+" icon to create a new connection:

![VoTT Connection - Select Add Connection](img/vott_connector_home_select_add.png)

This form appears, fill it to create a new connection:

![VoTT Connection Add](img/vott_add_connector.png)

You must select "DeepDetect Platform Storage" inside the Provider menu:

![VoTT Connection Add - Select Provider](img/vott_add_connector_select_provider.png)

You will find the following options for the DeepDetect Platform Storage provider:

![VoTT Connection Add - DeepDetect Platform Storage](img/vott_add_connector_deepdetect.png)

* **Best Practive** : you should name your connection with a reference to the data path you're using so it'll be easier to find the right connection when you'll be creating a new project.
* **Data Storage Location** : where your images are stored on DeepDetect Platform. If your images are stored in */opt/platform/data/client/images/*, you must fill */client/images/* in this input;
* **Model Type** : for a classification job, please select *detection* in this menu.

## Create Project

![VoTT - Select New Project](img/vott_home_select_new_project.png)

![VoTT New Project](img/vott_new_project.png)

![VoTT New Project - Connections](img/vott_new_project_select_connector.png)

## Active Learning

TBD

## Tag Editor

When the project has been created, the *Tag Editor* tab will be available, with images from the connection

![VoTT Tag Editor](img/vott_tag_editor.png)

## Result Folder

TBD
