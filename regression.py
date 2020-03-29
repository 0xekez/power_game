import numpy as np
import matplotlib.pyplot as plt

from player import Player

# Performs a linear regression on past clearing prices to guess the
# future clearing price.
class Regression(Player):
    def __init__(self):
        super().__init__("regression")
        self.clearing_prices = []
        self.m = 0
        self.b = 0
        self.update_count = 0

    def receive_update(self, update):
        self.clearing_prices.append(update)
        self.update_count += 1

        # Least squares:
        # https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.lstsq.html
        y = np.array(self.clearing_prices)
        x = np.arange(self.update_count)
        A = np.vstack([x, np.ones(len(x))]).T
        self.m, self.b = np.linalg.lstsq(A, y, rcond=None)[0]

    def bid(self, demand):
        cp_guess = self.m * (self.update_count + 1) + self.b
        my_bid = []
        for plant in self.power_plants[:-1]:
            my_bid.append([plant, plant.price_per_kwh])
        my_bid.append([self.power_plants[-1], cp_guess])

        return my_bid

    def plot(self):
        y = np.array(self.clearing_prices)
        x = np.arange(self.update_count)
        plt.plot(x, y, 'o', label='Original data', markersize=1)
        plt.plot(x, self.m*x + self.b, 'r', label='Fitted line')

        plt.legend()
        plt.show()
