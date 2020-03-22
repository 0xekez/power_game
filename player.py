from bank import Bank
from power_plant import PowerPlant

# Class that represents a player
class Player:
    def __init__(self, name):
        self.name = name
        Bank().create_account(self.name)
        self.power_plants = []
    
    # Returns a list of bids where bids are in the form (power_plant,
    # price_per_kwh) (the power plant, and the price that they will
    # sell at from that plant. _demand_ is the amount of power that is
    # needed for this round.
    def bid(self, demand):
        return []

    # Called whenever a new game loop begins.
    def tick(self):
        for plant in self.power_plants:
            plant.tick()

    # Called at the end of every game loop. Update contains
    # information about the end results of a round.
    def receive_update(self, update):
        return None

    def add_plant(self, power_plant):
        power_plant.set_owner(self.name)
        self.power_plants.append(power_plant)
