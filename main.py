import pygame
from pygame.locals import *
import button
import menu_buttons

#create display window
pygame.init()
height = 400
widht = 650
var = 0
cor_x = 0
speedd = 2
win = pygame.display.set_mode((widht, height))
pygame.display.set_caption('CrystallAdv')
clock = pygame.time.Clock()
fps = 60
next_level = 0
score = 0
last_score = 0
movement = 1
movent_conter = 10
cordinat_x = 560
#load button images
start_img = pygame.image.load('assets/start_btn.png').convert_alpha()
exit_img = pygame.image.load('assets/exit_btn.png').convert_alpha()
menu_btn = pygame.image.load('assets/menu.png').convert_alpha()
replay_btn = pygame.image.load('assets/replay.png').convert_alpha()
home_btn = pygame.image.load('assets/home.png').convert_alpha()
bg = pygame.image.load('assets/bg.png')
bg1 = pygame.image.load('assets/bg1.png')

bg_menu = pygame.image.load('assets/menu/bg.png')
grass = pygame.image.load('assets/menu/grass.png')
grass_1 = pygame.image.load('assets/menu/grass_1.png')
grass_2 = pygame.image.load('assets/menu/grass_2.png')
trap = pygame.image.load('assets/grass.png')
icon =  pygame.image.load('assets/player/stand.png')
bluecrystall =  pygame.image.load('assets/bluecriystal.png')
pinkcrystall =  pygame.image.load('assets/pinkcrystal.png')
bride = pygame.image.load('assets/gras.png')
# scale/size 
size_bg = pygame.transform.scale(bg,(widht,height))
size_bg1 = pygame.transform.scale(bg1,(widht,height))
size_bg_menu = pygame.transform.scale(bg_menu,(widht,height))
size_grass = pygame.transform.scale(grass, (35,40))
size_icon = pygame.transform.scale(icon,(20,20))
size_trap = pygame.transform.scale(trap, (160,100))
size_bluecrystall = pygame.transform.scale(bluecrystall, (11,11))
size_pinkcrystall = pygame.transform.scale(pinkcrystall, (11,11))
#create button instances
start_button = button.Button(270, 240, start_img, 0.8)
exit_button = button.Button(270, 300, exit_img, 0.8)
menu_button = menu_buttons.Button(10, 4, menu_btn, 0.8, 27, 27)
replay_button = menu_buttons.Button(370, 250, replay_btn, 0.8, 35, 35)
home_button = menu_buttons.Button(300, 250, home_btn, 0.8, 35, 35)
# animate 
right = [ pygame.image.load('assets/menu/player/R1.png'),
		  pygame.image.load('assets/menu/player/R2.png'),
		  pygame.image.load('assets/menu/player/R3.png')
		]
left = [ pygame.image.load('assets/player/left/l1.png'),
		  pygame.image.load('assets/player/left/l2.png'),
		  pygame.image.load('assets/player/left/l3.png')
		]
fire = [pygame.image.load('assets/fire/F1.png'),
		pygame.image.load('assets/fire/F2.png'),
		pygame.image.load('assets/fire/F3.png'),
		pygame.image.load('assets/fire/F4.png')
		]
walkCount = 0
rightcon = True
pygame.display.set_icon(size_icon)

