import numpy as np
import math as mt
from scipy.stats import norm
import matplotlib.pyplot as plt

class InventoryManagement:
    
    def __init__(self, past_demands, past_leadtimes, demand, holding_cost_per_unit, setup_cost, instock_rate, period_length = 7, daily_working_hours = 10):
        
        self.demand = demand
        self.holding_cost_per_unit = holding_cost_per_unit
        self.setup_cost = setup_cost
        self.instock_rate = instock_rate
        self.period_length = period_length
        self.daily_working_hours = daily_working_hours
        self.past_demands = past_demands
        self.past_leadtimes = past_leadtimes
        self.std_demand = None
        self.avg_leadtime_hours = None
        self.std_leadtime_hours = None
        self.quantity = None
        self.safety_stock = None
        self.reorder_point = None
        self.order_cost = None
        self.holding_cost = None
        self.total_cost = None
        self.calculate_leadtimes()
        self.calculate_std_demand()
    
    
    
    def print_sq_policy(self):
        """
        Prints InventoryManagement attributes.
        
        Args: None
        
        Returns: Nothing
        """
        print(F"demand: {self.demand}")
        print(F"std_demand: {self.std_demand}")
        print(F"past_demands: {self.past_demands}")
        print(F"past_leadtimes: {self.past_leadtimes}")
        print(F"avg_leadtime_hours: {self.avg_leadtime_hours}")
        print(F"std_leadtime_hours: {self.std_leadtime_hours}")
        print(F"holding_cost_per_unit: {self.holding_cost_per_unit}")
        print(F"setup_cost: {self.setup_cost}")
        print(F"instock_rate: {self.instock_rate}")
        print(F"period_length: {self.period_length}")
        print(F"daily_working_hours: {self.daily_working_hours}")
        print(F"quantity: {self.quantity}")
        print(F"safety_stock: {self.safety_stock}")
        print(F"reorder_point: {self.reorder_point}")
        print(F"order_cost: {self.order_cost}")
        print(F"holding_cost: {self.holding_cost}")
        print(F"total_cost: {self.total_cost}")
  
        
        
    
    def calculate_sq_policy(self):
        """
        Calculates optimal reorder policy (order quanity, reorder point, safety stock and costs) for give instock rate.

        Args: None

        Returns: Nothing

        """
        if((self.instock_rate <= 0) | (self.instock_rate >=1)):
            raise ValueError(F"instock rate must be between 0 and 1 (input was {self.instock_rate})")
        
        # Calculates avg_leadtime and std_leadtime for given period working hours
        avg_leadtime = self.avg_leadtime_hours/(self.period_length*self.daily_working_hours)
        std_leadtime = self.std_leadtime_hours/(self.period_length*self.daily_working_hours)
        
        # Calculates avg_leadtime and std_leadtime during leadtime
        avg_demand_during_leadtime = avg_leadtime * self.demand
        std_demand_during_leadtime = mt.sqrt(avg_leadtime*(self.std_demand**2)+(self.demand**2)*(std_leadtime**2))
        
        # Applies generic optimal order quanity formula
        self.quantity = round((mt.sqrt((2*self.demand*self.setup_cost)/self.holding_cost_per_unit)), 0)
        
        # Calculates safety stock
        z = norm.ppf(self.instock_rate)
        self.safety_stock = round((z * std_demand_during_leadtime), 2)
        
        # Calculates reorder point
        self.reorder_point = round((avg_demand_during_leadtime + self.safety_stock), 2)
        
        # Calculates order cost
        self.order_cost = self.calculate_order_cost(self.quantity)
        
        # Calculates holding cost
        self.holding_cost = self.calculate_holding_cost(self.quantity)
        
        # Calculates total cost
        self.total_cost = round((self.holding_cost + self.order_cost), 2)
     
    
    
    def calculate_order_cost(self, q):
        """
        Calculates order cost

        Args: None

        Returns: order_cost
        """
        return self.demand/q*self.setup_cost
        
        
        
    def calculate_holding_cost(self, q):
        """
        Calculates holding cost

        Args: None

        Returns: holding_cost
        """
        return (q/2+self.safety_stock)*self.holding_cost_per_unit
    
    
    
    def calculate_leadtimes(self, sample=True):
        """
        Calculates standard deviation and average for leadtimes based on past leadtimes

        Args: None

        Returns: Nothing
        """
        
        n = len(self.past_leadtimes)
        
        self.avg_leadtime_hours = sum(self.past_leadtimes)/n
        
        # Sample
        if(sample):
            self.std_leadtime_hours = mt.sqrt(sum([(x-self.avg_leadtime_hours)**2 for x in self.past_leadtimes]) / (n-1))
        # Population
        else:
            self.std_leadtime_hours = mt.sqrt(sum([(x-self.avg_leadtime_hours)**2 for x in self.past_leadtimes]) / n)
        
        
        
    def calculate_std_demand(self, sample=True):
        """
        Calculates standard deviation for demand based on past demands

        Args: None

        Returns: Nothing
        """
        
        n = len(self.past_demands)
        
        mean = sum(self.past_demands)/n
        
        # Sample
        if(sample):
            self.std_demand = mt.sqrt(sum([(x-mean)**2 for x in self.past_demands]) / (n-1))
        # Population
        else:
            self.std_demand = mt.sqrt(sum([(x-mean)**2 for x in self.past_demands]) / n)
        
        
    def plot_sql_policty(self):
        """
        Plot cost development for given inventory model.

        Args: None

        Returns: Nothing
        """
        bottom_end = int(self.quantity/2)
        top_end = int(self.quantity*2)
        possible_quantities = list(range(bottom_end, top_end))
        
        order_costs = []
        holding_costs = []
        total_costs = []
        
        for q in possible_quantities:
            oc = self.calculate_order_cost(q)
            order_costs.append(oc)
            hc = self.calculate_holding_cost(q)
            holding_costs.append(hc)
            tc = oc + hc
            total_costs.append(tc)
            
        fig, ax = plt.subplots(figsize=(10, 6))
            
        ax.plot(possible_quantities, order_costs, label="Order costs", color="red")
        ax.plot(possible_quantities, holding_costs, label="Holding costs", color="orange")
        ax.plot(possible_quantities, total_costs, label="Total costs", color="green")
        ax.grid(color='lightgrey', linestyle='-', linewidth=1)
        ax.set_facecolor("white")
        ax.legend(fontsize=14, loc=4)
        plt.title("Cost Development for Inventory Model", fontsize=16) 
        plt.xlabel("Quantity", fontsize=14)
        plt.ylabel("Costs", fontsize=14)
        plt.show()
        
        

        
    
