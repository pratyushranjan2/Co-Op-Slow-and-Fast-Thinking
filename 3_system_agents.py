# line 587, pacman.py - the process for loading an agent has been defined
# 3_system_agents.py
# --------------
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

import sys
from util import manhattanDistance
from game import Directions, GameStateData
import random, util
import copy
import pickle
import numpy as np
import random
import copy

from game import Agent, Actions
from qlearningAgents import ApproximateQAgent


def betterEvaluationFunction(currentGameState, pacmanInfo):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    """Calculating distance to the closest food pellet"""
    
    normalisedEvaluation = False
    pacmanIndex = pacmanInfo['agentIndex']
    newPos = currentGameState.getPacmanPosition(pacmanIndex)
    newFood = currentGameState.getFood()
    newFoodList = newFood.asList()
    min_food_distance = -1
    for food in newFoodList:
        distance = util.manhattanDistance(newPos, food)
        if min_food_distance >= distance or min_food_distance == -1:
            min_food_distance = distance

    """Calculating the distances from pacman to the ghosts. Also, checking for the proximity of the ghosts (at distance of 1) around pacman."""
    distances_to_ghosts = 1
    proximity_to_ghosts = 0
    for ghost_state in currentGameState.getGhostPositions():
        distance = util.manhattanDistance(newPos, ghost_state)
        distances_to_ghosts += distance
        if distance <= 1:
            proximity_to_ghosts += 1

    """Obtaining the number of capsules available"""
    newCapsule = currentGameState.getCapsules()
    numberOfCapsules = len(newCapsule)

    """Combination of the above calculated metrics."""
    if normalisedEvaluation:
        normScore = currentGameState.data.layout.numFood*10
        normGhostProxi = currentGameState.data.layout.numGhosts
        
        return currentGameState.getPacmanScore(pacmanInfo['agentIndex'])/normScore + (1 / float(min_food_distance)) - (1 / float(distances_to_ghosts)) - proximity_to_ghosts/normGhostProxi - numberOfCapsules
    
    
    return currentGameState.getPacmanScore(pacmanInfo['agentIndex']) + (1 / float(min_food_distance)) - (1 / float(distances_to_ghosts)) - proximity_to_ghosts - numberOfCapsules

class System1Agent(Agent): #system 1 is capable of gameplay on its own
    """
    Code modelling actions of system 1 comes here
    """

    def __init__(self):
        self.q_learning_agent = ApproximateQAgent(extractor = 'SimpleExtractor',numTraining=-1) #need to figure out how to pass args here
        self.q_learning_agent.setEpsilon(0)
        with open('network_weights.pkl', 'rb') as input:
            trained_weights = pickle.load(input)
            self.q_learning_agent.setWeights(trained_weights)
        with open('features.pkl', 'rb') as input:
            extractor_used = pickle.load(input)
            self.q_learning_agent.setExtractor(extractor_used)
    def getAction(self,gameState, pacmanInfo):
        assert pacmanInfo != None
        return self.q_learning_agent.getAction(gameState, pacmanInfo)

class BlockingAgent(Agent):
    def getAction(self, gameState, pacmanInfo):
        pacmanIndex = pacmanInfo['agentIndex']
        legalActions = gameState.getLegalActions(pacmanIndex, pacmanInfo)

        pos = gameState.getPacmanPosition(self.index)
        speed = 1

        actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
        newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]

        opponentPacmanPositions = gameState.getPacmanTeamPositions(team=2,\
                                    ignore=gameState.data.deadPacmans)
        distancesToOpponents = []
        for pos in newPositions:
            min_distance = min([manhattanDistance(pos, opponentPos) for opponentPos in opponentPacmanPositions])
            distancesToOpponents.append(min_distance)
        
        bestDist = min(distancesToOpponents)
        bestActions = [action for action, dist in zip(legalActions, distancesToOpponents)\
                                    if dist == bestDist]
        
        return random.choice(bestActions)

class ProximityBlockingAgent(BlockingAgent, object):
    def __init__(self):
        self.escapeSys = System1Agent()
    
    def getAction(self, gameState, pacmanInfo):
        pacmanIndex = pacmanInfo['agentIndex']
        newPos = gameState.getPacmanPosition(pacmanIndex)
        proximity_to_ghosts = 0
        
        for ghost_state in gameState.getGhostPositions():
            distance = util.manhattanDistance(newPos, ghost_state)
            if distance <= 2:
                proximity_to_ghosts += 1
        if proximity_to_ghosts > 0:
            return self.escapeSys.getAction(gameState, pacmanInfo)
        
        return super(ProximityBlockingAgent, self).getAction(gameState, pacmanInfo)

