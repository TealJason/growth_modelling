#Growth_sim.py

import math
import pandas as pd
from matplotlib import pyplot as plt
import os
from pprint import pprint
class GompertzGrowth:
    def __init__(self, N0, Ninf, μopt, temperature, Tmin, Tmax,Topt):
        """
        k0: baseline death rate at Tmax
        alpha: how fast death increases with temperature
        """
        self.N0 = N0 # Initial population density
        self.Ninf = Ninf # Maximum population density
        self.temperature = temperature + 273.15 # Current temperature in kelvin
        self.Tmin = Tmin + 273.15 # Minimum temperature for growth in kelvin
        self.Tmax = Tmax + 273.15 # Maximum temperature for growth in kelvin
        self.Topt = Topt + 273.15 # Optimal temperature for growth in kelvin
        self.μopt = μopt # Optimal growth rate

    def temperature_dependent_growth_rate(self):
        #µ(𝑇)=µ𝑜𝑝𝑡·(𝑇−𝑇𝑚𝑎𝑥)·(𝑇−𝑇𝑚𝑖𝑛)2(𝑇𝑜𝑝𝑡−𝑇𝑚𝑖𝑛)·[(𝑇𝑜𝑝𝑡−𝑇𝑚𝑖𝑛)·(𝑇−𝑇𝑜𝑝𝑡)−(𝑇𝑜𝑝𝑡−𝑇𝑚𝑎𝑥)·(𝑇𝑜𝑝𝑡+𝑇𝑚𝑖𝑛−2·𝑇)]  This is this the new equation I'm trying to implment Lobry and Rosso 1991 it will take bacterial growth under optimal conditions and modify it based on optimal maximal and minimal temperatures, the CTMI model
       
        # µ 'chemical potenial of substate at temperature T'
        # µopt 'optimal chemical potential of substrate'
        # Topt optimal temperature for growth
        # Tmin minimum temperature for growth
        # Tmax maximum temperature for growth
        # T current temperature
        # For now we will use a simplified version that reduces growth rate linearly beyond Tmax and clamps to zero below Tmin
        
        if self.temperature < self.Tmin:
            print("No growth below minimum temperature")
            return 0  # No growth below minimum temperature
        elif self.temperature > self.Tmax:
            #μdeath​(T)=−k⋅(T−Tmax​)
            print("temperature above maximum, applying death rate")
            k = 0.1 * self.μopt  # Death rate constant, should adjust in species info and define better
            μ_death = k * (self.temperature - self.Tmax)
            return -μ_death   # Negative growth rate indicates death
        else: #normal growth rate  modification
            print("temperature within growth range, applying growth rate")
            numerator = (self.temperature - self.Tmax) * (self.temperature - self.Tmin)**2
            denomenator = (self.Topt - self.Tmin) * ((self.Topt - self.Tmin)*(self.temperature - self.Topt) - (self.Topt - self.Tmax)*(self.Topt + self.Tmin - 2*self.temperature))
            μ = self.μopt *  (numerator/ denomenator)
            return  μ #The current growth rate at the given temperature 

    def evaluate_at_time_step(self, t, μ):
        
        # CASE 1: Growth
        if μ > 0:
            density_at_step = self.N0 * math.exp(math.log(self.Ninf / self.N0) * (1 - math.exp(-μ * t)))
            return density_at_step
        # CASE 2: Death
        else:
            N_min = 1e-6
            density_at_step = self.N0 * math.exp(-math.log(self.N0 / N_min) * math.exp(-μ * t))
            return density_at_step

def run_simulation(model,number_of_time_steps):
    time_steps = []
    densitys = []
    μ  = model.temperature_dependent_growth_rate()
    
    print(f"Current growth rate μ: {μ}")
    for t in range(0, number_of_time_steps): #Evaluate for 30 time steps
        time_steps.append(t) # Make a list of the current time step
        densitys.append(model.evaluate_at_time_step(t, μ)) # make a list of the growth density at the current time step

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
    }
    species_stats = species_temperatures.get(species)
    return species_stats

def run_model(ininital_density,platau_density,growth_rate,temperature,species,number_of_time_steps):
    ininital_density= int(ininital_density,)
    platau_density = int(platau_density)
    growth_rate = float(growth_rate)
    temperature = float(temperature)
    number_of_time_steps = int(number_of_time_steps)
    
    tmin, tmax, topt = get_max_min_optimal_temperature(species)
    model=GompertzGrowth(ininital_density,platau_density,growth_rate,temperature,tmin,tmax,topt)
    growth_data = run_simulation(model,number_of_time_steps)
    greatest_growth_index = get_highest_growth_step(growth_data)
    basic_plotting(growth_data,greatest_growth_index)
    return growth_data
    