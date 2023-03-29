import gymnasium as gym
import numpy as np
import pygame

class WaterDesalinationEnvironment(gym.Environment):
    Fossil_Fuel = 0
    Photovoltaic_Panel = 1
    Battery = 2
    def __init__(self):
        self.action_space_discrete = {'Fossil Fuel': 0, 'Photovoltaic Panel': 1, 'Battery': 2} # Selecting the energy source
        self.action_space_continuous = {'Power': 0} # In Watts
        self.state_space = {'Current height of feed water': 0, 'Current height of permeate water': 1,
                            'Current battery charge': 2, 'Osmotic pressure': 3,
                            'Fossil fuel source - switch': 4, 'Photovoltaic panel source - switch': 5, 'Battery source - switch': 6,
                            'Power': 7}
        
        # Setting some limits in the environment
        self.max_height_feed_water_tank = 10 # Meters, maybe
        self.min_height_feed_water_tank = 0.5 # Meters, maybe

        self.max_height_permeate_water_tank = 10 # Meters, maybe
        self.min_height_permeate_water_tank = 0 # Meters, maybe
    
    def step(self, action):
        # Here, action is the energy source
        state = state_calculation(action)
        reward = reward_calculation(action)
        done = check_done(action)
        info = {}
        return state, reward, done, info

    def reset(self):
        self.reset_flag = True
        state = state_calculation()
        return state

    def reward_calculation(self):
        reward = 0

        return reward

    def state_calculation(self, action):
        if self.reset_flag == True:
            self.current_height_feed_water_tank = self.max_height_brine_water_tank / 2
            self.current_height_permate_water_tank = 0 # Meters, maybe
            self.current_battery_charge = 0 # In percentage
            self.current_energy_source = 0 # 0 = Fossil Fuel, 1 = Photovoltaic Panel, 2 = Battery
            self.current_time = 0 # In minutes
            self.current_power = 0 # In Watts
            self.current_osmotic_pressure = 0 # In psi
            self.reset_flag = False
        elif action == Fossil_Fuel:
            self.current_energy_source = 0
        elif action == Photovoltaic_Panel:
            self.current_energy_source = 1
        elif action == Battery:
            self.current_energy_source = 2
        else:
            raise ValueError("Received invalid action={} which is not part of the action space".format(action))
        if reset_flag == False:
            if self.current_energy_source == 0:
                self.current_power = 1000 # In Watts
            elif self.current_energy_source == 1:
                self.current_power = 500
            elif self.current_energy_source == 2:
                self.current_power = 200
            else:

        height_feed_water = 0
        osmotic_pressure = 0
        return state    
    def check_done(self):
        pass