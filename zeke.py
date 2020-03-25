import matplotlib.pyplot as plt

from player import Player
from bank import Bank
from power_plant import plant_groups

# Based on the observation that clearing price seems to be roughly a
# function of demand, lets try and "memoize" clearing prices for
# various amounts of demand.
class Zeke(Player):
    def __init__(self):
        super().__init__("zeke")
        self.memory = {}
        self.last_demand = 0

    def bid(self, demand):
        self.last_demand = demand
        demand = round(demand) % 100

        if demand in self.memory:
            # If we beleive that we have predicted the clearing price,
            # then we want to attempt to drive it up, while
            # positioning as many of our plants below it as
            # possible. In order to do this, we position all of our
            # plants who's price is less than the predicted price at
            # 80% of the predicted price. This way we hope to drive up
            # the price, while not risking that some of our plants
            # will price too high.
            predicted = self.memory[demand]
            return [[plant, max(predicted * 0.5, plant.price_per_kwh)]
                    for plant in self.power_plants]

        # Otherwise, bid every plant at its marginal cost.
        return [[plant, plant.price_per_kwh] for plant in self.power_plants]

    def receive_update(self, clearing_price):
        demand = round(self.last_demand) % 100
        if demand in self.memory:
            # Take the average.
            self.memory[demand] += clearing_price
            self.memory[demand] /= 2
        else:
            self.memory[demand] = clearing_price
