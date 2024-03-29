import sys
import gymnasium as gym
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ddpg import DDPGagent
from utils import *
from water_desalination_environment import env 

environment = env()

agent = DDPGagent(environment)
#noise = OUNoise(environment.action_space_discrete)
batch_size = 128
rewards = []
avg_rewards = []

for episode in range(50):
    state = environment.reset()
    #noise.reset()
    episode_reward = 0
    
    for step in range(500):
        action = agent.get_action(state)
        print(action)
        #action = noise.get_action(action, step)
        new_state, reward, done, _ = environment.step(action) 
        agent.memory.push(state, action, reward, new_state, done)
        
        if len(agent.memory) > batch_size:
            agent.update(batch_size)        
        
        state = new_state
        episode_reward += reward

        if done:
            sys.stdout.write("episode: {}, reward: {}, average _reward: {} \n".format(episode, np.round(episode_reward, decimals=2), np.mean(rewards[-10:])))
            break

    rewards.append(episode_reward)
    avg_rewards.append(np.mean(rewards[-10:]))

plt.plot(rewards)
plt.plot(avg_rewards)
plt.plot()
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.show()