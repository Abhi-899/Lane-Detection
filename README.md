# Lane-Detection
This project is one of the important modules of the complete autonomous cars project where we will try to visualize the lanes that is needed to be traversed along with the amount of curvature at each turning.

# Technical Requirements
The technical reqirements are as follows:

• Python 3.7

• The OpenCV-Python module

• The NumPy module

• The Matplotlib module

To identify the lanes, we need some images and a video. The dataset we will be using here is provided by Murtaza's workshop.The reason behind picking this dataset is the presence of a controlled environment which allows for better and easier thresholding. The methodology and pipeline we follow for this project relies on several assumptions that might not be true in the real world, though it can be adjusted to correct for that.
# Concept
The idea is to find the path using color detection or edge detector and then getting the curve using summation of pixels in the y direction i.e a histogram. We can split the task into 5 different steps. This includes Thresholding, Warping , Histogram, Averaging, and Displaying. Hence we will be building different functions for each of these operations and then we will apply them as a pipeline in the the function getLaneCurve(img,display) over each frame read from the test video
