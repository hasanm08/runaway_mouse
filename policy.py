import numpy as np
EpochStateAction = np.load('StateActionAtEpoch_15000.npz')['arr_0']
print(EpochStateAction[:, 0, 0, 0, :])
StateAction = np.sum(EpochStateAction, axis=0)
# print(np.shape(StateAction)) => (32, 31, 5, 8)
print(StateAction[0, 0, 0, :])
MaxStateAction = np.argmax(StateAction, axis=3, keepdims=True)

# print(np.shape(MaxStateAction))  # => (32, 31, 5,1)
# print(MaxStateAction[1, 1, 1, :]) is index of best action

np.savez_compressed("policy", MaxStateAction)
