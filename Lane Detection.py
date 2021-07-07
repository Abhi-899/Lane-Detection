# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 01:14:57 2021

@author: Param
"""
#!pip install opencv-python
import cv2
import numpy as np

# helper functions
def thresholding(img):
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    non_White = np.array([85, 0, 0])
    White = np.array([179, 160, 255])
    mask_White= cv2.inRange(hsv,non_White,White)
    return mask_White

def init_trackbars(init_track_vals,wT=480, hT=240):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Width Top", "Trackbars", init_track_vals[0],wT//2, nothing)
    cv2.createTrackbar("Height Top", "Trackbars", init_track_vals[1], hT, nothing)
    cv2.createTrackbar("Width Bottom", "Trackbars", init_track_vals[2],wT//2, nothing)
    cv2.createTrackbar("Height Bottom", "Trackbars", init_track_vals[3], hT, nothing)

def nothing(a):
    pass

def val_trackbars(wT=480, hT=240):
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([(widthTop, heightTop), (wT-widthTop, heightTop),
                      (widthBottom , heightBottom ), (wT-widthBottom, heightBottom)])
    return points

def draw_points(img,points):
    for x in range( 0,4):
        cv2.circle(img,(int(points[x][0]),int(points[x][1])),15,(0,0,255),cv2.FILLED)
    return img

# For perspective transform
def warp_img (img,points,w,h,inv=False):
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    if inv:
        mat = cv2.getPerspectiveTransform(pts2,pts1)
    else:
        mat = cv2.getPerspectiveTransform(pts1,pts2)
    warpedimg = cv2.warpPerspective(img,mat,(w,h))
    return warpedimg

# For pixel summation 
def get_hist(img,min_percent=0.1,display=False,region=1):
  if region==1:
      hist_values=np.sum(img,axis=0)
  else:
      hist_values=np.sum(img[img.shape[0]//region:,:],axis=0)
  hist_values=np.sum(img,axis=0)
  max_pix=np.max(hist_values)
  min_pix=min_percent*max_pix

  indices=np.where(hist_values>=min_pix)
  base=int(np.average(indices))

  if display:
    img_hist=np.zeros((img.shape[0],img.shape[1],3),np.uint8)
    
    for x,intensity in enumerate(hist_values):
      cv2.line(img_hist,(x,img.shape[0]),(x,img.shape[0]-intensity//255//region),(0,255,0),1)
      cv2.circle(img_hist,(base,img.shape[0]),15,(255,0,0),cv2.FILLED)   
    return base,img_hist 
  return base

# For stacked display
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

#our model
avg_val=10      
curves_list=[]
def getLaneCurve(img,display=2):
    img_copy=img.copy()
    imgThres =  thresholding(img)
    h,w,c=img.shape
    points=val_trackbars()
    imgWarp=warp_img(imgThres,points,w,h)
    WarpPoints=draw_points(img_copy,points)
    midpt,imghist=get_hist(imgWarp,display=True,min_percent=0.5,region=4)
    base,imghist=get_hist(imgWarp,display=True,min_percent=0.9)
    curve0=base-midpt
    curves_list.append(curve0)
    if len(curves_list)>avg_val:
        curves_list.pop(0)
    curve=int(sum(curves_list)/len(curves_list))
    
    #Display
    if display != 0:
        imgInvWarp = warp_img(imgWarp, points, w, h, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:h // 3, 0:w] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        img_copy = cv2.addWeighted(img_copy, 1, imgLaneColor, 1, 0)
        midY = 450
        cv2.putText(img_copy, str(curve), (w // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(img_copy, (w // 2, midY), (w // 2 + (curve * 3), midY), (255, 0, 0), 5)
        cv2.line(img_copy, ((w // 2 + (curve * 3)), midY - 25), (w // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w1 = w // 20
            cv2.line(img_copy, (w1 * x + int(curve // 50), midY - 10),
                     (w1 * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
        #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        #cv2.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3);
    if display == 2:
        imgStacked = stackImages(0.8, ([img, WarpPoints, imgWarp],
                                             [imghist, imgLaneColor, img_copy]))
        cv2.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv2.imshow('Resutlt', img_copy)
 
    #### NORMALIZATION
    curve = curve/100
    if curve>1: curve ==1
    if curve<-1:curve == -1
 
    return curve

    cv2.imshow("thesholded image",imgThres)
    cv2.imshow("Birdeye View",imgWarp)
    cv2.imshow("points",WarpPoints)
    cv2.imshow("Histogram",imghist)
    
if __name__ == '__main__': 
    cap = cv2.VideoCapture('vid1.mp4')
    init_track_vals=[102,54,32,163]
    init_trackbars(init_track_vals)
    frame_count=0
    curves_list=[]
    while True:
      frame_count +=1
      if cap.get(cv2.CAP_PROP_FRAME_COUNT) ==frame_count:
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
        frame_count=0
      _ , img = cap.read() # GET THE IMAGE
      img = cv2.resize(img,(480,240)) # RESIZE
      curve=getLaneCurve(img,display=2)
      print(curve)
      cv2.waitKey(1)
      cv2.destroyAllWindows()
      
cap.release()  
