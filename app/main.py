import cv2
import numpy as np
import time
import sys
import os
from flask import Flask, flash, render_template, Response, request, redirect
from werkzeug.utils import secure_filename
from camera import VideoCamera

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

	
@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = 'background.jpg'
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect('/')


# def resize(dst,img):
#     width = img.shape[1]
#     height = img.shape[0]
#     dim = (width, height)
#     resized = cv2.resize(dst, dim, interpolation = cv2.INTER_AREA)
#     return resized

        
# def gen(key):
#     cap = cv2.VideoCapture('time.mp4')
    
#     # Read until video is completed
#     while(cap.isOpened()):
#       # Capture frame-by-frame
#         ret, img = cap.read()
#         if ret == True:
#             img = cv2.resize(img, (640,480), fx=0.5, fy=0.5) 
#             frame = cv2.imencode('.jpg', img)[1].tobytes()
#             yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#             time.sleep(0.1)
#         else: 
#             break
    
#     video = cv2.VideoCapture(0)    
#     # time.sleep(10)
#     success, ref_img = video.read()
#     flag = 0
    
#     while(1):
#         success, img = video.read()
#         bg = cv2.imread('./static/background.jpg')
#         bg = resize(bg, ref_img)
#         if flag==0:
#             ref_img = img
#         # create a mask
#         diff1 = cv2.subtract(img, ref_img)
#         diff2 = cv2.subtract(ref_img,img)
#         diff = diff1+diff2
#         diff[abs(diff)<20.0]=0
#         gray = cv2.cvtColor(diff.astype(np.uint8), cv2.COLOR_BGR2GRAY)
#         gray[np.abs(gray)< 10] = 0
#         fgmask=gray.astype(np.uint8)
#         fgmask[fgmask>5]=255
#         fgmask = cv2.medianBlur(fgmask,5)
        
#         #invert the mask
#         fgmask_inv = cv2.bitwise_not(fgmask)
#         fgmask_inv = cv2.medianBlur(fgmask_inv,5)

#         #use the mask to extract the relevent parts from FG and BG
#         fgimg = cv2.bitwise_and(img,img,mask=fgmask)
#         bgimg = cv2.bitwise_and(bg,bg,mask=fgmask_inv)
#         #combine both bg and fg images
#         dst = cv2.add(bgimg, fgimg)
#         # cv2.imshow('Backgroung removal', dst)
#         frame = cv2.imencode('.jpg', dst)[1].tobytes()
#         yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#         # key = cv2.waitKey(10)
#         if ord('q') == key:
#             break
#         elif ord('d') ==key:
#             flag = 1
#             # print('background captured')
#         elif ord('r') == key:
#             flag = 0
            # print('ready to capture new bg')

# @app.route('/video_feed')
# def video_feed():
#     """Video streaming route. Put this in the src attribute of an img tag."""
#     return Response(gen(100),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_fed')
def video_fed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
   

if __name__ == '__main__':
    app.run(debug=True)