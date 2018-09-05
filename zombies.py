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
    def __eq__(self,other):
        return self.name == other.name
    def __ne__(self,other):
        return not self.__eq__(other)
        

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



##Prints off a screen representing the current play area

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

##adds an object o at position (x,y) in the obj array
def add_obj(o,x,y):
    if objs[x,y] == None:
        objs[x,y]=[o,[]]
    else:
        #print("2 scooops!??!?")
        multi_obj = [o,objs[x,y]]
        objs[x,y]=multi_obj
    #print(objs[x,y])
    return

##removes the top object at the position
def remove_obj(pos):
    objs[pos[0],pos[1]]=objs[pos[0],pos[1]][1]
    
## Calculates the distance between two objects 
def distance(pos1, pos2):
    dis = math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)
    return dis

##build_radius builds a circle of radius r around point pos. 
##
## build_radius(r,pos) :
##     int Pos -> list(Pos)

def build_radius(r,pos):
    points = []
    for i in range(-r,r):
        for j in range(-r,r):
            if distance(pos,[i,j])<=r:
                points +=[[i,j]]
    return points

def build_vector(pos,dr):
    vector = []
    newpos = pos.copy()
    x=newpos[0]
    y=newpos[1]
    i = 1
    if dr == 1:
        while newpos[0] > 0 and newpos[1] < map_size[1]:
            newpos = [x-i,y+i]
            vector += [newpos.copy()] 
            i += 1
    elif dr == 2:
        while newpos[1] < map_size[1]:
            newpos = [x,y+i]
            vector += [newpos.copy()]
            print (newpos)
            i+=1
    elif dr == 3:
        while newpos[0] < map_size[0] and newpos[1] < map_size[1]:
            newpos=[x+i,y+i]
            vector += [newpos.copy()]
            i+=1
    elif dr == 4:
        while newpos[0] > 0:
            newpos=[x-i,y]
            vector += [newpos.copy()]
            i+=1
    elif dr == 6:
        while newpos [0] < map_size[0]:
            newpos = [x+i,y]      
            vector += [newpos.copy()]
            i+=1
    elif dr == 7:
        while newpos[0] > 0 and newpos[1] >0:
            newpos = [x-i,y-i]
            vector += [newpos.copy()]
            i+=1
    elif dr == 8:
        while newpos[1] > 0:
            newpos = [x,y-i]
            vector += [newpos.copy()]
            i+=1
    elif dr == 9:    
        while newpos[0] < map_size[0] and newpos[1] > 0:
            newpos = [x+i,y-i] 
            vector += [newpos.copy()]
            i+=1
    return vector
    
        
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
################################################################################
##                                                                            ##
##                  ZZZZ   ZZZ  Z   Z ZZZ  ZZZ ZZZZ  ZZZ                      ##
##                     Z  Z   Z ZZ ZZ Z Z   Z  Z    Z                         ##
##                    Z   Z   Z Z Z Z ZZZ   Z  ZZZ   ZZ                       ##
##                   Z    Z   Z Z   Z Z  Z  Z  Z       Z                      ##
##                  ZZZZ   ZZZ  Z   Z ZZZ  ZZZ ZZZZ ZZZ                       ##
##                                                                            ##
################################################################################

zombielist = []

## make_zombie(x,y) mutates the zombie list to add an additional zombie. Also
##    adds it to the object list. 
## make_zombie int int -> obj

def make_zombie(x,y):
    
    if x < 0 or x > map_size[0] or y < 0 or y >map_size[1]:
        return []

    global zombielist 
    
    zombiehp = 25
    newzombie = obj('z',"zomb",zombiehp,2) 
    zombielist += [[newzombie,x,y]]
    add_obj(newzombie,x,y)
    return newzombie

## move_zombies() : mutates the objects array to change the positions of the 
##     zombies
##
    

