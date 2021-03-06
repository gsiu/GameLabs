import pygame, sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_START_X = 10
PADDLE_START_Y = 250
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SPEED = 8
BALL_WIDTH_HEIGHT = 16

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Load sounds
pong = pygame.mixer.Sound("pong.wav")
ping = pygame.mixer.Sound("ping.wav")
win =  pygame.mixer.Sound("Coin_Sound.wav")

# This is a rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

# Your paddle vertically centered on the left side
p1_paddle_rect = pygame.Rect((PADDLE_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))

# Enemy's paddle vertically centered on the right side
p2_paddle_rect = pygame.Rect((SCREEN_WIDTH - PADDLE_START_X - PADDLE_WIDTH, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))

# Create the center line
line = pygame.Rect((SCREEN_WIDTH / 2 - 2, 0), (4, SCREEN_HEIGHT))

# Scoring: +1 point if opponent misses the ball
p1_score, p2_score = 0, 0

# Load the font for displaying the score, game over message
font = pygame.font.Font(None, 30)
game_over_font = pygame.font.Font(None, 50)

# Screen Booleans
game_over = False
menu = True

# Bool for 1P Mode
OnePMode = False

# Variables used if in 1P Mode: slow enemy after 3 hits from player 
p1_hits = 0
p1_hit_limit = 3
enemy_Speed = BALL_SPEED 

