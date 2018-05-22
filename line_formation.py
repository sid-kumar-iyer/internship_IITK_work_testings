import json
import math as m
import numpy as np
import random as r
import cv2



def line_f(m_c_thresh, dis_thresh):

    b_im='/home/bvr/data/grapheks/box_thresh/sea051-lvl1-li-bl-lg.png'
    img=cv2.imread(b_im)

    with open('filtered.json') as json_file:  
        data = json.load(json_file)
    origin=data[0]['origin'] 

    with open('parameters_of_lines.json') as json_file:  
        data = json.load(json_file)


    #thresh = 0.8
    v = [(m, c) for _, li, m, c in data if li > m_c_thresh]


    l=len(v)
    #print(l)
    V=np.array(v)
    print(V.shape)
    M=V[:,0]
    C=V[:,1]
    dist=np.full((l,l),0., dtype=np.float32)
    for i in range(l):
        for j in range(i+1,l):
            dist[i,j] = np.linalg.norm(V[i]-V[j])
    x_0=np.zeros(l)
    x_1=np.full((l,),828)
    y_0=C
    y_1=M*x_1+C
    XY=np.stack((x_0,y_0,x_1, y_1)).T
    XY=np.round(XY).astype(np.int)
    print(len(XY))


    res=[]
    #dis_thresh=3
    lab=0
    for i in range(l):
        for j in range(i+1,l):
            if(dist[i,j]<dis_thresh):
                res.append((lab,v[i],v[j],i+1,j+1))
            else:
                 res.append((1,v[i],v[j],i+1,j+1)) 

    for x0,y0,x1,y1 in XY:
        img=cv2.line(img,(x0,y0),(x1,y1),(255,0,0),1)

    orig_pnt=cv2.circle(img,(origin[1],origin[0]), 3, (0,0,255), 1)
    # origin[::-1]

    cv2.imwrite('/home/siddharth/code/pr1/line_connections.png',img)     
    cv2.imwrite('/home/siddharth/code/pr1/line_connections.png',orig_pnt)

