import os
import random
import matplotlib.image as mpimg
import numpy as np
import cv2
import math as m
import random as rn
import json




def bnd(x_rand,y_rand,img,angl,point_det_thr):
    y_max,x_max= img.shape
    j=0
    theta=[]
    limit=[]
    dist=[]

    for i in angl:
        j+=1
        x, y, r=fnd(i,x_rand,y_rand,img,point_det_thr)
        l=(y, x)
        theta.append(i)
        limit.append(l)
        dist.append(r)
    return theta,limit,dist




def fnd(theta,or_x,or_y,img,point_det_thr):
    r=1
    y_max,x_max= img.shape
    
    while True:
        p_x=or_x + r * m.cos(theta)
        p_y=or_y + r * m.sin(theta)
        
        #print((p_y, p_x))
        
        if(p_x > x_max - 1 or p_y > y_max - 1 or p_x < 0 or p_y < 0):
            return m.inf,m.inf,r
       
        v=value(p_x,p_y,img)
        r+=1
        if(v>=point_det_thr):
            return p_x,p_y,r



def value(x,y,img):
    
    dy, dx = y - m.floor(y), x - m.floor(x)
    y0, x0 = y, x
    y1, x1 = y0 + m.ceil(dy), x0 + m.ceil(dx)
    
    p1_x,p1_y=m.floor(x0),m.floor(y0)
    p2_x,p2_y=m.floor(x0),m.floor(y1)
    p3_x,p3_y=m.floor(x1),m.floor(y0)
    p4_x,p4_y=m.floor(x1),m.floor(y1)
    
    v_00 = img[p1_y, p1_x]
    v_01 = img[p3_y, p3_x]
    v_10 = img[p2_y, p2_x]
    v_11 = img[p4_y, p4_x]
    v = np.array([
        v_00, v_01, v_10, v_11
    ])
    
    f_00 = dy * dx
    f_01 = dy * (1 - dx)
    f_10 = (1 - dy) * dx
    f_11 = (1 - dy) * (1 - dx)
    f = np.array([
        f_00, f_01, f_10, f_11
    ])
    f = 1 / (f + 1e-8)
    f /= np.sum(f)
    return np.dot(v, f)

def inter(k,origins=None, num_points_random=1,theta_range=2*m.pi, theta_offset=0,point_det_thr=1):
    ''' ORIGINS is a list of points (x, y) and if ORIGINS is None, calculate a list of random points with list length = NUM_POINTS_RANDOM'''
    box_img='/home/bvr/data/grapheks/box_thresh/sea051-lvl1-li-bl-lg.png'
    img=mpimg.imread(box_img)
    y_max,x_max= img.shape
    angl=[]
    #k=1000
    if origins is None :
        origins = [(rn.randrange(x_max), rn.randrange(y_max))
                   for _ in range(num_points_random)]
        
    for i in range(1,k):
        theta=((theta_range)/k)*i + theta_offset
        #print(m.tan(theta))
        angl.append(theta)
        res=[]
        
    for x_rand, y_rand in origins:
        #print(y_rand,x_rand)
        th,li,r= bnd(x_rand,y_rand,img,angl,point_det_thr)
        print(len(li))
        p1= [(y, x) for y, x in li if x is not m.inf and y is not m.inf]
        with open('all_values.json', 'w') as outfile:
            json.dump(li, outfile)
            
        if(len(p1)==0):
            raise IndexError("try again")            
            
        print(len(p1))    
        src = li
        p=np.array(src)
        th_0=[]
        r_0=[]
        l=len(p1)     
        ii=np.nonzero(np.all(p!=np.inf,axis=1))
        #print(ii[0])
        for i in ii[0]:
            th_0.append(th[i])
            r_0.append(r[i])   
        result={'origin':(y_rand, x_rand),'theta':th_0,'r':r_0,'p':p1,'num_points':l}
        res.append(result)
    with open('filtered.json', 'w') as outfile:
             json.dump(res, outfile)
    
    
    '''check'''
    
    b_im='/home/bvr/data/grapheks/box_thresh/sea051-lvl1-li-bl-lg.png'
    img=cv2.imread(b_im)
    img=cv2.circle(img,(x_rand,y_rand), 3, (255,0,0), 1)
    #cv2.imwrite('/home/siddharth/code/pr1/testimage.png',o)
    for yt,xt in p1:
        yt, xt = int(round(yt)), int(round(xt))
        orig_pnt=cv2.circle(img,(xt,yt), 1, (0,0,255), 1)
        #cv2.imwrite('/home/siddharth/code/pr1/testimage.png',img) 
        cv2.imwrite('/home/siddharth/code/pr1/testimage.png',orig_pnt)
        




