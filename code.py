
#Jerry the cheese lover_2D
#Humayra Basith Meem \\ 

#>>>>>>>>>  GAME MECHANICS <<<<<<<<<<<<<<<
# left click on ball >>score will increase (+5), ball is removed , laser is shown , collision with ball  reduces health 
# eat cheese >> score will increase (+5) , game speed will increase 
# avoid brick , otherwise game over 

#>>>>>>>> CONTROLS <<<<<<<<<
#keyboard movement >>  left arrow and right arrow
#laser shoot , play , pause , back , reset button >> left click 

#>>>>>>>>>> TroubleShoot <<<<<<<<<<
#for speed related issue :  change the values of speed at  line = 71 , 449 and if needed max speed , initialize_game 
# for 60hz display 0.05 speed is suggested , for 144 hz display 0.5 is suggested . might differ from cpu configurations and display capabilities as well. 

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

move_speed=30  #jerry
head_center_x = 150
head_radius=50
head_center_y =100
bypass= 0

#new
remove_ball_x=0
remove_ball_y=0

brick_list=[]
time_interval_brick = 0
current_time_brick = 0

cheese_list = []
time_interval_cheese = 0
current_time_cheese = 0
now=0  #new
now2=0 #new

ball_list=[]
time_interval_ball = 0
current_time_ball=0

play_button_visible= True
current_mode=0
laser= False #new

score=0
health=5
cheese_collect=0
highest_score=0


#new
num_shot=5
shoot_list=[]
shoot_speed=2.0

max_speed=20
speed=0.4

def circle_Points(cx, cy, x, y):
    glVertex2f(x + cx, y + cy)
    glVertex2f(-x + cx, y + cy)
    glVertex2f(x + cx, -y + cy)
    glVertex2f(-x + cx, -y + cy)
    glVertex2f(y + cx, x + cy)
    glVertex2f(-y + cx, x + cy)
    glVertex2f(y + cx, -x + cy)
    glVertex2f(-y + cx, -x + cy)

def mid_circle(cx, cy, radius):
    d = 1 - radius
    x = 0
    y = radius

    while x <= y:
        circle_Points(cx, cy, x, y)
        x += 1

        if d <= 0:
            d = d + 2 * x + 1
        else:
            y -= 1
            d = d + 2 * (x - y) + 1
        circle_Points(cx, cy, x, y)

################################################## mid point line algo######################    start

def draw_line(x1,y1,x2,y2):
  # find the zone
  zone = find_zone(x1,y1,x2,y2)
  # convert the coordinate values to zone 0
  x1,y1 = convert_to_zone0(x1,y1,zone)
  x2,y2 = convert_to_zone0(x2,y2,zone)
  #mid point line with zone 0
  glBegin(GL_POINTS)
  midpoint_line(x1,y1,x2,y2,zone)
  glEnd()



def find_zone(x1,y1,x2,y2):
   dx = x2-x1
   dy = y2-y1
   if dx>dy:
     if dx>0 and dy>0 :
       zone = 0
     elif dx<0 and dy>0:
       zone = 3
     elif dx < 0 and dy < 0:
        zone = 4
     else:
        zone = 7

   else :
      if dx>0 and dy>0 :
        zone = 1
      elif dx<0 and dy>0 :
        zone =2
      elif dx < 0 and dy < 0:
        zone = 5
      else :
        zone = 6
   return zone

def convert_to_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x,-y

def midpoint_line(x1,y1,x2,y2,zone):
  dx = x2 - x1
  dy = y2 - y1
  d = 2*dy-dx
  E = 2*dy
  NE = 2*(dy-dx)
  y=y1

  for x in range(int(x1), int(x2) + 1): # last iteration will be x2
    cx,cy = convert_to_original(x,y,zone)
    glVertex2f(cx,cy)
    if d>0:
      d+= NE
      y+= 1
    else :
      d+= E



