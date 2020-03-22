from player import Player
from power_plant import PowerPlant

class Bob(Player):
    def __init__(self):
        # Initialize a player class with the name bob. This will
        # handle creating a bank account and getting all of our
        # variables in order.
        super().__init__("bob")

        # Add some power plants.
        self.add_plant(PowerPlant(price=73.72, capacity=1900))
        self.add_plant(PowerPlant(40.94, 650))

    def bid(self, demand):
        my_bid = []
        for plant in self.power_plants:
            my_bid.append([plant, plant.price_per_kwh * 1.25])
        return my_bid
