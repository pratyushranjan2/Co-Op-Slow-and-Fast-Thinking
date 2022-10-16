
def readFileInput():

    global f

    # agents in team 1
    team1_size = int(f.readline())
    
    team1 = []
    solver1 = []

    for i in range(team1_size):
        [x, y, solver] = [int(i) for i in f.readline().split()]
        team1.append([x,y])
        solver1.append(solver)

    # # agents in team 1 that solely block
    # blockers = team1+1

    # while(blockers<0 or blockers>team1):
    #     blockers = input("Number of agents in team 1 purposed to block: ")

    # agents in team 2
    team2_size = int(f.readline())
    
    team2 = []
    solver2 = []

    for i in range(team2_size):
        [x, y, solver] = [int(i) for i in f.readline().split()]
        team2.append([x,y])
        solver2.append(solver)

    # ghosts
    ghosts_size = int(f.readline())
    ghosts = []

    for i in range(ghosts_size):
        [x, y] = [int(i) for i in f.readline().split()]
        ghosts.append([x,y])
    
    return [team1, solver1, team2, solver2, ghosts]

def agentsInput():
    # agents in team 1
    team1_size = 0

    while(team1_size<=0):
        team1_size = input("Number of agents in team 1: ")
    
    team1 = []
    solver1 = []

    for i in range(team1_size):
        x, y = 0, 0
        x = input("Row: ")
        y = input("Column: ")
        team1.append([x,y])

        solver = input("1: s1 solver \t 2: s2 solver\n")
        solver1.append(solver)

    # # agents in team 1 that solely block
    # blockers = team1+1

    # while(blockers<0 or blockers>team1):
    #     blockers = input("Number of agents in team 1 purposed to block: ")

    # agents in team 1
    team2_size = 0

    while(team2_size<=0):
        team2_size = input("Number of agents in team 2: ")
    
    team2 = []
    solver2 = []

    for i in range(team2_size):
        x, y = 0, 0
        x = input("Row: ")
        y = input("Column: ")
        team2.append([x,y])

        solver = input("2: s1 solver \t 2: s2 solver\n")
        solver2.append(solver)

    # ghosts
    ghosts = -1

    while(ghosts<0):
        ghosts = input("Number of agents as ghosts: ")
    
    # positions = []

    # for i in range(team1):
    #     x = input("Row: ")
    #     y = input("Column: ")
    #     positions.append([x,y])

    return [team1, solver1, team2, solver2, ghosts]

f = open("configs.txt")
sets = int(f.readline())

for _ in range(sets):
    inp = readFileInput()
    print(inp)


    # config = readFileInput()
    # print(config)
    # ind = 0

    # mas_args['pacmans'] = []
    # mas_args['nteams'] = 2

    # # team1
    # for i in range(len(config[0])):
    #     pacman_type = loadAgent("System"+str(config[1][i])+"Agent", noKeyboard)
    #     pacman_ind = pacman_type(**agentOpts)
    #     pacman_ind.index = ind
    #     pacman_ind.team = 0
    #     mas_args['pacmans'].append(pacman_ind)

    #     ind += 1
    
    # # team2
    # for i in range(len(config[2])):
    #     pacman_type = loadAgent("System"+str(config[3][i])+"Agent", noKeyboard)
    #     pacman_ind = pacman_type(**agentOpts)
    #     pacman_ind.index = ind
    #     pacman_ind.team = 1
    #     mas_args['pacmans'].append(pacman_ind)

    #     ind += 1
    
    # for pm in mas_args['pacmans']:
    #     pm.numPacman = ind