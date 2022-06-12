#!/usr/bin/python3

from operator import is_
import cv2
from cv2 import threshold
import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PIL import Image
from PIL import ImageOps

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
target = cv2.imread('alvo.jpg')
target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
_, target = cv2.threshold(target, 127, 255, cv2.THRESH_BINARY)

cameraMatrix = np.array(
    [
        [305.63204, 0        , 307.02195],
        [0        , 299.37624, 258.75539],
        [0        , 0        , 1        ],
    ], dtype = np.float64
)
cameraMatrix = np.array(
    [
        [305.63204*1.3, 0        , 327.02195],
        [0        , 299.37624*1.3, 248.75539],
        [0        , 0        , 1        ],
    ], dtype = np.float64
)

distCoeffs = np.array([-0.03318, 0.09094, 0.02252, 0.00253, 0.00000], dtype = np.float64)

# distCoeffs = np.array([0.09043, -0.20861 , -0.00432, -0.00635, 0.00000], dtype = np.float64)


openCV_to_openGL = np.array(
    [
        [1, 0, 0,0],
        [0,-1, 0,0],
        [0, 0,-1,0],
        [0, 0, 0,1]
    ]
    , dtype = np.float64
)

rotval = 0


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

def object3D(obj, tra, rotation, colr): # x,y,z is the world position
    global openCV_to_openGL, rotval
    rot = cv2.Rodrigues(rotation)[0]

    viewmat = np.zeros((4,4),dtype = np.float64)
    for i in range(3):
        for j in range(3):
            viewmat[i][j] = rot[i][j]
        viewmat[i][3] = tra[i][0]
    viewmat[3][3] = 1
    viewmat = viewmat.T

    viewmat = viewmat @ openCV_to_openGL

    if (tra[0] > -1.24 and tra[0] < 4.92 and tra[1] > -5.87 and tra[1] < -2.83 and tra[2] > 10.68 and tra[2] < 16.26):
        rotval *= -1


    # glTranslate(3,-2,0)
    glPushMatrix()
    glLoadMatrixd(viewmat)

    # glTranslate(x,y,z)
    # glMultMatrixf(rotation)
    # glRotate(-90,1,0,0)

    glDisable(GL_TEXTURE_2D)

    glRotate(-90,1,0,0)
    glColor(1/2,0,0)
    gluCylinder( gluNewQuadric() , 1/10 , 1/10 , 3 , 10 , 10)

    glTranslate(0,0,3)
    glutSolidCone(1/2,1,10,10)
    glTranslate(-0,-0,-3)

    glColor(1,1,1)
    glRotate(90,1,0,0)
    # if tra[0] > -1.24 and tra[0] < 4.92 and tra[1] > -5.87 and tra[1] < -2.83 and tra[2] > 10.68 and tra[2] < 16.26: #not (tra[0] >= -1.5 and tra[1] >= -6 and tra[2] >= 10.5):
    #     glColor(*colr)
    glutWireCube(3)
    # if tra[0] > -1.24 and tra[0] < 4.92 and tra[1] > -5.87 and tra[1] < -2.83 and tra[2] > 10.68 and tra[2] < 16.26: #not (tra[0] >= -1.5 and tra[1] >= -6 and tra[2] >= 10.5):
    #     glColor(1,1,1)
    glEnable(GL_TEXTURE_2D)
    # renderiza o modelo do Pikachu
    glTranslate(0,0,-1)
    glRotate(rotval,0,0,1)
    glCallList(obj.gl_list)
    glRotate(-rotval,0,0,1)
    glTranslate(0,0,1)
    # glRotate(90,1,0,0)
    # glTranslate(0,0,1)

    # glTranslate(0,0,-1)
    # glRotate(-rotation[0],rotation[1],rotation[2],rotation[3])
    # glMultMatrixf(rotation.T)

    glPopMatrix()
    # glTranslate(-3,2,0)
    # glTranslate(-x,-y,-z)

    if (tra[0] > -1.24 and tra[0] < 4.92 and tra[1] > -5.87 and tra[1] < -2.83 and tra[2] > 10.68 and tra[2] < 16.26):
        rotval *= -1
    rotval+=1
    

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

