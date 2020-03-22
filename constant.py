from player import Player
from power_plant import PowerPlant

# Tries to make a 25% profit on each sale.
class Constant(Player):
    def __init__(self):
        # Initialize a player class with the name bob. This will
        # handle creating a bank account and getting all of our
        # variables in order.
        super().__init__("constant")

    def bid(self, demand):
        my_bid = []
        for plant in self.power_plants:
            # Just try to sell our power at a rate that gives us a
            # decent profit.
            my_bid.append([plant, plant.price_per_kwh * 1.25])
        return my_bid
