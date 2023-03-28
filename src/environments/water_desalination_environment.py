import gymnasium as gym
import numpy as np
import pygame

class WaterDesalinationEnvironment(gym.Environment):
    def __init__(self, config):
        self.action_space = {'Fossil Fuel': 0, 'Photovoltaic Panel': 1, 'Battery': 2}
        self.state_space = {'Current height of brine water': 0, 'Current height of feed water': 1, 'Salt rejection': 2,
                            'Recovery rate': 3, 'Current battery charge': 4, 'Osmotic pressure': 5,
                            'Fossil fuel source - switch': 6, 'Photovoltaic panel source - switch': 7, 'Battery source - switch': 8,
                            'Power': 9, }
        
        # Setting some limits in the environment
        self.max_height_brine_water_tank = 8 # Meters, maybe
        self.min_height_brine_water_tank = 0.5 # Meters, maybe

        self.max_height_permeate_water_tank = 8 # Meters, maybe
        self.min_height_permeate_water_tank = 0 # Meters, maybe
    
    def step(self, action):
        # Here, action is the one-hot encoded energy source
        state = state_calculation(action)
        reward = reward_calculation(action)
        done = check_done(action)
        info = {}
        return state, reward, done, info

    def reset(self):
        self.current_height_brine_water_tank = self.max_height_brine_water_tank / 2
        self.current_height_permate_water_tank = 0
        self.current_battery_charge = 0
        self.current_energy_source = 0 # 0 = Fossil Fuel, 1 = Photovoltaic Panel, 2 = Battery
        pass

    def reward_calculation(self):
        reward = 0

        return reward

    def state_calculation(self):
        height_feed_water = 0
        osmotic_pressure = 0
        return 
    
    def check_done(self):
        pass