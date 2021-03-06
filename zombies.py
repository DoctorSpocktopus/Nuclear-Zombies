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
    wallhp = 200
    return obj(wallchar,"wall",wallhp,2)




##************************************************************************

## Defining player variables 

curpos = [100,103]

player = obj('@',"user",100,1)

# Zombies need to role over this number to hit
player_armour = 15

# Starting inventory
inventory = []

# Starting ammo count
ammo = 0 

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
        ## The number of lines from the top where the display comes from
        starting_line = 2
        if y==ypos+starting_line:
            screen+="          Ammo"
        if y==ypos+starting_line+1:
            global ammo
            ammo_str = ""
            for j in range(0,ammo):
                ammo_str += "!"
            for j in range(0,13-ammo):
                ammo_str += "-"
            screen+="          "+ammo_str            
        if y==ypos+starting_line+3:
            screen+="          Health"
        if y==ypos+starting_line+4:
            hp_str=""
            for j in range(0,player.hp//20):
                hp_str+="<3"
            for j in range(0,5-player.hp//20):
                hp_str+="__"
            screen+="          "+hp_str
        screen+="\n"
        
    print(screen)
    
    return

##adds an object o at position (x,y) in the obj array
def add_obj(o,x,y): 
    if objs[x,y] == None:
        objs[x,y]=[o]
    else:
        #print("2 scooops!??!?")
        multi_obj = [o]+objs[x,y]
        objs[x,y]=multi_obj
    #print(objs[x,y])
    return

##removes the top object at the position
def remove_obj(pos):
    objs[pos[0],pos[1]]=objs[pos[0],pos[1]][1:]
    
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
    for i in range(pos[0]-r,pos[0]+r):
        for j in range(pos[0]-r,pos[0]+r):
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
    for i in checksquare:
        if i.solid > 0:
            return False
    return True
        

def make_refuse():
    rfse = obj("%","rfse",100,0)
    return(rfse)

##
##
##
##
        
bomblist = []
        
def make_bomb(pos):
    global bomblist
    bomb = obj('*',"bomb",1,0)
    bomblist += [[bomb,pos[0],pos[1]]]
    add_obj(bomb,pos[0],pos[1])
    return 

#implement recursively with recursive helper that removes extras

def null_obj():
    return obj(".","null",1,0)


def explosion(pos):
    blast_radius = 4
    blast_damage = 40+random.randint(1,20)
    rad = build_radius(blast_radius,pos)
    for p in rad: 
        p_o_list = objs[p[0],p[1]]
        if p_o_list:
            for i in range(0,len(p_o_list)):
                o=p_o_list[i]
                o.hp -= blast_damage 
                if o.hp <= 0:
                    p_o_list[i] = null_obj()
                    if o.solid > 0:
                        p_o_list[i] = make_refuse()
            #This could cause issues later on - shallow vs deep copy?
            new_p_o_list = p_o_list.copy()
            print(p_o_list)
            for o in p_o_list:
                try:
                    new_p_o_list = new_p_o_list.remove(null_obj())
                except:
                    pass
            p_o_list=new_p_o_list
            print(p_o_list)
            

def use_bombs():
    global bomblist
    for b in bomblist:
        explosion([b[1],b[2]])
    bomblist = []
    
        
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
    global player
    global player_armour
    
    detectr = 5
        
        
    #The basket out of 1-20 where the zombie moves randomly
    randmove = range(1,4)
    #The basket out of 1-20 where the zombie moves towards the player
    dirmove = range(5,15)
         
    # makes a copy of the zombie list, then creates a list of their positions
    zombiepos = zombielist.copy()
    zombiepos = list(map(lambda z: [z[1],z[2]],zombiepos))
    
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
        
        
        detectr = 10
        stealth = 6
        
        #determines if the zombie is close to the player
        close = (distance([x,y],curpos)<=stealth)

        #resets the directional movement variables if the player is close
        
        if close : 
            attack = distance([x,y],curpos) <=math.sqrt(2)   
            
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
            if not attack:
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
            else:
                if random.randint(1,20)>=player_armour:
                    player.hp -= 10 + random.randint(1,20)
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

## shoot : takes nothing, then creates a vector. Examines each sqaure in the 
## vector's path and reduces the health by 

def shoot():
    
    global ammo
    
    def hit(obj,x,y):   
        weapon_damage = 10+random.randint(5,20)
        obj.hp -= weapon_damage
        if obj.hp <= 0:
            remove_obj([x,y])    
            add_obj(make_refuse(),x,y)
    
    global curpos
    misschance = 0.25
    try:
        cmd = int(input(" _"))
    except:
        return
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
        global ammo
        ## Checks for ammo first
        if ammo <= 0:
            if not obj('=','ammo',20,0) in inventory:
                return False
            ## Reload
            inventory.remove(obj('=','ammo',20,0))
            ammo = 13
        ammo -= 1
        shoot()
        return True
    ## do nothing
    elif cmd == '.':
        return True
    ## detonate bombs
    elif cmd == 'c':
        use_bombs()
        return True
    else:
        return False


##  ____    _    _          _        ____   ____   ____   ____
## |____|  |_|xx|X|XXXXXXXX|||      |____| |____| |____| |____|
## |____|       |X|         $       |____| |____| |____| |____|
## |____|       |X|         $       |____| |____| |____| |____|
## |____|       |X|      SETTING    |____| |____| |____| |____|
## |____|       |X| PROPS &         |____| |____| |____| |____|


##



add_obj(player,curpos[0],curpos[1])

##
## Outer borders 
##

## building(ulpos,size,doordir): creates a size x size square "building" 
## which has upper left corner at position ulpos, and "doors" (open
## spaces) at sides indicated in doordir
##
## doordir is a multiple of all desired door edges

##  2 OO 3 OO5
##  O        O
## 19        7
##  O        O
## 17OO 13 OO11

##For example, if you wanted the top and bottom to be open, you would set 
## doordir = 3*5
##For a box with no corners, 
## doordir = 2*5*11*17
##For a box with only corners,
## doordir = 3*7*13*19
##For nothing,
## doordir = 3*7*13*19*2*5*11*17
##For everything,
## doordir = 1

def make_building(ulpos,size,doordir):
    
    if doordir % 2 != 0:
        add_obj(make_wall(),ulpos[0],ulpos[1])
    if doordir % 3 != 0:
        for i in range(1,size-1):
            add_obj(make_wall(),ulpos[0]+i,ulpos[1])
    if doordir % 5 != 0:
        add_obj(make_wall(),ulpos[0]+size-1,ulpos[1])
    if doordir % 7 != 0: 
        for i in range(1,size-1):
            add_obj(make_wall(),ulpos[0]+size-1,ulpos[1]+i)
    if doordir % 11 != 0: 
        add_obj(make_wall(),ulpos[0]+size-1,ulpos[1]+size-1)
    if doordir % 13 != 0:
        for i in range(1,size-1):
            add_obj(make_wall(),ulpos[0]+i,ulpos[1]+size-1)
    if doordir % 17 != 0:
        add_obj(make_wall(), ulpos[0],ulpos[1]+size-1)
    if doordir % 19 != 0: 
        for i in range(1,size-1):
            add_obj(make_wall(), ulpos[0], ulpos[1]+i)
    return

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
    
    #for i in range(1,5):
    add_obj(obj('=',"ammo",20,0),101,101)
    add_obj(obj('=',"ammo",20,0),101,102)
    add_obj(obj('=',"ammo",20,0),101,103)
    add_obj(obj('=',"ammo",20,0),101,104)
    add_obj(obj('=',"ammo",20,0),101,105)
    
    
    make_building([100,100],11,19*13)
    make_building([89,100],11,19*7)
    make_building([78,100],11,13*7)
    for i in range(0,4):    
        add_obj(obj('=',"ammo",20,0),92+i,103)
        add_obj(obj('=',"ammo",20,0),92,103+i)
        add_obj(obj('=',"ammo",20,0),92+i,103+4)
        add_obj(obj('=',"ammo",20,0),92+4,103+i) 
    add_obj(obj('=',"ammo",20,0),92+4,103+4) 
    make_building([93,104],3,1)
    add_obj(obj('=',"ammo",20,0),94,105) 
    
    make_building([91,102],7,1)
    
    make_building([100,111],6,3*13)
    make_building([105,111],6,3*13)
    make_building([100,117],11,3*19)

    
    make_building([78,111],6,3*13)
    make_building([83,111],6,3*13)
    make_building([78,117],11,3*7)    
    
    make_building([89,117],11,19*7*13)
    make_building([92,125],5,2*5*11*17)
    make_building([93,126],3,1)
    
    make_building([70,141],60,2*5*7*11*13*17*19)
    
    ##
    ## HOME OF THE BADDIES!
    ##
    
    make_zombie(101,97)
    make_zombie(101,98)
    make_zombie(102,98)
    make_zombie(103,98)
    make_zombie(104,98)
    for i in range(1,30):
        make_zombie(94+random.randint(-10,10),130+random.randint(1,10))
        
    ##bombs 
    
    add_obj(obj('=',"ammo",20,0),101,102)
    add_obj(obj('=',"ammo",20,0),101,103)
    add_obj(obj('=',"ammo",20,0),101,104)    
    make_bomb([101,101])

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
        if player.hp <= 0:
            add_obj(obj('%',"dead",1,1),curpos[0],curpos[1])
            make_screen(curpos)
            input("You fall, only to rise as a member of the shambling dead")
            exit()
            
    #print(curpos)
