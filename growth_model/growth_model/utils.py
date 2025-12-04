#Growth_sim.py

import math
import pandas as pd
from matplotlib import pyplot as plt
import os
class GompertzGrowth:
    def __init__(self, N0, Ninf, μopt, temperature, Tmin, Tmax,Topt):
        """
        k0: baseline death rate at Tmax
        alpha: how fast death increases with temperature
        """
        self.N0 = N0 # Initial population density
        self.Ninf = Ninf # Maximum population density
        self.temperature = temperature # Current temperature
        self.Tmin = Tmin # Minimum temperature for growth
        self.Tmax = Tmax #  Maximum temperature for growth
        self.Topt = Topt
        self.μopt = μopt

        def temperature_dependent_growth_rate(self):
        #µ(𝑇)=µ𝑜𝑝𝑡·(𝑇−𝑇𝑚𝑎𝑥)·(𝑇−𝑇𝑚𝑖𝑛)2(𝑇𝑜𝑝𝑡−𝑇𝑚𝑖𝑛)·[(𝑇𝑜𝑝𝑡−𝑇𝑚𝑖𝑛)·(𝑇−𝑇𝑜𝑝𝑡)−(𝑇𝑜𝑝𝑡−𝑇𝑚𝑎𝑥)·(𝑇𝑜𝑝𝑡+𝑇𝑚𝑖𝑛−2·𝑇)]  This is this the new equation I'm trying to implment Lobry and Rosso 1991 it models bacterial growth while accounting for enzyme denatureation, the CTMI model
       
        # µ chemical potenial of substate at temperature T
        # µopt optimal chemical potential of substrate
        # Topt optimal temperature for growth
        # Tmin minimum temperature for growth
        # Tmax maximum temperature for growth
        # T current temperature
        # For now we will use a simplified version that reduces growth rate linearly beyond Tmax
            denom = (self.temperature - self.Topt)**2
            delim = (self.Topt - self.Tmin) * ((self.Topt - self.Tmin)*(self.temperature - self.Topt) - (self.Topt - self.Tmax)*(self.Topt + self.Tmin - 2*self.temperature))
            μ = self.μopt *  (denom/ delim)
            return  μ

    def evaluate(self, t):
        μ = self.temperature_dependent_growth_rate()

        # CASE 1: Growth
        if μ > 0:
            density_at_step = self.N0 * math.exp(math.log(self.Ninf / self.N0) * (1 - math.exp(-μ * t)))
            return 
        # CASE 2: Death
        else:
            N_min = 1e-6
            density_at_step = self.N0 * math.exp(-math.log(self.N0 / N_min) * math.exp(-μ * t))
            return density_at_step

         
    
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

def get_max_min_optimal_temperature(species):
    species_temperatures = {
        "E.coli": (5, 45, 37),
        "S.aureus": (10, 50, 37),
        "L.monocytogenes": (0, 45, 30),
        "P.aeruginosa": (4, 42, 37),
        "B.subtilis": (10, 50, 37),
        "ecoli": (5, 45, 37),
    }
    return species_temperatures.get(species, (5, 45, 37))

def run_model(ininital_density,platau_density,growth_rate,temperature,species):
    ininital_density= float(ininital_density,)
    platau_density = float(platau_density)
    growth_rate = float(growth_rate)
    
    tmax, tmin, topt = get_max_min_optimal_temperature(species)
    model=GompertzGrowth(ininital_density,platau_density,growth_rate,temperature=37,Tmin=5,Tmax=45,c=0.01)
    growth_data = create_data(model)
    
    
    greatest_growth_index = get_highest_growth_step(growth_data)
    
    basic_plotting(growth_data,greatest_growth_index)
    return growth_data
    