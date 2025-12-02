#Growth_sim.py

import math
import pandas as pd
from matplotlib import pyplot as plt
import os
class GompertzGrowth:
    def __init__(self, N0, Ninf, b_max, temperature, Tmin, Tmax, c):
        """
        N0: initial density
        Ninf: maximum density
        b_max: max growth rate at optimal temperature
        temperature: current temperature
        Tmin: minimum growth temperature
        Tmax: maximum growth temperature
        c: 'an additional parameter to enable the model to fit the data for temperatures above the optimal temperature' #thanks ratowsky nice paper 
        """
        self.N0 = N0
        self.Ninf = Ninf
        self.b_max = b_max
        self.temperature = temperature
        self.Tmin = Tmin
        self.Tmax = Tmax
        self.c = c
        
    #I need to figure out how this adjustmen in the growth is actually working
    def adjusted_growth_rate(self):
        T = self.temperature

        if T <= self.Tmin or T >= self.Tmax:
            return 0.0  # no growth

        # Ratkowsky with above-optimum tail
        mu_sqrt = self.b_max * (T - self.Tmin) * (1 - math.exp(self.c * (T - self.Tmax)))
        
        if mu_sqrt < 0:
            return 0.0
        
        return mu_sqrt ** 2

    def evaluate(self, t):
        b_adj = self.adjusted_growth_rate()

        if b_adj >= 0:
            # Standard Gompertz growth
            return self.N0 * math.exp(math.log(self.Ninf / self.N0) * (1 - math.exp(-b_adj * t)))
        else:
            # Death-phase Gompertz
            k = -b_adj
            N_min = 1e-6
            return self.N0 * math.exp(-math.log(self.N0 / N_min) * math.exp(-k * t))


def create_data(model):
    time_steps = []
    growth_levels = []
    
    for t in range(0, 50):
        time_steps.append(t)
        growth_levels.append(model.evaluate(t))

    growth_data = pd.DataFrame({
        "time_step": time_steps,
        "growth_level": growth_levels
    })

    return growth_data

def get_highest_growth_step(growth_data):
    #Go through the df checking the change between each step, return the step with the greatest change
    greatest_growth = 0
    greatest_growth_index = 0
    
    for i in range(len(growth_data) - 1):
        current_change = growth_data["growth_level"][i + 1] - growth_data["growth_level"][i]
        if current_change > greatest_growth:
            greatest_growth = current_change
            greatest_growth_index = i
    return greatest_growth_index

def basic_plotting(growth_data, greatest_growth_index):
    # Save path
    image_path = os.path.join(os.path.dirname(__file__), "../static/images", "scatter_growth.png")
    
    plt.figure(figsize=(6, 4))
    plt.plot(growth_data["time_step"], growth_data["growth_level"], 
             marker='o', color='tab:blue', linestyle='-', linewidth=2, markersize=6, label="Growth")
    
    # Add vertical dotted line at the point of greatest change
    plt.axvline(
        x=growth_data["time_step"][greatest_growth_index], 
        color='red', linestyle='--', linewidth=2, label='Max Growth Change'
    )
    
    plt.xlabel("Time Step", fontsize=12)
    plt.ylabel("Growth Level", fontsize=12)
    plt.title("Bacterial Growth over Time (Gompertz Model)", fontsize=14)
    
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(image_path)
    plt.close()
    
def run_model(ininital_density,platau_density,growth_rate):
    ininital_density= float(ininital_density,)
    platau_density = float(platau_density)
    growth_rate = float(growth_rate)
    
    model=GompertzGrowth(ininital_density,platau_density,growth_rate,temperature=37,Tmin=5,Tmax=45,c=0.01)
    growth_data = create_data(model)
    greatest_growth_index = get_highest_growth_step(growth_data)
    
    basic_plotting(growth_data,greatest_growth_index)
    return growth_data
    