def move_zombies():
    global zombielist
    global curpos
    
    detectr = 5
        
        
    #The basket out of 1-20 where the zombie moves randomly
    randmove = range(1,4)
    #The basket out of 1-20 where the zombie moves towards the player
    dirmove = range(5,15)
         
    # makes a copy of the zombie list, then creates a list of their positions
    zombiepos = zombielist.copy()
    zombiepos = map(lambda z: [z[1],z[2]],zombiepos)
    
    for z in zombielist:
        x = z[1]
        y = z[2]
        
        zpos = [0,0]
        
        event = random.randint(1, 20)
        
        #checks if zombie is not there and removes it if it isn't
        if not objs[x,y] or objs[x,y][0].name != "zomb":
            zombielist.remove(z)
            continue
        
        
        #determines if the zombie is close to any other zombies
        closez = False
        rad = build_radius(detectr,[x,y])
        for p in rad:
            if p in zombiepos:
                zpos = p
                closez = True
                break
        
        #determines if the zombie is close to the player
        close = (distance([x,y],curpos)<=detectr)
        #resets the directional movement variables if the player is close
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
        ## moves towards the player
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
        ## moves towards a zombie
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
    return  
        
        
    
##
##  ____    _       ___    _    _  ____   ____
## |  _ \  | |     / _ \  \ \_/ / |  __| |  _ \
## | |_| | | |    | |_| |  \   /  | |_   | |_| |
## |  __/  | |    |  _  |   | |   |  _|  |    /
## | |     | |__  | | | |   | |   | |__  | |\ \
## |_|     |____| |_| |_|   |_|   |____| |_| \_\
##

## shoot : takes nothing, then creates a vector. Examines 

def shoot():
    
    def hit(obj,x,y):   
        weapon_damage = 400+random.randint(5,20)
        obj.hp -= weapon_damage
        if obj.hp <= 0:
            remove_obj([x,y])    
    
    global curpos
    misschance = 0.25
    cmd = int(input(" _"))
    vec = build_vector(curpos,cmd)
    running_objs = []
    for i in vec:
        if objs[i[0],i[1]]:
            running_objs = objs[i[0],i[1]]
            if running_objs[0].solid == 1:
                if random.random() > misschance :
                    hit(running_objs[0],i[0],i[1])
                    return
            elif running_objs[0].solid ==2:
                hit(running_objs[0],i[0],i[1])
                return
            
    
        
    

## action : takes a command, cmd, (number from 1-4,6-9, or 'g') and then returns 
##    True if an action was taken, False otherwise. 
##
##action : Char -> Bool
##

def action(cmd):
    global inventory
    global curpos
    if cmd in ['1','2','3','4','6','7','8','9']:
        temppos = curpos.copy()
        curpos = move_obj(player,int(cmd),curpos)
        return not(curpos == temppos)
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
    ## Shooting
    elif cmd == '5':
        ## Checks for ammo first
        if not obj('=','ammo',20,0) in inventory:
            return False
        shoot()
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

for i in range(2,map_size[0]-1):
    add_obj(make_wall(),i,0)
    add_obj(make_wall(),i,1)
    add_obj(make_wall(),i,2)
    add_obj(make_wall(),i,map_size[1]-1)
    add_obj(make_wall(),i,map_size[1]-2)
    add_obj(make_wall(),i,map_size[1]-3)

for i in range(2,map_size[1]-2): 
    add_obj(make_wall(),0,i) 
    add_obj(make_wall(),1,i) 
    add_obj(make_wall(),2,i)
    add_obj(make_wall(),map_size[0]-1,i)   
    add_obj(make_wall(),map_size[0]-2,i)   
    add_obj(make_wall(),map_size[0]-3,i)

level = 1

if level == 1:
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
    
    add_obj(make_wall(),110,106)
    add_obj(make_wall(),110,105)
    
    add_obj(obj('=',"ammo",20,0),100,105)
    add_obj(obj('=',"ammo",20,0),100,106)
    
    ##
    ## HOME OF THE BADDIES!
    ##
    
    make_zombie(100,98)
    make_zombie(101,98)
    make_zombie(102,98)
    make_zombie(103,98)
    make_zombie(104,98)


##******************************************************************************
##******************************************************************************
##******************************************************************************


##
##The little loop that could 
##

make_screen(curpos)

while 1:
    actioned = False
    move_zombies()
    while not actioned:
        make_screen(curpos)
        print()
        curcommand = input('_')
        if curcommand == "r":
            some = int(input("#100s?"))
            try:
                for n in range(1,some):
                    for i in range(1,100):
                        move_zombies()
            except:
                print(zombielist)
        elif curcommand == 'f':
            print(zombielist)
            checker = input("pos?")
            make_screen(list(map(int,checker.split(','))))
            input()
        actioned = action(curcommand)
    #print(curpos)
