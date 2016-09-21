import pygame
import numpy
import math
import subprocess
import datetime
from timeit import default_timer as timer
import csv
#from client import *



# A function for drawing dashed lines
def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    if (x1 == x2):
        ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcoords = [x1] * len(ycoords)
    elif (y1 == y2):
        xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycoords = [y1] * len(xcoords)
    else:
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round(math.sqrt(a**2 + b**2))
        dx = dl * a / c
        dy = dl * b / c

        xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
        ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(surf, color, start, end, width)


pygame.init()

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255,0,0)


# Define the coordinates
up = 'Friendly'
down = 'Unfriendly'
left = 'Boring'
right = 'Engaging'

text_up = pygame.font.Font(None,20)
text_down = pygame.font.Font(None,20)
text_left = pygame.font.Font(None,20)
text_right = pygame.font.Font(None,20)


# Setting FPS
FPS = 60

# Loop until the user clicks the close button.
done = False
fileopened = 0
recording = 0

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
#joystick_count = pygame.joystick.get_count()


joystick = pygame.joystick.Joystick(0)
joystick.init()


# Get the name from the OS for the controller/joystick
name = joystick.get_name()
pygame.display.set_caption("DUAL AXIS RATING: " + 'Not recording!')

# Set the width and height of the screen [width,height]
size = 500
screen = pygame.display.set_mode([size,size])


# Setting up the edge for a rating area
edge = 90

# Starting client
#client_thread = Client()
#client_thread.connect()

# Timing
begin = 999999999999

with open('templog.csv', 'a') as f:
    writer = csv.DictWriter(f, fieldnames=["date", "elapsed_time", "raw_x", "raw_y", "x", "y", 'recording', 'pause'],
                            delimiter=',')
    writer.writeheader()


# -------- Main Program Loop -----------
while done == False:

    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(white)


    # Drawing the coordinate
    pygame.draw.line(screen, black, (size / 2, edge), (size / 2, size-edge))
    pygame.draw.line(screen,black,(edge,size/2),(size-edge,size/2))
    draw_dashed_line(screen,black,(edge-1,edge-1),(size-edge+1,edge-1),1,3)
    draw_dashed_line(screen, black, (edge - 1, edge - 1), (edge - 1,size-edge+1), 1, 3)
    draw_dashed_line(screen, black, (edge - 1,size-edge+1), (size - edge + 1, size-edge + 1), 1, 3)
    draw_dashed_line(screen, black, (size - edge + 1, size-edge + 1), (size-edge + 1, edge-1), 1, 3)

    # Putting words on coordinate
    textImg = text_up.render(up,False,black)
    textSize = text_up.size(up)
    screen.blit(textImg,((size-textSize[0])/2,(edge-textSize[1])/2))

    textImg = text_up.render(down, False, black)
    textSize = text_up.size(down)
    screen.blit(textImg, ((size - textSize[0]) / 2, (size - (edge-textSize[1]) / 2)))

    textImg = text_up.render(left, False, black)
    textSize = text_up.size(left)
    screen.blit(textImg, ((edge-textSize[0])/2,(size-textSize[1])/2))

    textImg = text_up.render(right, False, black)
    textSize = text_up.size(right)
    screen.blit(textImg, (size-edge+(edge-textSize[0])/2,(size-textSize[1])/2))



    # Draw a red circle to represent (x,y)
    raw_x = joystick.get_axis(0)
    raw_y = joystick.get_axis(1)

    x = int((size/2-edge)*raw_x+size/2)
    y = int((size/2-edge)*raw_y+size/2)


    pygame.draw.circle(screen,red,(x,y),5,2)


    pygame.display.update()


    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Go ahead and update the screen with what we've drawn.
    #pygame.display.flip()

    # Limit to certain FPS
    clock.tick(FPS)

    # EVENT PROCESSING STEP
    pause = 0

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        #if event.type == pygame.JOYAXISMOTION:
            #print("Joystick moved.")

        if event.type == pygame.JOYBUTTONUP and fileopened == 0:
            fileopened = 1
            subprocess.Popen(['python', 'movie.py'])
            pygame.display.set_caption("DUAL AXIS RATING: " + 'Video frame opened, not recording!')

        if event.type == pygame.JOYBUTTONDOWN and fileopened == 1 and recording == 0:
            recording = 1
            pygame.display.set_caption("DUAL AXIS RATING: " + 'Recording now!')
            begin = timer()
        if event.type == pygame.KEYDOWN:
            pause = 1


    # Recording data
    time = '%s' % datetime.datetime.now()
    now = timer()
    elapsed = now - begin
    rateflow = str(time)+','+str(elapsed)+','+str(raw_x)+','+str(raw_y) + ','+ str(x)+','+str(y)+','+str(recording)+','+str(pause)
    print 'DATA', rateflow
    #client_thread.send(rateflow)

    row = [time,elapsed,raw_x,raw_y,x,y,recording,pause]
    with open('templog.csv', 'a') as f:
        w = csv.writer(f)
        w.writerow(row)



# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()