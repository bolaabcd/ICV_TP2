#!/usr/bin/python3
import cv2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame

window = 0                                             # glut window number
width, height = 500, 400                               # window size

texture = -1
vidcap = cv2.VideoCapture('entrada.mp4')
success,image = vidcap.read()
assert(success)
assert(image.max() <= 255 and image.min() >= 0)
cv2.imwrite('./frames/1.jpg',image)
surf = pygame.surfarray.make_surface(image)
image = pygame.image.tostring(surf, 'RGBA', 1)
ix, iy = surf.get_rect().size
texid = None

def draw_rect(x, y, width, height):
    glBegin(GL_QUADS)                                  # start drawing a rectangle
    glTexCoord2f(0,0)
    glVertex2f(x, y)                                   # bottom left point
    glTexCoord2f(1,0)
    glVertex2f(x + width, y)                           # bottom right point
    glTexCoord2f(1,1)
    glVertex2f(x + width, y + height)                  # top right point
    glTexCoord2f(0,1)
    glVertex2f(x, y + height)                          # top left point
    glEnd()                                            # done drawing a rectangle

def drawQuad(centerX, centerY, textureID):
    verts = ((1, 1), (1,-1), (-1,-1), (-1,1))
    texts = ((1, 0), (1, 1), (0, 1), (0, 0))
    surf = (0, 1, 2, 3)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textureID)

    glBegin(GL_QUADS)
    for i in surf:
        glTexCoord2f(texts[i][0], texts[i][1])
        glVertex2f(centerX + verts[i][0], centerY + verts[i][1])
    glEnd()
    
    glDisable(GL_TEXTURE_2D)

def draw():                                            # ondraw is called all the time
    global texid
    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen
    glLoadIdentity()                                   # reset position
    # refresh2d(width, height)                           # set mode to 2d


    # texid = glGenTextures(1)
    # glBindTexture(GL_TEXTURE_2D, texid)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
    #     GL_LINEAR)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
    #     GL_LINEAR)
    # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_BGRA,
    #     GL_UNSIGNED_BYTE, image)

    # glColor3f(0.0, 0.0, 1.0)                           # set color to blue

    
    
    dep = 10
    larg = 1.13
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texid)
    glBegin(GL_POLYGON)
    glTexCoord2f(1,1)
    glVertex3f(larg*dep*-6/9,larg*dep*-0.5,-dep)
    glTexCoord2f(1,0)
    glVertex3f(larg*dep*6/9,larg*dep*-0.5,-dep)
    glTexCoord2f(0,0)
    glVertex3f(larg*dep*6/9,larg*dep*0.5,-dep)
    glTexCoord2f(0,1)
    glVertex3f(larg*dep*-6/9,larg*dep*0.5,-dep)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    # x,y, width, height = -0.5, -0.5, 1, 1
    # glBegin(GL_QUADS)
    # # glTexCoord2f(0, 0)
    # glVertex3f(x, y, -2)
    # # glTexCoord2f(1, 0) 
    # glVertex3f(x + width, y, -2)
    # # glTexCoord2f(1, 1)  
    # glVertex3f(x + width, y + height, -2)
    # # glTexCoord2f(0, 1)
    # glVertex3f(x, y + height, -2)
    # glEnd()

    # draw_rect(10, 10, 200, 100)                        # rect at (10, 10) with width 200, height 100
   
    # drawQuad(0,0,texture)

    glutSwapBuffers()                                  # important for double buffering

def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()   

# # initialization
# glutInit()                                             # initialize glut
# glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
# glutInitWindowSize(width, height)                      # set window size
# glutInitWindowPosition(0, 0)                           # set window position
# window = glutCreateWindow("noobtuts.com")              # create window with title

# # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
# # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
# # texture = glGenTextures(1)
# # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image) # GL_TEXTURE_RECTANGLE
# # # glBindTexture(GL_TEXTURE_2D, texture)


# glutDisplayFunc(draw)                                  # set draw function callback
# glutIdleFunc(draw)                                     # draw all the time
# glutMainLoop()                                         # start everything


def initOpenGL(dimensions):
    global texid
    (width, height) = dimensions
    
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
 
    fovy = 45
    aspect = (width)/(height)
    gluPerspective(fovy, aspect, 0.1, 100.0)

    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
        GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
        GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_BGRA,
        GL_UNSIGNED_BYTE, image)

def idleCallback():

    glutPostRedisplay()

dimensions = (640, 480)
glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION)
glutInitWindowSize(*dimensions)
window = glutCreateWindow(b'Codigo de teste')

initOpenGL(dimensions)

glutDisplayFunc(draw)
glutIdleFunc(idleCallback)

glutMainLoop()
