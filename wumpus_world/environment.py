from enum import Enum


BOUNCE_PUNISHMENT = -10

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

    next_x, next_y = x, y
    if action == Action.LEFT.value:
        next_x -= 1
    elif action == Action.RIGHT.value:
        next_x += 1
    elif action == Action.UP.value:
        next_y += 1
    elif action == Action.DOWN.value:
        next_y -= 1

    next_x, next_y, bounce_punishment = validate_out_of_bounds(next_x, next_y)
    reward = reward_array[next_x][next_y] + bounce_punishment
    game_ended = reward == -1000 or reward == 1000
    return next_x, next_y, reward, game_ended

def validate_out_of_bounds(x, y):
    bounce = False
    if x > 3:
        x = 3
        bounce = True
    elif x < 0:
        x = 0
        bounce = True
    if y > 3:
        y = 3
        bounce = True
    elif y < 0:
        y = 0
        bounce = True
    bounce_punishment = BOUNCE_PUNISHMENT if bounce else 0
    return x, y, bounce_punishment
