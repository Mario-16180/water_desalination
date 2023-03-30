import gymnasium as gym
import numpy as np
import math

class env():
    Fossil_Fuel = 0
    Photovoltaic_Panel = 1
    Battery = 2
    def __init__(self):
        self.action_space_discrete = {'Fossil Fuel': 0, 'Photovoltaic Panel': 1, 'Battery': 2} # Selecting the energy source
        self.action_space_continuous = {'Power': 0} # In Watts
        # self.state_space = {'Current height of feed water': 0, 'Current height of permeate water': 1,
        #                    'Current battery charge': 2, 'Osmotic pressure': 3,
        #                    'Fossil fuel source - switch': 4, 'Photovoltaic panel source - switch': 5, 'Battery source - switch': 6,
        #                    'Power': 7}
        self.state_space = {'Current height of feed water': 0, 'Current height of permeate water': 1,
                            'Current battery charge': 2, 'Current energy source': 3, 'Current time': 4}
        
        # Setting some limits and real life characteristics of the devices in the environment
        self.max_height_feed_water_tank = 4 # Meters
        self.min_height_feed_water_tank = 0.5 # Meters

        self.max_height_permeate_water_tank = 4 # Meters
        self.min_height_permeate_water_tank = 0 # Meters

        self.cubic_meters_per_day_capacity = 9.1 # Cubic meters per day

        self.recovery_rate = 0.5 # Constant percentage for now. In the future, it will be a function of the water flow rate and cubic meters per day capacity.
    
    def step(self, action):
        state = self.state_calculation(action)
        reward = self.reward_calculation()
        done = self.check_done()
        info = {}
        return state, reward, done, info

    def reset(self):
        self.reset_flag = True
        state = self.state_calculation(0)
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
        if self.done == True:
            raise ValueError("The environment has already been terminated. Please reset the environment before calling step() again.")
        if self.reset_flag == True:
            self.current_height_feed_water_tank = self.max_height_feed_water_tank / 2
            self.current_height_permeate_water_tank = 0 # Meters, maybe
            self.current_battery_charge = 0.1 # In percentage
            self.current_energy_source = 0 # 0 = Fossil Fuel, 1 = Photovoltaic Panel, 2 = Battery
            self.current_time = 0 # In minutes. Can be used as a variable to represent weather, or it could be switched to irradiation.
            
            self.current_power = 6000 # In Watts # For now, let's ignore this, because it is constant and it is tautological with the energy source.
            self.current_osmotic_pressure = 0 # In psi # Ignored for now, but will be used later.

            self.reset_flag = False
        else:
            if action == self.Fossil_Fuel:
                self.current_energy_source = 0
                if self.current_battery_charge < 1.0: # In percentage
                    self.current_battery_charge += 0.001 
                self.current_power = 6000 # In Watts
            elif action == self.Photovoltaic_Panel:
                self.current_energy_source = 1
                self.current_power = 4000 # In Watts
            elif action == self.Battery:
                self.current_energy_source = 2
                if self.current_battery_charge > 0: # In percentage
                    self.current_battery_charge -= 0.001 
                    self.current_power = 5000 # In Watts
                else:
                    # If the battery has no charge, let's switch to fossil fuel, which can provide power to the system.
                    self.current_energy_source = 0
                    self.current_power = 6000 # In Watts
            else:
                raise ValueError("Received invalid action={} which is not part of the action space".format(action))
            
            ##### Calculation of water flows
            # Equation from the paper "Sizing methodology based on design..."
            self.current_pre_permeate_water_flow = 0.01224 * self.current_power ** (0.5341) * self.cubic_meters_per_day_capacity ** (0.5525) / 60 # Cubic meters per minute
            # Calculation of Qp with constant recovery rate
            self.current_permeate_water_flow = self.recovery_rate * self.current_pre_permeate_water_flow # Qp

            ##### Calculation of heights

            ## Feed water tank
            # Calculation of the new height of the feed water tank
            self.feed_water_flow_input_height = 0.0081664 * math.sin(2*math.pi*self.current_time/180) + 0.0081664
            # The input of feed water to its tank is a sine wave with a period of 180 minutes that represents the input water in terms of height.
            
            self.current_feed_water_flow_output_height = self.current_pre_permeate_water_flow / 8 # In meters. Needs revision.
            # The output of the feed water tank is the input to the water pump, and it represents a decrease in height of the feed water tank. It's just the division between
            # the flow rate of the feed water and the area of the pipe that connects the feed water tank to the water pump. It is divided by 1 (as in 1 m^2 to get meters) just for this 
            # first version of the environment. Ideally, in the future, we should consider the design of the water tanks and the pipes.

            self.current_height_feed_water_tank += self.feed_water_flow_input_height - self.current_feed_water_flow_output_height # In meters
            
            ## Permeate water tank
            # Calculation of the new height of the permeate water tank
            self.current_permeate_water_flow_input_height = self.current_permeate_water_flow / 8 # In meters. It is divided by 8, assuming that the surface area of the tank
            # is 8 m^2. Needs revision, but can work for the first version of the environment.

            self.current_height_permeate_water_tank += self.current_permeate_water_flow_input_height # In meters

        state = [self.current_height_feed_water_tank, self.current_height_permeate_water_tank, self.current_battery_charge, self.current_energy_source, self.current_time]
        return np.array(state)
    
    def check_done(self):
        # The conditions to terminate the episode are as follows:
        # 1. There is no more water in the feed water tank
        # 2. The permeate water tank is full
        # 3. It has elapsed 24 hours
        if (self.current_height_feed_water_tank <= self.min_height_feed_water_tank) or (self.current_height_permeate_water_tank >= self.max_height_permeate_water_tank) or (self.current_time >= 1440):
            self.done = True
            return True
        else:
            self.done = False
            return False