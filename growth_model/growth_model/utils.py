#Growth_sim.py

import math
import pandas as pd
from matplotlib import pyplot as plt
import os
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
    
    model=GompertzGrowth(ininital_density,platau_density,growth_rate)
    growth_data = create_data(model)
    greatest_growth_index = get_highest_growth_step(growth_data)
    
    basic_plotting(growth_data,greatest_growth_index)
    return growth_data
    