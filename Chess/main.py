import pygame
from data.Board import Board

if not pygame.display.get_init():
    pygame.display.init()
if not pygame.font.get_init():
    pygame.font.init()

img_path = 'Sprites/w_queen.png'
icon = pygame.image.load(img_path)
pygame.display.set_icon(icon)
WINDOW_SIZE = (800, 800)
FONT = pygame.font.SysFont("Consolas", int(WINDOW_SIZE[0]/10))
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chess")
win_w = "White Wins!"
win_b = "Black Wins!"
stale = "Stalemate!"
winningrect = pygame.Rect((WINDOW_SIZE[0]//2)-255, (WINDOW_SIZE[1]//2)-75, WINDOW_SIZE[0]/1.5, WINDOW_SIZE[1]/6)
board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])
running = True
def draw(display):
	display.fill('white')
	board.draw(display)
	pygame.display.update()
#FIXED ALL BUGS (All found during testing that is)
#OPTIMIZED RAM AND CPU USAGE
if __name__ == '__main__':
	while running:
		mx, my = pygame.mouse.get_pos()
		event = pygame.event.wait() 
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN: 
			if event.button == 1:
				board.handle_click(mx, my)
		if board.is_in_checkmate('white') == 'mate': 
			print('Black wins!')
			print('Thanks for playing!')
			draw(screen)
			winner_b = FONT.render(win_b, True, (24, 25, 66))
			pygame.draw.rect(screen, 'grey', winningrect)
			screen.blit(winner_b, ((WINDOW_SIZE[0]//2)-225, (WINDOW_SIZE[1]//2)-50))
			pygame.display.update()
			pygame.time.wait(3000)
			running = False
		elif board.is_in_checkmate('black') == 'mate': 
			print('White wins!')
			print('Thanks for playing!')
			draw(screen)
			winner_w = FONT.render(win_w, True, (216, 216, 237))
			pygame.draw.rect(screen, 'grey', winningrect)
			screen.blit(winner_w, ((WINDOW_SIZE[0]//2)-225, (WINDOW_SIZE[1]//2)-50))
			pygame.display.update()
			pygame.time.wait(3000)
			running = False
		elif board.is_in_checkmate('white') == 'stalemate' or board.is_in_checkmate('black') == 'stalemate':
			print('Stalemate!')
			print('Thanks for playing!')
			draw(screen)
			stalemate = FONT.render(stale, True, (115, 115, 145))
			pygame.draw.rect(screen, 'grey', winningrect)
			screen.blit(stalemate, ((WINDOW_SIZE[0]//2)-225, (WINDOW_SIZE[1]//2)-50))
			pygame.display.update()
			pygame.time.wait(3000)
			running = False
		draw(screen)
	
