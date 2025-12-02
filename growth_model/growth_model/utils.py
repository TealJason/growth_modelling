#Growth_sim.py

import math
import pandas as pd
from matplotlib import pyplot as plt
import os
class GompertzGrowth:
    def __init__(self, N0, Ninf, b_max, temperature, Tmin, Tmax, c, k0=0.001, alpha=0.2):
        """
        k0: baseline death rate at Tmax
        alpha: how fast death increases with temperature
        """
        self.N0 = N0
        self.Ninf = Ninf
        self.b_max = b_max
        self.temperature = temperature
        self.Tmin = Tmin
        self.Tmax = Tmax
        self.c = c
        self.k0 = k0
        self.alpha = alpha

    def growth_rate(self):
        T = self.temperature

        # no growth below Tmin or above Tmax
        if T <= self.Tmin or T >= self.Tmax:
            return 0.0

        # Ratkowsky above-optimal extension
        mu_sqrt = self.b_max * (T - self.Tmin) * (1 - math.exp(self.c * (T - self.Tmax)))
        if mu_sqrt < 0:
            return 0.0

        return mu_sqrt ** 2  # final μ

    def death_rate(self):
        T = self.temperature
        if T <= self.Tmax:
            return 0.0

        # Arrhenius-like death scaling
        return self.k0 * math.exp(self.alpha * (T - self.Tmax))

    def evaluate(self, t):
        μ = self.growth_rate()
        k = self.death_rate()

        # CASE 1: Growth
        if μ > 0:
            return self.N0 * math.exp(math.log(self.Ninf / self.N0) *
                                      (1 - math.exp(-μ * t)))
        # CASE 2: Death
        if k > 0:
            N_min = 1e-6
            return self.N0 * math.exp(-math.log(self.N0 / N_min) *
                                      math.exp(-k * t))

        # CASE 3: No change
        return self.N0
    
def create_data(model):
    time_steps = []
    densitys = []
    
    for t in range(0, 30):
        time_steps.append(t)
        densitys.append(model.evaluate(t))

    growth_data = pd.DataFrame({
        "time step": time_steps,
        "density": densitys
    })

    return growth_data

def get_highest_growth_step(growth_data):
    #Go through the df checking the change between each step, return the step with the greatest change
    greatest_growth = 0
    greatest_growth_index = 0
    
    for i in range(len(growth_data) - 1):
        current_change = growth_data["density"][i + 1] - growth_data["density"][i]
        if current_change > greatest_growth:
            greatest_growth = current_change
            greatest_growth_index = i
    return greatest_growth_index

def basic_plotting(growth_data, greatest_growth_index):
    # Save path
    image_path = os.path.join(os.path.dirname(__file__), "../static/images", "scatter_growth.png")
    
    plt.figure(figsize=(6, 4))
    plt.plot(growth_data["time step"], growth_data["density"], 
             marker='o', color='tab:blue', linestyle='-', linewidth=2, markersize=6, label="Growth")
    
    # Add vertical dotted line at the point of greatest change
    plt.axvline(
        x=growth_data["time step"][greatest_growth_index], 
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
    
    model=GompertzGrowth(ininital_density,platau_density,growth_rate,temperature=90,Tmin=5,Tmax=45,c=0.01)
    growth_data = create_data(model)
    greatest_growth_index = get_highest_growth_step(growth_data)
    
    basic_plotting(growth_data,greatest_growth_index)
    return growth_data
    