class RechargeEnergyMixin:
    MAX_ENERGY: int = 100


    def recharge_energy(self, amount: int) -> None:
        self.energy += amount
        if self.energy > self.MAX_ENERGY:
            self.energy = self.MAX_ENERGY

        self.save()