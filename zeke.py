import matplotlib.pyplot as plt
from player import Player
from bank import Bank
from power_plant import plant_groups

# Increase prices until we stop making money.
class Zeke(Player):
    def __init__(self):
        super().__init__("zeke")

        self.last_balance = 0
        self.balance_deltas = []
        self.balances = []

        self.cost_modifier = 0.1

        # Compute the total amount of power avaliable on the market.
        self.supply = sum([
            sum([plant.capacity for plant in group]) for group in plant_groups])

    def reset(self):
        self.last_balance = 0
        self.balance_deltas = []
        self.balances = []

        self.cost_modifier = 0.1

    def plot(self):
        plt.figure()

        plt.subplot(211)
        plt.plot(self.balance_deltas)
        plt.ylabel("balance deltas")

        plt.subplot(212)
        plt.plot(self.balances)
        plt.ylabel("balance over time")
        plt.show()

    def tick(self):
        super().tick()

        current_balance = Bank().check_balance("zeke")
        balance_delta = current_balance - self.last_balance

        if balance_delta > 0:
            self.cost_modifier *= 2
        if balance_delta <= 0:
            self.cost_modifier /= 1.5

        self.balance_deltas.append(balance_delta)
        self.balances.append(current_balance)
        self.last_balance = current_balance

    def bid(self, demand):
        my_bid = [[plant, plant.price_per_kwh*(1+self.cost_modifier)]
                  for plant in self.power_plants]
        return my_bid
