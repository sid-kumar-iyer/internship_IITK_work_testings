
import json
import math as m

def s(l,n):
    x=0
    xy=0
    y=0
    x2=0
    for i in range(n):
            xy+=l[i][0] * l[i][1]
            x+=l[i][0]
            y+=l[i][1]
            x2+=l[i][0] ** 2
    return x,y,xy,x2

def linearity(l,n):
    dis=0
    for i in range(n-1):
        dis+=m.sqrt((l[i][0]-l[i+1][0]) ** 2 + (l[i][1]-l[i+1][1]) ** 2)
    lin=(m.sqrt((l[0][0]-l[n-1][0]) ** 2 + (l[0][1]-l[n-1][1]) ** 2 ))/dis
    return lin

def slope(l,n):
    x,y,xy,x2=s(l,n)
    m=(n * xy - (x * y))/(n*x2 - x ** 2)
    return m


def intercept(l,n):
    x,y,xy,x2=s(l,n)
    c=(x2 * y - (x * xy))/(n*x2 - (x ** 2))
    return c

if __name__ == "__main__":
    with open('filtered.json') as json_file:  
        data = json.load(json_file)
    data=data[0]['p']
    div=30    
    rem=len(data)%div
    n=len(data)-rem
    lab=0
    f_data=[]
    flag=0
    for i in range(0,n,15):
    
        if(flag==1):

            break
        l=[]
        for j in range(i,i+div):

            l.append(data[j])
            if(i+div == n):

                flag=1
        li=[]    
        li.append(lab)    
        li.append(linearity(l,div))
        li.append(slope(l,div))
        li.append(intercept(l,div))
        lab+=1
        f_data.append(li)
l=[]            
for i in range(n,len(data),1):
    l.append(data[i])
for i in range(0,div-rem):
    l.append(data[i])
        
li=[]
li.append(lab)
li.append(linearity(l,div))
li.append(slope(l,div))
li.append(intercept(l,div))
f_data.append(li)
with open('parameters_of_lines.json','w') as json_file:
    json.dump(f_data,json_file) 