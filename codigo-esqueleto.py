#!/usr/bin/python3

import cv2

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PIL import Image

from objloader import *

vidcap = cv2.VideoCapture('entrada.mp4')
success,image = vidcap.read()
assert(success)
assert(image.max() <= 255 and image.min() >= 0)
surf = pygame.surfarray.make_surface(image)
image = pygame.image.tostring(surf, 'RGBA', 1)
ix, iy = surf.get_rect().size
background_texture = None
pikapika = None
 
def initOpenGL(dimensions):
    global background_texture
    global pikapika
    (width, height) = dimensions
    
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
 
    fovy = 45
    aspect = (width)/(height)
    gluPerspective(fovy, aspect, 0.1, 100.0)


    pikapika = OBJ("Pikachu.obj", swapyz=True)

    background_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, background_texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
        GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
        GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_BGRA,
        GL_UNSIGNED_BYTE, image)

def object3D(obj):

    # translada o objeto para ficar 10 unidades distante da camera (para podermos ver o objeto)
    glTranslate(0,0,-10)

    # move o model em y para centralizar ele
    glTranslate(0,-2,0)
    # rotaciona o modelo para podermos ve-lo de frente
    #glRotate(90,1,0,0)
    glRotate(-90,1,0,0)
    # renderiza o modelo do Pikachu
    glCallList(obj.gl_list)

    # renderiza um cubo
    glutWireCube(2.0)

def draw_background():
    global background_texture
    depth = 10
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

def update_image():
    global background_texture
    global vidcap

    success,image = vidcap.read()
    # assert(success)
    if not success:
        vidcap = cv2.VideoCapture('entrada.mp4')
        success,image = vidcap.read()

    assert(image.max() <= 255 and image.min() >= 0)
    cv2.imwrite('./frames/1.jpg',image)
    surf = pygame.surfarray.make_surface(image)
    image = pygame.image.tostring(surf, 'RGBA', 1)
    ix, iy = surf.get_rect().size
    # glTexSubImage2D(GL_TEXTURE_2D, 0, 0,0, ix, iy, GL_BGRA,
    #     GL_UNSIGNED_BYTE, image)
    glBindTexture(GL_TEXTURE_2D, background_texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_BGRA,
        GL_UNSIGNED_BYTE, image)

def displayCallback():
    global pikapika


    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Desenhar fundo
    update_image()
    draw_background()

    # carregar o modelo 3D do Pikachu
    glEnable(GL_TEXTURE_2D)
    object3D(pikapika) 
    glDisable(GL_TEXTURE_2D)


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