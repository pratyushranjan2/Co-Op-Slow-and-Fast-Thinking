# pacman.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
Pacman.py holds the logic for the classic pacman game along with the main
code to run a game.  This file is divided into three sections:

  (i)  Your interface to the pacman world:
          Pacman is a complex environment.  You probably don't want to
          read through all of the code we wrote to make the game runs
          correctly.  This section contains the parts of the code
          that you will need to understand in order to complete the
          project.  There is also some code in game.py that you should
          understand.

  (ii)  The hidden secrets of pacman:
          This section contains all of the logic code that the pacman
          environment uses to decide who can move where, who dies when
          things collide, etc.  You shouldn't need to read this section
          of code, but you can if you want.

  (iii) Framework to start a game:
          The final section contains the code for reading the command
          you use to set up the game, then starting up a new game, along with
          linking in all the external parts (agent functions, graphics).
          Check this section out to see all the options available to you.

To play your first game, type 'python pacman.py' from the command line.
The keys are 'a', 's', 'd', and 'w' to move (or arrow keys).  Have fun!
"""
from game import GameStateData
from game import Game
from game import Directions
from game import Actions
from util import nearestPoint
from util import manhattanDistance
from multiprocessing import Pool
from collections import OrderedDict
import util, layout
import sys, types, time, random, os
import pandas as pd
import  cPickle
from datetime import datetime, timedelta
import os
import traceback

###################################################
# YOUR INTERFACE TO THE PACMAN WORLD: A GameState #
###################################################

class GameState:
    """
    A GameState specifies the full game state, including the food, capsules,
    agent configurations and score changes.

    GameStates are used by the Game object to capture the actual state of the game and
    can be used by agents to reason about the game.

    Much of the information in a GameState is stored in a GameStateData object.  We
    strongly suggest that you access that data via the accessor methods below rather
    than referring to the GameStateData object directly.

    Note that in classic Pacman, Pacman is always agent 0.
    """

    ####################################################
    # Accessor methods: use these to access state data #
    ####################################################

    # static variable keeps track of which states have had getLegalActions called
    explored = set()
    def getAndResetExplored():
        tmp = GameState.explored.copy()
        GameState.explored = set()
        return tmp
    getAndResetExplored = staticmethod(getAndResetExplored)

    def getLegalActions( self, agentIndex=0, pacmanInfo=None):
        """
        Returns the legal actions for the agent specified.
        """

        # ai = agentIndex
        # if pacmanInfo: ai=pacmanInfo['agentIndex']
        # print agentIndex, pacmanInfo != None
        
#        GameState.explored.add(self)
        if self.isWin() or self.isLose(): return []

        if agentIndex < self.data.numPacman:  # Pacman is moving
            return PacmanRules.getLegalActions( self, pacmanInfo )
        else:
            return GhostRules.getLegalActions( self, agentIndex )

    def generateSuccessor( self, agentIndex, action, numPacman, deadPacmans, pacmanInfo, team_map):
        """
        Returns the successor state after the specified agent takes the action.
        """
        # Check that successors exist
        if self.isWin() or self.isLose(): raise Exception('Can\'t generate a successor of a terminal state.')

        # Copy current state
        state = GameState(self)

        # Let agent's logic deal with its action's effects on the board
        if agentIndex < numPacman:  # Pacman is moving
            state.data._eaten = [False for i in range(state.getNumAgents())]
            PacmanRules.applyAction( state, action, pacmanInfo )
        else:                # A ghost is moving
            GhostRules.applyAction( state, action, agentIndex )

        # Time passes
        if agentIndex < numPacman:
            state.data.scoreChange += -TIME_PENALTY # Penalty for waiting around
            state.data.scores[pacmanInfo['team']] += -TIME_PENALTY
        else:
            GhostRules.decrementTimer( state.data.agentStates[agentIndex] )

        # Resolve multi-agent effects
        GhostRules.checkDeath( state, agentIndex, numPacman, team_map )

        # Book keeping
        state.data._agentMoved = agentIndex
        state.data.score += state.data.scoreChange
        if agentIndex < numPacman:
            state.data.scores[pacmanInfo['team']] += state.data.scoreChange
        GameState.explored.add(self)
        GameState.explored.add(state)
        return state

    def getLegalPacmanActions( self ):
        return self.getLegalActions( 0 )

    def generatePacmanSuccessor( self, action ):
        """
        Generates the successor state after the specified pacman move
        """
        return self.generateSuccessor( 0, action )

    def getPacmanState( self, agentIndex=0 ):
        """
        Returns an AgentState object for pacman (in game.py)

        state.pos gives the current position
        state.direction gives the travel vector
        """
        return self.data.agentStates[agentIndex].copy()
    
    def getPacmanStates(self, numPacman, ignore=[]):
        return [self.data.agentStates[i] for i in range(numPacman)\
                if i not in ignore]

    def getPacmanPosition( self, agentIndex=0 ):
        return self.data.agentStates[agentIndex].getPosition()

    def getPacmanPositions( self, numPacman, ignore=[] ):
        return [ self.data.agentStates[i].getPosition() for i in range(numPacman)\
                    if i not in ignore ]
    
    def getPacmanTeamPositions( self, team, ignore=[] ):
        pacman_ids = self.data.team1 if team == 1 else self.data.team2
        return [ self.data.agentStates[i].getPosition() for i in pacman_ids\
                    if i not in ignore ]
    
    def getAllAgentPositions(self):
        return [ self.data.agentStates[i].getPosition() for i in range(len(self.data.agentStates)) ]

    def getGhostStates( self ):
        return self.data.agentStates[self.data.numPacman:]

    def getGhostState( self, agentIndex ):
        if agentIndex == 0 or agentIndex >= self.getNumAgents():
            raise Exception("Invalid index passed to getGhostState")
        return self.data.agentStates[agentIndex]

    def getGhostPosition( self, agentIndex ):
        if agentIndex < self.data.numPacman:
            raise Exception("Pacman's index passed to getGhostPosition")
        return self.data.agentStates[agentIndex].getPosition()

    def getGhostPositions(self):
        return [s.getPosition() for s in self.getGhostStates()]

    def getNumAgents( self ):
        return len( self.data.agentStates )

    def getScore( self ):
        return float(self.data.score)
    
    def getTeamScore(self, team):
        return self.data.scores[team]

    def getCapsules(self):
        """
        Returns a list of positions (x,y) of the remaining capsules.
        """
        return self.data.capsules

    def getNumFood( self ):
        return self.data.food.count()

    def getFood(self):
        """
        Returns a Grid of boolean food indicator variables.

        Grids can be accessed via list notation, so to check
        if there is food at (x,y), just call

        currentFood = state.getFood()
        if currentFood[x][y] == True: ...
        """
        return self.data.food

    def getWalls(self):
        """
        Returns a Grid of boolean wall indicator variables.

        Grids can be accessed via list notation, so to check
        if there is a wall at (x,y), just call

        walls = state.getWalls()
        if walls[x][y] == True: ...
        """
        return self.data.layout.walls

    def hasFood(self, x, y):
        return self.data.food[x][y]

    def hasWall(self, x, y):
        return self.data.layout.walls[x][y]

    def isLose( self ):
        return self.data._lose

    def isWin( self ):
        return self.data._win
    
    def allDeadIn(self, team):
        for pacmanAgent in self.pacmanAgents:
            if pacmanAgent.team == team and pacmanAgent.index not in self.data.deadPacmans:
                return False
        return True

    #############################################
    #             Helper methods:               #
    # You shouldn't need to call these directly #
    #############################################

    def __init__( self, prevState = None ):
        """
        Generates a new state by copying information from its predecessor.
        """
        if prevState != None: # Initial state
            self.data = GameStateData(prevState.data)
            self.pacmanAgents = prevState.pacmanAgents
        else:
            self.data = GameStateData()

    def deepCopy( self ):
        state = GameState( self )
        state.data = self.data.deepCopy()
        return state

    def __eq__( self, other ):
        """
        Allows two states to be compared.
        """
        return hasattr(other, 'data') and self.data == other.data

    def __hash__( self ):
        """
        Allows states to be keys of dictionaries.
        """
        return hash( self.data )

    def __str__( self ):

        return str(self.data)

    def initialize( self, layout, nteams, team1, team2, biasedGhost, numGhostAgents=1000 ):
        """
        Creates an initial game state from a layout array (see layout.py).
        """
        self.data.initialize(layout, nteams, team1, team2, biasedGhost, numGhostAgents)

############################################################################
#                     THE HIDDEN SECRETS OF PACMAN                         #
#                                                                          #
# You shouldn't need to look through the code in this section of the file. #
############################################################################

SCARED_TIME = 40    # Moves ghosts are scared
COLLISION_TOLERANCE = 0.7 # How close ghosts must be to Pacman to kill
TIME_PENALTY = 1 # Number of points lost each round

class ClassicGameRules:
    """
    These game rules manage the control flow of a game, deciding when
    and how the game starts and ends.
    """
    def __init__(self, timeout=30):
        self.timeout = timeout

    def newGame( self, layout, pacmanAgent, pacmanAgents, numPacman, nteams, biasedGhost, shuffleTurns, startingIndex, ghostAgents, display, quiet = False, catchExceptions=False):
        agents = [pacmanAgent] + ghostAgents[:layout.getNumGhosts()]
        mas_agents = [agent for agent in pacmanAgents] + ghostAgents[:layout.getNumGhosts()]
        team1 = [agent.index for agent in pacmanAgents if agent.team == 0]
        team2 = [agent.index for agent in pacmanAgents if agent.team == 1]
        initState = GameState()
        initState.initialize( layout, nteams, team1, team2, biasedGhost, len(ghostAgents) )
        game = Game(agents, mas_agents, layout.numPacman, biasedGhost, shuffleTurns, display, self, startingIndex=startingIndex, catchExceptions=catchExceptions)
        game.state = initState
        game.state.pacmanAgents = pacmanAgents
        self.initialState = initState.deepCopy()
        self.quiet = quiet
        return game

    def process(self, state, game):
        """
        Checks to see whether it is time to end the game.
        """
        if state.isWin(): self.win(state, game)
        if state.isLose(): self.lose(state, game)

    def win( self, state, game ):
        if not self.quiet: print "All food consumed! Scores: " + str(state.data.scores)
        game.gameOver = True

    def lose( self, state, game ):
        if not self.quiet:
            x,y = state.getPacmanPosition()
            columns = ["x" , "y"]
            rows = [x,y]
            df = pd.DataFrame(columns = columns)

            # if(os.stat("heat_map_sys0().csv").st_size != 0):
            #     df.loc[len(columns)] = rows
            #     df.to_csv ("heat_map_sys0().csv", index = None,mode='a', header=False)
            # else:
            #     df.append(rows)
            #     df.to_csv ("heat_map_sys0().csv", index = None, header=True)
            print "Game Over! Scores: " + str(state.data.scores)
        game.gameOver = True

    def getProgress(self, game):
        return float(game.state.getNumFood()) / self.initialState.getNumFood()

    def agentCrash(self, game, agentIndex):
        if agentIndex == 0:
            print "Pacman crashed"
        else:
            print "A ghost crashed"

    def getMaxTotalTime(self, agentIndex):
        return self.timeout

    def getMaxStartupTime(self, agentIndex):
        return self.timeout

    def getMoveWarningTime(self, agentIndex):
        return self.timeout

    def getMoveTimeout(self, agentIndex):
        return self.timeout

    def getMaxTimeWarnings(self, agentIndex):
        return 0

class PacmanRules:
    """
    These functions govern how pacman interacts with his environment under
    the classic game rules.
    """
    PACMAN_SPEED=1

    def getLegalActions( state, pacmanInfo ):
        """
        Returns a list of possible actions.
        """
        assert pacmanInfo != None
        #print state.getPacmanPositions(pacmanInfo['numPacman'])
        agentIndex = pacmanInfo['agentIndex']
        trgPacmanState = state.getPacmanState(agentIndex)
        # otherPacmanPositions should ignore current pacman
        # and dead pacmans
        ignorePositions = state.getPacmanPositions(pacmanInfo['numPacman'],\
                                                        ignore=[ agentIndex ] + state.data.deadPacmans)
        if state.data.biasedGhost:
            ignorePositions += state.getGhostPositions()
            
        return Actions.getMASPossibleActions( trgPacmanState.configuration, ignorePositions, state.data.layout.walls )
        #return Actions.getPossibleActions( state.getPacmanState().configuration, state.data.layout.walls )
    getLegalActions = staticmethod( getLegalActions )

    def applyAction( state, action, pacmanInfo ):
        """
        Edits the state to reflect the results of the action.
        """
        assert pacmanInfo != None
        agentIndex = pacmanInfo['agentIndex']
        legal = PacmanRules.getLegalActions( state, pacmanInfo )
        if action not in legal:
            raise Exception("Illegal action " + str(action))

        #pacmanState = state.data.agentStates[0]
        pacmanState = state.data.agentStates[agentIndex]

        # Update Configuration
        vector = Actions.directionToVector( action, PacmanRules.PACMAN_SPEED )
        pacmanState.configuration = pacmanState.configuration.generateSuccessor( vector )

        # Eat
        next = pacmanState.configuration.getPosition()
        nearest = nearestPoint( next )
        if manhattanDistance( nearest, next ) <= 0.5 :
            # Remove food
            PacmanRules.consume( nearest, state )
    applyAction = staticmethod( applyAction )

    def consume( position, state ):
        x,y = position
        # Eat food
        if state.data.food[x][y]:
            state.data.scoreChange += 10
            state.data.food = state.data.food.copy()
            state.data.food[x][y] = False
            state.data._foodEaten = position
            # TODO: cache numFood?
            numFood = state.getNumFood()
            if numFood == 0 and not state.data._lose:
                state.data.scoreChange += 500
                state.data._win = True
        # Eat capsule
        if( position in state.getCapsules() ):
            state.data.capsules.remove( position )
            state.data._capsuleEaten = position
            # Reset all ghosts' scared timers
            for index in range( 1, len( state.data.agentStates ) ):
                state.data.agentStates[index].scaredTimer = SCARED_TIME
    consume = staticmethod( consume )

class GhostRules:
    """
    These functions dictate how ghosts interact with their environment.
    """
    GHOST_SPEED=1.0
    def getLegalActions( state, ghostIndex ):
        """
        Ghosts cannot stop, and cannot turn around unless they
        reach a dead end, but can turn 90 degrees at intersections.
        """
        conf = state.getGhostState( ghostIndex ).configuration
        if state.data.biasedGhost:
            team1PacmanPositions = state.getPacmanTeamPositions(team=1, ignore=state.data.deadPacmans)
            possibleActions = Actions.getBiasedGhostPossibleActions(conf, team1PacmanPositions, state.data.layout.walls)
        else:
            possibleActions = Actions.getPossibleActions( conf, state.data.layout.walls )
        reverse = Actions.reverseDirection( conf.direction )
        if Directions.STOP in possibleActions:
            possibleActions.remove( Directions.STOP )
        if reverse in possibleActions and len( possibleActions ) > 1:
            possibleActions.remove( reverse )
        return possibleActions
    getLegalActions = staticmethod( getLegalActions )

    def applyAction( state, action, ghostIndex):

        legal = GhostRules.getLegalActions( state, ghostIndex )
        #print action
        #print legal
        if action not in legal:
            raise Exception("Illegal ghost action " + str(action))

        ghostState = state.data.agentStates[ghostIndex]
        speed = GhostRules.GHOST_SPEED
        if ghostState.scaredTimer > 0: speed /= 2.0
        vector = Actions.directionToVector( action, speed )
        ghostState.configuration = ghostState.configuration.generateSuccessor( vector )
    applyAction = staticmethod( applyAction )

    def decrementTimer( ghostState):
        timer = ghostState.scaredTimer
        if timer == 1:
            ghostState.configuration.pos = nearestPoint( ghostState.configuration.pos )
        ghostState.scaredTimer = max( 0, timer - 1 )
    decrementTimer = staticmethod( decrementTimer )

    def checkDeath( state, agentIndex, numPacman, team_map):
        #pacmanPosition = state.getPacmanPosition()
        pacmanPositions = state.getPacmanPositions(numPacman)
        if agentIndex < numPacman: # Pacman just moved; Anyone can kill him
            for index in range( numPacman, len( state.data.agentStates ) ):
                ghostState = state.data.agentStates[index]
                ghostPosition = ghostState.configuration.getPosition()
                pacmanPosition = state.getPacmanPosition(agentIndex)
                if GhostRules.canKill( pacmanPosition, ghostPosition ):
                    GhostRules.collide( state, ghostState, index, agentIndex, numPacman, team_map )
                # for pacmanIndex, pacmanPosition in enumerate(pacmanPositions):
                #     if pacmanIndex in state.data.deadPacmans: continue
                #     if GhostRules.canKill( pacmanPosition, ghostPosition ):
                #         GhostRules.collide( state, ghostState, index, pacmanIndex, numPacman, team_map )
        else:
            ghostState = state.data.agentStates[agentIndex]
            ghostPosition = ghostState.configuration.getPosition()
            # if GhostRules.canKill( pacmanPosition, ghostPosition ):
            #     GhostRules.collide( state, ghostState, agentIndex )
            for pacmanIndex, pacmanPosition in enumerate(pacmanPositions):
                if pacmanIndex in state.data.deadPacmans: continue
                if GhostRules.canKill( pacmanPosition, ghostPosition ):
                    GhostRules.collide( state, ghostState, agentIndex, pacmanIndex, numPacman, team_map )
    checkDeath = staticmethod( checkDeath )

    def collide( state, ghostState, agentIndex, pacmanIndex, numPacman, team_map):
        if ghostState.scaredTimer > 0:
            state.data.scoreChange += 200
            state.data.scores[ team_map[pacmanIndex] ] += 200
            GhostRules.placeGhost(state, ghostState)
            ghostState.scaredTimer = 0
            # Added for first-person
            state.data._eaten[agentIndex] = True
        else:
            state.data.deadPacmans.append(pacmanIndex)
            state.data.agentStates[pacmanIndex].alive = False
            state.data.scores[ team_map[pacmanIndex] ] -= 50
            #print "Pacman #"+str(pacmanIndex)+" died"
            
            if state.allDeadIn(team_map[pacmanIndex]):
                #print "Team #" + str(team_map[pacmanIndex]) + " eliminated"
                state.data.scores[ team_map[pacmanIndex] ] -= 500
                state.data._lose = True
            
            # if not state.data._win and len(state.data.deadPacmans)==numPacman:
            #     print "all pacman dead"
            #     state.data.scoreChange -= 500
            #     state.data.scores[ team_map[pacmanIndex] ] -= 500
            #     state.data._lose = True
    collide = staticmethod( collide )

    def canKill( pacmanPosition, ghostPosition ):
        return manhattanDistance( ghostPosition, pacmanPosition ) <= COLLISION_TOLERANCE
    canKill = staticmethod( canKill )

    def placeGhost(state, ghostState):
        ghostState.configuration = ghostState.start
    placeGhost = staticmethod( placeGhost )

#############################
# FRAMEWORK TO START A GAME #
#############################

data_file_name = ""

def default(str):
    return str + ' [Default: %default]'

def parseAgentArgs(str):
    if str == None: return {}
    pieces = str.split(',')
    opts = {}
    for p in pieces:
        if '=' in p:
            key, val = p.split('=')
        else:
            key,val = p, 1
        opts[key] = val
    return opts

def readCommand( argv ):
    """
    Processes the command used to run pacman from the command line.
    """
    from optparse import OptionParser
    usageStr = """
    USAGE:      python pacman.py <options>
    EXAMPLES:   (1) python pacman.py
                    - starts an interactive game
                (2) python pacman.py --layout smallClassic --zoom 2
                OR  python pacman.py -l smallClassic -z 2
                    - starts an interactive game on a smaller board, zoomed in
    """
    parser = OptionParser(usageStr)

    parser.add_option('-n', '--numGames', dest='numGames', type='int',
                      help=default('the number of GAMES to play'), metavar='GAMES', default=1)
    parser.add_option('-l', '--layout', dest='layout',
                      help=default('the LAYOUT_FILE from which to load the map layout'),
                      metavar='LAYOUT_FILE', default='mediumClassic')
    parser.add_option('-p', '--pacman', dest='pacman',
                      help=default('the agent TYPE in the pacmanAgents module to use'),
                      metavar='TYPE', default='KeyboardAgent')
    # parser.add_option('--p1', '--pacman1', dest='pacman1',
    #                   help=default('the agent TYPE in the pacmanAgents module to use'),
    #                   metavar='TYPE', default='KeyboardAgent')
    # parser.add_option('--p2', '--pacman2', dest='pacman2',
    #                   help=default('the agent TYPE in the pacmanAgents module to use'),
    #                   metavar='TYPE', default='KeyboardAgent')
    parser.add_option('-t', '--textGraphics', action='store_true', dest='textGraphics',
                      help='Display output as text only', default=False)
    parser.add_option('-q', '--quietTextGraphics', action='store_true', dest='quietGraphics',
                      help='Generate minimal output and no graphics', default=False)
    parser.add_option('-g', '--ghosts', dest='ghost',
                      help=default('the ghost agent TYPE in the ghostAgents module to use'),
                      metavar = 'TYPE', default='RandomGhost')
    parser.add_option('-k', '--numghosts', type='int', dest='numGhosts',
                      help=default('The maximum number of ghosts to use'), default=10)
    parser.add_option('-z', '--zoom', type='float', dest='zoom',
                      help=default('Zoom the size of the graphics window'), default=1.0)
    parser.add_option('-f', '--fixRandomSeed', action='store_true', dest='fixRandomSeed',
                      help='Fixes the random seed to always play the same game', default=False)
    parser.add_option('-r', '--recordActions', action='store_true', dest='record',
                      help='Writes game histories to a file (named by the time they were played)', default=False)
    parser.add_option('--replay', dest='gameToReplay',
                      help='A recorded game file (pickle) to replay', default=None)
    parser.add_option('-a','--agentArgs',dest='agentArgs',
                      help='Comma separated values sent to agent. e.g. "opt1=val1,opt2,opt3=val3"')
    parser.add_option('-x', '--numTraining', dest='numTraining', type='int',
                      help=default('How many episodes are training (suppresses output)'), default=0)
    parser.add_option('--frameTime', dest='frameTime', type='float',
                      help=default('Time to delay between frames; <0 means keyboard'), default=0.1)
    parser.add_option('-c', '--catchExceptions', action='store_true', dest='catchExceptions',
                      help='Turns on exception handling and timeouts during games', default=False)
    parser.add_option('--timeout', dest='timeout', type='int',
                      help=default('Maximum length of time an agent can spend computing in a single game'), default=30)
    parser.add_option('--fname', type='str',dest ='fname',
                      help='The name of the file(with extension) where the final game information is added')

    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    args = OrderedDict()
    mas_args = OrderedDict()

    # Fix the random seed
    if options.fixRandomSeed: random.seed('cs188')

    # File where final info is added on completion
    global data_file_name
    data_file_name = options.fname
    # if options.fname is None:
    #     print "Not storing final result, file not given"

    # Choose a layout
    args['layout'] = layout.getLayout( options.layout )
    if args['layout'] == None: raise Exception("The layout " + options.layout + " cannot be found")

    # Choose a Pacman agent
    noKeyboard = options.gameToReplay == None and (options.textGraphics or options.quietGraphics)
    pacmanType = loadAgent(options.pacman, noKeyboard)
    pacman1Type = loadAgent('System1Agent', noKeyboard)
    pacman2Type = loadAgent('System1Agent', noKeyboard)
    pacman3Type = loadAgent('System1Agent', noKeyboard)
    pacman4Type = loadAgent('System1Agent', noKeyboard)
    pacman5Type = loadAgent('System1Agent', noKeyboard)
    pacman6Type = loadAgent('System1Agent', noKeyboard)
    pacman7Type = loadAgent('System1Agent', noKeyboard)
    pacman8Type = loadAgent('System1Agent', noKeyboard)
    agentOpts = parseAgentArgs(options.agentArgs)
    if options.numTraining > 0:
        args['numTraining'] = options.numTraining
        if 'numTraining' not in agentOpts: agentOpts['numTraining'] = options.numTraining
    pacman = pacmanType(**agentOpts) # Instantiate Pacman with agentArgs
    pacman1 = pacman1Type(**agentOpts) # Instantiate Pacman1 with agentArgs
    pacman2 = pacman2Type(**agentOpts) # Instantiate Pacman2 with agentArgs
    pacman3 = pacman3Type(**agentOpts) # Instantiate Pacman3 with agentArgs
    pacman4 = pacman4Type(**agentOpts) # Instantiate Pacman3 with agentArgs
    pacman5 = pacman5Type(**agentOpts) # Instantiate Pacman3 with agentArgs
    pacman6 = pacman6Type(**agentOpts) # Instantiate Pacman3 with agentArgs
    pacman7 = pacman7Type(**agentOpts) # Instantiate Pacman3 with agentArgs
    pacman8 = pacman8Type(**agentOpts) # Instantiate Pacman3 with agentArgs
    pacman1.index = 0
    pacman2.index = 1
    pacman3.index = 2
    pacman4.index = 3
    pacman5.index = 4
    pacman6.index = 5
    pacman7.index = 6
    pacman8.index = 7
    pacman1.team = 0
    pacman2.team = 0
    pacman3.team = 1
    pacman4.team = 1
    pacman5.team = 1
    pacman6.team = 1
    pacman7.team = 1
    pacman8.team = 1
    args['pacman'] = pacman
    mas_args['pacmans'] = [pacman1, pacman2, pacman3, pacman4, pacman5, pacman6, pacman7, pacman8]
    mas_args['nteams'] = 2
    numPacman = len(mas_args['pacmans'])
    mas_args['numPacman'] = numPacman
    mas_args['biasedGhost'] = False
    mas_args['shuffleTurns'] = False
    mas_args['startingIndex'] = 0
    pacman1.numPacman = len(mas_args['pacmans'])
    pacman2.numPacman = len(mas_args['pacmans'])
    pacman3.numPacman = len(mas_args['pacmans'])
    pacman4.numPacman = len(mas_args['pacmans'])
    pacman5.numPacman = len(mas_args['pacmans'])
    pacman6.numPacman = len(mas_args['pacmans'])
    pacman7.numPacman = len(mas_args['pacmans'])
    pacman8.numPacman = len(mas_args['pacmans'])

    # Don't display training games
    if 'numTrain' in agentOpts:
        options.numQuiet = int(agentOpts['numTrain'])
        options.numIgnore = int(agentOpts['numTrain'])

    # Choose a ghost agent
    ghostType = loadAgent(options.ghost, noKeyboard)
    #args['ghosts'] = [ghostType( i+1 ) for i in range( options.numGhosts )]
    args['ghosts'] = [ghostType( i+numPacman ) for i in range( options.numGhosts )]

    # Choose a display format
    if options.quietGraphics:
        import textDisplay
        args['display'] = textDisplay.NullGraphics()
    elif options.textGraphics:
        import textDisplay
        textDisplay.SLEEP_TIME = options.frameTime
        args['display'] = textDisplay.PacmanGraphics()
    else:
        import graphicsDisplay
        args['display'] = graphicsDisplay.PacmanGraphics(options.zoom, frameTime = options.frameTime)
    args['numGames'] = options.numGames
    args['record'] = options.record
    args['catchExceptions'] = options.catchExceptions
    args['timeout'] = options.timeout
    args['numTraining'] = 0

    # Special case: recorded games don't use the runGames method or args structure
    if options.gameToReplay != None:
        print 'Replaying recorded game %s.' % options.gameToReplay
        import cPickle
        f = open(options.gameToReplay)
        try: recorded = cPickle.load(f)
        finally: f.close()
        recorded['display'] = args['display']
        replayGame(**recorded)
        sys.exit(0)

    return args, mas_args

def loadAgent(pacman, nographics):
    # Looks through all pythonPath Directories for the right module,
    pythonPathStr = os.path.expandvars("$PYTHONPATH")
    if pythonPathStr.find(';') == -1:
        pythonPathDirs = pythonPathStr.split(':')
    else:
        pythonPathDirs = pythonPathStr.split(';')
    pythonPathDirs.append('.')

    for moduleDir in pythonPathDirs:
        if not os.path.isdir(moduleDir): continue
        moduleNames = [f for f in os.listdir(moduleDir) if f.endswith('gents.py')]
        for modulename in moduleNames:
            try:
                module = __import__(modulename[:-3])
            except ImportError:
                continue
            if pacman in dir(module):
                if nographics and modulename == 'keyboardAgents.py':
                    raise Exception('Using the keyboard requires graphics (not text display)')
                return getattr(module, pacman)
    raise Exception('The agent ' + pacman + ' is not specified in any *Agents.py.')

def replayGame( layout, actions, display ):
    import pacmanAgents, ghostAgents
    rules = ClassicGameRules()
    agents = [pacmanAgents.GreedyAgent()] + [ghostAgents.RandomGhost(i+1) for i in range(layout.getNumGhosts())]
    game = rules.newGame( layout, agents[0], agents[1:], display )
    state = game.state
    display.initialize(state.data)

    for action in actions:
            # Execute the action
        state = state.generateSuccessor( *action )
        # Change the display
        display.update( state.data )
        # Allow for game specific conditions (winning, losing, etc.)
        rules.process(state, game)

    display.finish()

def par(i):
    global save_df
    layout, pacman, ghosts, display, numGames, record, catchExceptions, timeout, numTraining = [i[1] for i in args.items()]
    pacmans = mas_args['pacmans']
    numPacman = mas_args['numPacman']
    nteams = mas_args['nteams']
    biasedGhost = mas_args['biasedGhost']
    shuffleTurns = mas_args['shuffleTurns']
    startingIndex = mas_args['startingIndex']

    rules = ClassicGameRules(timeout)
    start_time = time.time()
    beQuiet = i < numTraining
    if beQuiet:
        import textDisplay
        gameDisplay = textDisplay.NullGraphics()
        rules.quiet = True
    else:
        gameDisplay = display
        rules.quiet = False
    game = rules.newGame( layout, pacman, pacmans, numPacman, nteams, biasedGhost, shuffleTurns, startingIndex, ghosts, gameDisplay, beQuiet, catchExceptions)
    scores, deadPacmans, steps_alive, is_win = game.run()
    row = pd.DataFrame({'scores': [scores], 'deadPacmans': [deadPacmans], 'steps_alive': [steps_alive], 'is_win': [is_win]})
    
    if save:
        if os.path.isfile(save_file):
            save_df = pd.read_csv(save_file)
        save_df = pd.concat([save_df, row], axis=0, sort=False)
        save_df.to_csv(save_file, index=False)
    
    print scores, deadPacmans
    elapsed_time = time.time() - start_time
    columns = ["time","score","result"]
    score = game.state.getScore()
    win = game.state.isWin()
    rows = [elapsed_time,score,win]
    df = pd.DataFrame(columns = columns)

    global data_file_name
    if data_file_name is not None:
        data_file_name = data_file_name
        if(os.stat(data_file_name).st_size != 0):
            df.loc[len(columns)] = rows
            df.to_csv (data_file_name, index = None,mode='a', header=False)
        else:
            df.append(rows)
            df.to_csv (data_file_name, index = None, header=True)

    # if not beQuiet: games.append(game)

    if record:
        fname = ('recorded-game-%d' % (i + 1)) +  '-'.join([str(t) for t in time.localtime()[1:6]])
        f = file(fname, 'w')
        components = {'layout': layout, 'actions': game.moveHistory}
        cPickle.dump(components, f)
        f.close()

def runGames( layout, pacman, ghosts, display, numGames, record, numTraining = 0, catchExceptions=False, timeout=30 ):
    import __main__
    import time
    __main__.__dict__['_display'] = display

    rules = ClassicGameRules(timeout)
    games = []
    # par( layout, pacman, ghosts, display, numGames, record, numTraining = 0, catchExceptions=False, timeout=30)
    for i in range( numGames ):
        beQuiet = i < numTraining
        if beQuiet:
                # Suppress output and graphics
            import textDisplay
            gameDisplay = textDisplay.NullGraphics()
            rules.quiet = True
        else:
            gameDisplay = display
            rules.quiet = False
        game = rules.newGame( layout, pacman, ghosts, gameDisplay, beQuiet, catchExceptions)

        start_time = time.time()
        game.run()
        elapsed_time = time.time() - start_time

        columns = ["time","score","result"]

        print_interval=100
        if i%print_interval == 0:
            print pacman,": Finished",i,"games"

        score = game.state.getScore()
        win = game.state.isWin()
        rows = [elapsed_time,score,win]
        df = pd.DataFrame(columns = columns)

        global data_file_name
        if data_file_name is not None:
            data_file_name = data_file_name
            if(os.stat(data_file_name).st_size != 0):
                df.loc[len(columns)] = rows
                df.to_csv (data_file_name, index = None,mode='a', header=False)
            else:
                df.append(rows)
                df.to_csv (data_file_name, index = None, header=True)

        if not beQuiet: games.append(game)

        if record:
            import time, cPickle
            fname = ('recorded-game-%d' % (i + 1)) +  '-'.join([str(t) for t in time.localtime()[1:6]])
            f = file(fname, 'w')
            components = {'layout': layout, 'actions': game.moveHistory}
            cPickle.dump(components, f)
            f.close()

    if (numGames-numTraining) > 0:
        scores = [game.state.getScore() for game in games]
        wins = [game.state.isWin() for game in games]
        winRate = wins.count(True)/ float(len(wins))
        # print("Final win state: ",wins)
        # print 'Average Score:', sum(scores) / float(len(scores))
        # print 'Scores:       ', ', '.join([str(score) for score in scores])
        # print 'Win Rate:      %d/%d (%.2f)' % (wins.count(True), len(wins), winRate)
        # print 'Record:       ', ', '.join([ ['Loss', 'Win'][int(w)] for w in wins])

    return games

def multi_run_wrapper(args):
   return par(*args)

if __name__ == '__main__':
    """
    The main function called when pacman.py is run
    from the command line:

    > python pacman.py

    See the usage string for more details.

    > python pacman.py --help
    """
    # name of the file to save report for
    # simulation session
    
    save = True
    if save:
        now = datetime.now()
        save_file = 'reports/' + str(now.day) + '-' + str(now.month) + '-' + str(now.year) + \
                    '_' + \
                    str(now.hour) + '.' + str(now.minute) + '.' + str(now.second) + '.csv'
        info_file = 'reports/' + str(now.day) + '-' + str(now.month) + '-' + str(now.year) + \
                    '_' + \
                    str(now.hour) + '.' + str(now.minute) + '.' + str(now.second) + '.txt'
        info = 'nT1=2\nnT2=6\nT1S1=1\nT2S1=1\nT1S2=0\nT2S2=0\nT1B1=0\nnG=1\nbiased_ghost=False\n'
        f = open(info_file, 'w')
        f.write(info+'\n')
        f.close()
        save_df = pd.DataFrame(columns=['scores', 'deadPacmans', 'steps_alive', 'is_win'])

    # If code is ran parallelly using Poll, then logs will cause
    # confusion. To properly interpret logs, just run one instance
    # like par(0), or par(0), par(1), par(2), ... sequentially.
    args, mas_args = readCommand( sys.argv[1:] ) # Get game components based on input
    # runGames( **args )

    # print args.keys()
    # all_in = []
    # print [i[1] for i in args.items()]
    # for i in range(args['numGames']):
    #     all_in.append((i, [i[1] for i in args.items()]))
    # print range(args['numGames'])
    # pool = Pool(processes=14)
    # result = pool.map(par, range(args['numGames']))
    # par(0)
    # print "save = " + str(save)
    for i in range(args['numGames']):
        try:
            par(i)
        except:
            print 'sim-' + str(i+1) + 'failed'
    #print result[:2]
    #print len(result)

    # import cProfile
    # cProfile.run("runGames( **args )")
    pass