class System2Agent(Agent): #system 2 is capable of gameplay on its own
    """
    Code modelling actions of system 2 comes here
    """

    def __init__(self, evalFn = 'betterEvaluationFunction', depth = '2'):
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def getAction(self, gameState, pacmanInfo):
        # print("Game state type:",type(gameState))
        # print("Game state:",gameState)
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        assert pacmanInfo != None
        pacmanIndex = pacmanInfo['agentIndex']
        numPacman = pacmanInfo['numPacman']
        team_map = pacmanInfo['team_map']
        policy = 'random'
        #print "before: " + str(gameState.data.scores) + ", " + str(len(gameState.getFood().asList())) + ", " + str(gameState.data.score) + ", " + str(gameState.data.deadPacmans)
        
        def getLegalActions(agent, state, info):
            legalActions = state.getLegalActions(agent, info)
            if policy == 'random':
                random.shuffle(legalActions)
                return legalActions[:3]
            return legalActions
        
        def expectimax(agent, depth, currentGameState):
            #print "agent = " + str(agent) + " agentIndex: " + str(pacmanInfo['agentIndex'])
            if pacmanIndex in currentGameState.data.deadPacmans or currentGameState.isWin() or currentGameState.isLose() or depth == self.depth:  # return the utility in case the defined depth is reached or the game is won/lost.
                return self.evaluationFunction(currentGameState, pacmanInfo)
            if agent == pacmanIndex:  # maximizing for pacman
                legalActions = getLegalActions(agent, currentGameState, pacmanInfo)
                return max(expectimax(agent+1, depth, currentGameState.generateSuccessor(agent, new_action, numPacman, currentGameState.data.deadPacmans, pacmanInfo, team_map)) for new_action in legalActions)
            else:  # performing expectimax action for ghosts/chance nodes.
                nextAgent = agent + 1  # calculate the next agent and increase depth accordingly.
                while (nextAgent in currentGameState.data.deadPacmans):
                    nextAgent += 1
                if gameState.getNumAgents() == nextAgent:
                    nextAgent = 0
                if nextAgent == pacmanIndex:
                    depth += 1
                if agent in currentGameState.data.deadPacmans:
                    return expectimax(nextAgent, depth, currentGameState)
                info = None
                # info for another pacman. Not the one for whom actions
                # are being evaluated
                if agent < numPacman:
                    info = copy.deepcopy(pacmanInfo)
                    info['agentIndex'] = agent
                    info['team'] = team_map[agent]
                legalActions = getLegalActions(agent, currentGameState, info)
                return sum(expectimax(nextAgent, depth, currentGameState.generateSuccessor(agent, new_action, numPacman, currentGameState.data.deadPacmans, info, team_map)) for new_action in legalActions) / float(len(legalActions))

        """Performing maximizing task for the root node i.e. pacman"""
        maximum = float("-inf")
        action = Directions.WEST
        for agent_action in gameState.getLegalActions(pacmanIndex, pacmanInfo):
            utility = expectimax(pacmanIndex+1, 0, gameState.generateSuccessor(pacmanIndex, agent_action, numPacman, gameState.data.deadPacmans, pacmanInfo, team_map))
            if utility > maximum or maximum == float("-inf"):
                maximum = utility
                action = agent_action
        #print "after: " + str(gameState.data.scores) + ", " + str(len(gameState.getFood().asList())) + ", " + str(gameState.data.score) + ", " + str(gameState.data.deadPacmans)
        return action