def get_targets(quads):
    global target
    global image

    grayimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, trimg = cv2.threshold(grayimg, 127, 255, cv2.THRESH_BINARY)

    retq, reto = [], []
    for quad in quads:
        twid, thei = target.shape[0], target.shape[1]
        input_points = quad.tolist()
        output_points = np.array([[0,thei-1],[0,0],[twid-1,0]])
        for j in range(4):
            input_points2 = np.array(input_points[:-1]).astype(np.float32)
            output_points = output_points.astype(np.float32)

            wa = cv2.getAffineTransform(input_points2, output_points)
            dst = cv2.warpAffine(trimg,wa,(twid,thei))

            sim = ((dst-dst.mean())/dst.std()*(target-target.mean())/target.std()).mean()

            # cv2.imshow(str(test) + ' ' +str(j) + ' ' + str(sim),dst)
            # cv2.waitKey()
            input_points = [input_points[-1]]+input_points[:-1]
            if sim >= 50/100: # normalized cross-correlation
                # input_points = [input_points[3], input_points[2], input_points[1], input_points[0]]
                # input_points = [input_points[-1]]+input_points[:-1]
                # input_points = [input_points[-1]]+input_points[:-1]
                # input_points = [input_points[-1]]+input_points[:-1]
                # input_points = [input_points[-1]]+input_points[:-1]
                # print(input_points)
                retq.append(np.array(input_points, dtype = np.float32))
                reto.append(j)
                break
    return retq, reto

