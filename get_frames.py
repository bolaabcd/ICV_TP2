#!/usr/bin/python3

from operator import is_
import cv2
from cv2 import threshold
import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *



vidcap = cv2.VideoCapture('entrada.mp4')
success,image = vidcap.read()
i = 0
while success:
    print(i)
    if i% 144 == 0:
        cv2.imwrite("./frames/"+str(i) + ".jpg", image)
    assert(image.max() <= 255 and image.min() >= 0)
    success,image = vidcap.read()
    i += 1



# Post-Calibration:
"""
Calibration results after optimization (with uncertainties):

Focal Length:          fc = [ 305.63204   299.37624 ] +/- [ 31.21264   27.35409 ]
Principal point:       cc = [ 307.02195   258.75539 ] +/- [ 8.57489   17.54686 ]
Skew:             alpha_c = [ 0.00000 ] +/- [ 0.00000  ]   => angle of pixel axes = 90.00000 +/- 0.00000 degrees
Distortion:            kc = [ -0.03318   0.09094   0.02252   0.00253  0.00000 ] +/- [ 0.09034   0.18810   0.01571   0.01322  0.00000 ]
Pixel error:          err = [ 1.66291   1.57933 ]

Note: The numerical errors are approximately three times the standard deviations (for reference).


Recommendation: Some distortion coefficients are found equal to zero (within their uncertainties).
                To reject them from the optimization set est_dist=[0;0;1;1;0] and run Calibration

"""