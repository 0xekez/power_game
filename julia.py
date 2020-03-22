from player import Player
from power_plant import plant_groups

# Tries to make a 25% profit on each sale.
class Julia(Player):
    def __init__(self):
        # Initialize a player class with the name bob. This will
        # handle creating a bank account and getting all of our
        # variables in order.
        super().__init__("julia")
        self.past_clearing_prices = []
        self.past_ccps = []

    def bid(self, demand):
        my_bid = []
        ccp = self.competative_clearing_price(demand)
        for plant in self.power_plants:
            #bids competative clearing price for each of my plants
            my_bid.append([plant, ccp])
        return my_bid

    def receive_update(self, update):
        self.past_clearing_prices += [update]

    def competative_clearing_price(self, demand):
        all_plants = []
        for group in plant_groups:
            all_plants += [plant for plant in group]
        demand_left, ccp = demand, 0
        while demand_left > 0:
            if not all_plants:
                return ccp
            lowest_bid, lowest_bidding_index = 100000, 0
            for i in range(0, len(all_plants)):
                plant = all_plants[i]
                if plant.price_per_kwh < lowest_bid:
                    lowest_bid, lowest_bidding_index = plant.price_per_kwh, i
            lowest_bidder = all_plants[lowest_bidding_index]
            if lowest_bidder.capacity <= demand_left:
                ccp += lowest_bid*lowest_bidder.capacity
                demand_left -= lowest_bidder.capacity
                all_plants = all_plants[:lowest_bidding_index]+all_plants[lowest_bidding_index+1:]
            else:
                ccp += lowest_bid*demand_left
                demand_left = 0
        return ccp
