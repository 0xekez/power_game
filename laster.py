from player import Player
from power_plant import PowerPlant

# Prices each plant at the max of the last clearing prices and its
# operation cost.
class Laster(Player):
    def __init__(self):
        super().__init__("laster")
        self.last_clearing_price = 0

    def bid(self, demand):
        my_bid = []
        for plant in self.power_plants:
            my_bid.append(
                [plant, max([self.last_clearing_price, plant.price_per_kwh])])
        return my_bid

    def receive_update(self, update):
        self.last_clearing_price = update
