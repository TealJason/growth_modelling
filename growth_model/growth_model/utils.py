#Growth_sim.py

import math
import pandas as pd

class GompertzGrowth:
    def __init__(self, initial_density, plateau_density, growth_rate):
        self.N0 = initial_density
        self.Ninf = plateau_density
        self.b = growth_rate

    def evaluate(self, t):
        # Gompertz model:
        # N(t) = N0 * exp( ln(Ninf/N0) * (1 - exp(-b t)) )
        return self.N0 * math.exp(math.log(self.Ninf / self.N0) * (1 - math.exp(-self.b * t)))


def create_data(model):
    time_steps = []
    growth_levels = []
    
    for t in range(0, 25):
        time_steps.append(t)
        growth_levels.append(model.evaluate(t))

    growth_data = pd.DataFrame({
        "time_step": time_steps,
        "growth_level": growth_levels
    })

    return growth_data

def run_model(ininital_density,platau_density,growth_rate):
    ininital_density= int(ininital_density,)
    platau_density = int(platau_density)
    growth_rate = int(growth_rate)
    
    model=GompertzGrowth(ininital_density,platau_density,growth_rate)
    growth_data = create_data(model)
    print(growth_data)
    return growth_data
    