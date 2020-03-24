from player import Player
from power_plant import plant_groups

class Marginal(Player):
  def __init__(self):
      super().__init__("marginal")

  def bid(self, demand):
      my_bid = []
      for plant in self.power_plants:
          #bids marginal price for all plants
          my_bid.append([plant, plant.price_per_kwh])
      return my_bid
