#%% import package
import numpy as np
from openpiv import tools, scaling, pyprocess, validation, process, filters
import matplotlib.pyplot as plt
import os
import sys

import cv2
from PIL import Image
import pandas as pd

#%% read data from file
inputFilePath = '/Volumes/LiuHongData/StreamExperiment_10292019/Control240s10fpsResult'
os.chdir(inputFilePath)
data = np.loadtxt('0.txt')
m, n = data.shape
Result = data
Result[:,2] = 0.
Result[:,3] = 0.
Result[:,4] = 0.
for i in range(390):
    txtName = str(i) + '.txt'
    data = np.loadtxt(txtName)
    m, n = data.shape
    for j in range(m):
        if(data[j][4] == 0):
            Result[j][4] += 1.
            Result[j][2] += data[j][2]
            Result[j][3] += data[j][3]
for i in range(m):
    if (Result[i][4] != 0.):
        Result[i][2] /= Result[i][4]
        Result[i][3] /= Result[i][4]

#%% save the Result data as txt for tecplot
CalibrateData = 1 #micro meter per pixel
Result[:,0:5] *= CalibrateData
#tools.save(Result[:,0], Result[:,1], Result[:,2], Result[:,3], 'Result.txt')
np.savetxt('result.txt', Result,delimiter=',',fmt='%8f')
tools.display_vector_field('389.txt', scale=1000, width=0.0025)

#%% Check data size
print(data.shape)
