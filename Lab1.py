import numpy as np
from PIL import Image, ImageOps
import math
#создали матрицу
img_mat=np.zeros((2000, 2000, 3), dtype=np.uint8)#unsigned int восьмибитный

def draw_line0(image, x0, y0, x1, y1, color): #с шагом
    step=1/100
    for t in np.arange (0, 1, step):
        x = round ((1.0 - t)*x0 + t*x1)
        y = round ((1.0 - t)*y0 + t*y1)
        image[y, x] = color

def draw_line1(image, x0, y0, x1, y1, color):#шаг от значений
    count = math.sqrt((x0 - x1)**2 +(y0 - y1)**2)
    step=1/count
    for t in np.arange (0, 1, step):
        x = round ((1.0 - t)*x0 + t*x1)
        y = round ((1.0 - t)*y0 + t*y1)
        image[y, x] = color

def draw_line2(image, x0, y0, x1, y1, color): #по x
    for x in range (x0, x1):
        t = (x-x0)/(x1 - x0)
        y = round ((1.0 - t)*y0 + t*y1)
        image[y, x] = color

def draw_line3(image, x0, y0, x1, y1, color): #по x если x0 > x1
    if (x0 > x1):
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    for x in range (x0, x1):
        t = (x-x0)/(x1 - x0)
        y = round ((1.0 - t)*y0 + t*y1)
        image[y, x] = color

def draw_line4(image, x0, y0, x1, y1, color): #по x если x0 > x1 и меняем y на x если больше
    xchange = False
    if (abs(x0 -x1) < abs(y0 - y1)):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    if (x0 > x1):
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    for x in range (x0, x1):
        t = (x-x0)/(x1 - x0)
        y = round ((1.0 - t)*y0 + t*y1)
        if (xchange):
            image[x, y] = color
        else:
            image[y, x] = color

def draw_line5(image, x0, y0, x1, y1, color): #по x если x0 > x1 и меняем y на x если больше, y убираем
    xchange = False
    derror = 0.0
    
    if (abs(x0 -x1) < abs(y0 - y1)): #меняем y на x если больше
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    if (x0 > x1): #если x0 > x1
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    y = y0
    dy = abs(y1 - y0)/(x1 - x0)

    if (y1 > y0):
        y_update = 1
    else:
        y_update = -1

    for x in range (x0, x1): #сам цикл который рисует
        if (xchange):
            image[x, y] = color
            
        else:
            image[y, x] = color
        derror += dy
        if (derror > 0.5):
            derror -= 1.0
            y += y_update

#Умножим все части, которые посвящены вычислению шага, на 2*(x1 - x0)
def draw_line6(image, x0, y0, x1, y1, color): #Алгоритм Брезенхема
    xchange = False
    derror = 0.0
    
    if (abs(x0 -x1) < abs(y0 - y1)): #меняем y на x если больше
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    if (x0 > x1): #если x0 > x1
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    y = y0
    dy = 2*abs(y1 - y0) #умножили на 2 тут

    if (y1 > y0):
        y_update = 1
    else:
        y_update = -1

    for x in range (x0, x1): #сам цикл который рисует
        if (xchange):
            image[x, y] = color
            
        else:
            image[y, x] = color
        derror += dy
        if (derror > (x1 - x0)): #умножили на 2 тут
            derror -= 2*(x1 - x0) #умножили на 2 тут
            y += y_update

#циклы лучше не использовать в питоне, но мы будем
for i in range(2000):
    for j in range(2000):
        #img_mat[i, j]=[randint(0, 255), randint(0, 255), randint(0, 255)]
        img_mat[i, j]=[255, 255, 255] 

""""
for k in range(13):
        x0, y0= 100, 100
        x1=int(100+95*math.cos((2*3.14/13)*k))
        y1=int(100+95*math.sin((2*3.14/13)*k))
        #draw_line0(img_mat, x0, y0, x1, y1, [0, 0, 0])
        #draw_line1(img_mat, x0, y0, x1, y1, [0, 0, 0])
        #draw_line2(img_mat, x0, y0, x1, y1, [0, 0, 0])
        #draw_line3(img_mat, x0, y0, x1, y1, [0, 0, 0])
        #draw_line4(img_mat, x0, y0, x1, y1, [0, 0, 0])
        #draw_line5(img_mat, x0, y0, x1, y1, [0, 0, 0])
        draw_line6(img_mat, x0, y0, x1, y1, [0, 0, 0])
"""

file=open('model_1.obj')
v=[]
f=[]
for s in file:
    sp=s.split()
    if(sp[0]=='v'):
        v.append([float(sp[1]), float(sp[2]),float(sp[3])])
    if(sp[0]=='f'):
        f.append([int(sp[1].split('/')[0]), int(sp[2].split('/')[0]), int(sp[3].split('/')[0])])
#for i in range(0, len(v)):
    #img_mat[int(8000*v[i][1]+1000), int(8000*v[i][0]+1000)]=[0, 0, 0]
for k in range (len(f)):
    x0=int(8000*v[f[k][0]-1][0]+1000)
    y0=int(8000*v[f[k][0]-1][1]+1000)
    x1=int(8000*v[f[k][1]-1][0]+1000)
    y1=int(8000*v[f[k][1]-1][1]+1000)
    x2=int(8000*v[f[k][2]-1][0]+1000)
    y2=int(8000*v[f[k][2]-1][1]+1000)
    draw_line6(img_mat, x0, y0, x1, y1, [64, 224, 208])
    draw_line6(img_mat, x0, y0, x2, y2, [64, 224, 208])
    draw_line6(img_mat, x2, y2, x1, y1, [64, 224, 208])


            

#сохраняем картинку в файл
img=Image.fromarray(img_mat, mode='RGB') #mode l чб, ргб и так понятно
img.save('img.png')