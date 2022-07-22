import numpy as np
import random


class GameInfo:
    def random_pos(self):
        n = random.randint(0, 5)
        m = random.randint(0, 5)
        while self.board[n, m] != 0:
            n = random.randint(0, 5)
            m = random.randint(0, 5)
        return (n, m)

    def __init__(self, board=None, blocks=None, mouse=None, cat=None, cheese=None):
        if(board != None):
            self.board = board
            return
        if blocks != None:
            self.blocks = blocks
        else:
            self.blocks = [self.random_pos() for _ in range(4)]

        self.board = (np.zeros((6, 6)))
        for item in self.blocks:
            self.board[item] = -1
        if cheese != None:
            self.cheese = cheese
        else:
            self.cheese = [self.random_pos() for _ in range(5)]

        for item in self.cheese:
            self.board[item] = 3
        if mouse != None:
            self.mouse = mouse
        else:
            self.mouse = self.random_pos()
        self.board[self.mouse] = 1

        if cat != None:
            self.cat = cat
        else:
            self.cat = self.random_pos()
        self.board[self.cat] = 2

        self.nest = self.random_pos()
        self.board[self.nest] = 4

    def __str__(self):
        return str(self.board)

    def __repr__(self):
        return str(self.board)


class GameBoard:
    def print_board(self):
        if not self.need_print:
            return
        print("")
        print(5*" 🧱 ")
        for i in range(6):
            print("🧱", end="")
            for j in range(6):
                if self.board[i, j] == 0:
                    print("   ", end="")
                elif self.board[i, j] == 1:
                    print("🐭", end="")
                elif self.board[i, j] == 2:
                    print("😼", end="")
                elif self.board[i, j] == 3:
                    print("🧀", end="")
                elif self.board[i, j] == 4:
                    print("🕳️", end="")
                elif self.board[i, j] == 5:
                    print("😼🧀", end="")
                elif self.board[i, j] == -1:
                    print("🚧", end="")
            print("🧱")
        print(5*" 🧱 ")
        print("")

    def value(self, pos):
        if self.board[pos] == 0:
            return 0  # empty
        elif self.board[pos] == 2:
            return -15  # cat
        elif self.board[pos] == 3:
            return 10  # cheese
        elif self.board[pos] == 4:
            return 5  # nest
        elif self.board[pos] == 5:
            return -5  # cheese + cat
        print(self.board[pos])
        raise ValueError('A very specific bad thing happened.')

    def check_range(self, pos):
        i, j = pos
        if(i < 0 or i > 5 or j < 0 or j > 5):
            return False
        return True

    def cat_move(self):
        x, y = self.cat
        positions = []
        items = []
        for i in range(6):
            for j in range(6):
                items.append((i, j))
        for item in items:
            if((self.board[item] != -1) and (self.board[item] != 4)):
                # not blocks items and not nest and in board range
                positions.append(item)
        index = random.randint(0, len(positions)-1)  # random move
        new_pos = positions[index]
        if new_pos == self.mouse:
            self.game_ended = True
            self.cat_wins = True
            self.print_board()
        if new_pos in self.cheese:
            # cat moves to cheese
            self.board[self.cat] = 0
            self.cat = new_pos
            self.board[self.cat] = 5
            return

        self.board[self.cat] = 0
        self.cat = new_pos
        self.board[self.cat] = 2

    def find_next(self, action=None):
        x, y = self.mouse
        positions = []
        items = [(x, y-1), (x-1, y-1), (x-1, y), (x-1, y+1),
                 (x, y+1), (x+1, y+1), (x+1, y), (x+1, y-1)]
        for item in items:
            if(self.check_range(item) and (self.board[item] != -1)):
                # not blocks items and in board range
                positions.append(item)
            else:
                positions.append((-1, -1))
        if len(positions) == 0:
            self.game_ended = True
            return
        values = [self.value(item) if item != (-1, -1) else -100
                  for item in positions]  # next state values
        max_pos = np.argmax(values)
        if action != None:
            max_pos = action
            if action >= len(positions):
                max_pos = random.randint(0, len(positions)-1)
        self.earned_value += values[max_pos]
        self.board[self.mouse] = 0
        self.mouse = positions[max_pos]
        return (self.calcStateNum(), values[max_pos], positions[max_pos])

    def calcStateNum(self, mouse=None):
        mouse_pos = self.mouse
        if mouse != None:
            mouse_pos = mouse
        i = self.mouse_valid_board.index(mouse_pos)
        j = self.cat_valid_board.index(self.cat)
        k = self.cheese_count-1
        return (i, j, k)

    def update(self, max_pos):
        pos = self.mouse
        if self.board[max_pos] == 0:
            # empty
            self.board[pos] = 1
        elif self.board[max_pos] == 2:
            # cat
            self.board[pos] = 2  # cat remains game ends
            self.game_ended = True
            self.cat_wins = True
        elif self.board[max_pos] == 3:
            # cheese
            self.board[pos] = 1  # cheese had eaten
            self.cheese.remove(pos)
            self.cheese_count -= 1
        elif self.board[max_pos] == 4:
            # nest
            self.board[pos] = 4  # mouse moved to nest
            self.game_ended = True
            self.mouse_wins = True
        elif self.board[max_pos] == 5:
            # nest
            # cheese will be eaten by mouse and mouse will be eaten by cat
            self.board[pos] = 2
            self.game_ended = True
            self.cat_wins = True  # cat remains game ends
        pass

    def move(self, action=None):
        self.cat_move()
        state = self.calcStateNum()
        reward = 0
        if(not self.game_ended):
            state, reward, max_pos = self.find_next(action=None)
            self.update(max_pos)
        return (state, reward)

    def play(self):
        while (not self.game_ended):
            self.move()
            self.print_board()
        print("Game Ended Winner is", "Cat" if(self.cat_wins)else"Mouse")
        print("Earned value", self.earned_value)
        pass

    def __init__(self, need_print=True, info=None, state_action=None):
        self.state_action = {}
        if(state_action != None):
            self.state_action = state_action
        self.need_print = need_print
        self.game_ended = False
        self.mouse_wins = False
        self.cat_wins = False
        self.gamma = 0.95
        self.earned_value = 0
        self.start_info = GameInfo(blocks=[(1, 1), (2, 2), (4, 1), (4, 3)])
        if(info != None):
            self.start_info = info

        self.board = self.start_info.board
        self.blocks = self.start_info.blocks
        self.cheese = self.start_info.cheese
        self.cheese_count = len(self.cheese)
        self.mouse = self.start_info.mouse
        self.cat = self.start_info.cat
        self.nest = self.start_info.nest

        self.positional_board = []
        for i in range(6):
            for j in range(6):
                self.positional_board.append((i, j))
        self.mouse_valid_board = [
            item for item in self.positional_board if item not in self.blocks]
        self.cat_valid_board = [
            item for item in self.mouse_valid_board if item not in [self.nest]]

        if(self.need_print):
            print("\nInitial state\n")
            self.print_board()
            print("\nGame begins\n")
        # self.play()


game = GameBoard()
print("init board was :")
game.start_info
