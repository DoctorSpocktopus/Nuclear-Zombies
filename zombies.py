import random
import os
import numpy as np
import math

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

inventory =[]

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
    if objs[x,y] == None:
        objs[x,y]=[o,[]]
    else:
        #print("2 scooops!??!?")
        multi_obj = [o,objs[x,y]]
        objs[x,y]=multi_obj
    #print(objs[x,y])
    return

def remove_obj(pos):
    #print(objs[pos[0],pos[1]])
    objs[pos[0],pos[1]]=objs[pos[0],pos[1]][1]
    #print(objs[pos[0],pos[1]])

def distance(pos1, pos2):
    dis = math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)
    return dis

def build_radius(r,x,y):
    points = []
    for i in range(-r,r):
        for j in range(-r,r):
            if distance([x,y],[i,j])<=r:
                points +=[[i,j]]
    return points

## empty(pos): Consumes a position (x,y) and returns False if something of greater
## than 0 solidness is inside the square, True otherwise. 
## empty(list(int,int)->bool)

def move_obj(obj,cmd,x,y):
    newpos = []
    if cmd == 1:
        #x-1,y+1
        newpos = [x-1,y+1]
    elif cmd == 2:
        #y+1
        newpos = [x,y+1]
    elif cmd == 3:
        #x+1,y+1
        newpos=[x+1,y+1]
        
    elif cmd == 4:
        #x-1
        newpos=[x-1,y]
        
    elif cmd == 5:
        #0
        newpos = [x,y]
    elif cmd == 6:
        #x+1
        newpos = [x+1,y]
        
    elif cmd == 7:
        #x-1,y-1
        newpos = [x-1,y-1]
        
    elif cmd == 8:
        #y-1
        newpos = [x,y-1]
    elif cmd == 9:    
        #x+1,y-1
        newpos = [x+1,y-1]
        
    if empty(newpos):
        remove_obj([x,y])
        add_obj(obj,newpos[0],newpos[1])
        return newpos
    return [x,y]

def empty(pos):
    checksquare = objs[pos[0],pos[1]]
    if checksquare == None or checksquare == []:
        return True
    if checksquare[1] == []:
        if checksquare[0].solid > 0:
            return False
        else:
            return True
    else:
        if checksquare[0].solid > 0:
            return False
        else:
            return True and empty(checksquare[1])
    

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
        #print("the square's empty, I swear")
        remove_obj(curpos)
        curpos = temppos
        add_obj(player,curpos[0],curpos[1])
        return True
    return False


##
##zzzzz  zzz  z   z zzz  zzz zzzz  zzz
##   z  z   z zz zz z  z  z  z    z
##  z   z   z z z z zzz   z  zzz   zz
## z    z   z z   z z  z  z  z       z
##zzzzz  zzz  z   z zzz  zzz zzzz zzz 
##

zombielist = []

def make_zombie(x,y):
    global zombielist 
    
    zombiehp =25
    newzombie = obj('z',"zomb",zombiehp,2) 
    zombielist += [[newzombie,x,y]]
    add_obj(newzombie,x,y)
    return newzombie




def move_zombies():
    global zombielist
    global curpos
    
    detectr = 5
    
    for z in zombielist:
        x = z[1]
        y = z[2]
        event = random.randint(1, 20)
        
        detectr = 5
        
        #random movement
        #if event in range(1,4):
        #    cmd = random.randint(1,9)
        #    newpos = move_obj(z[0],cmd,x,y)
        #    z[1]=newpos[0]
        #    z[2]=newpos[1]
        if 1:#distance([x,y],curpos)<=detectr:
            cmd = 0
            if curpos[1] == y:
                if curpos[0] == x:
                    cmd = 5
                elif curpos[0] < x:
                    cmd = 4
                elif curpos[0] > x:
                    cmd = 6
            elif curpos[1] > y:
                if curpos[0] == x:
                    cmd = 2
                elif curpos[0] < x:
                    cmd = 1
                elif curpos[0] > x:
                    cmd = 3
            elif curpos[1] < y:
                if curpos[0] == x:
                    cmd = 8
                elif curpos[0] < x:
                    cmd = 7
                elif curpos[0] > x:
                    cmd = 9
            newpos = move_obj(z[0],cmd,x,y)
            z[1]=newpos[0]
            z[2]=newpos[1]        
    return  
        
        
    
##
##  ____    _       ___    _    _  ____   ____
## |  _ \  | |     / _ \  \ \_/ / |  __| |  _ \
## | |_| | | |    | |_| |  \   /  | |_   | |_| |
## |  __/  | |    |  _  |   | |   |  _|  |    /
## | |     | |__  | | | |   | |   | |__  | |\ \
## |_|     |____| |_| |_|   |_|   |____| |_| \_\
##

def action(cmd):
    global inventory
    global curpos
    if cmd in ["w","a","s","d"]:
        return move(cmd)
    elif cmd == 'g':
        items = []
        remove_obj(curpos)
        here=objs[curpos[0],curpos[1]]
        print(here)
        while here != []:
            print(here) 
            items += [here[0]]
            remove_obj(curpos)
            here=objs[curpos[0],curpos[1]]            
        inventory += items
        print(inventory)
        add_obj(player,curpos[0],curpos[1])
        return True 
    else:
        return False


##  _    _          
## |_|xx|X|XXXXXXXX|||
##      |X|         $
##      |X|         $
##      |X|      SETTING
##      |X| PROPS & 

add_obj(player,0,0)

for i in range(0,20):
    add_obj(make_wall(),i,1)
    add_obj(make_wall(),i,10)

add_obj(obj('=',"ammo",20,0),1,0)

make_zombie(0,2)
make_zombie(0,3)
make_zombie(2,0)
make_zombie(2,2)
make_zombie(2,3)
make_zombie(4,15)

##******************************************************************************
##******************************************************************************
##******************************************************************************


##
##The little loop that could 
##

make_screen(curpos)

while 1:
    actioned = False
    while not actioned:
        move_zombies()
        curcommand = input('_')
        print()
        actioned = action(curcommand)
        make_screen(curpos)
    #print(curpos)
