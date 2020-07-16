#%% import package
import cv2

# %% decompose video into images
VideoPath = "./video/1.avi"
ImagePath = "./image/"
videoFrames = 25000
vidcap = cv2.VideoCapture(VideoPath)
success,image = vidcap.read()
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
count = 0
success = True
while success and count < videoFrames:
    cv2.imwrite(ImagePath + "Imgae%08d.PILF.tif" % count, image[:,0:152])     # save frame as PNG file
    success,image = vidcap.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # print ('Read a new frame: ', success)
    count += 1

# %%
