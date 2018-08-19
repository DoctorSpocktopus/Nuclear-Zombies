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

curpos = [100,103]

player = obj('@',"user",100,1)

inventory = []

##************************************************************************


##terminal is 23 characters high, -1 for the input line 

screen_size = [21,21]

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
    objs[pos[0],pos[1]]=objs[pos[0],pos[1]][1]
    
def distance(pos1, pos2):
    dis = math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)
    return dis

def build_radius(r,pos):
    points = []
    for i in range(-r,r):
        for j in range(-r,r):
            if distance(pos,[i,j])<=r:
                points +=[[i,j]]
    return points

## empty(pos): Consumes a position (x,y) and returns False if something of greater
## than 0 solidness is inside the square, True otherwise. 
## empty(list(int,int)->bool)

def move_obj(obj,cmd,pos):
    newpos = pos.copy()
    x=newpos[0]
    y=newpos[1]
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
        remove_obj([pos[0],pos[1]])
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
##ZZZZ   ZZZ  Z   Z ZZZ  ZZZ ZZZZ  ZZZ
##   Z  Z   Z ZZ ZZ Z Z   Z  Z    Z   
##  Z   Z   Z Z Z Z ZZZ   Z  ZZZ   ZZ
## Z    Z   Z Z   Z Z  Z  Z  Z       Z
##ZZZZ   ZZZ  Z   Z ZZZ  ZZZ ZZZZ ZZZ 
##

zombielist = []

def make_zombie(x,y):
    global zombielist 
    
    zombiehp =25
    newzombie = obj('z',"zomb",zombiehp,2) 
    zombielist += [[newzombie,x,y]]
    add_obj(newzombie,x,y)
    return newzombie

## Need to impliment sorting of zombie array by distance from somewhere
    

def move_zombies():
    global zombielist
    global curpos
    
    detectr = 5
        
    randmove = range(1,4)
    dirmove = range(5,15)
    
    lastz = zombielist[0]
    
    zombiepos = zombielist.copy()
    zombipos = map(lambda z: [z[1],z[2]],zombiepos)
    
    for z in zombielist:
        x = z[1]
        y = z[2]
        
        zpos = [0,0]
        
        event = random.randint(1, 20)
        
        rad = build_radius(detectr,[x,y])
        
        close = (distance([x,y],curpos)<=detectr)
        closez = False        
        
        for p in rad:
            if p in zombipos:
                zpos = p
                closez = True
                break
        
        detectr = 5
        if close : 
            randmove = [1]
            dirmove = range(2,20)        
        else:
            randmove = range(1,10)
            dirmove = range(11,20)            
        
        ## random movement
        if event in randmove or (not close and not closez):
            cmd = random.randint(1,9)
            newpos = move_obj(z[0],cmd,[x,y])
            z[1]=newpos[0]
            z[2]=newpos[1]
        elif close and (event in dirmove):
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
            newpos = move_obj(z[0],cmd,[x,y])
            z[1]=newpos[0]
            z[2]=newpos[1]
        #moves towards a zombie
        elif closez and (event in dirmove):
            cmd = 0
            if zpos[1] == y:
                if zpos[0] == x:
                    cmd = 5
                elif zpos[0] < x:
                    cmd = 4
                elif zpos[0] > x:
                    cmd = 6
            elif zpos[1] > y:
                if zpos[0] == x:
                    cmd = 2
                elif zpos[0] < x:
                    cmd = 1
                elif zpos[0] > x:
                    cmd = 3
            elif zpos[1] < y:
                if zpos[0] == x:
                    cmd = 8
                elif zpos[0] < x:
                    cmd = 7
                elif zpos[0] > x:
                    cmd = 9
            newpos = move_obj(z[0],cmd,[x,y])
            z[1]=newpos[0]
            z[2]=newpos[1]            
        lastz = z
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
    if cmd in ['1','2','3','4','6','7','8','9']:
        curpos = move_obj(player,int(cmd),curpos)
        return True
    elif cmd == 'g':
        items = []
        remove_obj(curpos)
        here=objs[curpos[0],curpos[1]]
        while here != []:
            items += [here[0]]
            remove_obj(curpos)
            here=objs[curpos[0],curpos[1]]
        inventory += items
        add_obj(player,curpos[0],curpos[1])
        return True 
    else:
        return False


##  ____    _    _          _        ____   ____   ____   ____
## |____|  |_|xx|X|XXXXXXXX|||      |____| |____| |____| |____|
## |____|       |X|         $       |____| |____| |____| |____|
## |____|       |X|         $       |____| |____| |____| |____|
## |____|       |X|      SETTING    |____| |____| |____| |____|
## |____|       |X| PROPS &         |____| |____| |____| |____|

add_obj(player,curpos[0],curpos[1])

##
## Outer borders 
##

for i in range(0,map_size[0]-1):
    add_obj(make_wall(),i,0)
    add_obj(make_wall(),i,map_size[1]-1)

for i in range(0,map_size[1]-1): 
    add_obj(make_wall(),0,i) 
    add_obj(make_wall(),map_size[0]-1,i)   

##
## Starting building
##

for i in range(90,111):
    add_obj(make_wall(),i,101)
    add_obj(make_wall(),i,110)
for i in range(101,105): 
    add_obj(make_wall(),90,i)
    add_obj(make_wall(),110,i)      
for i in range(107,110): 
    add_obj(make_wall(),90,i)
    add_obj(make_wall(),110,i)      

add_obj(obj('=',"ammo",20,0),100,105)
add_obj(obj('=',"ammo",20,0),100,106)

make_zombie(2,2)


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
        if curcommand == "r":
            some = int(input("#100s?"))
            for n in range(1,some):
                for i in range(1,100):
                    move_zombies()
            make_screen(curpos)
        print()
        actioned = action(curcommand)
        make_screen(curpos)
    #print(curpos)
