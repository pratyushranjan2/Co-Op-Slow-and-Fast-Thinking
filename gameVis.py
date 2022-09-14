import pygame, sys

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
GRID_HEIGHT = 7
GRID_WIDTH = 22

UNIT_SIZE = 50

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (64, 64, 64)
BLUE = (0, 127, 255)
GREEN = (0, 255, 64)
YELLOW = (255, 255, 0)
RED = (200, 0, 0)

WALL = '%'
PACMAN = 'P'
GHOST = 'G'
FOOD = '.'
BLANK = ' '

def loadState(filename):
    state_grid = []

    with open(filename, 'r') as f:
        state_grid = [line.strip() for line in f.readlines()]
    
    return state_grid

def initGrid(state_grid):
    global GRID_HEIGHT, GRID_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, UNIT_SIZE

    GRID_WIDTH = len(state_grid[0])
    GRID_HEIGHT = len(state_grid)
    SCREEN_WIDTH = UNIT_SIZE*GRID_WIDTH
    SCREEN_HEIGHT = UNIT_SIZE*GRID_HEIGHT

def logReader():
    pass

def drawCell(surface, cell, xpos, ypos):
    
    global GRID_HEIGHT, GRID_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, UNIT_SIZE

    rect = pygame.Rect(ypos*UNIT_SIZE, xpos*UNIT_SIZE, UNIT_SIZE, UNIT_SIZE)
    food = pygame.Rect((ypos+3.0/8.0)*UNIT_SIZE, (xpos+3.0/8.0)*UNIT_SIZE, UNIT_SIZE/4, UNIT_SIZE/4)
    player = pygame.Rect((ypos+0.25)*UNIT_SIZE, (xpos+0.25)*UNIT_SIZE, UNIT_SIZE/2, UNIT_SIZE/2)

    color = BLACK

    if cell == WALL:
        color = GREY

    elif cell == PACMAN:
        color = YELLOW
        rect = player

    elif cell == GHOST:
        color = RED
        rect = player

    elif cell == FOOD:
        color = WHITE
        rect = food

    pygame.draw.rect(surface, color, rect)
    

def drawGameState(state_grid, surface):

    surface.fill(BLACK)

    for w in range(GRID_WIDTH):
        for h in range(GRID_HEIGHT):
            cell = state_grid[h][w]
            drawCell(surface, cell, h, w)


def main():
    
    fileName = "layouts/mas3.lay"
    state_grid = loadState(fileName)
    print(state_grid)

    # state_grid =   ["%%%%%%%%%%%%%%%%%%%%%%",
    #                 "%.......%G  G%.......%",
    #                 "%..%%...%%  %%...%%..%",
    #                 "%..%%.%........%.%%..%",
    #                 "%..%%.%.%%%%%%.%.%%..%",
    #                 "%.........P.......P..%",
    #                 "%%%%%%%%%%%%%%%%%%%%%%"]

    initGrid(state_grid)
    
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pacman!")
    surface.fill(BLACK)

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # if event.type == pygame.KEYDOWN:
            #     pygame.quit()
            #     sys.exit()
        
        drawGameState(state_grid, surface)
        pygame.display.update()

if __name__=="__main__":
    main()
