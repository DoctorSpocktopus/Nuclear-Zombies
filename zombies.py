import random
import os
import numpy as np

class obj:
    def __init__(obj,char,name,hp,solid):
        obj.char=char
        obj.name = name #str, len =4
        obj.hp = hp #int 
        obj.solid = solid #int, 0-2
    def __repr__(obj):
        return "({0},{1},{2},{3})".format(obj.char,obj.name,obj.hp,obj.solid)

#Some default objects

def make_wall():
    wallchar = 'O'
    wallhp = 1000
    return obj(wallchar,"wall",wallhp,2)



##************************************************************************

## Defining player variables 

curpos = [0,0]

player = obj('@',"user",100,1)

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

def add_obj(o,x,y):
    print(objs[x,y])
    if objs[x,y] == None:
        objs[x,y]=[o,[]]
    else:
        print("2 scooops!??!?")
        multi_obj = [o,objs[x,y]]
        objs[x,y]=multi_obj
    print(objs[x,y])
    return

def remove_obj(pos):
    #print(objs[pos[0],pos[1]])
    objs[pos[0],pos[1]]=objs[pos[0],pos[1]][1]
    #print(objs[pos[0],pos[1]])

## empty(pos): Consumes a position (x,y) and returns False if something of greater
## than 0 solidness is inside the square, True otherwise. 
## empty(list(int,int)->bool)

def empty(pos):
    checksquare = objs[pos[0],pos[1]]
    if checksquare == None or checksquare == []:
        return True
    return False
        
    

def move(cmd):
    global curpos 
    
    temppos = curpos.copy()
    if   curcommand == "w":
        temppos[1]-=1
    elif curcommand == 'a':
        temppos[0]-=1
    elif curcommand == 's':
        temppos[1]+=1
    elif curcommand == 'd':
        temppos[0]+=1
    if empty(temppos):
        print("the square's empty, I swear")
        remove_obj(curpos)
        curpos = temppos
        add_obj(player,curpos[0],curpos[1])
        return True
    return False

    
for i in range(0,20):
    add_obj(make_wall(),i,1)
    add_obj(make_wall(),i,10)


add_obj(player,0,0)

while 1:
    moved = False
    while not moved:
        curcommand = input('_')
        print()
        moved = move(curcommand)
        make_screen(curpos)
    
