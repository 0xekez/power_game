import numpy as np
import matplotlib.pyplot as plt

from player import Player
from power_plant import plant_groups

# Calculates the clearing price from a set of bids. Bids are in the
# form (power_plant, bidded_price). Demand is the amount of power that
# is need for this bid cycle.
def calculate_clearing_price(bids, demand):
    bids = sorted(bids, key=lambda bid: bid[1])
    for bid in bids:
        demand -= bid[0].remaining_power
        if demand <= 0:
            return bid[1]
    # If there are not enough bids to satisfy demand, return the last
    # bid.
    return bids[-1][1]

# Performs a linear regression on past agressiveness score where an
# agressiveness score is defined as how much more was bid than cost.
class Alice(Player):
    def __init__(self):
        super().__init__("alice")
        self.m = 0
        self.b = 0
        self.update_count = 0

        self.min_bids = []
        for group in plant_groups:
            for plant in group:
                self.min_bids.append([plant, plant.price_per_kwh])

        self.past_bases = []
        self.past_cps = []

    def bid(self, demand):
        # Calculate what the min clearing price would be.
        base_cp = calculate_clearing_price(self.min_bids, demand)
        self.past_bases.append(base_cp)

        cp_guess = (len(self.past_cps) + 1) * self.m + self.b
        
        return [[plant, max([plant.price_per_kwh, cp_guess])]
                 for plant in self.power_plants]

    def receive_update(self, update):
        self.past_cps.append(update)

    def tick(self):
        super().tick()

        agro = []
        for i in range(len(self.past_cps)):
            agro.append(self.past_cps[i] / self.past_bases[i])

        y = np.array(agro)
        x = np.arange(len(agro))
        A = np.vstack([x, np.ones(len(x))]).T
        self.m, self.b = np.linalg.lstsq(A, y, rcond=None)[0]

    def plot(self):
        agro = []
        for i in range(len(self.past_cps)):
            agro.append(self.past_cps[i] / self.past_bases[i])

        y = np.array(agro)
        x = np.arange(len(agro))

        plt.plot(x, y, 'o', label='Original data', markersize=1)
        plt.plot(x, self.m*x + self.b, 'r', label='Fitted line')

        plt.legend()
        plt.show()
