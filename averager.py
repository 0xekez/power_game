from player import Player
from power_plant import PowerPlant

# Prices each plant at the max of average historical clearing prices
# and its operation cost.
class Averager(Player):
    def __init__(self):
        super().__init__("averager")
        self.past_closing_prices = []

    def bid(self, demand):
        if not self.past_closing_prices:
            return []

        my_bid = []
        average_closing = sum(self.past_closing_prices)/len(self.past_closing_prices)
        for plant in self.power_plants:
            my_bid.append(
                [plant, max([average_closing, plant.price_per_kwh])])
        return my_bid

    def receive_update(self, update):
        self.past_closing_prices.append(update)
