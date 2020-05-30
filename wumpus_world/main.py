import time

import numpy as np
import random
from wumpus_world.environment import Action, step


def get_action_with_max_value(Q, x, y):
    return Q.argmax(axis=0)[x][y]

def qlearning():
    print("Started learning...")
    # Setting learning parameters
    number_of_episodes = 20000
    gamma = 0.9
    alpha = 0.4
    epsilon = 0.4
    max_steps_number = 40

    num_actions = len([action.value for action in Action])
    Q = np.zeros((num_actions, 4, 4))
    sum_of_rewards = np.zeros(number_of_episodes)

    for episode in range(number_of_episodes):
        if epsilon > 0.1:
            epsilon -= 0.005
        x, y = 0, 0
        step_number = 0
        game_ended = False
        sum_of_rewards[episode] = 0
        last_2_actions = [(None, None), (x, y)]
        while not game_ended:
            step_number += 1
            if random.uniform(0, 1) < epsilon: # epsilon-greedy policy
                action = random.randrange(num_actions) # get random action
            else:
                action = get_action_with_max_value(Q, x, y) # get action with highest value in Q for x, y
            next_x, next_y, reward, end = step(x, y, action) # get next step from environment
            if next_x == last_2_actions[0][0] and next_y == last_2_actions[0][1]: # check if agent is oscillating between 2 fields
                reward -= 20
            Q[action][x][y] += alpha*(reward + gamma*get_action_with_max_value(Q, next_x, next_y) - Q[action][x][y]) # TD equation
            last_2_actions[0] = last_2_actions[1] # update environment variables
            last_2_actions[1] = (next_x, next_y)
            x, y = next_x, next_y
            sum_of_rewards[episode] += reward

            if step_number == max_steps_number or end: # check if episode ended
                game_ended = True
        if episode % 1000 == 0:
            print(f"Sum of rewards for episode {episode}: {sum_of_rewards[episode]}")

    return Q

def run(Q):
    max_steps_number = 20
    x, y = 0, 0
    step_number = 0
    game_ended = False
    sum_of_rewards = 0

    while not game_ended:
        step_number += 1
        action = get_action_with_max_value(Q, x, y)
        print(f"x: {x}, y: {y}, action: {Action(action).name}")
        next_x, next_y, reward, end = step(x, y, action)

        x, y = next_x, next_y
        sum_of_rewards += reward

        if step_number == max_steps_number or end:
            game_ended = True

    print(f"Score: {sum_of_rewards}")

if __name__ == "__main__":
    Q = qlearning()
    run(Q)