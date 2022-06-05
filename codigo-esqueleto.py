#!/usr/bin/python3

import cv2
import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


from objloader import *

vidcap = cv2.VideoCapture('entrada.mp4')
success,image = vidcap.read()
assert(success)
assert(image.max() <= 255 and image.min() >= 0)
surf = pygame.surfarray.make_surface(image)
imagepygame = pygame.image.tostring(surf, 'RGBA', 1)
ix, iy = surf.get_rect().size
background_texture = None
pikapika1 = None
pikapika2 = None
pikapika3 = None
 
def initOpenGL(dimensions):
    global background_texture
    global imagepygame
    global pikapika1
    global pikapika2
    global pikapika3
    (width, height) = dimensions
    
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
 
    fovy = 45
    aspect = (width)/(height)
    gluPerspective(fovy, aspect, 0.1, 100.0)


    pikapika1 = OBJ("Pikachu.obj", swapyz=True)
    pikapika2 = OBJ("Pikachu.obj", swapyz=True)
    pikapika3 = OBJ("Pikachu.obj", swapyz=True)

    background_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, background_texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
        GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
        GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_BGRA,
        GL_UNSIGNED_BYTE, imagepygame)

def object3D(obj, x, y, z, rotation): # x,y,z is the world position
    glTranslate(x,y,z)
    glRotate(*rotation)
    # renderiza o modelo do Pikachu
    glCallList(obj.gl_list)

    glTranslate(0,0,1)
    glutWireCube(2)

    glTranslate(0,0,-1)
    glRotate(-rotation[0],rotation[1],rotation[2],rotation[3])
    glTranslate(-x,-y,-z)
    

def draw_background():
    global background_texture
    depth = 100 # max profundidade
    scale = 1.13
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, background_texture)
    glBegin(GL_POLYGON)
    glTexCoord2f(1,1)
    glVertex3f(scale*depth*-6/9,scale*depth*-0.5,-depth)
    glTexCoord2f(1,0)
    glVertex3f(scale*depth*6/9,scale*depth*-0.5,-depth)
    glTexCoord2f(0,0)
    glVertex3f(scale*depth*6/9,scale*depth*0.5,-depth)
    glTexCoord2f(0,1)
    glVertex3f(scale*depth*-6/9,scale*depth*0.5,-depth)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def area_rect_pixels(coords):
    assert(len(coords) == 4)
    p1,p2,p3,p4 = coords
    return abs(np.cross(p2-p1,p4-p1)/2)+abs(np.cross(p2-p3,p4-p3)/2)

def find_good_quadrilaterals(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, tr = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(tr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    quads = []

    for cnt in cnts:
        approx = cv2.approxPolyDP(
            cnt, 0.02 * cv2.arcLength(cnt, True), True)
    
        if len(approx) == 4 and approx[0][0][0] != 0 and area_rect_pixels(approx[:,0]) > 1000:
            quads.append(approx[:,0])
            # cv2.drawContours(image, [cnt], 0, (0, 0, 255), 5) # para debugar, mostra quadrilateros
    return image, quads

def update_image():
    global background_texture
    global vidcap
    global image
    global imagepygame

    success,image = vidcap.read()
    if not success:
        vidcap = cv2.VideoCapture('entrada.mp4')
        success,image = vidcap.read()
    assert(success)
    assert(image.max() <= 255 and image.min() >= 0)

    image, quads = find_good_quadrilaterals(image)

    surf = pygame.surfarray.make_surface(image)
    imagepygame = pygame.image.tostring(surf, 'RGBA', 1)
    ix, iy = surf.get_rect().size
    glBindTexture(GL_TEXTURE_2D, background_texture)
    glTexSubImage2D(GL_TEXTURE_2D, 0, 0,0, ix, iy, GL_BGRA,
        GL_UNSIGNED_BYTE, imagepygame)
    # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_BGRA,
    #     GL_UNSIGNED_BYTE, image) # para debugar, mais lento que subimage mas menos chance de erro

def displayCallback():
    global pikapika1
    global pikapika2
    global pikapika3

    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # glTranslate(10,0,-10) # pra ver mei de lado, debugar
    # glRotate(45,0,1,0)
    
    # Desenhar fundo
    update_image()
    draw_background()

    # carregar o modelo 3D do Pikachu
    glEnable(GL_TEXTURE_2D)
    object3D(pikapika1,3,-2,-10,(-90,1,0,0)) 
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_2D)
    object3D(pikapika2,-3,-2,-10,(-90,1,0,0)) 
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_2D)
    object3D(pikapika3,0,-2,-10,(-90,1,0,0)) 
    glDisable(GL_TEXTURE_2D)

    # glRotate(-45,0,1,0)
    # glTranslate(-10,-0,10)
    glutSwapBuffers()    
    

def idleCallback():

    glutPostRedisplay()
    
    
if __name__ == '__main__':
    
    dimensions = (640, 480)
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION)
    glutInitWindowSize(*dimensions)
    window = glutCreateWindow(b'Realidade Aumentada: Pikachu')
    
    initOpenGL(dimensions)
    
    glutDisplayFunc(displayCallback)
    glutIdleFunc(idleCallback)
    
    glutMainLoop()