def convert_to_original(x,y,zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

################################################# mid point line algo######################   end
def draw_jerry():
    global head_center_x,head_radius,head_center_y 
    new_body_radius=30
    if health==5:
        
        body_radius=new_body_radius
    elif 0<health<5:
        body_radius = new_body_radius - (5 - health) * 3
        if body_radius < 1:
            body_radius = 1
    elif health==0:
        body_radius=0

     # Draw Jerry's head
    glColor3f(1.0, 0.75, 0.8)  
    glPointSize(2)
    glBegin(GL_POINTS)
    mid_circle(head_center_x, head_center_y, head_radius)
    glEnd()

    # Draw Jerry's eyes
    eye_radius = 5
    eye_offset = 20

    glColor3f(1.0, 0.75, 0.8)  
    glPointSize(2)
    glBegin(GL_POINTS)
    mid_circle(head_center_x - eye_offset, head_center_y + eye_offset, eye_radius)
    glEnd()
    glColor3f(1.0, 0.75, 0.8)  
    glPointSize(2)
    glBegin(GL_POINTS)
    mid_circle(head_center_x + eye_offset, head_center_y + eye_offset, eye_radius)
    glEnd()

    # Draw Jerry's mouth (triangle)
    mouth_x1 = head_center_x - 10
    mouth_y1 = head_center_y - 25
    mouth_x2 = head_center_x + 10
    mouth_y2 = head_center_y - 25
    mouth_x3 = head_center_x
    mouth_y3 = head_center_y - 35

    glColor3f(1.0, 0.75, 0.8)   
    
    draw_line(mouth_x1, mouth_y1,mouth_x2, mouth_y2)
    draw_line(mouth_x2,mouth_y2,mouth_x3,mouth_y3)
    draw_line(mouth_x1,mouth_y1,mouth_x3,mouth_y3)
    
    

    # Draw three straight lines from the mouth (lighter brown color)
    
    # Jerry's mustache
    
    glColor3f(1.0, 0.75, 0.8)
    glPointSize(2)
    draw_line( mouth_x1 - 30, mouth_y1,mouth_x1-5, mouth_y1) # why it doesnt work if i wanna draw right point to left point
    draw_line(mouth_x1 - 30, mouth_y1-4,mouth_x1-5, mouth_y1-4 )
    draw_line(mouth_x2+5, mouth_y2, mouth_x2 + 30, mouth_y2)
    draw_line(mouth_x2+5, mouth_y2-4, mouth_x2 + 30, mouth_y2-4)
    


  

    # Draw Jerry's ears (circles)
    ear_radius = 8
    ear_offset = 40

    glColor3f(1.0, 0.75, 0.8)  # Brown color (dark)
    glPointSize(2)
    glBegin(GL_POINTS)
    mid_circle(head_center_x - ear_offset, head_center_y + ear_offset, ear_radius)
    mid_circle(head_center_x + ear_offset, head_center_y + ear_offset, ear_radius)
    glEnd()

    # Draw Jerry's body (circle)
    
    body_center_x = head_center_x
    body_center_y = head_center_y - 70

    glColor3f(1.0, 0.75, 0.8)  # Brown color (medium)
    glPointSize(2)
    glBegin(GL_POINTS)
    mid_circle(body_center_x, body_center_y, body_radius)
    glEnd()



def initialize():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WINDOW_WIDTH, 0.0, WINDOW_HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def cheese_function():
    for cheese in cheese_list:
            draw_cheese(cheese['x'], cheese['y'], cheese['size'], cheese['color'])
    if not cheese_list:
            new_cheese ={'x': random.randint(0, WINDOW_WIDTH - 20), 'y': WINDOW_HEIGHT, 'size': random.randint(30,50),
                       'color': (1,1,0)}  
            cheese_list.append(new_cheese)
   
    
def draw_cheese(x,y,size,color):
    glColor3f(*color)
    draw_line(x,y,x+(size)/3,y+(size/4)*3)
    draw_line(x+(size)/3,y+(size/4)*3,x+2*(size)/3,y+(size/4)*3)
    draw_line(x+(size/3),y,x+2*(size)/3,y+(size/4)*3)
    draw_line(x,y,x+(size/3),y)
    draw_line(x+size,y,x+2*(size)/3,y+(size/4)*3) # why doesnt work reverse 
    draw_line(x+(size/3),y,x+size,y)


def brick_function():
    for brick in brick_list:
        draw_brick(brick['x'], brick['y'], brick['size'],brick['color'])
    if not brick_list:
            new_brick ={'x': random.randint(0, WINDOW_WIDTH - 10), 'y': WINDOW_HEIGHT, 'size': random.randint(20,30),'color': (0.8,0.4,0.1)}  
            brick_list.append(new_brick)
            

def draw_brick(x, y, size,color):
    glColor3f(*color) 

    #horizontal lines
    draw_line(x,y,x+size,y)
    draw_line(x,y+(size/4)*3,x+size,y+(size/4)*3)
    draw_line(x+(size/4),y+size,x+(size/4)*5,y+size)

    #vertical lines
    draw_line(x+0.1,y+0.1,x,y+(size/4)*3)
    draw_line(x+size+0.1,y+0.1,x+size,y+(size/4)*3)
    draw_line( x + 5 * (size / 4), y + (size / 4),x + 0.5 + (size / 4) * 5, y + size  )
    
    #diagonal line
    draw_line(x+size,y+(size/4)*3,x+(size/4)*5,y+size)
    draw_line(x+size,y,x+5*(size)/4,y+(size/4)) 
    draw_line(x,y+(size/4)*3,x+(size/4),y+size)


def ball_fuction(): 
    for ball in ball_list:
        draw_ball(ball['cx'], ball['cy'], ball['radius'],ball['color'])
    if not ball_list:
            new_ball ={'cx': random.randint(0, WINDOW_WIDTH - 10), 'cy': WINDOW_HEIGHT,'radius': random.randint(20,25), 'color': (1.0,0.0,0.0)}   
            ball_list.append(new_ball)
          

def draw_ball(cx,cy,radius,color):
    glColor3f(*color)
    glPointSize(2)
    glBegin(GL_POINTS)
    mid_circle(cx, cy, radius)
    mid_circle(cx+3, cy+2, radius-4)
    mid_circle(cx+3, cy+2, radius-5)
    glEnd()
    


    

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_jerry()
    if health!=0:
        cheese_function()
        brick_function()
        ball_fuction()

    cross_button()
    back_button()
    shoot_laser() #new
   
    if play_button_visible:
       play_button()
       #print(speed)
    else:
       pause_button()
       print(speed)
    glutSwapBuffers()
    


def keyboard_special_keys(key, x, y):
    global move_speed,health,current_mode
    if health!=0 and current_mode==0:
        if key == GLUT_KEY_LEFT:
            
            move_jerry('left')
            
        elif key == GLUT_KEY_RIGHT:
            # print("keyboard_special_keys working right")
            move_jerry('right')

        
def move_jerry(direction):
    global head_center_x,head_radius
    if direction == 'left':
        head_center_x = max(head_radius, head_center_x - move_speed)
    elif direction == 'right': 
        head_center_x = min(WINDOW_WIDTH-head_radius, head_center_x+ move_speed)
    glutPostRedisplay()        
######################################  
def update_objects():
    global time_interval_brick, current_time_brick
    global time_interval_cheese, current_time_cheese
    global time_interval_ball, current_time_ball
    global current_mode,play_button_visible
    global head_center_y,head_radius,head_center_x ,score,health,max_speed,speed,highest_score,cheese_collect

    current_time_brick = glutGet(GLUT_ELAPSED_TIME)
    current_time_cheese = glutGet(GLUT_ELAPSED_TIME)
    current_time_ball = glutGet(GLUT_ELAPSED_TIME)
    
    if current_mode==0 and health!=0:
    # For bricks
        if current_time_brick - time_interval_brick > 3500:  # Adjust time interval as needed
            time_interval_brick = current_time_brick
            add_brick()
        for brick in brick_list:
            brick['y'] -= speed
            if brick['y']<=0:
                brick_list.remove(brick)
            if jerry_clash_brick(head_center_y,head_radius,head_center_x ,brick):
                brick_list.remove(brick)
                health=0
                if score<highest_score:
                    print('You Ara A loser')
                    print("can't beat the highest score")
                    print("SCORE:",score)
                    print("CHEESE_COLLECT:",cheese_collect)
                else:
                    print("CONGOOOOO YOU BEAT THE HIGHEST SCORE")
                    print('New Highest_Score:',highest_score)
                    print("CHEESE_COLLECT:",cheese_collect)
            for cheese in cheese_list:
                    if cheese_clash_brick(cheese,brick):
                        brick_list.remove(brick)
            
        # For cheese
        if current_time_cheese - time_interval_cheese > 4300:  # Adjust time interval as needed
            time_interval_cheese = current_time_cheese
            add_cheese()

        for cheese in cheese_list:
            cheese['y'] -= speed
            if cheese['y']<=0:
                cheese_list.remove(cheese)
            if jerry_clash_cheese(head_center_y,head_radius,head_center_x ,cheese):
                cheese_list.remove(cheese)
                speed = min(speed+0.3,max_speed)
                #print('speed',speed)
                score+=5
                cheese_collect+=1
                highest_score=max(highest_score,score)
                print('score:',score)
                print("CHEESE_COLLECT:",cheese_collect)
           


        # For balls
        if current_time_ball - time_interval_ball > 3000:  # Adjust time interval as needed
            time_interval_ball = current_time_ball
            add_ball()
        for ball in ball_list:
            ball['cy'] -= speed
            if ball['cy']<=0:
                ball_list.remove(ball)
            if jerry_clash_ball(head_center_y,head_radius,head_center_x ,ball):
                ball_list.remove(ball)
                #speed = min(speed+0.001,max_speed)
                health-=1
                print('health:',health)
            ##newly add
            #for ball in ball_list:
            for cheese in cheese_list:
                if cheese_clash_ball(cheese,ball):
                    ball_list.remove(ball)
            for brick in brick_list:
                if brick_clash_ball(brick,ball):
                    brick_list.remove(brick)
                    

        
def jerry_clash_cheese(head_center_y,head_radius,head_center_x ,cheese):
    return (
        head_center_x-head_radius < cheese['x'] + cheese['size'] and
        head_center_x+head_radius > cheese['x'] and
        head_center_y-head_radius < cheese['y'] + cheese['size'] and
        head_center_y+head_radius > cheese['y']
    )   

def cheese_clash_brick(cheese,brick):
    return (
        brick['x'] < cheese['x'] + cheese['size'] and
        brick['x'] +brick['size']> cheese['x'] and
        brick['y']< cheese['y'] + cheese['size'] and
        brick['y'] + brick['size']  > cheese['y']
    )
#-----------------newly add--------------
def cheese_clash_ball(cheese,ball):
    return (
        ball['cx']-ball['radius'] < cheese['x'] + cheese['size'] and
        ball['cx'] +ball['radius']> cheese['x'] and
        ball['cy']-ball['radius']< cheese['y'] + cheese['size'] and
        ball['cy'] + ball['radius']  > cheese['y']
    )
        
def brick_clash_ball(brick,ball):
    return (
        ball['cx']-ball['radius']< brick['x'] + brick['size'] and
        ball['cx'] +ball['radius']> brick['x'] and
        ball['cy']-ball['radius']< brick['y'] + brick['size'] and
        ball['cy'] + ball['radius']  > brick['y']
    )

#-----------------newly add--------------
        

def jerry_clash_ball(head_center_y,head_radius,head_center_x ,ball):
    return (
        head_center_x-head_radius < ball['cx'] + ball['radius'] and
        head_center_x+head_radius > ball['cx']-ball['radius'] and
        head_center_y-head_radius < ball['cy'] + ball['radius'] and
        head_center_y+head_radius > ball['cy']-ball['radius']
    )
       
def jerry_clash_brick(head_center_y,head_radius,head_center_x ,brick):
    return (
        head_center_x-head_radius < brick['x'] + brick['size'] and
        head_center_x+head_radius > brick['x'] and
        head_center_y-head_radius < brick['y'] + brick['size'] and
        head_center_y+head_radius > brick['y']
    )  

def add_ball():
    new_ball = {'cx': random.randint(50, WINDOW_WIDTH - 50), 'cy': WINDOW_HEIGHT, 'radius':20,'color': (1.0,0.0,0.0)}
    ball_list.append(new_ball) 
    

def add_brick():
    new_brick = {'x': random.randint(50, WINDOW_WIDTH - 50), 'y': WINDOW_HEIGHT, 'size': random.randint(30, 50),'color': (0.8,0.4,0.1)}
    brick_list.append(new_brick)

def add_cheese():
    new_cheese = {'x': random.randint(0, WINDOW_WIDTH - 10), 'y': WINDOW_HEIGHT, 'size': random.randint(30, 50),
                  'color': (1, 1, 0)}
    cheese_list.append(new_cheese)


def initialize_game(msg=False):
    global brick_list,ball_list,cheese_list,score,health,speed,cheese_collect
    brick_list = []
    ball_list = []
    cheese_list=[]
    score = 0
    cheese_collect=0
    health=5
    speed=0.4
    if msg:
        print("Starting Over!!")  


#buttons
def back_button():
    glColor3f(0.0, 1.0, 1.0)
    bx1 = 15 # minimum x value
    bx2 = bx1+50 # max x value
    bx_mid = int(bx1 + (bx2 - bx1) / 2)
    by1 = WINDOW_HEIGHT-60 # y min
    by2 = WINDOW_HEIGHT-20  # y max
    by_mid = int(by1 + (by2 - by1) / 2)
    draw_line(bx1, by_mid, bx_mid, by2)
    draw_line(bx1, by_mid, bx2, by_mid)
    draw_line(bx1, by_mid, bx_mid, by1)


def play_button():  #bypassing print draw_line 
    global bypass,play_button_visible #new

    play_button_visible = True
    glColor3f(0.7, 1.0, 0.7)
    px1 = WINDOW_WIDTH/2  # minimum x value
    px2 = px1+40 # max x value
    py1 = WINDOW_HEIGHT-60  # y min
    py2 = WINDOW_HEIGHT-20 # y max
    py_mid = int(py1 + (py2 - py1) / 2)
    draw_line(px1, py2, px2, py_mid)
    draw_line(px1, py1, px1 - 0.0000001, py2)
    draw_line(px1, py1, px2, py_mid)


def pause_button():
    global play_button_visible
    play_button_visible = False

    glColor3f(0.7, 1.0, 0.7)
    tx1 = WINDOW_WIDTH/2  # minimum x value
    tx2 = tx1+40 # max x value
    ty1 = WINDOW_HEIGHT-60 # y min
    ty2 = WINDOW_HEIGHT-20 # y max

    t_part = int((tx2 - tx1) / 3)

    #print("PAUSED")
    draw_line(tx1 + t_part - 0.001, ty1, tx1 + t_part, ty2)
    draw_line(tx1 + 2 * t_part - 0.0001, ty1, tx1 + 2 * t_part, ty2)


def cross_button():   
    glColor3f(1.0, 0.0, 0.0)
    cx1 = int((WINDOW_WIDTH)-60)  # minimum x value
    cx2 = int((WINDOW_WIDTH)-20)  # max x value
    cx_mid = int(cx1 + (cx2 - cx1) / 2)
    cy1 =  int((WINDOW_HEIGHT)-60)  # y min
    cy2 = int((WINDOW_HEIGHT)-20)  # y max
    cy_mid = int(cy1 + (cy2 - cy1) / 2)
    draw_line(cx1, cy1, cx2, cy2)
    draw_line(cx1, cy2, cx2, cy1)
    



def mouse_click(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # print("CLICK BUTTON",x,y)
        button_click(x, y)
        
    

def button_click(x, y):  
    back_button_click(x, y)
    play_button_click(x, y)
    cross_button_click(x, y) 
    # shooted(x,y)  #new
    check_gun_ball_clash(x,y) #new




def back_button_click(x, y):
    global speed
    x1, x2 = int(15),int(15+50)
    y1, y2 =  WINDOW_HEIGHT-60 , WINDOW_HEIGHT-20 
    if x1 <= x <= x2 and y1 <= WINDOW_HEIGHT - y <= y2:
        print("reset")
        #speed=0.005
        initialize_game(msg=True)


def toggle_play_pause_button():
    global play_button_visible, current_mode
    play_button_visible = not play_button_visible
    current_mode = 0 if play_button_visible else 1
    



def play_button_click(x, y):
    
    x1, x2 = WINDOW_WIDTH/2, int((WINDOW_WIDTH/2)+40)
    y1, y2 =WINDOW_HEIGHT-60 , WINDOW_HEIGHT-20 

    if x1 <= x <= x2 and y1 <= WINDOW_HEIGHT - y <= y2:
        #print(speed)#########################################
        toggle_play_pause_button()
        glutPostRedisplay()


def cross_button_click(x, y):
    x1, x2 = int((WINDOW_WIDTH)-60),int((WINDOW_WIDTH)-20)
    y1, y2 = WINDOW_HEIGHT-60 , WINDOW_HEIGHT-20 
    if x1 <= x <= x2 and y1 <= WINDOW_HEIGHT - y <= y2:
        print("Goodbye! Score:",score)
        print("CHEESE_COLLECT:",cheese_collect)
        glutLeaveMainLoop()

def animation(value=None):

    if current_mode==0:
        update_objects()
        glutPostRedisplay()
        #glutTimerFunc(1000 // 60, animation, 0)
        
        
        
        



        
#new
def initialize_shooting(): #new
    global head_radius,head_center_y 
    for _ in range(num_shot):
        x = head_radius+head_center_y 
        
        shoot_list.append([x,shoot_speed])


def draw_shots(): #new
    glColor3f(1.0, 1.0, 1.0)
    glPointSize(2)
    glBegin(GL_POINTS)
    for x, _ in shoot_list:
        glVertex2f(x,0)
    glEnd()


def shooted(x,y):  #new
    global score,health,WINDOW_HEIGHT
    x1,x2= int(WINDOW_HEIGHT- 60),int(WINDOW_HEIGHT- 90) #notsure
    
    y1,y2=int(90),int(60)

    if x2 <= x <= x1 :
        if y2 <= WINDOW_HEIGHT-y <= y1:
            print("SHOT")



    
def check_gun_ball_clash(x,y):
    global ball,ball_list,score,bypass,laser,remove_ball_x,remove_ball_y ,max_speed,highest_score,cheese_collect
    # print("passes shooted",x,y)
    
    for ball in ball_list:
     if gun_clash_ball(x,WINDOW_HEIGHT-y ,ball) :
        score+=5
        highest_score=max(highest_score,score)
        #speed = min(speed+0.001,max_speed)
        print('score:',score)
        print("CHEESE_COLLECT:",cheese_collect)
        laser=True #new
        remove_ball_x=ball['cx']
        remove_ball_y=ball['cy']
        # print(remove_ball_x,remove_ball_y)
        shoot_laser()
        ball_list.remove(ball)
        
def shoot_laser():#new
    global laser,now,now2,remove_ball_x,remove_ball_y,head_center_x,head_center_y,head_radius
    now2 = glutGet(GLUT_ELAPSED_TIME)
    
    glColor3f(0.0, 1.0, 1.0)
    if laser==True: #new
      draw_line(head_center_x,head_center_y+head_radius,remove_ball_x,remove_ball_y)
    if now2 - now > 300:  # Adjust time interval as needed
            now = now2 
            laser=False

def gun_clash_ball(mx,my ,ball):
    # print("this is ball",ball)
    bx1,bx2 = ball['cx']-ball['radius'] , ball['cx']+ball['radius']
    by1,by2 = ball['cy']+ball['radius'] , ball['cy']-ball['radius']
    return (
        mx <= bx2 and
        mx >= bx1 and
        my <= by1 and
        my >= by2
    )         
    
    

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Jerry the Cheese Lover")
glutDisplayFunc(showScreen)
glutIdleFunc(animation)

glClearColor(0.0, 0.0, 0.0, 0.0)
glutSpecialFunc(keyboard_special_keys)
glutMouseFunc(mouse_click)
glEnable(GL_DEPTH_TEST)
initialize()
initialize_game()
glutMainLoop()

#>>>>>>>>>>>>>>>>>>>>>>>>>>>> Work Distribution <<<<<<<<<<<<<<<<<<<<<<<

#ALL individual items are made with MIDPOINT LINE ALGORITHM AND  MID POINT CIRCLE ALGORITHM , ONLY GLPOINTS ARE USED 

# Era:
# ----------------
# ball draw ,brick draw and brick all function
# Jerry collision with cheese, ball and  brick
# pause ,Play, reset all function AND ICON SHOW 
# all score implement
#brick collision with cheese
#storing balls in ball list  and more

# Nasif :
#--------------------
#mid point circle implementation  and midpoint line algorithm merge
# jerry draw  and movement , cross button implement ,function
#cheese draw
# laser mechanic 
#ball removal during collisions between laser and ball
#alternate method of gluttimefunction ( if required to updatee objects) >> alternative codes given at the end part of this file and more




#Humayra
#--------------------
#Time span >> helps to animate objects at a better arranged order 
#ball drop
#cheese ball Collision
#ball brick collision
#jerry size decreasing eating cheeses  and more 

##################################################################################







# alternative if user dont want to use  glut time function 

# def update_objects():
#     global cheese_speed, brick_speed, ball_speed
#     global time_interval_brick, current_time_brick
#     global time_interval_cheese, current_time_cheese
#     global time_interval_ball, current_time_ball
#     global current_mode,play_button_visible,game_over
#     global head_center_y,head_radius,head_center_x ,score,health,max_speed,speed, time_interval

#     current_time_brick = glutGet(GLUT_ELAPSED_TIME)
#     current_time_cheese = glutGet(GLUT_ELAPSED_TIME)
#     current_time_ball = glutGet(GLUT_ELAPSED_TIME)
    
#     if current_mode==0 and health!=0:
   
#         if len(brick_list) ==0 :
#             add_brick()  
#         else: 
#            for brick in brick_list:
            
#             brick['y'] -=speed 
#             if brick['y']<=450 and len(brick_list)==1:

#                     add_brick() 
#             if brick['y']<=0:
#                 print("removed")
#                 brick_list.remove(brick)
          
#             if jerry_clash_brick(head_center_y,head_radius,head_center_x ,brick):  
#                 brick_list.remove(brick)
#                 health=0
#                 print('You Ara A loser')
#             for cheese in cheese_list:
#                 if cheese_clash_brick(cheese,brick):
#                     brick_list.remove(brick)

#         if len(cheese_list)==0 :
#             add_cheese()  
#         else:
#          for cheese in cheese_list:
#             if score == 0:
#                 cheese['y'] -= speed
#             else:    
#                cheese['y'] -= speed  #score*0.001
#             if cheese['y']<=500 and len(cheese_list)<=1:
#                     # print("two pass")
                    
#                     add_cheese() 
               
            
#             if cheese['y']<=0:  #NEW
                
#                 cheese_list.remove(cheese)
#             if jerry_clash_cheese(head_center_y,head_radius,head_center_x ,cheese):
#                 print("clash with cheese")
#                 cheese_list.remove(cheese)
#                 print("speed bef clash with cheese")
#                 speed = min(speed+2,max_speed)
#                 print("speed bef after with cheese")
#                 print('speed',speed)
#                 score+=5
#                 time_interval = time_interval - time_interval*2.5/100
                
#                 print('score:',score)
           


   
#         if ball_list ==0 :
#             add_ball() 
        
                
#         else:       
#          for ball in ball_list:
#             ball['cy'] -= speed
#             if ball['cy']<=450 and len(ball_list)<=1:
#                     # print("two pass")
                    
#                     add_ball() 
            
#             # print("ball cy",ball['cy'])
            
#             if ball['cy']<=0: #NEW
#                 print("removed")
#                 ball_list.remove(ball)
#             if jerry_clash_ball(head_center_y,head_radius,head_center_x ,ball):
#                 ball_list.remove(ball)
#                 # speed = min(speed+0.001,max_speed)
#                 health-=1
#                 print('health:',health)

# #