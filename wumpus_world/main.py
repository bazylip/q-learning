import time

import numpy as np
import random
import matplotlib.pyplot as plt
from wumpus_world.environment import Action, step


def get_action_with_max_value(Q, x, y):
    return Q.argmax(axis=0)[x][y]

def qlearning():
    # Setting learning parameters
    number_of_episodes = 20000
    gamma = 1
    alpha = 0.8
    epsilon = 0.1
    max_steps_number = 100

    num_actions = len([action.value for action in Action])
    Q = np.zeros((num_actions, 4, 4))
    sum_of_rewards = np.zeros(number_of_episodes)

    for episode in range(number_of_episodes):
        x, y = 0, 0
        step_number = 0
        game_ended = False
        sum_of_rewards[episode] = 0
        while not game_ended:
            step_number += 1
            if random.uniform(0, 1) < epsilon:
                action = random.randrange(num_actions) # get random action
            else:
                action = get_action_with_max_value(Q, x, y) # get action with highest value in Q for x, y
            #print(f"Step number: {step_number}, x: {x}, y: {y}, action {action}")
            next_x, next_y, reward, end = step(x, y, action)
            Q[action][x][y] = Q[action][x][y] + \
                              alpha*(reward + gamma*get_action_with_max_value(Q, next_x, next_y) - Q[action][x][y])
            x, y = next_x, next_y
            sum_of_rewards[episode] += reward

            if step_number == max_steps_number or end:
                game_ended = True
        if episode % 1000 == 0:
            print(f"Sum of rewards for episode {episode}: {sum_of_rewards[episode]}")

    return Q

def validate(Q):
    validation_episodes = 1000
    max_steps_number = 20
    sum_of_rewards = np.zeros(validation_episodes)
    #print(Q)
    for episode in range(validation_episodes):
        x, y = 0, 0
        step_number = 0
        game_ended = False
        sum_of_rewards[episode] = 0
        while not game_ended:
            step_number += 1
            action = get_action_with_max_value(Q, x, y)
            #print(f"x: {x}, y: {y}, action: {action}")
            next_x, next_y, reward, end = step(x, y, action)

            x, y = next_x, next_y
            sum_of_rewards[episode] += reward

            if step_number == max_steps_number or end:
                game_ended = True
        #time.sleep(10)
    print(f"Average validation return {np.average(sum_of_rewards)}")

if __name__ == "__main__":
    Q = qlearning()
    validate(Q)