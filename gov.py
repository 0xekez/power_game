""" Class that handles player bids and payments. """

import random
from functools import reduce

from bank import Bank

class Gov:
    """
    Government class that handles distributing money and setting
    clearing price. Intended to serve as an alternative to our rather
    large main file.
    """
    def __init__(self, players, plant_groups):
        self.players = players
        self.plant_groups = plant_groups
        assert len(players) <= len(plant_groups), \
            "number of players needs to be <= number of power plant groups."

    def randomize_power_plants(self):
        """ Shuffles power plant groups among current players. """
        random.shuffle(self.plant_groups)
        for player, group in zip(self.players, self.plant_groups):
            player.power_plants = group
            # Update the plant's owners.
            for plant in group:
                plant.set_owner(player.name)

    def reset(self):
        """ Resets the simulation. """
        Bank().reset()
        self.players = [p.__class__() for p in self.players]
        self.randomize_power_plants()

    def simulate_round(self, demand):
        """
        Simulates a single round of the simulation. Returns the clearing
        price for that round.
        """
        # Inform all of the players and power plants that a round is
        # beginning.
        for player in self.players:
            player.tick()
        for group in self.plant_groups:
            for plant in group:
                plant.tick()
        # Get bids from players.
        bids = []
        for player in self.players:
            bids.extend(player.bid(demand))
        # Calculate clearing price.
        clearing_price = Gov.calculate_clearing_price(bids, demand)
        # Generate the power.
        Gov.generate_power(bids, demand, clearing_price)
        # Update players on clearing price for this round.
        for player in self.players:
            player.receive_update(clearing_price)
        return clearing_price

    @staticmethod
    def calculate_clearing_price(bids, demand):
        """ Calculates the clearing price for a round. """
        bids = sorted(bids, key=lambda bid: bid[1])
        for bid in bids:
            demand -= bid[0].remaining_power
            if demand <= 0:
                return bid[1]
        # If demand is not met, return the highest bid price.
        return bids[-1][1]

    @staticmethod
    def generate_power(bids, demand, clearing_price):
        # Order the plants from lowest to highest price.
        bids = sorted(bids, key=lambda bid: bid[1])
        for bid in bids:
            plant = bid[0]
            # Determine the power we'd like from this plant.
            power_wanted = min([plant.remaining_power, demand])
            # Pay the plant's owner for the power we're going to
            # generate.
            assert plant.owner is not None, "bad"
            Bank().deposit(plant.owner, clearing_price * power_wanted)
            # Generate the power.
            demand -= plant.generate(power_wanted)
            if demand == 0:
                break

    @staticmethod
    def calculate_demand():
        """ Calculates the power demand for a round """
        # Gaussian distribution with same mean and stddev as hugh's
        # classes dataset.
        demand = random.gauss(15778.57143, 2418.961691)
        return demand
