## Eye-tracker based on Raspberry Pi

###### An eye-tracker is a device for measuring eye positions and eye movement. The glasses-type is a glasses-like type of Eye-tracker wearing like glasses.

###### Eye tracking is the process of measuring either the point of gaze or the motion of an eye relative to the head. 

### Content Introduction

1. **Adjusting**

   Photo of 9 crosses for adjustment, regression analysis for mapping parameter

2. **IntroPhoto**  (Introduction photos)

   Photos of general introduction

3. **PupilSample**

   Origin Matlab testing program for pupil detection, and grayscale eye photos of every eye-directions to test detection

4. **src**  (Source code)

   Core program files:

   ​	(File 1~3 & 4 run on PC, 4 runs on Raspberry Pi)

   1. <u>RecvPupilDetMap.py</u>

      Main file of project

      Receive eye-cam picture to detect pupil. Receive front-cam picture and map cross on the picture.

   2. <u>pupildet.py</u>

      The essential function of pupil detection.

   3. <u>tools.py</u>

      Misc methods for adjustment, image processing, connection, etc.

   4. <u>sendvideo2.py</u>

      Program run on Raspberry Pi to transfer images to PC server.

   5. <u>GetWinMousePos.py</u>

      Program to help adjust mapping parameter.



Introduction video is below:**

[Introduction Video -- YOUTUBE](https://youtu.be/Bhi8Y2sCANM)

![Eye-trackre](D:\GitHub\eyetracker-raspberrypi\IntroPhoto\PortablePart.JPG)