# Game loop
while True:
	# Let player decide between 1 and 2 player
	if menu == True:
		# Clear the screen
		screen.fill((255, 255, 255))
		
		# Make and blit fonts for menu
		Title = game_over_font.render("Pong", 1, (0, 0, 0))
		Title_width = Title.get_rect()[2]
		screen.blit(Title, ((SCREEN_WIDTH - Title_width)/ 2, 200))
		
		OneP = font.render("Press '1' for One Player", 1, (0, 0, 0))
		OneP_width = OneP.get_rect()[2]
		OneP_height = OneP.get_rect()[3]
		screen.blit(OneP, ((SCREEN_WIDTH - OneP_width)/ 2, SCREEN_HEIGHT / 2))
		
		TwoP = font.render("Press '2' for Two Player", 1, (0, 0, 0))
		TwoP_width = TwoP.get_rect()[2]
		TwoP_height = TwoP.get_rect()[3]
		screen.blit(TwoP, ((SCREEN_WIDTH - TwoP_width)/ 2, SCREEN_HEIGHT / 2 + OneP_height))
		
		# Event handler
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
				pygame.quit()
		if pygame.key.get_pressed()[pygame.K_ESCAPE]:
			sys.exit(0)
			pygame.quit()
		elif pygame.key.get_pressed()[pygame.K_1]:
			menu = False
			OnePMode = True
		elif pygame.key.get_pressed()[pygame.K_2]:
			menu = False
			OnePMode = False
		
		# Flip the display
		pygame.display.flip()
		
	elif game_over == False:
		# Event handler
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
				pygame.quit()
			# Control the paddle with the mouse
			elif event.type == pygame.MOUSEMOTION:
				p1_paddle_rect.centery = event.pos[1]
			# correct paddle position if it's going out of window
			if p1_paddle_rect.top < 0:
				p1_paddle_rect.top = 0
			elif p1_paddle_rect.bottom >= SCREEN_HEIGHT:
				p1_paddle_rect.bottom = SCREEN_HEIGHT
			
			if p2_paddle_rect.top < 0:
				p2_paddle_rect.top = 0
			elif p2_paddle_rect.bottom >= SCREEN_HEIGHT:
				p2_paddle_rect.bottom = SCREEN_HEIGHT

		# Two player mode
		if OnePMode == False:
			# This tests if w/s are pressed; if yes, move p1's paddle
			if pygame.key.get_pressed()[pygame.K_w] and p1_paddle_rect.top > 0:
				p1_paddle_rect.top -= BALL_SPEED
			elif pygame.key.get_pressed()[pygame.K_s] and p1_paddle_rect.bottom < SCREEN_HEIGHT:
				p1_paddle_rect.top += BALL_SPEED		
			# This tests if up/down are pressed; if yes, move p2's paddle
			if pygame.key.get_pressed()[pygame.K_UP] and p2_paddle_rect.top > 0:
				p2_paddle_rect.top -= BALL_SPEED
			elif pygame.key.get_pressed()[pygame.K_DOWN] and p2_paddle_rect.bottom < SCREEN_HEIGHT:
				p2_paddle_rect.top += BALL_SPEED
				
		# One player mode
		else:
			# This tests if up/down are pressed; if yes, move p1's paddle
			if pygame.key.get_pressed()[pygame.K_UP] and p1_paddle_rect.top > 0:
				p1_paddle_rect.top -= BALL_SPEED
			elif pygame.key.get_pressed()[pygame.K_DOWN] and p1_paddle_rect.bottom < SCREEN_HEIGHT:
				p1_paddle_rect.top += BALL_SPEED		
			# Move enemy's paddle according to ball position
			if p2_paddle_rect.center[1] > ball_rect.center[1] and p2_paddle_rect.top > 0:
				p2_paddle_rect.top -= enemy_Speed
			elif p2_paddle_rect.center[1] < ball_rect.center[1]and p2_paddle_rect.bottom < SCREEN_HEIGHT:
				p2_paddle_rect.top += enemy_Speed
			# Slow the enemy if player 1 has returned 10 hits
			if p1_hits >= p1_hit_limit:
				p1_hits = 0
				enemy_Speed -= 1
		
			
		if pygame.key.get_pressed()[pygame.K_ESCAPE]:
			sys.exit(0)
			pygame.quit()
		
		# Update ball position
		ball_rect.left += ball_speed[0]
		ball_rect.top += ball_speed[1]
		
		# Ball collision with rails
		if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
			ball_speed[1] = -ball_speed[1]
			ping.play()
			
		# A player has scored
		if ball_rect.right >= SCREEN_WIDTH:
			ball_rect.topleft = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
			ball_speed = [BALL_SPEED, BALL_SPEED]
			p1_score += 1
			# Reset enemy's speed (only used in 1P mode)
			enemy_Speed = BALL_SPEED
			win.play()
		if ball_rect.left <= 0:
			ball_rect.topleft = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
			ball_speed = [-1 * BALL_SPEED, BALL_SPEED]
			p2_score += 1
			# Reset enemy's speed (only used in 1P mode)
			enemy_Speed = BALL_SPEED
			win.play()
				
		# A player has won
		if p1_score == 11:
			game_over = True
			winner = 1
		elif p2_score == 11:
			game_over = True
			winner = 2
			
		# Test if the ball is hit by the paddle; if yes reverse speed and play sound
		if p1_paddle_rect.colliderect(ball_rect):
			ball_speed[0] = -ball_speed[0]
			pong.play()
			# Increment number of hits p1 has returned (only used in 1P mode)
			p1_hits += 1
		elif p2_paddle_rect.colliderect(ball_rect):
			ball_speed[0] = -ball_speed[0]
			pong.play()	
			
		# Clear screen
		screen.fill((255, 255, 255))
		
		# Render the centerline, ball, paddles, and the score
		pygame.draw.rect(screen, (255, 0, 0), line) # Center line
		pygame.draw.rect(screen, (0, 0, 0), p1_paddle_rect) # Your paddle
		pygame.draw.rect(screen, (0, 0, 0), p2_paddle_rect) # Enemy's paddle
		pygame.draw.circle(screen, (0, 0, 0), ball_rect.center, ball_rect.width / 2) # The ball
		
		p1_score_text = font.render(str(p1_score), True, (0, 0, 0))
		screen.blit(p1_score_text, ((SCREEN_WIDTH / 4) - font.size(str(p1_score))[0] / 2, 5)) # Player's score
		
		p2_score_text = font.render(str(p2_score), True, (0, 0, 0))
		screen.blit(p2_score_text, ((3 * SCREEN_WIDTH / 4) - font.size(str(p1_score))[0] / 2, 5)) # Computer's score
		
		
		# Update screen and wait 20 milliseconds
		pygame.display.flip()
		pygame.time.delay(20)
		
	# Game Over
	else:
		# Clear screen
		screen.fill((255, 255, 255))

		# Create Game Over message
		G_Over = game_over_font.render("Game Over", 1, (0, 0, 0))
		G_Over_width = G_Over.get_rect()[2]
		G_Over_height = G_Over.get_rect()[3]
		screen.blit(G_Over, ((SCREEN_WIDTH - G_Over_width)/ 2, SCREEN_HEIGHT / 2))
		
		if winner == 1:
			message = "Player 1"
		else:
			message = "Player 2"
		
		NewGame = font.render("Winner: " + message + ". To play again, press 'R'", 1, (0, 0, 0))
		NewGame_width = NewGame.get_rect()[2]
		screen.blit(NewGame, ((SCREEN_WIDTH - NewGame_width)/2, SCREEN_HEIGHT / 2 + G_Over_height))

		# Event handling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		if pygame.key.get_pressed()[pygame.K_ESCAPE]:
			sys.exit(0)
			pygame.quit()
		elif pygame.key.get_pressed()[pygame.K_r]:
			# Reset values to start a new game
			menu = True
			game_over = False
			p1_paddle_rect.topleft = (PADDLE_START_X, PADDLE_START_Y)
			p2_paddle_rect.topleft = (SCREEN_WIDTH - PADDLE_START_X - PADDLE_WIDTH, PADDLE_START_Y)
			p1_score, p2_score = 0, 0

			# Send the ball to the loser
			if winner == 1:
				ball_rect.topleft = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
				ball_speed = [1 * BALL_SPEED, BALL_SPEED]

			else:
				ball_rect.topleft = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
				ball_speed = [-1 * BALL_SPEED, BALL_SPEED]

		# Flip the display
		pygame.display.flip()

