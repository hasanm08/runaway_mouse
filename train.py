import random
from gameBoard import GameBoard
import numpy as np


boardDim = 36      # size of the board
# numStates = 32
numActions = 8     # 8 directions that the mouse can move
StateAction = np.zeros((32, 31, 5, 8))
lr = 0.7    # learning rate.
gamma = 0.8     # discount rate
# epsilon = 0.24     # exploration rate in training game
numEpochs = 15000      # number of games to train for
StateActionAtEpoch = np.zeros((numEpochs, 32, 31, 5, 8))
# bestLength = 0
print("Training for", numEpochs, "games...")
for epoch in range(numEpochs):
    game = GameBoard(need_print=False)
    #    print("New Game")
    state = game.calcStateNum()
    gameOver = False
    score = 0
    while not gameOver:
        print("state is:", state)
        # if random.uniform(0, 1) < epsilon:
        #     action = random.randint(0, 7)
        # else:
        #     possibleQs = StateAction[state, :]
        #     action = np.argmax(possibleQs)
        action = random.randint(0, 7)
        tmp = game.move(action=action)
        new_state, reward = game.move(action=action)
        print("reward", reward)
        gameOver = game.game_ended
        StateAction[state[0], state[1], state[2], action] = StateAction[state[0], state[1], state[2], action] + lr * (reward + gamma *
                                                                                                                      np.max(StateAction[new_state[0], new_state[1], new_state[2], :]) - StateAction[state[0], state[1], state[2], action])
        state = new_state

    StateActionAtEpoch[epoch, :, :, :, :] = np.copy(StateAction)
np.savez_compressed("StateActionAtEpoch_15000", StateActionAtEpoch)
