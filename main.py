import random
import matplotlib.pyplot as plt

from bank import Bank
from gov import Gov
from plotter import MultiGraphPlotter, show_bar, SingleGraphPlotter
from power_plant import PowerPlant, plant_groups
from player import Player

from laster import Laster
from averager import Averager
from constant import Constant
from julia import Competative
from zeke import Zeke
from regression import Regression
from alice import Alice
from julia import Julia
from marginal import Marginal
from julia import Julinear

players = [Laster(), Zeke(), Julia(), Julinear(), Constant(), Competative(), Marginal()]

TheGov = Gov(players, plant_groups)
Plotter = MultiGraphPlotter(window=100)
MoneyPlotter = SingleGraphPlotter(window=100)
# The number of times to repeat the simulation.
repeats = 10
# The number of rounds per simulation.
rounds = 24 * 365

# Rather or not we should plot.
plot = True

# Set up win counts. A player 'wins' if at the end of a round they
# have the most money in their bank account.
wins = {}
for player in players:
    wins[player.name] = 0

for repeat in range(repeats):
    TheGov.reset()
    Plotter.reset("demand")
    Plotter.reset("clearing price")
    for _ in range(rounds):
        demand = Gov.calculate_demand()
        clearing_price, bids = TheGov.simulate_round(demand)

        if plot:
            show_bar(bids, players, clearing_price, demand)
            Plotter.add_info("demand", demand)
            Plotter.add_info("clearing price", clearing_price)
            Plotter.draw()

            for player in players:
                bal = Bank().check_balance(player.name)
                MoneyPlotter.add_info(player.name, bal)
            MoneyPlotter.draw()
            
    winner = max(Bank.the_bank, key=Bank.the_bank.get)
    wins[winner] += 1

results = list(reversed(["{} -> {}".format(k, v) for k, v in sorted(wins.items(), key=lambda item: item[1])]))
for place in range(len(results)):
    print("#{}: {}".format(place + 1, results[place]))
