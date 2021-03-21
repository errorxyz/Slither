import pygame
import time
import random

pygame.init()
#defining variables here
disp_width = 800
disp_height = 600
block_size = 10
appleThickness = 20
FPS = 20
img = pygame.image.load('snakeblack.png')
apple = pygame.image.load('appleblack.png')
direction = "right"

smallfont = pygame.font.SysFont("comicsansms", 35)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 65)

black=(255,255,255)
white=(0,0,0)
red=(255,0,0)
green=(0,155,0)

gameDisplay=pygame.display.set_mode((disp_width,disp_height))

pygame.display.set_caption('Slither')

clock = pygame.time.Clock()

def pause():
	pause = True
	msg_to_screen("Paused", black, -100, "large")
	msg_to_screen("press c to continue or press q to quit", black, 50, "small")
	while pause:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					pygame.quit()
					quit()
				elif event.key == pygame.K_c:
					pause = False
		pygame.display.update()
		clock.tick(5)

def score(score):
	text = smallfont.render("Score: "+str(score), True, black)
	gameDisplay.blit(text, [0,0])
	pygame.display.update()

def appleGen():
	appleX = round(random.randrange(0,disp_width-appleThickness))
	appleY = round(random.randrange(0, disp_height-appleThickness))
	return appleX, appleY
	
def gameIntro():
	intro = True
	
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
						pygame.quit()
						quit()
				elif event.key == pygame.K_c:
						intro = False
		gameDisplay.fill(white)
		msg_to_screen("Welcome to Slither", green, -100, "large")
		msg_to_screen("The Objective of the game is to eat red apples", black, -30, "small")
		msg_to_screen("If you bite yourself or go outta the screen...", black, 10, "small")
		msg_to_screen("THEN YOU ARE DEAD", black, 50, "small")
		msg_to_screen("Press c to play, p to pause or q to quit", black, 90, "small")
		pygame.display.update()
		clock.tick(5)
	

def snake(snakeList, block_size):
	
	if direction == "right":
		head = pygame.transform.rotate(img, 270)
	elif direction == "left":
		head = pygame.transform.rotate(img, 90)
	elif direction == "up":
		head = img
	elif direction == "down":
		head = pygame.transform.rotate(img, 180)
	
	
	gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
	
	for XnY in snakeList[:-1]:
		pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size,block_size])
		
def text_objects(text,color, size):
	if size == "small":
		textSurface=smallfont.render(text,True,color)
	elif size == "medium":
		textSurface=medfont.render(text,True,color)
	elif size == "large":
		textSurface=largefont.render(text,True,color)
	return textSurface, textSurface.get_rect()

def msg_to_screen(msg, color, y_displace = 0, size="small"):
	textSurf, textRect = text_objects(msg,color, size)
	textRect.center = (disp_width /2), (disp_width /2)+y_displace
	gameDisplay.blit(textSurf,textRect)

def gameLoop():
	global direction
	gameExit=False
	gameOver=False
	
	lead_x=disp_width/2
	lead_y=disp_height/2
	
	lead_x_change = 0
	lead_y_change = 0
	
	snakeList = []
	snakeLength = 1
	
	appleX, appleY = appleGen()
	
	while not gameExit:
		if gameOver == True:
			msg_to_screen("Game Over!", red, y_displace = -50, size = "large")
			msg_to_screen("press c to continue or q to quit", black, y_displace=50, size="medium")
		while gameOver == True:
			pygame.display.update()
			for event in pygame.event.get():
			
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameExit = True
						gameOver =False
					if event.key == pygame.K_c:
						gameLoop()
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				gameExit=True
				
			if event.type == pygame.KEYDOWN:
				
				if event.key == pygame.K_a:
					direction = "left"
					lead_x_change = -block_size
					lead_y_change = 0
				elif event.key == pygame.K_d:
					direction = "right"
					lead_x_change = block_size
					lead_y_change = 0
				elif event.key == pygame.K_w:
					direction = "up"
					lead_y_change = -block_size
					lead_x_change = 0
				elif event.key == pygame.K_s:
					direction = "down"
					lead_y_change = block_size
					lead_x_change = 0
				elif event.key == pygame.K_p:
					pause()
					
		if lead_x >= disp_width or lead_x < 0 or lead_y >= disp_height or lead_y < 0:
			gameOver = True
		lead_x += lead_x_change
		lead_y += lead_y_change
		
		gameDisplay.fill(white)
		pygame.draw.rect(gameDisplay, black, [disp_width,0,5,disp_height])
		pygame.draw.rect(gameDisplay, black,[0,disp_height,disp_width,5])
		gameDisplay.blit(apple, [appleX, appleY])

		if len(snakeList) > snakeLength:
			del snakeList[0]
		
		for eachSegment in snakeList[:-1]:
			if eachSegment == snakeHead:
				gameOver = True
		
		snakeHead = []
		snakeHead.append(lead_x)
		snakeHead.append(lead_y)
		snakeList.append(snakeHead)
		snake(snakeList, block_size)
		score(snakeLength-1)
		pygame.display.update()
		
		
		if lead_x > appleX and lead_x < appleX + appleThickness or lead_x + block_size > appleX and lead_x + block_size < appleX + appleThickness:
			
			if lead_y > appleY and lead_y < appleY + appleThickness or lead_y + block_size > appleY and lead_y + block_size < appleY + appleThickness:
				
				appleX, appleY = appleGen()
				snakeLength += 1
			
		clock.tick(FPS)	
	
	pygame.quit()
	quit()

gameIntro()
gameLoop()
