import gym
from gym import spaces

from src.params import *
from src.microgrid import Microgrid


class MicrogridEnv(gym.Env):
    def __init__(self, data_dict):
        """Set up environment.

        Params:
            data_dict: hourly environment data. Should contain the following keys: "energy_demand", "solar_irradiance",
            "wind_speed", and "rate_consumption_charge". Each key should map to a list value containing the hourly
            data for that variable.
        """
        # Initialize the Microgrid
        self.microgrid = Microgrid()
        self.step_count = 0
        self.data_dict = data_dict  # hourly data of solar irradiance, wind speed, energy price, energy demand

        # Define action space
        actions = [2,  # purchase energy for load (yes/no)
                   2,  # purchase energy to load battery (yes/no)
                   2,  # discharge battery (yes/no)
                   3,  # solar (support load, charge battery, sell to utility grid)
                   3,  # wind (support load, charge battery, sell to utility grid)
                   3,  # generator (support load, charge battery, sell to utility grid)
                   2,  # use solar energy (on/off)
                   2,  # use wind energy (on/off)
                   2   # use generator energy (on/off)
                   ]

        # Define the action space
        self.action_space = spaces.MultiDiscrete(actions)

        # Define observation space (i.e. environment state)
        self.observation_space = spaces.Box(low=np.array([0] * 4 + [soc_min]),
                                            high=np.array([10_000,  # solar irradiance (W/m^2)
                                                           100,  # wind speed (m/s)
                                                           10,  # electricity price to sell for ($/kWh)
                                                           10_000,  # energy demand in kWh
                                                           soc_max,  # battery status
                                                           ]),
                                            dtype=np.float64)

    def reset(self, **kwargs):
        """Needs to be defined for gym. Reset the environment to its initial state and return an initial observation."""
        self.step_count = 0
        self.microgrid = Microgrid()  # Reset the Microgrid to its initial state
        return self.get_observation()  # Return the initial observation

    @staticmethod
    def get_action_dict(action):
        action_dict = {
            "purchased": action[0:2],
            "discharged": action[2],
            "solar": action[3],
            "wind": action[4],
            "generator": action[5],
            "adjusting_status": action[6:9],
        }
        return action_dict

    def get_observation(self):
        # Extract relevant information from the Microgrid's state and return it as an observation (environment state)
        return [self.microgrid.solar_irradiance, self.microgrid.wind_speed, self.microgrid.energy_price_utility_grid,
                self.microgrid.energy_demand, self.microgrid.soc]

    def compute_reward(self):
        # Negative costs as reward
        return -self.microgrid.cost_of_epoch()

    def step(self, action):
        """Needs to be defined for gym. Perform one step (= episode).

        Params:
            action: action chosen by agent to be performed in environment
        """
        action_dict = self.get_action_dict(action)

        # Execute the chosen action on the Microgrid
        self.microgrid.transition(action_dict, self.data_dict, self.step_count)

        # Calculate the reward (i.e. negative costs of that episode)
        reward = self.compute_reward()

        # Check if the episode is done (termination condition)
        self.step_count += 1
        max_epochs = len(self.data_dict["wind_speed"])
        done = self.step_count >= max_epochs

        # Return the next observation, reward, done flag, and any additional info to gym
        return self.get_observation(), reward, done, {}

    def render(self, mode='human'):
        """Save environment and action information of each step"""
        mg = self.microgrid

        info = {
            "reward": self.compute_reward(),
            "operational_cost": mg.operational_cost(),
            "purchased_energy_cost": mg.energy_purchased,
            "purchased_energy_battery": mg.energy_for_battery_bought,
            "purchased_energy_load": mg.energy_for_load_bought,
            "sell_back_revenue": mg.sell_back_reward(),
            "energy_demand": mg.energy_demand,
            "energy_load": mg.energy_total,
            "discharged": mg.actions_discharged,

            "purchase_energy": mg.actions_purchased,
            "energy_battery_discharged": mg.actions_discharged,

            "energy_generated_solar": mg.energy_generated_solar(),
            "solar": mg.actions_solar,

            "energy_generated_wind": mg.energy_generated_wind(),
            "wind": mg.actions_wind,

            "energy_generated_generator": mg.energy_generated_generator(),
            "generator": mg.actions_generator,

            "actions_adjusting_status": mg.actions_adjusting_status,
            "soc": mg.soc,
            "solar_irradiance": mg.solar_irradiance,
            "wind_speed": mg.wind_speed,
            "energy_price_utility_grid": mg.energy_price_utility_grid,
        }
        return info