def find_good_quadrilaterals(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, tr = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(tr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    quads = []

    test = 0
    for cnt in cnts:
        approx = cv2.approxPolyDP(
            cnt, 0.02 * cv2.arcLength(cnt, True), True)
    
        if len(approx) == 4 and approx[0][0][0] != 0 and area_rect_pixels(approx[:,0]) > 1000:
            quads.append(approx[:,0])
            # print(cnt, approx[:,0])

            # # debugging targets:
            # global target
            # grayimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # _, trimg = cv2.threshold(grayimg, 127, 255, cv2.THRESH_BINARY)

            # twid, thei = target.shape[0], target.shape[1]
            # input_points = approx[:,0].tolist()
            # output_points = np.array([[0,thei-1],[0,0],[twid-1,0]])
            # draw = False
            # for j in range(4):
            #     input_points2 = np.array(input_points[:-1]).astype(np.float32)
            #     output_points = output_points.astype(np.float32)

            #     wa = cv2.getAffineTransform(input_points2, output_points)
            #     dst = cv2.warpAffine(trimg,wa,(twid,thei))

            #     # sim = np.abs(dst - target).mean()
            #     sim = ((dst-dst.mean())/dst.std()*(target-target.mean())/target.std()).mean()
            #     # cv2.imshow(str(test) + ' ' +str(j) + ' ' + str(sim),dst)
            #     # cv2.waitKey()
            #     input_points = [input_points[-1]]+input_points[:-1]
            #     if sim >= 50/100: # normalized cross-correlation
            #         draw = True
            #         break
            # if draw:
            #     cv2.drawContours(image, [cnt], 0, (0, 0, 255), 5) # para debugar, mostra quadrilateros
    return image, quads

def update_image():
    global background_texture
    global vidcap
    global image
    global imagepygame
    global cameraMatrix
    global distCoeffs

    success,image = vidcap.read()
    if not success:
        vidcap = cv2.VideoCapture('entrada.mp4')
        success,image = vidcap.read()
    assert(success)
    assert(image.max() <= 255 and image.min() >= 0)

    image, quads = find_good_quadrilaterals(image)
    where_pika, orientation = get_targets(quads)
    # print(orientation)
    where_pika = np.array(where_pika, dtype = np.float64)
    siz = 2
    # obj_pts = np.array([[0,0,siz],[0,0,0],[siz,0,0],[siz,0,siz]], dtype = np.float64)
    obj_pts = np.array([[siz/2,-siz/2,0],[-siz/2,-siz/2,0],[-siz/2,siz/2,0],[siz/2,siz/2,0]], dtype = np.float64)

    rot1 = rot2 = rot3 = np.array([[0],[0],[0]], dtype = np.float64)
    tra1 = tra2 = tra3 = np.array([[100],[100],[100]], dtype = np.float64)

    if len(where_pika) > 0:
        success, rot1, tra1 = cv2.solvePnP(obj_pts, where_pika[0], cameraMatrix, distCoeffs)
        assert(success)
    if len(where_pika) > 1:
        success, rot2, tra2 = cv2.solvePnP(obj_pts, where_pika[1], cameraMatrix, distCoeffs)
        assert(success)
    if len(where_pika) > 2:
        success, rot3, tra3 = cv2.solvePnP(obj_pts, where_pika[2], cameraMatrix, distCoeffs)
        assert(success)
    # print("img:")
    # print(where_pika)
    # print("rots:")
    # print(rot1)
    # print(rot2)
    # print(rot3)
    # print("trs:")
    # print(tra1)
    # print(tra2)
    # print(tra3)
    # cv2.imshow('a',image)
    # cv2.waitKey()
    # tra1[0][0] = 3.4
    # tra1[1][0] = 1.8
    # tra1[2][0] = 11.99
    # tra1[0][0] -= 1.2
    # tra1[1][0] -= 0.208
    # tra1 -= [[1.2],[0.208],[0]]
    # tra2 -= [[-1.2],[-0.208],[0]]
    # tra3 -= [[1.2],[-2.208],[0]]
    # tra1[1]+=1
    # tra2[1]+=1
    # tra3[1]+=1
    # tra1/=1.3
    # tra1[2]*=1.3
    # tra2/=1.3
    # tra2[2]*=1.3
    # tra3/=1.3
    # tra3[2]*=1.3

    surf = pygame.surfarray.make_surface(image)
    imagepygame = pygame.image.tostring(surf, 'RGBA', 1)
    ix, iy = surf.get_rect().size
    glBindTexture(GL_TEXTURE_2D, background_texture)
    glTexSubImage2D(GL_TEXTURE_2D, 0, 0,0, ix, iy, GL_BGRA,
        GL_UNSIGNED_BYTE, imagepygame)
    # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_BGRA,
    #     GL_UNSIGNED_BYTE, image) # para debugar, mais lento que subimage mas menos chance de erro
    return (rot1, tra1), (rot2, tra2), (rot3, tra3)

tra1lim, tra2lim, tra3lim = ((-1e8, 1e8), (-1e8, 1e8), (-1e8, 1e8)), ((-1e8, 1e8), (-1e8, 1e8), (-1e8, 1e8)), ((-1e8, 1e8), (-1e8, 1e8), (-1e8, 1e8))
framem = 0
def displayCallback():
    global pikapika1
    global pikapika2
    global pikapika3
    global tra1lim, tra2lim, tra3lim, framem

    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # glTranslate(10,0,-50) # pra ver mei de lado, debugar
    # glRotate(45,0,1,0)
    
    # Atualizar imagem
    (rot1, tra1), (rot2, tra2), (rot3, tra3) = update_image()
    # Desenhar fundo
    draw_background()

    # carregar o modelo 3D dos Pikachus
    # print("Tras:")
    # print(tra1)
    # print(tra2)
    # print(tra3)
    # if framem == 544 or framem == 582 or framem == 1082:
    #     tra1lim, tra2lim, tra3lim = ((-1e8, 1e8), (-1e8, 1e8), (-1e8, 1e8)), ((-1e8, 1e8), (-1e8, 1e8), (-1e8, 1e8)), ((-1e8, 1e8), (-1e8, 1e8), (-1e8, 1e8))
    # if tra1[0][0] != 100:
    #     tra1lim = (
    #         (max(tra1lim[0][0], tra1[0][0]), min(tra1lim[0][1], tra1[0][0])),
    #         (max(tra1lim[1][0], tra1[1][0]), min(tra1lim[1][1], tra1[1][0])),
    #         (max(tra1lim[2][0], tra1[2][0]), min(tra1lim[2][1], tra1[2][0]))
    #     )
    # if tra2[0][0] != 100:
    #     tra2lim = (
    #         (max(tra2lim[0][0], tra2[0][0]), min(tra2lim[0][1], tra2[0][0])),
    #         (max(tra2lim[1][0], tra2[1][0]), min(tra2lim[1][1], tra2[1][0])),
    #         (max(tra2lim[2][0], tra2[2][0]), min(tra2lim[2][1], tra2[2][0]))
    #     )
    # if tra3[0][0] != 100:
    #     tra3lim = (
    #         (max(tra3lim[0][0], tra3[0][0]), min(tra3lim[0][1], tra3[0][0])),
    #         (max(tra3lim[1][0], tra3[1][0]), min(tra3lim[1][1], tra3[1][0])),
    #         (max(tra3lim[2][0], tra3[2][0]), min(tra3lim[2][1], tra3[2][0]))
    #     )
    # print("Lims: ")
    # print(tra1lim)
    # print(tra2lim)
    # print(tra3lim)
    # print(framem)
    framem += 1
    # cv2.imshow('a',image)
    # cv2.waitKey()
    object3D(pikapika1,tra1,rot1, (1,0,0))
    object3D(pikapika1,tra2,rot2, (0,1,0)) 
    object3D(pikapika1,tra3,rot3, (0,0,1)) 

    # glRotate(-45,0,1,0)
    # glTranslate(-10,-0,50)
    glutSwapBuffers()    
    if framem > 1:
        pix = glReadPixels(0,0,640,480,GL_RGBA,GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGBA", (640, 480), pix)
        image = ImageOps.flip(image) # in my case image is flipped top-bottom for some reason
        image.save('./framesafter/arq'+str(framem)+'.png', 'PNG')
    

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