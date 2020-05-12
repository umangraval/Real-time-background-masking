import cv2
import numpy as np
import time
import sys
from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')



def resize(dst,img):
    width = img.shape[1]
    height = img.shape[0]
    dim = (width, height)
    resized = cv2.resize(dst, dim, interpolation = cv2.INTER_AREA)
    return resized

def gen(key):
    video = cv2.VideoCapture(0)
    # backg = cv2.VideoCapture("ocean.mp4")
    print(5)
    time.sleep(1)
    print(4)
    time.sleep(1)
    print(3)
    time.sleep(1)
    print(2)
    time.sleep(1)
    print(1)
    time.sleep(1)
    success, ref_img = video.read()
    flag = 0
    
    while(1):
        success, img = video.read()
        bg = cv2.imread('back.jpg')
        bg = resize(bg, ref_img)
        # if flag==0:
        ref_img = img
        # create a mask
        #diff1 = cv2.subtract(img, ref_img)
        diff2 = cv2.subtract(ref_img,img)
        # diff = diff1+diff2
        diff1[abs(diff1)<30.0]=0
        gray = cv2.cvtColor(diff1.astype(np.uint8), cv2.COLOR_BGR2GRAY)
        gray[np.abs(gray)< 10] = 0
        fgmask=gray.astype(np.uint8)
        fgmask[fgmask>5]=255
        #invert the mask
        fgmask_inv = cv2.bitwise_not(fgmask)
        #use the mask to extract the relevent parts from FG and BG
        fgimg = cv2.bitwise_and(img,img,mask=fgmask)
        bgimg = cv2.bitwise_and(bg,bg,mask=fgmask_inv)
        #combine both bg and fg images
        dst = cv2.add(bgimg, fgimg)
        # cv2.imshow('Backgroung removal', dst)
        frame = cv2.imencode('.jpg', dst)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # key = cv2.waitKey(10)
        if ord('q') == key:
            break
        elif ord('d') ==key:
            flag = 1
            # print('background captured')
        elif ord('r') == key:
            flag = 0
            print('ready to capture new bg')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(100),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/control', methods=['POST'])
def control():
    return Response(gen(request.form['control']),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

    

if __name__ == '__main__':
    app.run(debug=True)