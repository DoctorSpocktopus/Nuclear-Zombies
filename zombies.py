import random
import os
import numpy as np

class obj:
    def __init__(obj,x,y,char,name,hp,solid):
        obj.x = x #int
        obj.y = y #int
        obj.char=char
        obj.name = name #str, len =4
        obj.hp = hp #int 
        obj.solid = solid #int, 0-2
    def __repr__(obj):
        return "({0},{1},{2},{3},{4},{5})".format(obj.x,obj.y,obj.char,obj.name,obj.hp,obj.solid)

#Some default objects

def make_wall(x,y):
    wallchar = 'O'
    wallhp = 1000
    return obj(x,y,wallchar,"wall",wallhp,2)

##************************************************************************

## Defining player variables 

curpos = [0,0]

player = obj(0,0,'@',"user",100,1)

##************************************************************************


##terminal is 23 characters high, -1 for the input line 

screen_size = [55,21]

map_size = [200,200]

objs = np.empty((map_size[0],map_size[1]),dtype=type(player),order='C')


def make_screen(pos):
    
    screen = ""
    
    xpos = pos[0]-(screen_size[0]//2)
    ypos = pos[1]-(screen_size[1]//2)
     
    for y in range(ypos,ypos+screen_size[1]):
        for x in range(xpos,xpos+screen_size[0]):
            curobj = objs[x,y]
            if curobj:
                if type(curobj) != type(player):
                    curobj = curobj[0]
                screen+=curobj.char
            else:
                screen+='.'
        screen+="\n"
        
    print(screen)
    
    return

def add_obj(o):
    if not objs[o.x,o.y]:
        objs[o.x,o.y]=o
    else:
        print("2 scooops!??!?")
        multi_obj = [o,objs[o.x,o.y]]
        objs[o.x,o.y]=multi_obj
    return

def remove_obj(pos):
    if type(objs[pos[0],pos[1]])==type(player):    
        objs[pos[0],pos[1]]=''
    #else:
     #   objs[pos[0],pos[1]]=objs[pos[0],pos[1]][1]
    
for i in range(0,20):
    add_obj(make_wall(i,1))
    add_obj(make_wall(i,10))



while 1:
    curcommand = input('_')
    print()
    remove_obj(curpos)
    if   curcommand == "w":
        curpos[1]-=1
    elif curcommand == 'a':
        curpos[0]-=1
    elif curcommand == 's':
        curpos[1]+=1
    elif curcommand == 'd':
        curpos[0]+=1
    player.x=curpos[0]
    player.y=curpos[1]
    add_obj(player)
    make_screen(curpos)