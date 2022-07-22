import numpy as np
from gameBoard import *
policy = np.load('policy.npz')['arr_0']
game = GameBoard(need_print=True, info=GameInfo(blocks=[(1, 1), (2, 2), (4, 1), (4, 3)], mouse=(0, 0), cat=(3, 1),
                                                cheese=[(0, 2), (2, 3), (3, 2), (4, 2), (5, 3)]))
#    print("New Game")
state = game.calcStateNum()
action = policy[state[0], state[1], state[2], :]
tmp = game.move(action=action)
new_state, reward = game.move(action=action)
print("reward", reward)
state = new_state
game.play()
