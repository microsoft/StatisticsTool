# Introduction 
This tool helps Data Science team to debug their algorithm outputs and compare them with the GT.
This tool was created by Ben Fishman and Yoav Lotem
Code modifications were made by Ben Azran

# Getting Started
1. pip install -r requirements.txt
2. Change directory to flask_GUI.py path
3. Run python flask_GUI.py
4. Type localhost:5000 at the browser and start using the tool

# Required Folders
1. Prediction Folder - contains all the predictions file
2. Ground Truth Folder - contains all the GT files
3. Images Folder - contains sub-folders of videos (each such folder contains the video's frames)
4. Output Folder - an empty folder in which the data is saved to

# Formats
All the files in the folders should have a FILENAME_XXXX.FILETYPE format for matching predictions, labels, and images:
1. FILENAME - could be any name without dots (.) - doesn't have to be the same for matching predictions/labels/images.
2. _XXXX - a serial number to match labels, predictions, and frames folder (For example: GT_0001.csv, PRD_0001.csv, CATS_0001 corresponds to each other).
3. .FILETYPE - could be of any type such as .json or .csv (The image folder shouldn't have any .filetype ending since it's a folder).

# Further Details
For more information, please read the wiki.png in this directory.