class System0Agent(Agent):
    def __init__(self, settings):
        self.system_1_model = System1Agent()
        self.system_2_model = System2Agent()
        self.proximity = settings['proximity']
        # self.exp = settings['exp_id']
        # self.threshF = 0.5 # threshold factor
        # self.expActions = [
        #     [self.system_1_model, self.system_1_model, self.system_1_model, self.system_1_model],
        #     [self.system_1_model, self.system_1_model, self.system_1_model, self.system_2_model],
        #     [self.system_1_model, self.system_1_model, self.system_2_model, self.system_1_model],
        #     [self.system_1_model, self.system_2_model, self.system_1_model, self.system_1_model],
        #     [self.system_2_model, self.system_1_model, self.system_1_model, self.system_1_model],
        #     [self.system_2_model, self.system_2_model, self.system_1_model, self.system_1_model],
        #     [self.system_2_model, self.system_1_model, self.system_2_model, self.system_1_model],
        #     [self.system_2_model, self.system_1_model, self.system_1_model, self.system_2_model],
        #     [self.system_1_model, self.system_2_model, self.system_2_model, self.system_1_model],
        #     [self.system_1_model, self.system_2_model, self.system_1_model, self.system_2_model],
        #     [self.system_1_model, self.system_1_model, self.system_2_model, self.system_2_model],
        #     [self.system_1_model, self.system_2_model, self.system_2_model, self.system_2_model],
        #     [self.system_2_model, self.system_1_model, self.system_2_model, self.system_2_model],
        #     [self.system_2_model, self.system_2_model, self.system_1_model, self.system_2_model],
        #     [self.system_2_model, self.system_2_model, self.system_2_model, self.system_1_model],
        #     [self.system_2_model, self.system_2_model, self.system_2_model, self.system_2_model],
        # ]
    
    def getAction(self, gameState, pacmanInfo):
        if self.proximity:
            newPos = gameState.getPacmanPosition()
            proximity_to_ghosts = 0
            for ghost_state in gameState.getGhostPositions():
                distance = util.manhattanDistance(newPos, ghost_state)
                if distance <= 2:
                    proximity_to_ghosts += 1
            if proximity_to_ghosts > 0:
                return self.system_2_model.getAction(gameState, pacmanInfo)
        
        # N1 = len(gameState.data.team1)
        # N2 = len(gameState.data.team2)
        # alive1 = len(gameState.getPacmansAlive(0))
        # alive2 = len(gameState.getPacmansAlive(1))

        # if alive1 >= self.threshF * N1 and alive2 >= self.threshF * N2:
        #     move = self.expActions[self.exp][0].getAction(gameState, pacmanInfo)
        
        # elif alive1 >= self.threshF * N1 and alive2 < self.threshF * N2:
        #     move = self.expActions[self.exp][1].getAction(gameState, pacmanInfo)
        
        # elif alive1 < self.threshF * N1 and alive2 >= self.threshF * N2:
        #     move = self.expActions[self.exp][2].getAction(gameState, pacmanInfo)
        
        # else:
        #     move = self.expActions[self.exp][3].getAction(gameState, pacmanInfo)

        # return move

        otherTeamScore = gameState.data.scores[not self.team]
        ownTeamScore = gameState.data.scores[self.team]
        if otherTeamScore > ownTeamScore:
            move = self.system_2_model.getAction(gameState, pacmanInfo)
        else:
            move = self.system_1_model.getAction(gameState, pacmanInfo)
        return move


class ProximityAgent(System0Agent):
    def __init__(self,proxi_dist=2,escape_sys=2):
        System0Agent.__init__(self)
        self.proxi_dist = float(proxi_dist)
        self.escape_sys = int(escape_sys)
        
    def getAction(self,gameState,pacmanInfo):
        # return self.system_1_model.getAction(gameState)
        assert pacmanInfo != None
        newPos = gameState.getPacmanPosition()
        distances_to_ghosts = 1
        proximity_to_ghosts = 0
        for ghost_state in gameState.getGhostPositions():
            distance = util.manhattanDistance(newPos, ghost_state)
            distances_to_ghosts += distance
            if distance <= self.proxi_dist:
                proximity_to_ghosts += 1
        if proximity_to_ghosts < 1:
            if self.escape_sys == 2:
                move = self.system_1_model.getAction(gameState, pacmanInfo)
            else:
                move = self.system_1_model.getAction(gameState, pacmanInfo)
        else: #high proximity, escape
            if self.escape_sys == 2:
                move = self.system_1_model.getAction(gameState, pacmanInfo)
            else:
                move = self.system_1_model.getAction(gameState, pacmanInfo)
        return move

class RandomChoiceAgent(System0Agent):
    def __init__(self, prob_sys1):
        System0Agent.__init__(self)
        self.prob_sys1 = float(prob_sys1)
        # self.d = {1:0,2:0}

    def getAction(self,gameState):
        system_to_use = np.random.choice([1,2], p=[self.prob_sys1,1 - self.prob_sys1])
        # self.d[system_to_use] += 1
        # print self.d
        if system_to_use == 1:
            return self.system_1_model.getAction(gameState)
        else:
            return self.system_2_model.getAction(gameState)

class ProximityAndFoodAgent(System0Agent):
    def __init__(self,food_thresh=0.5):
        System0Agent.__init__(self)
        self.threshold = food_thresh
        self.total_food_num = 65.0

    def getAction(self,gameState):
        newPos = gameState.getPacmanPosition()
        distances_to_ghosts = 1
        proximity_to_ghosts = 0
        for ghost_state in gameState.getGhostPositions():
            distance = util.manhattanDistance(newPos, ghost_state)
            distances_to_ghosts += distance
            if distance <= 2:
                proximity_to_ghosts += 1

        if proximity_to_ghosts < 1:
            ratio = gameState.getNumFood()/self.total_food_num
            if (float(ratio) >= float(self.threshold)):
                move = self.system_2_model.getAction(gameState)
            else:
                move = self.system_1_model.getAction(gameState)
        else:
            move = self.system_2_model.getAction(gameState)
        return move
