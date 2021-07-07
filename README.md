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
 Here we are simply converting our image to HSV color space and then applying a range of color to find. This color could be found using the colorpicker.py as discussed earlier which helps to swiftly adjust the threshold(max and min) for each of the HSV channels.

## Warping (for Perspective transformation)
![image](https://user-images.githubusercontent.com/64439578/124719271-98c81c00-df24-11eb-82bf-988f9e36e960.png)
If we were flying over the road, and watching it from a bird's eye view, the lanes would be
parallel(as shown in the 3rd image), but in the thresholded(1st) and actual images(2nd) they are not, because of the perspective.
The perspective depends on the focal length of the lens (lenses with a shorter focal
length show a stronger perspective) and the position of the camera. Once the camera is
mounted on a car, the perspective is fixed, so we can take it into consideration and correct
the image.

OpenCV has a method to compute the perspective transformation:

getPerspectiveTransform().

It takes two parameters, both arrays of four points, identifying the trapezoid of the
perspective. One array is the source and one array is the destination. This means that the
same method can be used to compute the inverse transformation, by just swapping the
parameters:
```
pers_mat = cv2.getPerspectiveTransform(src, dst)
pers_mat_inv = cv2.getPerspectiveTransform(dst,src)
```
The src are the co-ordinates of the trapezoid whereas the dst are the coordinates of the rectangle.So finally we can get the transformed image by applying:
```
cv2.warpPerspective(img, pers_mat, warp_size,flags=cv2.INTER_AREA)
```
INTER_AREA is preferrred as we are stretching a part of the image in order to perform the transformation.
The challenge here is to get the co-ordinates for the src and the dst.We can retrieve them manually by plotting the image with 'axis=True' to get a brief idea of the co-ordinate values. But Murtaza's workshop gives a much better alternative.

We can create two functions for the trackbars. One that initializes the trackbars and the second that get the current value from them.Let us have a look at the 2 functions.
```
def init_trackbars(init_track_vals,wT=480, hT=240):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Width Top", "Trackbars", intialTracbarVals[0],wT//2, nothing)
    cv2.createTrackbar("Height Top", "Trackbars", intialTracbarVals[1], hT, nothing)
    cv2.createTrackbar("Width Bottom", "Trackbars", intialTracbarVals[2],wT//2, nothing)
    cv2.createTrackbar("Height Bottom", "Trackbars", intialTracbarVals[3], hT, nothing)
 
def val_trackbars(wT=480, hT=240):
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([(widthTop, heightTop), (wT-widthTop, heightTop),
                      (widthBottom , heightBottom ), (wT-widthBottom, heightBottom)])
    return points
    
```    