class Player(object):
	def __init__(self,x,y,imageRight,imageLeft, health):
		self.x = x
		self.y = y 
		self.imageRight = imageRight
		self.imageLeft = imageLeft
		self.char = pygame.image.load('assets/player/stand.png')
		self.death = pygame.image.load('assets/death.png')
		self.health = health
		self.vel = 2
		self.walkCount = 0
		self.right = False 
		self.left = False
		self.isJump = False
		self.jumpCount = 10
		self.cor_x = 20
		self.jump = 0
		self.moving = True
		self.con_x = 20

	def draw(self):
		self.move()
		if self.walkCount + 1 >= 27:
			self.walkCount = 0
		if self.health > 60:
			if self.right:
				win.blit(self.imageRight[self.walkCount//9], (self.x, self.y))
				self.walkCount += 1
			elif self.left:
				win.blit(self.imageLeft[self.walkCount//9], (self.x, self.y))
				self.walkCount += 1			
			else:
				self.walkCount = 0
				win.blit(self.char, (self.x,self.y))
		else:
			win.blit(self.death, (self.x, self.y))

	def move(self):

		keys = pygame.key.get_pressed()
		if self.moving:	
			if keys[pygame.K_RIGHT]:
				if self.x <= 630:
					self.x += self.vel
					self.con_x += 2
					self.cor_x += 2
					if self.isJump:
						self.x += 3
						self.cor_x += 3
				else:
					self.x = 20

				self.right = True
				self.left = False

			elif keys[pygame.K_LEFT] and self.x > self.vel: 	
				self.x -= self.vel
				if self.jump < 2:
					if self.isJump:
						self.x -= 3
						self.cor_x -= 3
				self.left = True
				self.right = False
			else:
				self.right = False
				self.left = False

			if not(self.isJump):
				if keys[pygame.K_SPACE]:
					self.isJump = True
			else:
				if self.jumpCount >= -10:
					self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.25
					self.jumpCount -= 1
				else:
					self.jumpCount = 10
					self.isJump = False
		else:
			self.right = False
			self.left = False

class Fire(object):
	def __init__(self, x, y, image):
		self.x = x 
		self.y = y
		self.image = image
		self.on = True
		self.fireCount = 0
	
	def draw(self):
		if self.fireCount + 1 >= 16:
			self.fireCount = 0

		if self.on:
			win.blit(self.image[self.fireCount//4], (self.x,self.y))
			self.fireCount += 1

def drawwindow():
	player.draw()
	text = font.render(': ' + str(score), 1, (255,255,255))
	win.blit(text, (610, 25))
	win.blit(size_bluecrystall, (590, 25))
	win.blit(size_pinkcrystall, (570, 25))
	
def drawtext():
	score_text = score_font.render(str(last_score), 1, (255,255,255))
	win.blit(score_text, (340, 220))
	lose_text = score_font.render('Game Over', 1, (255,255,255))
	win.blit(lose_text, (300, 200))

def animationplayer():
	global walkCount, rightcon
	if walkCount +1 >= 27:
		walkCount = 0

	if rightcon:
		win.blit(right[walkCount//9], (326,135))
		walkCount +=1


player = Player(20,130,right,left,100)
fire_effect = Fire(170,45, fire)
fire_effect_1 = Fire(595,45, fire)
font = pygame.font.SysFont('comicsans', 22, True)
score_font = pygame.font.SysFont('comicsans', 24, True)


on = False
running = True
poss = 0
#game loop
run = True
while run:
	if var <= 3:
		win.blit(size_bg_menu,(0,0))
		win.blit(grass_1,(cor_x,0))
		win.blit(grass_2,(cor_x,370))
		win.blit(size_grass, (320, 170))
		animationplayer()
		cor_x -= speedd
		if abs(cor_x) >= 180:
			cor_x = 0
	else:		
		if player.cor_x <= 634:
			win.blit(size_bg, (0,0))		
		else:
			win.blit(size_bg1, (0,0))
			if next_level < 1:
				next_level += 1

			if next_level >= 1:
				win.blit(bride,(cordinat_x, 160))
				if player.health > 0:
					cordinat_x -= movement
					movent_conter -= 2
					if abs(movent_conter) > 700:
						movement *= -1
						movent_conter = 2
						movent_conter *= movement
						
				if player.x >= 96:
					if player.y <= 300:
						if player.isJump == True:
							if player.x == player.x:
								player.x += 4
						else:
							player.y += 10
							player.moving = False
							walkCount = 0
					else:
						if player.health > 0:	
							player.health -= 10
		if next_level < 1:
			fire_effect.draw()
			fire_effect_1.draw()
			if player.left == True:
				player.cor_x -= 2
			if player.con_x > 330:
				win.blit(size_trap,(350,poss))
				if poss < 165:
					poss += 2
			if player.con_x < 70:
				win.blit(pinkcrystall, (80,150))
			else:
				if score < 1:
					score += 1
			if player.con_x < 140:	
				win.blit(bluecrystall, (150,150))
			else:
				if score < 2:
					score += 1
			if player.con_x < 210:
				win.blit(bluecrystall, (220,150))
			else:
				if score < 3:
					score += 1
			if player.con_x < 290:
				win.blit(pinkcrystall, (300,150))
			else:
				if score < 4:
					score += 1

	if running:
		if start_button.draw(win):
			print('START')
			running = False
			
		if exit_button.draw(win):
			break
	else:
				
		if player.health > 0:
			if menu_button.draw(win):
				var = 0
				running = True
				if next_level > 0:
					next_level -= 1
			else:
				if var <= 200:
					var += 1
		else:
			drawtext()
			if home_button.draw(win):
				var = 0
				running = True
				if next_level > 0:
					next_level -= 1
			else:
				if var <= 200:
					var += 1
			if replay_button.draw(win):
				print('replay')
			if last_score < 400:
				last_score += 1
		drawwindow()
		#print(var)
		
	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False

	print(movent_conter)
	clock.tick(fps)
	pygame.display.update()

pygame.quit()