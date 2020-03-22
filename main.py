from bank import Bank
from power_plant import PowerPlant
from player import Player

from bob import Bob

import random

def calculate_clearing_price(bids, demand):
    last_bid = 0

    while demand > 0:
        if len(bids) == 0:
            return last_bid
        current_bid = bids.pop(0)
        current_plant = current_bid[0]
        current_price = current_bid[1]

        last_bid = current_price
        power_wanted = min([current_plant.remaining_power, demand])

        demand -= power_wanted

    return last_bid  

players = [Bob()]

while True:
    # Gaussian distribution with same mean and stddev as hugh's
    # classes dataset.
    demand = random.gauss(15778.57143, 2418.961691)
    demand = round(demand)
    bids = []

    # Get the bids for each player and tell them the round is starting.
    for player in players:
        player.tick()
        bids.extend(player.bid(demand))

    # Sort the bids by price.
    bids = sorted(bids, key=lambda bid: bid[1])
    clearing_price = calculate_clearing_price(bids.copy(), demand)

    while demand > 0:
        if len(bids) == 0:
            break

        # Pop the first bid from the bid stack.
        current_bid = bids.pop(0)
        # Get the current power plant.
        current_plant = current_bid[0]
        # Get the bidded price.
        current_price = current_bid[1]

        # Determine the amount of power that we'd like from this
        # plant.
        power_wanted = min([current_plant.remaining_power, demand])

        # Pay the plants owner for the power.
        Bank().deposit(current_plant.owner, clearing_price * power_wanted)

        # Generate the power.
        demand -= current_plant.generate(power_wanted)

    # Let each player know what happened.
    for player in players:
        player.receive_update(clearing_price)
