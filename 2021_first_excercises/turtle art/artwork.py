from turtle import Turtle
from random import random, randint, seed
from math import sin
 
colordeck=['maroon','crimson','red','#ff5500','#ffaa00','yellow','green yellow','lime','cyan','#0064ff','blue','purple']
#I have to use custom oranges and a custom blue because the regular colors look eggregious
 
def cut_colordeck(r):
    """
    (int) -> list
    returns a copy of the color deck that has the same order but has all of it's elements moved forward by an index r
    
    >>>cut_colordeck(2)
    ['red', '#ff5500', '#ffaa00', 'yellow', 'green yellow', 'lime', 'cyan', '#0064ff', 'blue', 'purple', 'maroon', 'crimson']
    >>>cut_colordeck(11)
    ['purple', 'maroon', 'crimson', 'red', '#ff5500', '#ffaa00', 'yellow', 'green yellow', 'lime', 'cyan', '#0064ff', 'blue']
    >>>cut_colordeck(0)
    ['maroon','crimson','red','#ff5500','#ffaa00','yellow','green yellow','lime','cyan','#0064ff','blue','purple']
    """
    r%=12
    return colordeck[r:]+colordeck[:r]
'''
def goto(t,x,y): #this function doesnt even save me time or anything, so useless
    t.penup()
    t.goto(x,y)
    t.pendown
'''
 
def diamond(size, angle, pitch, color, t):
    """
    (num,num,num,str,turtle)->void
    produces a diamond with given specification at the location of the turtle
    >>>t=Turtle()
    >>>diamond(0,0,0,'red',t)
    >>>diamond(50,20,0,'red',t)
    >>>diamond(90,90,55,'orange',t)
    """
    # I put the t=Turtle call in the diamondcircle function because i wanted to put a goto command.
    #t.color(color)#
    t.fillcolor(color)
    t.begin_fill()#
    t.left(90+angle/2-pitch)
    t.forward(size) # I tried using a for loop here and it was a mess. For loop would be more useful with a
    t.right(angle)  # shape that has more sides. 4 sides just isnt worth the effort.
    t.forward(size)
    t.right(180-angle)
    t.forward(size)
    t.right(angle)
    t.forward(size)
    t.end_fill()#
    t.right(270-angle/2-pitch) # I want the orientation to reset after im done so diamondcircle can properly work
    
def fandiamond_rainbow(size,angle,pitch,x,y):
    """
    (num,num,num,num) -> void
    produces a triple radius of diamons with rainbow color and descending size. produces rainbow effect.
    >>>fandiamond_rainbow(90,30,40,0,0)
    >>>fandiamond_rainbow(90,40,30,50,50)
    >>>fandiamond_rainbow(0,0,0,0,0)
    """
    t=Turtle()
    t.hideturtle()
    t.speed('fastest')
    t.penup()
    t.goto(x,y)
    t.pendown()
    difference=360*random() #i want the shape to start at a random orientation, looks nice
    ratio=0.97
    deck=cut_colordeck(randint(0,12)) #starting at marron/red is 2x as likely
    for i in range(2):
        for c in deck:
            diamond(size,angle,difference,c,t)
            size*=ratio
            difference+=pitch
            pitch*=0.95
            angle*=0.98
            ratio*=0.995
 
def fandiamond_fade(color,fade,size,angle,pitch,x,y):
    """
    (str,str,num,num,num,num) -> void
    produces a triple radius of diamons with rainbow color and descending size. Produces fade effect
    >>>fandiamond_fade('0000000','+11+11+11',90,30,40,0,0)
    >>>fandiamond_fade('ffffff','-11-11-11',90,30,40,0,0)
    >>>fandiamond_fade('ff5500','-0f+04+10',90,30,40,0,0)
    """
    t=Turtle()
    t.hideturtle()
    t.speed('fastest')
    t.penup()
    t.goto(x,y)
    t.pendown() # I made this function after fandiamond_rainbow, enough of the code is different 
    difference=360*random() # that configuring a help is more time consuming
    ratio=0.97
    c_red=color[0:2]
    c_green=color[2:4]
    c_blue=color[4:6]
    colorcode=[c_red,c_green,c_blue]
    fade_red=int(fade[0:3],16)
    fade_green=int(fade[3:6],16)
    fade_blue=int(fade[6:9],16)
    fadecode=[fade_red,fade_green,fade_blue]
    for i in range(30):
        for j in range(3):
            colorcode[j]=int(colorcode[j],16)
            colorcode[j]+=fadecode[j]
            if colorcode[j]>255:
                colorcode[j]=255
                #fadecode[j]=0
            elif colorcode[j]<0:
                colorcode[j]=0
                #fadecode[j]=0
            colorcode[j]=hex(colorcode[j])[2:]
            colorcode[j]='0'*(2-len(colorcode[j]))+colorcode[j]
        
        c='#'+''.join(colorcode)
        diamond(size,angle,difference,c,t)
        size*=ratio
        difference+=pitch
        pitch*=0.95
        angle*=0.98
        ratio*=0.995
    
    
