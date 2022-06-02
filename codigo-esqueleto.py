#!/usr/bin/python3

import numpy as np
import cv2

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PIL import Image

from objloader import *
count = 0
texture = None
# tw, th = None, None

def initOpenGL(dimensions):

    (width, height) = dimensions
    
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
 
    fovy = 45
    aspect = (width)/(height)
    gluPerspective(fovy, aspect, 0.1, 100.0)
        
def object3D(obj):

    # translada o objeto para ficar 10 unidades distante da camera (para podermos ver o objeto)
    glTranslate(0,0,-10)

    # move o model em y para centralizar ele
    glTranslate(0,-2,0)
    # rotaciona o modelo para podermos ve-lo de frente
    # glRotate(90,1,0,0)
    glRotate(-90,1,0,0)
    # renderiza o modelo do Pikachu
    glCallList(obj.gl_list)

    # renderiza um cubo
    glutWireCube(2.0)

# def get_texture(image):
#     global texture
#     # # glUnbindTexture(GL_TEXTURE_2D, texture)
#     # # print(image)
#     # glDeleteTextures(1,texture)
#     # assert(image.max() <= 255 and image.min() >= 0)

#     # if texture == None:
#     #     texture = glGenTextures(1)

#     # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,   
#     #     GL_LINEAR)
#     # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
#     #     GL_LINEAR)
#     # # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
#     # image = np.array([[[255,0,0]]])
#     # image.astype(np.uint8)
#     # print(texture,image.shape)
#     # # glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
#     # # glPixelStorei(GL_UNPACK_ROW_LENGTH, 0);
#     # # glPixelStorei(GL_UNPACK_SKIP_PIXELS, 0);
#     # # glPixelStorei(GL_UNPACK_SKIP_ROWS, 0);
#     # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.shape[0], image.shape[1], 0, GL_RGBA,
#     #     GL_UNSIGNED_BYTE, image)
#     # #glBindTexture(GL_TEXTURE_2D, texture)

#     # Create one OpenGL texture
#     # GLuint textureID;
    
#     return texture

def draw_texture(image):
    global texture
    # glColor3f(1.0, 1.0, 1.0)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    # glBindTexture(GL_TEXTURE_2D, image)
    x, y, width, height = -0.5, -0.5, 1.0, 1.0
    glDisable(GL_TEXTURE_2D)

    glBegin(GL_QUADS)
    # glTexCoord2f(0, 0)
    glVertex3f(x, y, -2)
    # glTexCoord2f(1, 0) 
    glVertex3f(x + width, y, -2)
    # glTexCoord2f(1, 1)  
    glVertex3f(x + width, y + height, -2)
    # glTexCoord2f(0, 1)
    glVertex3f(x, y + height, -2)
    glEnd()
    
def displayCallback():
    global vidcap
    global count
    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    
    # carregar o modelo 3D do Pikachu
    obj = OBJ("Pikachu.obj", swapyz=True)

    # habilita o uso de texturas (o Pikachu tem textura)
    glEnable(GL_TEXTURE_2D)

    # vidcap = cv2.VideoCapture('entrada.mp4')
    # sucess,image = -1,-1
    # for i in range(count):
    #     success,image = vidcap.read()
    # if not sucess:
    #     vidcap = cv2.VideoCapture('entrada.mp4')
    #     success,image = vidcap.read()
    # count += 1
    
    success,image = vidcap.read()
    if success:
      count += 1
    else:
      count = 0
      vidcap = cv2.VideoCapture('entrada.mp4')
    # draw_texture(image)
    glEnable(GL_TEXTURE_2D)
    # # draw_image(image)
    # text = get_texture(image)
    # glBindTexture(GL_TEXTURE_2D, text)
    # glBegin(GL_QUADS);
    # # glTexCoord2f(0.0f, 0.0f);
    # glVertex3f(-0.5, -0.5, -10.0);
    # # glTexCoord2f(1.0f, 0.0f);
    # glVertex3f(0.5, -0.5, -10.0);
    # # glTexCoord2f(1.0f, 1.0f);
    # glVertex3f(0.5, 0.5, -10.0);
    # # glTexCoord2f(0.0f, 1.0f);
    # glVertex3f(-0.5, 0.5, -10.0);
    # glEnd();
    # glutWireCube(2.0)
    # glDisable(GL_TEXTURE_2D)
    object3D(obj)
        
    glutSwapBuffers()    
    

def idleCallback():

    glutPostRedisplay()
    
    
if __name__ == '__main__':

    import cv2
    # global tw, th

    vidcap = cv2.VideoCapture('entrada.mp4')
    success,image = vidcap.read()
    # count = 1
    # cv2.imwrite("./frames/frame%d.jpg" % count, image)
    
    texture = glGenTextures(1)

    tw, th = image.shape[0], image.shape[1]

    # "Bind" the newly created texture : all future texture functions will modify this texture
    glBindTexture(GL_TEXTURE_2D, texture)

    # Give the image to OpenGL
    glTexImage2D(GL_TEXTURE_2D, 0,GL_RGB, image.shape[0], image.shape[1], 0, GL_BGR, GL_UNSIGNED_BYTE, image)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)




    dimensions = (640, 480)
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION)
    glutInitWindowSize(*dimensions)
    window = glutCreateWindow(b'Realidade Aumentada [codigo esqueleto]')
    
    initOpenGL(dimensions)
    
    glutDisplayFunc(displayCallback)
    glutIdleFunc(idleCallback)
    
    glutMainLoop()