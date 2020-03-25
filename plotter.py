"""
Class that assists in visualizing data from the game.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches # For labels
import numpy as np


class Plotter:
    def __init__(self, title):
        self.data = []
        self.title = title
        plt.style.use("dark_background")

    def update(self, data):
        self.data.append(data)
        plt.cla()
        plt.plot(self.data)
        plt.title(self.title)
        plt.pause(0.05)

    def reset(self):
        self.data = []

class MultiPlotter:
    def __init__(self, window):
        self.data = {}
        self.window = window
        plt.style.use("dark_background")
    def add_info(self, cat, data):
        if cat not in self.data:
            self.data[cat] = []
        self.data[cat].append(data)
        self.data[cat] = self.data[cat][-self.window:]
    def reset(self, cat):
        if cat in self.data:
            del self.data[cat]
    def draw(self):
        plt.figure(1)
        for index, cat in enumerate(self.data):
            plt.subplot(len(self.data), 1, index + 1)
            plt.cla()
            plt.plot(self.data[cat], label=cat)
            plt.legend(loc="upper left")
        plt.pause(0.05)

def get_owner(plant):
    return plant.owner

def get_colormap(players):
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    colorMap = {}
    for index, player in enumerate(players):
        colorMap[player.name] = colors[index]
    return colorMap

def get_highest_bid(player, bids):
    bids = sorted(bids, key=lambda b: b[1])
    for bid in reversed(bids):
        if get_owner(bid[0]) == player.name:
            return bid[1]
    return 0

def show_bar(bids, players, clearing_price, demand):
    bids = sorted(bids, key=lambda b: b[1])

    # Widths are determined by the power plants relative capacity.
    max_cap = max([bid[0].capacity for bid in bids])
    widths = np.array([(bid[0].capacity/max_cap) for bid in bids])
    prices = np.array([bid[1] for bid in bids])

    colorMap = get_colormap(players)
    colors = np.array([colorMap[get_owner(bid[0])] for bid in bids])

    # Sort players by highest bid
    players = reversed(sorted(players, key=lambda p: get_highest_bid(p, bids)))
    patches = [mpatches.Patch(color=colorMap[p.name], label=p.name) for p in players]

    # Compute the indicies so the bars line up nicely.
    indicies = []
    for i in range(len(widths)):
        indicies.append(sum(widths[:i]))
    indicies = indicies = np.array(indicies)
    
    plt.figure(2)
    plt.cla()

    plt.axhline(y=clearing_price, color='r', linestyle='-')
    plt.axvline(x=demand/max_cap, color='r', linestyle='-')
    
    plt.legend(handles=patches, loc="upper left")
    plt.bar(indicies, prices, widths, align="edge", color=colors, edgecolor="black")
    plt.pause(0.05)
