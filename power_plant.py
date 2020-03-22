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
