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
The idea is to find the path using color detection or edge detector and then getting the curve using summation of pixels in the y direction i.e a histogram. We can split the task into 5 different steps. This includes Thresholding, Warping , Histogram, Averaging, and Displaying. Hence we will be building different functions for each of these operations and then we will apply them as a pipeline in the the function getLaneCurve(img,display) over each frame read from the test video.

Let us look at our functionalities one by one
# Helper Functions
## Thresholding
While for a human it is easy to follow a lane, for a computer, this is not something that is
so simple. One problem is that an image of the road has too much information. We need
to simplify it, selecting only the parts of the image that we are interested in. We will only
analyze the part of the image with the lane, but we also need to separate the lane from the
rest of the image, for example, using color selection which can be swiftly applied by a colorpicker script about which we will discuss later.
Now the idea here is to get the path using either Color or Edge Detection. So let us explore each color space and try to observe the results.
### RGB color space
The image can be decomposed into three channels: red, green, and blue. As we
know, OpenCV stores the image as BGR (meaning, the first byte is the blue channel, not
the red channel), but conceptually, there is no difference. So if we separate the three channels they almost look the same. We try to separate the lane by selecting the white pixels. As the
white color is (255, 255, 255), we could leave some margin and select the colors
above a certain threshold on the scale. But the value that we choose for the threshold is very important, and unfortunately, it is
dependent on the colors used for the lane and on the situation of the road especially the 'light conditions' and the above thresholding method with the RGB color space does not provide us enough control with the lighting parameter.

Hence a better choice would be the HLS or the HSV color space.
### HSV color space
The HSV color space divides the color into hue, saturation, and value, and it is related to
HLS. The result is therefore similar to HLS(hue lightness and saturation). The thresholding done using the HSV color space gives us a better result.The thresholding function is as follows:
```
def thresholding(img):
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    non_White = np.array([85, 0, 0])
    White = np.array([179, 160, 255])
    mask_White= cv2.inRange(hsv,non_White,White)
    return mask_White
 ```
 

