import numpy as np
from PIL import Image, ImageOps
import math
from random import randint
import sys
#создали матрицу
img_mat=np.zeros((2000, 2000, 3), dtype=np.uint8)#unsigned int восьмибитный
color=[64, 224, 208]

z_buf=np.zeros((2000, 2000, 1)) #z буффер
for i in range(2000):
    for j in range(2000):
        z_buf[i][j]=sys.maxsize


def bar(x0, y0, x1, y1, x2, y2, x, y):
    lambda0 = ((x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)) /  ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2)) 
    lambda1 = ((x0 - x2) * (y - y2) - (x - x2) * (y0 - y2)) /  ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lambda2 = 1.0 - lambda0 - lambda1

    return [lambda0, lambda1, lambda2]


def triangle(x0, y0, x1, y1, x2, y2, z0, z1, z2, img_mat):
    xmin = int(min(x0, x1, x2))
    xmax = int(max(x0, x1, x2))+1 #округлил вверх
    ymin = int(min(y0, y1, y2))
    ymax = int(max(y0, y1, y2))+1
    if (xmin < 0): 
        xmin = 0 
    if (ymin < 0): 
        ymin = 0 
    if (xmax>2000): 
        xmax=2000
    if (ymax>2000): 
        ymax=2000
    
    cos=cos_light(x0, y0, x1, y1, x2, y2, z0, z1, z2)
    if (cos>0):
        return

    #проверяем барицентрические координаты
    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            temp = bar(x0, y0, x1, y1, x2, y2, x, y)
            z=temp[0]*z0+temp[1]*z1+temp[2]*z2
            if (temp[0]>=0 and temp[1]>=0 and temp[2]>=0 and z<z_buf[y, x]):
                img_mat[y, x]=[cos*-255, cos*-255, 0]
                z_buf[y, x]=z

def n(x0, y0, x1, y1, x2, y2, z0, z1, z2):
    a = np.array([x1-x2, y1-y2, z1-z2])  
    b = np.array([x1-x0, y1-y0, z1-z0])  
    return np.cross(a, b) #векторное произведение

def cos_light(x0, y0, x1, y1, x2, y2, z0, z1, z2):
    n1=n(x0, y0, x1, y1, x2, y2, z0, z1, z2)
    l=[0,0,1]
    np0=np.dot(n1, l) #скалярное произведение
    n_l=np.sqrt(np.dot(n1, n1)) #длина вектора нормы
    temp = np0/n_l
    return temp


#циклы лучше не использовать в питоне, но мы будем
for i in range(2000):
    for j in range(2000):
        #img_mat[i, j]=[randint(0, 255), randint(0, 255), randint(0, 255)]
        img_mat[i, j]=[255, 255, 255] 


file=open('model_1.obj')
v=[]
f=[]
for s in file:
    sp=s.split()
    if(sp[0]=='v'):
        v.append([float(sp[1]), float(sp[2]),float(sp[3])])
    if(sp[0]=='f'):
        f.append([int(sp[1].split('/')[0]), int(sp[2].split('/')[0]), int(sp[3].split('/')[0])])

for k in range (len(f)):
    x0=v[f[k][0]-1][0]*8000+1000
    y0=v[f[k][0]-1][1]*8000+1000
    x1=v[f[k][1]-1][0]*8000+1000
    y1=v[f[k][1]-1][1]*8000+1000
    x2=v[f[k][2]-1][0]*8000+1000
    y2=v[f[k][2]-1][1]*8000+1000

    z0=v[f[k][0]-1][2]*8000+1000
    z1=v[f[k][1]-1][2]*8000+1000
    z2=v[f[k][2]-1][2]*8000+1000

    triangle(x0, y0, x1, y1, x2, y2, z0, z1, z2, img_mat)

#triangle(0.0, 0.0, 0.1, 0.0, 0.0, 0.1, img_mat)

            
#сохраняем картинку в файл
img=Image.fromarray(img_mat, mode='RGB') #mode l чб, ргб и так понятно
img = ImageOps.flip(img)
img.save('img.png')