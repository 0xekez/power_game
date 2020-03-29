from player import Player
from power_plant import plant_groups

class Competative(Player):
    # Bets the competative clearing price for all plants.
    def __init__(self, name='competative'):
        # Initialize a player class with the name bob. This will
        # handle creating a bank account and getting all of our
        # variables in order.
        super().__init__(name)
        self.past_clearing_prices = []
        self.past_ccps = []
        self.past_demands = []

    def bid(self, demand):
        my_bid = []
        ccp = self.competative_clearing_price(demand)
        for plant in self.power_plants:
            #bids competative clearing price for each of my plants
            my_bid.append([plant, ccp])
        self.record_demand_and_ccp(demand, ccp)
        return my_bid

    def record_demand_and_ccp(self, demand, ccp):
        #records ccp and demand for this hour
        self.past_ccps += [ccp]
        self.past_demands += [demand]

    def receive_update(self, update):
        #records clearing price for this hour
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
                ccp = lowest_bid
                demand_left -= lowest_bidder.capacity
                all_plants = all_plants[:lowest_bidding_index]+all_plants[lowest_bidding_index+1:]
            else:
                ccp = lowest_bid
                demand_left = 0
        return ccp

class Julia(Competative):
    #predicts clearing price based on average agressiveness of the market
    #bids all plants marginal except sometimes one at predicted cp
    def __init__(self, name = "julia"):
        super().__init__(name)
        self.past_agressions = []

    def bid(self, demand):
        my_bid = []
        ccp = self.competative_clearing_price(demand)
        predicted_cp = ccp
        if self.past_agressions:
            predicted_cp = self.predict_clearing_price(ccp)
        sorted_plants = sorted(self.power_plants, key=lambda plant: plant.price_per_kwh)
        intramarginal_plants, extramarginal_plants = [], []
        for plant in sorted_plants:
            if plant.price_per_kwh < predicted_cp:
                intramarginal_plants.append(plant)
            else:
                extramarginal_plants.append(plant)
        if len(intramarginal_plants)>2:
            #if we have enough intramarginal plants to have some stability
            #then we price one a little higher than predicted cp.
            for plant in intramarginal_plants[:-1]:
                my_bid.append([plant, plant.price_per_kwh])
            my_bid.append([intramarginal_plants[-1], predicted_cp])
            for plant in extramarginal_plants:
                my_bid.append([plant, plant.price_per_kwh])
        else:
            for plant in self.power_plants:
                #bids marginal price for each of my plants
                my_bid.append([plant, plant.price_per_kwh])
        self.record_demand_and_ccp(demand, ccp)
        return my_bid

    def receive_update(self, update):
        #records clearing price and adds an agressiveness score for this hour
        self.past_clearing_prices += [update]
        self.past_agressions += [update/(self.past_ccps[-1])]

    def predict_clearing_price(self, ccp):
        avg = lambda l: sum(l) / len(l)
        #predicts clearing price based on average of past market agressiveness
        return ccp * avg(self.past_agressions)

class Julinear(Julia):
    #the same as Julia, but predicts cp differently
    def __init__(self):
        super().__init__("julinear")

    def predict_clearing_price(self, ccp):
        #predicts cp by creating a line of best fit based on past past_agressions
        #to predict how agressive the market will be this time
        if len(self.past_agressions) > 1:
            slopes = []
            for i in range(1, len(self.past_agressions)):
                slopes += [(self.past_agressions[i]-self.past_agressions[0])/i]
            avg = lambda l: sum(l)/len(l)
            avg_slope = avg(slopes)
            predicted_agro = self.past_agressions[0] + avg_slope*len(self.past_agressions)
        else:
            predicted_agro = self.past_agressions[0]
        #predicts agressiveness with the average rate of change of
        #past agressiveness'
        predicted_cp = ccp * predicted_agro
        return predicted_cp
