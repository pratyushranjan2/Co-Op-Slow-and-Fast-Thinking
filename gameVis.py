import pygame, sys
import json
import time

STATE_GRID = []

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
GRID_HEIGHT = 7
GRID_WIDTH = 22

UNIT_SIZE = 50

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (64, 64, 64)
BLUE = (0, 127, 255)
GREEN = (0, 255, 64)
YELLOW = (220, 220, 0)
RED = (200, 0, 0)

# symbol macros
WALL = '%'
PACMAN = 'P'
GHOST = 'G'
FOOD = '.'
BLANK = ' '

# state vars

PACMANS = [0, 0, 1]
PACMAN_LIFE = [True, True, True]
PACMAN_POS = [[2,5], [10,5], [18,5]]
PACMAN_COLOR = [GREEN, BLUE]

GHOST_POS = [[9,1], [12,1]]

FOOD_POS = {}

INVERT = 6

# logs
LOGS = []
LOGSIZE = 0

def logReader(filename):
    global LOGS, LOGSIZE

    with open(filename, 'r') as f:
        LOGS = [line.strip() for line in f.readlines()]
    
    LOGSIZE = len(LOGS)

def loadState(filename):
    state_grid = []

    with open(filename, 'r') as f:
        state_grid = [line.strip() for line in f.readlines()]

    return state_grid

def initGrid(state_grid):
    global GRID_HEIGHT, GRID_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, UNIT_SIZE, INVERT

    GRID_WIDTH = len(state_grid[0])
    GRID_HEIGHT = len(state_grid)
    SCREEN_WIDTH = UNIT_SIZE*GRID_WIDTH
    SCREEN_HEIGHT = UNIT_SIZE*GRID_HEIGHT

    INVERT = GRID_HEIGHT-1

    for h in range(GRID_HEIGHT):
        for w in range(GRID_WIDTH):
            if(STATE_GRID[h][w]==FOOD):
                FOOD_POS[(h,w)] = 1
            else:
                FOOD_POS[(h,w)] = 0
    
    global STATE_GRID

    temp = []
    for s in STATE_GRID:
        temp.append(list(s))
    
    STATE_GRID = temp

def drawCell(surface, cell, xpos, ypos):
    
    global GRID_HEIGHT, GRID_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, UNIT_SIZE, STATE_GRID

    rect = pygame.Rect(ypos*UNIT_SIZE, xpos*UNIT_SIZE, UNIT_SIZE, UNIT_SIZE)
    food = pygame.Rect((ypos+3.0/8.0)*UNIT_SIZE, (xpos+3.0/8.0)*UNIT_SIZE, UNIT_SIZE/4, UNIT_SIZE/4)
    player = pygame.Rect((ypos+0.25)*UNIT_SIZE, (xpos+0.25)*UNIT_SIZE, UNIT_SIZE/2, UNIT_SIZE/2)

    color = BLACK

    if cell == WALL:
        color = GREY

    elif cell == PACMAN:
        color = BLACK
        rect = player

        for i in range(len(PACMAN_POS)):
            p = PACMAN_POS[i]

            if not PACMAN_LIFE[i]:
                continue

            if p == [ypos, xpos]:
                color = PACMAN_COLOR[PACMANS[i]]
                break

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

def updateState(log):
    # print "Pacmans died! Score: %d" % state.data.score
    # print "Pacman #"+str(pacmanIndex)+" died"
    # print "all pacman dead"
    # print positions, self.state.data.deadPacmans

    global STATE_GRID, PACMAN_LIFE, PACMAN_POS, FOOD_POS, GHOST_POS

    if log[0] == '[':
        log_list = json.loads(log)
        print (log_list)

        pos = log_list[0]
        plen = len(pos)

        for p in log_list[1]:
            PACMAN_LIFE[p] = False
            STATE_GRID[PACMAN_POS[p][1]][PACMAN_POS[p][0]] = BLANK

        for p in range(3):
            # print(PACMAN_POS[p][1], PACMAN_POS[p][0])
            STATE_GRID[PACMAN_POS[p][1]][PACMAN_POS[p][0]] = BLANK

            if(PACMAN_LIFE[p]):
                PACMAN_POS[p][0] = pos[p][0]
                PACMAN_POS[p][1] = INVERT-pos[p][1]
                STATE_GRID[PACMAN_POS[p][1]][PACMAN_POS[p][0]] = PACMAN
                FOOD_POS[(PACMAN_POS[p][1], PACMAN_POS[p][0])] = 0

        for p in range(2):
            # print(GHOST_POS[p][0], GHOST_POS[p][1])

            STATE_GRID[GHOST_POS[p][1]][GHOST_POS[p][0]] = FOOD
            if (FOOD_POS[(GHOST_POS[p][1], GHOST_POS[p][0])] == 0):
                STATE_GRID[GHOST_POS[p][1]][GHOST_POS[p][0]] = BLANK
            
            GHOST_POS[p][0] = int(pos[3+p][0])
            GHOST_POS[p][1] = INVERT-int(pos[3+p][1])
            STATE_GRID[GHOST_POS[p][1]][GHOST_POS[p][0]] = GHOST
    
    # elif log[:7] == "Pacmans" or log[:3] == "all":
    #     pass

    # elif log[:6] == "Pacman":
    #     # pnum = int(log[8:-5])
    #     # PACMAN_LIFE[pnum] = False
    #     pass

    else:
        print(log)



def main():
    
    global STATE_GRID, LOGS

    fileName = "layouts/mas3.lay"
    STATE_GRID = loadState(fileName)

    # STATE_GRID =   ["%%%%%%%%%%%%%%%%%%%%%%",
    #                 "%.......%G  G%.......%",
    #                 "%..%%...%%  %%...%%..%",
    #                 "%..%%.%........%.%%..%",
    #                 "%..%%.%.%%%%%%.%.%%..%",
    #                 "%.........P.......P..%",
    #                 "%%%%%%%%%%%%%%%%%%%%%%"]

    initGrid(STATE_GRID)

    # print(STATE_GRID)
    # print(GRID_HEIGHT, GRID_WIDTH)

    fileName = "logfiles/newlog"
    logReader(fileName)

    # print(FOOD_POS.keys())
    
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pacman!")
    surface.fill(BLACK)

    LOGPTR = 0

    while True:
        time.sleep(1)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # if event.type == pygame.KEYDOWN:
            #     pygame.quit()
            #     sys.exit()
        
        drawGameState(STATE_GRID, surface)
        pygame.display.update()

        if LOGPTR<LOGSIZE:
            log = LOGS[LOGPTR]
            updateState(log)
            LOGPTR += 5
        else:
            continue
        

if __name__=="__main__":
    main()
