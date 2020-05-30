from enum import Enum


class GuiLogic:
    def __init__(self):
        self.reset_board()
        self.rewards = {Field.EMPTY: -1, Field.AGENT: -1, Field.GOLD: 1000, Field.WUMPUS: -1000, Field.PIT: -1000}

    def reset_board(self):
        self.board_state = [[Field.AGENT, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                            [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                            [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                            [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]

    def update_field(self, x, y):
        if (x > 0 or y > 0) and (x < 4 and y < 4):
            value = self.board_state[x][y].value
            if value != 4:
                self.board_state[x][y] = Field(value + 1)
            else:
                self.board_state[x][y] = Field.EMPTY

    def update_agent(self, agent_x, agent_y):
        for x in range(4):
            for y in range(4):
                if self.board_state[x][y] == Field.AGENT:
                    self.board_state[x][y] = Field.EMPTY
        self.board_state[agent_x][agent_y] = Field.AGENT

    def convert_to_reward_array(self):
        reward_array = [[0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]]
        for x in range(4):
            for y in range(4):
                reward_array[x][y] = self.rewards.get(self.board_state[x][y])

        return reward_array

class Field(Enum):
    EMPTY = 1
    PIT = 2
    WUMPUS = 3
    GOLD = 4
    AGENT = 5

class Action(Enum):
    LEFT = 0
    RIGHT = 1
    DOWN = 2
    UP = 3