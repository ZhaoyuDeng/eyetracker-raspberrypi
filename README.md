## Eye-tracker based on Raspberry Pi

###### An eye-tracker is a device for measuring eye positions and eye movement. The glasses-type is a glasses-like type of Eye-tracker wearing like glasses.

This project of mine comes from an innovative experimental project of undergraduates, and uses funds of Hunan Normal University.

![Eye-tracker](https://github.com/Isaac-Deng/eyetracker-raspberrypi/blob/master/IntroPhoto/PortablePart.JPG)
**Introduction video is below:**
[Introduction Video -- YOUTUBE](https://youtu.be/Bhi8Y2sCANM)

### Content Introduction

#### 1. Adjusting

   Photo of 9 crosses for adjustment, regression analysis for mapping parameter

#### 2. IntroPhoto  (Introduction photos)

   Photos of hardware, detection images and adjusting images

#### 3. PupilSample

   Origin Matlab testing program for pupil detection, and grayscale eye photos of every eye-directions to test detection

#### 4. src  (Source code)

   Core program files:

   ​	(File 1~3 & 5 run on PC, 4 runs on Raspberry Pi)

   1. **RecvPupilDetMap.py**

      *Main file of project*

      Receive eye-cam picture to detect pupil. Receive front-cam picture and map cross on the picture.

   2. **pupildet.py**

      The essential function of pupil detection.

   3. **tools.py**

      Misc methods for adjustment, image processing, connection, etc.

   4. **sendvideo2.py**

      Program run on Raspberry Pi to transfer images to PC server.

   5. **GetWinMousePos.py**

      Program to help adjust mapping parameter.

      Other files are old files and don't work on this project.