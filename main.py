import random
import matplotlib.pyplot as plt

from bank import Bank
from gov import Gov
from power_plant import PowerPlant, plant_groups
from player import Player

from laster import Laster
from averager import Averager
from constant import Constant
from julia import Julia
from zeke import Zeke
from regression import Regression
from alice import Alice

players = [Constant(), Laster(), Averager(), Julia(), Zeke(), Regression(), Alice()]

TheGov = Gov(players, plant_groups)

# The number of times to repeat the simulation.
repeats = 10
# The number of rounds per simulation.
rounds = 24 * 365

# Set up win counts. A player 'wins' if at the end of a round they
# have the most money in their bank account.
wins = {}
for player in players:
    wins[player.name] = 0

for repeat in range(repeats):
    TheGov.reset()
    for _ in range(rounds):
        demand = Gov.calculate_demand()
        TheGov.simulate_round(demand)
    winner = max(Bank.the_bank, key=Bank.the_bank.get)
    wins[winner] += 1

results = list(reversed(["{} -> {}".format(k, v) for k, v in sorted(wins.items(), key=lambda item: item[1])]))
for place in range(len(results)):
    print("#{}: {}".format(place + 1, results[place]))


# # Calculates the clearing price from a set of bids. Bids are in the
# # form (power_plant, bidded_price). Demand is the amount of power that
# # is need for this bid cycle.
# def calculate_clearing_price(bids, demand):
#     bids = sorted(bids, key=lambda bid: bid[1])
#     for bid in bids:
#         demand -= bid[0].remaining_power
#         if demand <= 0:
#             return bid[1]
#     # If there are not enough bids to satisfy demand, return the last
#     # bid.
#     return bids[-1][1]

# # Randomly assigns the power plants to the players in the game. No
# # real reason for this to be a function because it only modifies
# # global state, but it cleans up the logic in the main loop a little
# # imo.
# def randomize_power_plants():
#     assert  len(players) <= len(plant_groups), "number of strategies needs to be <= number of plants"
#     random.shuffle(plant_groups)
#     for i in range(len(players)):
#         players[i].power_plants = plant_groups[i]
#         for plant in players[i].power_plants:
#             plant.set_owner(players[i].name)

# days = 100
# rounds = days * 24
# repeats = 1

# # Set up win counts. A player 'wins' if at the end of a round they
# # have the most money in their bank account.
# wins = {}
# for player in players:
#     wins[player.name] = 0

# # We track the clearing prices over time and plot them at the end.
# clearing_prices = []

# for repeat in range(repeats):
#     # Reset the bank.
#     Bank().reset()
#     # Reset the players.
#     players = [p.__class__() for p in players]
#     # Shuffle the power plants among the players.
#     randomize_power_plants()

#     rounds_clearing_prices = []
#     for i in range(rounds):
#         # Gaussian distribution with same mean and stddev as hugh's
#         # classes dataset.
#         demand = random.gauss(15778.57143, 2418.961691)
#         demand = round(demand)
#         bids = []
#         # Get the bids for each player and tell them the round is starting.
#         for player in players:
#             player.tick()
#             players_bids = player.bid(demand)
#             # Show a warning if a player bids a negative amount.
#             for bid in players_bids:
#                 if bid[1] < 0:
#                     print("[warning] {} placed a negative bid".format(player.name))
#             bids.extend(players_bids)

#         # Sort the bids by price.
#         clearing_price = calculate_clearing_price(bids, demand)
#         rounds_clearing_prices.append(clearing_price)

#         while demand > 0:
#             if len(bids) == 0:
#                 break

#             # Pop the first bid from the bid stack.
#             current_bid = bids.pop(0)
#             # Get the current power plant.
#             current_plant = current_bid[0]
#             # Get the bidded price.
#             current_price = current_bid[1]

#             # Determine the amount of power that we'd like from this
#             # plant.
#             power_wanted = min([current_plant.remaining_power, demand])

#             # Pay the plants owner for the power.
#             Bank().deposit(current_plant.owner, clearing_price * power_wanted)

#             # Generate the power.
#             demand -= current_plant.generate(power_wanted)

#         # Let each player know what happened.
#         for player in players:
#             player.receive_update(clearing_price)

#     clearing_prices.append(rounds_clearing_prices)
#     winner = max(Bank.the_bank, key=Bank.the_bank.get)
#     wins[winner] += 1

# results = list(reversed(["{} -> {}".format(k, v) for k, v in sorted(wins.items(), key=lambda item: item[1])]))
# for place in range(len(results)):
#     print("#{}: {}".format(place + 1, results[place]))

# # Plot the clearing prices over time.
# x = list(range(rounds)[-25:])
# for clearing_list in clearing_prices:
#     plt.plot(x, clearing_list[-25:], 'o', markersize=1)

# plt.title("Clearing Price Over Time")
# plt.ylabel("clearing price")
# plt.xlabel("round")
# plt.show()

# players[-1].plot()