def draw_J(t,size):
    """
    (turtle,num)->void
    produces a J at the location of the turtle of desired size
    >>>t=Turtle()
    >>>draw_J(t,0)
    >>>draw_J(t,50)
    >>>draw_J(t,-12)
    """
    t.forward(size/3)
    t.backward(2*size/3)
    t.forward(size/3)
    t.right(90)
    t.forward(size)
    t.right(180)
    t.circle(size/3,-180) #THIS WORKS!!!
    t.right(-90)
    
def initials(x,y,size,pitch):
    """
    (num,num,num,num)->void
    produces a copy of JJ with with given specifications
    >>>initials(0,0,50,0)
    >>>initials(50,50,60,150)
    >>>initials(-400,350,60,10)
    """
    t=Turtle()
    t.hideturtle()
    t.penup()
    t.goto(x,y)
    t.pendown()
    t.right(-pitch)
    t.color('dark slate blue')
    draw_J(t,size)
    t.penup()
    t.goto(x-size/5,y-size/3)
    t.pendown()
    t.color('indigo')
    draw_J(t,size)
 
def funky(level,Φ,colors):
    """
    (num,num,num)->void
    produces 2 sine waves out of phase by Φ with a colored interior on the y level 'level'
    >>>funky(0,0,1)
    >>>funky(-300,50,4)
    >>>funky(0,100,11)
    """
    deck=cut_colordeck(randint(0,11))
    start=-600
    t=Turtle()
    t.hideturtle()
    s=Turtle()
    s.hideturtle()
    s.penup()
    t.penup()
    t.hideturtle()
    s.hideturtle()
    t.speed('fastest')
    s.speed('fastest')
    t.penup()
    t.goto(start,level)
    t.pendown()
    s.penup()
    s.goto(start+Φ,level)
    s.pendown()
    c=0
    j=0
    color_dir='up'
    for i in range(400):
        t_x=3*i+start
        t_y=sin(3*i/30)*30+level
        s_x=3*i+start
        s_y=sin(3*(i+Φ)/30)*30+level
        t.goto(t_x,t_y)
        s.goto(s_x,s_y)
        if j>0:
            j-=1     #this is required, otherwise the function will skip colors
            continue # Nevertheless, at particular y levels and phases, it still doesnt work!!! >:(
        if t_y//5==s_y//5: #This piece of code is beyond repair!
            s.goto(t_x,t_y)
            s.fillcolor(deck[c%colors])
            t.fillcolor(deck[c%colors])
            t.end_fill()
            s.end_fill()
            t.begin_fill()
            s.begin_fill()
            if color_dir=='up':  #i did this because i wanted to keep color order
                c+=1
                if c>=colors-1:
                    color_dir='down'
            else:
                c-=1
                if c<=0:
                    color_dir='up'
            j=5
        #this is already far too much
 
def random_polygon():
    '''
    void->void
    creates a polygon of random color and of random sides at position (0,240)
    >>>random_polygon()
    '''
    t=Turtle()
    t.hideturtle()
    t.penup()
    t.goto(0,240)
    t.pendown
    n=randint(3,10)
    a=360/n
    c=colordeck[randint(0,11)]
    t.fillcolor(c)
    t.begin_fill()
    for i in range(n):
        t.forward(30)
        t.right(a)
    t.end_fill() #this really looks out of place in the drawing, but i have already spent too much time!
    
def my_artwork():
    """
    void-> void
    draws my masterpiece
    >>>my_artwork()
    """
    
    for i in range(0,8):
        funky(-350+i*100,randint(9,12)*10,randint(2,5)) # it is a shame i must cherry pick here. the function really cannot handle
                                                        # most inputs. The small phase selection really hurts
    
    for i in [-1,1]:
        for j in [-1,1]:
            c=randint(0,16777215)
            c=hex(c)[2:]
            fade=[]
            for k in range(3):
                k=randint(-20,20)
                k=hex(k)
                if k[0]=='-':
                    k=k[3:]
                    k='-'+'0'*(2-len(k))+k
                else:
                    k=k[2:]
                    k='+'+'0'*(2-len(k))+k #in hundsight, this could have been avoided in fandiamond_fade
                fade+=[k]
            fandiamond_fade(c,''.join(fade),90,34,40,i*230,j*230)
    fandiamond_rainbow(90,40,30,0,0)
    random_polygon()
    initials(-400,350,60,10)