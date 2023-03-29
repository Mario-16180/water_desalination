import gymnasium as gym
import numpy as np

class env():
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
        
        # Setting some limits and real life characteristics of the devices in the environment
        self.max_height_feed_water_tank = 10 # Meters, maybe
        self.min_height_feed_water_tank = 0.5 # Meters, maybe

        self.max_height_permeate_water_tank = 10 # Meters, maybe
        self.min_height_permeate_water_tank = 0 # Meters, maybe

        self.cubic_meters_per_day_capacity = 40 # Cubic meters per day
    
    def step(self, action):
        state = self.state_calculation(action)
        reward = self.reward_calculation()
        done = self.check_done()
        info = {}
        return state, reward, done, info

    def reset(self):
        self.reset_flag = True
        state = self.state_calculation()
        return state

    def reward_calculation(self):
        # In this first version of the environment, let's just use a simple reward function that penalizes the agent for not filling the permeate water tank in the 24 hours period,
        # and rewards the agent for filling the permeate water tank on time. If there's no more water left in the feed water tank, the agent does not get any reward, and the 
        # episode gets terminated. Moreover, the agent gets a small penalty for every time step that it takes to fill the permeate water tank.
        if self.current_time >= 1440:
            reward = -100
        elif self.current_height_permeate_water_tank >= self.max_height_permeate_water_tank:
            reward = 100
        elif self.current_height_feed_water_tank <= self.min_height_feed_water_tank:
            reward = 0
        else:
            reward = -1
        return reward

    def state_calculation(self, action):
        # The following comment lines will be used for the next version of the environment
        # Here, action is a list of the energy source and the power
        # action[0] is the energy source
        # action[1] is the power
        # source = action[0] # 0 = Fossil Fuel, 1 = Photovoltaic Panel, 2 = Battery
        # power = action[1] # Continuous value in Watts
        if self.reset_flag == True:
            self.current_height_feed_water_tank = self.max_height_feed_water_tank / 2
            self.current_height_permeate_water_tank = 0 # Meters, maybe
            self.current_battery_charge = 0 # In percentage
            self.current_energy_source = 0 # 0 = Fossil Fuel, 1 = Photovoltaic Panel, 2 = Battery
            self.current_time = 0 # In minutes
            self.current_power = 0 # In Watts
            self.current_osmotic_pressure = 0 # In psi
            self.reset_flag = False
        else:
            if action == Fossil_Fuel:
                self.current_energy_source = 0
                self.current_power = 6000 # In Watts
            elif action == Photovoltaic_Panel:
                self.current_energy_source = 1
                self.current_power = 5000 # In Watts
            elif action == Battery:
                self.current_energy_source = 2
                self.current_power = 5500 # In Watts
            else:
                raise ValueError("Received invalid action={} which is not part of the action space".format(action))
            self.current_permeate_water_flow = 0.01224 * self.current_power ** (0.5341) * self.cubic_meters_per_day_capacity ** (0.5525) # Equation from the paper
            
        state = [self.current_height_feed_water_tank, self.current_height_permeate_water_tank, self.current_battery_charge, self.current_osmotic_pressure, self.current_energy_source, self.current_time, self.current_power]
        return state
    
    def check_done(self):
        # The conditions to terminate the episode are as follows:
        # 1. There is no more water in the feed water tank
        # 2. The permeate water tank is full
        # 3. It has elapsed 24 hours
        if (self.current_height_feed_water_tank <= self.min_height_feed_water_tank) or (self.current_height_permeate_water_tank >= self.max_height_permeate_water_tank) or (self.current_time >= 1440):
            return True
        else:
            return False