import cv2
import numpy as np
import sys


def resize(dst,img):
    width = img.shape[1]
    height = img.shape[0]
    dim = (width, height)
    resized = cv2.resize(dst, dim, interpolation = cv2.INTER_AREA)
    return resized

video = cv2.VideoCapture(0)
# backg = cv2.VideoCapture("ocean.mp4")
success, ref_img = video.read()
flag = 0

while(1):
    success, img = video.read()
    # cv2.imshow('Original Video', img)
    bg = cv2.imread('back6.jpg')
    bg = resize(bg, ref_img)
    if flag==0:
        ref_img = img
    
    # create a mask
    diff1 = cv2.subtract(img, ref_img)
    diff2 = cv2.subtract(ref_img,img)
    diff = diff1+diff2
    diff[abs(diff)<13.0]=0
    gray = cv2.cvtColor(diff2.astype(np.uint8), cv2.COLOR_BGR2GRAY)
    gray[np.abs(gray)< 8] = 0
    fgmask=gray.astype(np.uint8)
    fgmask[fgmask>5]=255
    fgmask = cv2.medianBlur(fgmask,5)
    
    #invert the mask
    fgmask_inv = cv2.bitwise_not(fgmask)
    fgmask_inv = cv2.medianBlur(fgmask_inv,5)
    # cv2.imshow('fgmask', fgmask)
    # cv2.imshow('fgmask_inv',fgmask_inv)
    # Use the mask to extract the relevent parts from FG and BG
    fgimg = cv2.bitwise_and(img,img,mask=fgmask)
    bgimg = cv2.bitwise_and(bg,bg,mask=fgmask_inv)
    
    #combine both bg and fg images
    dst = cv2.add(bgimg, fgimg)
    cv2.imshow('Backgroung removal', dst)
    
    #Appling Histogram Equalization on each channel 
    R, G, B = cv2.split(dst)
    output1_R = cv2.equalizeHist(R)
    output1_G = cv2.equalizeHist(G)
    output1_B = cv2.equalizeHist(B)

    equ = cv2.merge((output1_R, output1_G, output1_B))
    cv2.imshow('After histogram equalization', equ)

    key = cv2.waitKey(5) & 0xFF
    if ord('q') == key:
        break
    elif ord('d') == key:
        flag = 1
        print('background captured')
    elif ord('r') == key:
        flag = 0
        print('ready to capture new bg')


cv2.destroyAllWindows()
video.release()
