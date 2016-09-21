import os
import sys
import vlc
import pygame
from socket import *


# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255,0,0)


# Setting up network connections
host = 'localhost'
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)



def callback(self, player):

	print
	print 'FPS =',  player.get_fps()
	print 'time =', player.get_time(), '(ms)'
	print 'FRAME =', .001 * player.get_time() * player.get_fps()

pygame.init()
screen = pygame.display.set_mode((800,600),pygame.RESIZABLE)
pygame.display.get_wm_info()

# initiate the joystick
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()

for i in range(joystick_count):
	joystick = pygame.joystick.Joystick(i)
	joystick.init()


filename = 'lec6a.mp4'
start = 0

print "Using %s renderer" % pygame.display.get_driver()
print 'Playing: %s' % filename

# Get path to movie specified as command line argument
movie = os.path.expanduser(filename)
# Check if movie is accessible
if not os.access(movie, os.R_OK):
	print('Error: %s file not readable' % movie)
	sys.exit(1)

# Create instane of VLC and create reference to movie.
vlcInstance = vlc.Instance()
media = vlcInstance.media_new(movie)

# Create new instance of vlc player
player = vlcInstance.media_player_new()

# Add a callback
em = player.event_manager()
em.event_attach(vlc.EventType.MediaPlayerTimeChanged, callback, player)

# Pass pygame window id to vlc player, so it can render its contents there.
win_id = pygame.display.get_wm_info()['window']
if sys.platform == "linux2": # for Linux using the X Server
	player.set_xwindow(win_id)
elif sys.platform == "win32": # for Windows
	player.set_hwnd(win_id)
elif sys.platform == "darwin": # for MacOS
	player.set_agl(win_id)

# Load movie into vlc player instance
player.set_media(media)

# Quit pygame mixer to allow vlc full access to audio device (REINIT AFTER MOVIE PLAYBACK IS FINISHED!)
pygame.mixer.quit()


# Show a message on the screen
msg = pygame.font.Font(None,40)
msgImg = msg.render("Press any button to start watching!",False,white)
msgSize = msg.size("Press any button to start watching!")
screen.blit(msgImg,((800-msgSize[0])/2,(600-msgSize[1])/2))
pygame.display.update()

# Play the video as long as button is pressed.
while start == 0:
	# EVENT PROCESSING STEP
    for event in pygame.event.get():  # User did something
		if event.type == pygame.QUIT:  # If user clicked close
			start = 1  # Flag that we are done so we exit this loop

		# Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
		if event.type == pygame.JOYBUTTONDOWN:
			screen.fill(white)
			player.play() # Start movie playback
			start = 1



while player.get_state() != vlc.State.Ended:
	data = str(player.get_time())
	UDPSock.sendto(data, addr)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(2)
		if event.type == pygame.KEYDOWN:
			player.pause()
			print "kEYDOWN"

