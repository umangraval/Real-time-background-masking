import cv2

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def resize(dst,img):
        width = img.shape[1]
        height = img.shape[0]
        dim = (width, height)
        resized = cv2.resize(dst, dim, interpolation = cv2.INTER_AREA)
        return resized

    
    def get_frame(self):
        success, ref_img = self.video.read()    
        ref_img = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
        # time.sleep(10)
        # flag = 0
        
        # bg = cv2.imread('./static/background.jpg')
        # bg = resize(bg, ref_img)
        # if flag==0:
        #     ref_img = img
        # create a mask
        # diff1 = cv2.subtract(bg, ref_img)
        # diff2 = cv2.subtract(ref_img,bg)
        # diff = diff1+diff2
        # diff[abs(diff)<20.0]=0
        # gray = cv2.cvtColor(diff.astype(np.uint8), cv2.COLOR_BGR2GRAY)
        # gray[np.abs(gray)< 10] = 0
        # fgmask=gray.astype(np.uint8)
        # fgmask[fgmask>5]=255
        # fgmask = cv2.medianBlur(fgmask,5)
        
        # #invert the mask
        # fgmask_inv = cv2.bitwise_not(fgmask)
        # fgmask_inv = cv2.medianBlur(fgmask_inv,5)

        # #use the mask to extract the relevent parts from FG and BG
        # fgimg = cv2.bitwise_and(img,img,mask=fgmask)
        # bgimg = cv2.bitwise_and(bg,bg,mask=fgmask_inv)
        # #combine both bg and fg images
        # dst = cv2.add(bgimg, fgimg)
        # # cv2.imshow('Backgroung removal', dst)
        # frame = cv2.imencode('.jpg', dst)[1].tobytes()
        # yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # # key = cv2.waitKey(10)
        # if ord('q') == key:
        #     break
        # elif ord('d') ==key:
        #     flag = 1
        #     # print('background captured')
        # elif ord('r') == key:
        #     flag = 0
        #     print('ready to capture new bg')

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', ref_img)
        return jpeg.tobytes()