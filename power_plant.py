from bank import Bank

# Class that represents a power plant.
class PowerPlant:
    def __init__(self, price, capacity, owner=None):
        self.price_per_kwh = price
        self.capacity = capacity
        self.remaining_power = capacity
        self.owner = owner

    # Updates this power plants owner.
    def set_owner(self, name):
        self.owner = name

    def generate(self, amount):
        # Verfiy the transaction.
        if amount > self.remaining_power:
            print("[error] only {}kwh of power remaining. queried for {}kwh"
                  .format(self.remaining_power, amount))
            return 0
        if amount < 0:
            print("[error] can't generate a negative amount of power")

        # Charge the owner for the generation.
        cost = self.price_per_kwh * amount
        success = Bank().withdraw(self.owner, cost)
        if not success:
           print("[error] could not withdraw money for power generation")
           return 0

        # Generate the power.
        self.remaining_power -= amount

        # Return the generated energy.
        return amount

    # Called whenever a new game loop begins.
    def tick(self):
        self.remaining_power = self.capacity

big_coal_plants = [
    PowerPlant(price=36.5, capacity=1900),
    PowerPlant(73.72, 250),
    PowerPlant(40.5, 300),
    PowerPlant(66.5, 150),
    PowerPlant(41.94, 350),
    PowerPlant(41.94, 950)
]

big_gass_plants = [
    PowerPlant(44.83, 400),
    PowerPlant(41.22, 650),
    PowerPlant(52.5, 550),
    PowerPlant(65.5, 150),
    PowerPlant(41.67, 950),
    PowerPlant(90.06, 200),
    PowerPlant(43.83, 700)
]

bay_views_plants = [
    PowerPlant(38.75, 335),
    PowerPlant(36.61, 665),
    PowerPlant(32.56, 750),
    PowerPlant(32.56, 750),
    PowerPlant(61.17, 150)
]

beachfront_plants = [
    PowerPlant(42.39, 650),
    PowerPlant(42.67, 850),
    PowerPlant(62.89, 150),
    PowerPlant(75.61, 300),
    PowerPlant(39.06, 300),
    PowerPlant(52.06, 150),
    PowerPlant(38.06, 700),
    PowerPlant(38.06, 700)
]

east_bay_plants = [
    PowerPlant(40.94, 650),
    PowerPlant(36.61, 650),
    PowerPlant(59.72, 700),
    PowerPlant(58.28, 150),
    PowerPlant(39.5, 700),
    PowerPlant(69.83, 150),
]

old_timers_plants = [
    PowerPlant(0, 1000),
    PowerPlant(34.5, 750),
    PowerPlant(34.5, 750),
    PowerPlant(49.61, 150),
    PowerPlant(53.94, 100),
]

fossil_light_plants = [
    PowerPlant(47.44, 150),
    PowerPlant(.5, 800),
    PowerPlant(49.17, 150),
    PowerPlant(75.89, 250),
    PowerPlant(11.5, 1000),
]

plant_groups = [big_coal_plants, big_gass_plants, bay_views_plants, beachfront_plants, east_bay_plants, old_timers_plants, fossil_light_plants]
