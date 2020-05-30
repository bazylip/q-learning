from enum import Enum


class Action(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
"""
reward_array = [[-1, -1, -1, -1],
                [-1000, 1000, -1000, -1],
                [-1, -1, -1, -1],
                [-1, -1, -1000, -1]]
"""
reward_array = [[-1, -1000, -1, -1000],
                [-1, -1, -1000, 1000],
                [-1, -1, -1, -1],
                [-1, -1, -1000, -1]]

def step(x, y, action):
    def validate_out_of_bounds(x, y):
        bounce_punishment = 0
        if x > 3:
            x = 3
            bounce_punishment = -10
        elif x < 0:
            x = 0
            bounce_punishment = -10
        if y > 3:
            y = 3
            bounce_punishment = -10
        elif y < 0:
            y = 0
            bounce_punishment = -10
        return x, y, bounce_punishment

    next_x, next_y = 0, 0
    if action == Action.LEFT.value:
        next_x = x - 1
        next_y = y
    elif action == Action.RIGHT.value:
        next_x = x + 1
        next_y = y
    elif action == Action.UP.value:
        next_x = x
        next_y = y + 1
    elif action == Action.DOWN.value:
        next_x = x
        next_y = y - 1

    next_x, next_y, bounce_punishment = validate_out_of_bounds(next_x, next_y)
    reward = reward_array[next_x][next_y] + bounce_punishment
    game_ended = reward == -1000 or reward == 1000
    return next_x, next_y, reward, game_ended
