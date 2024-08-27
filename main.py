import pygame
from random import randint
from sys import exit
from math import sin, pi
from setting import *

pygame.init()
screen = pygame.display.set_mode((1000, 400))
pygame.display.set_caption("DinoJump")

class Dino(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		run1 = pygame.image.load('graphics/Dino_Run01.png').convert_alpha()
		run1 = pygame.transform.rotozoom(run1, 0, 0.5)
		run2 = pygame.image.load('graphics/Dino_Run02.png').convert_alpha()
		run2 = pygame.transform.rotozoom(run2, 0, 0.5)	
		self.jump_im = pygame.image.load('graphics/Dino_Idle.png').convert_alpha()
		self.jump_im = pygame.transform.rotozoom(self.jump_im, 0, 0.5)	
		self.die = pygame.image.load('graphics/Dino_Die.png').convert_alpha()
		self.die = pygame.transform.rotozoom(self.die, 0, 0.5)
		self.index = 0
		self.frames = [run1, run2]
		self.image = self.frames[self.index]
		self.gravity = 0
		self.rect = self.image.get_rect(midbottom = (100, 345))
		self.mask = pygame.mask.from_surface(self.image)
		self.sound = pygame.mixer.Sound("jump.mp3")

	def jump(self):
		self.gravity += 1
		if game_active: self.rect.y += self.gravity
		if self.rect.bottom >= 345:
			self.rect.bottom = 345
			keys = pygame.key.get_pressed()
			if keys[pygame.K_SPACE]:
				self.gravity = -25
				self.sound.play()

	def change_frames(self):
		if game_active == False:
			self.image = self.die 
		else:
			if self.rect.bottom < 345:
				self.image = self.jump_im
			else:
				self.index += 0.08
				if self.index >= len(self.frames):
					self.index = 0
				self.image = self.frames[int(self.index)]
		
	def update(self):
		self.change_frames()
		self.jump()

class Obstacles(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		bird1 = pygame.image.load("graphics/Bird_01.png").convert_alpha()
		bird2 = pygame.image.load("graphics/Bird_02.png").convert_alpha()
		self.frames = [bird1, bird2]
		self.radian = 0
		self.index = 0
		self.image = self.frames[self.index] 
		self.rect = self.image.get_rect(midbottom = (randint(1000, 1200), 250))

	def change_frames(self):
		self.index += 0.08 
		if self.index >= len(self.frames):
			self.index = 0
		self.image = self.frames[int(self.index)]

	def move(self):
		self.rect.x -= 5
		self.radian += pi/30
		self.rect.bottom = 200 + 20*sin(self.radian)

	def destroy(self):
		if self.rect.right <= 0:
			self.kill()
	def update(self):
		if game_active:	
			self.move()
		self.change_frames()
		self.destroy()

def check_collide():
	global game_active
	if pygame.sprite.spritecollide(dino.sprite, obstacles, False, pygame.sprite.collide_mask):
		game_active = False
		print("collision")

def choose_obstacles(brand):
	if brand == 0: obstacles.add(Obstacles())
	else: create_cactus_list()

def create_cactus_list():
	global cactus_group
	cactus_new_list = []
	cactus_group.append(cactus_new_list)
	for i in range(3):
		size = randint(0,2)
		if i == 0:
			if size == 2:
				cactus_new_list.append(large_cactus.get_rect(bottomleft = (1000, 340)))
			elif size == 1:
				cactus_new_list.append(small_cactus.get_rect(bottomleft = (1000, 340)))
			else:
				cactus_new_list.append(pygame.Rect(1000,340, 1, 1))
		else:
			if size == 2:
				cactus_new_list.append(large_cactus.get_rect(bottomleft = (cactus_new_list[i-1].right , 340)))
			elif size == 1:
				cactus_new_list.append(small_cactus.get_rect(bottomleft = (cactus_new_list[i-1].right, 340)))
			else:
				cactus_new_list.append(pygame.Rect(cactus_new_list[i-1].right, 340, 1, 1))

def active_cactus_list():
	global cactus_group, game_active
	surf = large_cactus	
	if cactus_group:
		for cactus_list in cactus_group:
			for cactus in cactus_list:
				if cactus.width != 1:
					if cactus.width == 50: 
						surf = large_cactus
					elif cactus.width == 34:
						surf = small_cactus
					screen.blit(surf, cactus)
					if game_active:
						cactus.x -= 5
					cactus_mask = pygame.mask.from_surface(surf)
					if getattr(dino.sprite, "mask").overlap(cactus_mask, 
		(cactus.left - getattr(dino.sprite, "rect").left, cactus.top - getattr(dino.sprite, "rect").top)):
						game_active = False

		if cactus_group[0][2].right <= 0:
			cactus_group.pop(0)

def cal_score():
	global score
	current_time = pygame.time.get_ticks()
	score = int(current_time/1000 - start_time) 
	score_surf = font.render(f'Score: {score}', "black", False)
	score_rect = score_surf.get_rect(center = (500, 100))
	screen.blit(score_surf, score_rect)

background_1 = pygame.image.load('graphics/Ground.png').convert_alpha()
background_2 = pygame.image.load('graphics/Ground.png').convert_alpha()

large_cactus = pygame.image.load("graphics/Cactus_Large_Single.png").convert_alpha()
small_cactus = pygame.image.load("graphics/Cactus_Small_Single.png").convert_alpha()

bird1 = pygame.image.load("graphics/Bird_01.png").convert_alpha()
bird2 = pygame.image.load("graphics/Bird_02.png").convert_alpha()

retry = pygame.image.load("graphics/retry.png").convert_alpha()
retry_rect = retry.get_rect(center = (500, 200))

font = pygame.font.Font("Pixeltype.ttf", 50)
retry_text = font.render("Press Space To Play", "black", False)
retry_text_rect = retry_text.get_rect(center = (500, 100))

#Dinosaurce
dino = pygame.sprite.GroupSingle()
dino.add(Dino())

#Obstacle
obstacles = pygame.sprite.Group()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if game_active == True:
			if event.type == obstacles_event:
				choose_obstacles(randint(0,3))
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				cactus_group.clear()
				start_time = pygame.time.get_ticks()/1000
				getattr(dino.sprite, "rect").bottom = 345 
				obstacles.empty()

	#background
	screen.fill(screen_color)
	screen.blit(background_1, (bg_x,250))
	screen.blit(background_2, (bg_x+2400,250))
	#Dino
	dino.draw(screen)
	dino.update()

	#Obstacles
	obstacles.draw(screen)
	active_cactus_list()
	obstacles.update()
	if game_active:
		bg_x -= 5
		if bg_x <= -2400:
			bg_x = 0

		#Check collide
		check_collide()

		#Score
		cal_score()
	else:
		screen.blit(retry_text, retry_text_rect)
		if score != 0: screen.blit(retry, retry_rect)

	pygame.display.flip()
	clock.tick(60)
pygame.quit()