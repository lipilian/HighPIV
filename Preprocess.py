#%% import package∏
import numpy as np
from openpiv import tools, scaling, pyprocess, validation, process, filters
import matplotlib.pyplot as plt
import os
import sys
import cv2
from PIL import Image
import multiprocessing
from joblib import Parallel, delayed
import inspect
#%% important file information
fileNumber = 24000 #each image we have 3000 for 25 fps
fps = 2000
# Image crop information got from imageJ
x = 0 # Cut Start point x position
y = 0 # Cut Start point y position
height = 240 # Cut off muscle region
width = 320 # keep the origin size of the image width
bitSize = 8 # the number of bit for tif image
# maxIntensity = 1500 # highest intensity value from the image
# minIntensity = 700 # lowest intensity value from the image

#%% output the current working directory, will not influence the following steps
print(os.getcwd())
inputFilePath = './image/'
os.chdir(inputFilePath)
print(os.getcwd())

#%% sort the file to get file list
fileNameList = os.listdir(os.getcwd())
N = len(fileNameList)

#%% test the tuning
startFrame = 1300
DeltaFrame = 300
frame_a = tools.imread(fileNameList[startFrame])
frame_b = tools.imread(fileNameList[startFrame + DeltaFrame])
fig,ax = plt.subplots(1, 2, figsize = (50, 100))
ax[0].imshow(frame_a, cmap = plt.cm.gray)
ax[1].imshow(frame_b, cmap = plt.cm.gray)

# %%
winsize = 12 # pixels
searchsize = 12#pixels
overlap = 6 # piexels
dt = DeltaFrame*1./fps # piexels
u0, v0, sig2noise = process.extended_search_area_piv(frame_a.astype(np.int32), frame_b.astype(np.int32), window_size=winsize, overlap=overlap, dt=dt, search_area_size=searchsize, sig2noise_method='peak2peak' )
x, y = process.get_coordinates( image_size=frame_a.shape, window_size=winsize, overlap=overlap )
u1, v1, mask = validation.sig2noise_val( u0, v0, sig2noise, threshold = 1.3)
u2, v2 = filters.replace_outliers( u1, v1, method='localmean', max_iter=5, kernel_size=5)
u3, v3, mask1 = validation.local_median_val(u2,v2,3,3,1)
u4, v4 = filters.replace_outliers(u3, v3, method='localmean', max_iter=5, kernel_size=5)
tools.save(x, y, u4, v4, mask1, '../testResult/test.txt' )

tools.display_vector_field('../testResult/test.txt', scale=500, width=0.0025)
#%% define node
def process_node(i):
    DeltaFrame = 300;
    winsize = 12 # pixels
    searchsize = 12 #pixels
    overlap = 6 # piexels
    dt = DeltaFrame*1./fps # piexels
    frame_a = tools.imread(fileNameList[i])
    frame_b = tools.imread(fileNameList[i+DeltaFrame])
    u0, v0, sig2noise = process.extended_search_area_piv(frame_a.astype(np.int32), frame_b.astype(np.int32), window_size=winsize, overlap=overlap, dt=dt, search_area_size=searchsize, sig2noise_method='peak2peak' )
    x, y = process.get_coordinates( image_size=frame_a.shape, window_size=winsize, overlap=overlap )
    u1, v1, mask = validation.sig2noise_val( u0, v0, sig2noise, threshold = 1.3 )
    u2, v2 = filters.replace_outliers( u1, v1, method='localmean', max_iter=5, kernel_size=5)
    u3, v3, mask1 = validation.local_median_val(u2,v2,3,3,1)
    u4, v4 = filters.replace_outliers(u3, v3, method='localmean', max_iter=5, kernel_size=5)
    tools.save(x,y,u4,v4,mask1,'../testResult/' + str(i) + '.txt')
#%%
DeltaFrame = 300;
element_information = Parallel(n_jobs=6)(delayed(process_node)(node) for node in range(N - DeltaFrame))
#%% processing parameter
'''
winsize = 50 # pixels
searchsize = 50 #pixels
overlap = 25 # piexels
dt = DeltaFrame*1./fps # piexels
u0, v0, sig2noise = process.extended_search_area_piv(frame_a.astype(np.int32), frame_b.astype(np.int32), window_size=winsize, overlap=overlap, dt=dt, search_area_size=searchsize, sig2noise_method='peak2peak' )
x, y = process.get_coordinates( image_size=frame_a.shape, window_size=winsize, overlap=overlap )
u1, v1, mask = validation.sig2noise_val( u0, v0, sig2noise, threshold = 1.3)
u2, v2 = filters.replace_outliers( u1, v1, method='localmean', max_iter=5, kernel_size=10)
#x, y, u, v = scaling.uniform(x, y, u2, v2, scaling_factor = 96.52 )
tools.save(x, y, u2, v2, mask, '../muscle10fpsbotleft_results/test.txt' )
tools.display_vector_field('../muscle10fpsbotleft_results/test.txt', scale=10000, width=0.0025)
'''
#%%
'''
fileNameList = fileNameList[:1991]
fileNameList

#%% loop to generate velocity data to txt file
i = 0
winsize = 100 # pixels
searchsize = 100 #pixels
overlap = 50 # piexels
dt = 5*1./20 # piexels
while (i+5) <=1991:
    frame_a = tools.imread(fileNameList[i])
    frame_b = tools.imread(fileNameList[i+5])
    u0, v0, sig2noise = process.extended_search_area_piv(frame_a.astype(np.int32), frame_b.astype(np.int32), window_size=winsize, overlap=overlap, dt=dt, search_area_size=searchsize, sig2noise_method='peak2peak' )
    x, y = process.get_coordinates( image_size=frame_a.shape, window_size=winsize, overlap=overlap )
    u1, v1, mask = validation.sig2noise_val( u0, v0, sig2noise, threshold = 1.3 )
    u2, v2 = filters.replace_outliers( u1, v1, method='localmean', max_iter=5, kernel_size=5)
    tools.save(x,y,u2,v2,mask,'../20fpsResult/' + str(i) + '.txt')
    i += 1
i

#%% intensity and background information cancelling
# 1. Plot histogram for image a and image b

a = 1
'''
'''
plt.subplot(1, 2, 1)
plt.hist(frame_aCrop.ravel(),(maxIntensity - minIntensity),[minIntensity,maxIntensity])
plt.subplot(1, 2, 2)
plt.hist(frame_bCrop.ravel(),(maxIntensity - minIntensity),[minIntensity,maxIntensity])
plt.show
'''
#%% detect the background color from the raw image
