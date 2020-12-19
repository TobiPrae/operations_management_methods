import numpy as np


class Simplex:

    def __init__(self, unit_contribution_margins, machine_capacities, product_time_requirement, production_quantities=[], remaining_machine_time=[], profit=[]):

        self.unit_contribution_margins = unit_contribution_margins
        self.machine_capacities = machine_capacities
        self.product_time_requirement = product_time_requirement
        self.production_quantities = production_quantities
        self.remaining_machine_time = remaining_machine_time
        self.profit = profit

    def print_simplex(self):
        """
        Prints simplex attributes.

        Args: None

        Returns: Nothing
        """
        print(F"Unit contribution margins: {self.unit_contribution_margins}")
        print(F"Machine capacities: {self.machine_capacities}")
        print(
            F"Time requirements per product and machine: {self.product_time_requirement}")
        print(F"Optimal production quantities: {self.production_quantities}")
        print(F"Remaining machine times: {self.remaining_machine_time}")
        print(F"Profit: {self.profit}")

    def solve(self):
        """
        Description: Applies simplex algorithm to solve a linear optimization problem
        with multiple capacity constraints. Calculates optimal order quantities, remaining machine time and profit.

        Args: None

        Returns: Nothing

        """
        
        unit_contribution_margins = self.unit_contribution_margins
        machine_capacities = self.machine_capacities
        product_time_requirement = self.product_time_requirement
        
        n_constraints = len(machine_capacities)
        n_variables = len(unit_contribution_margins)

        # Checking for negative values and summing them up
        mc_neg = sum(element < 0 for element in machine_capacities)
        ucm_neg = sum(element < 0 for element in unit_contribution_margins)

        ptr_list = []

        for list in product_time_requirement:
            for element in list:
                if(element < 0):
                    ptr_list.append(1)
                else:
                    ptr_list.append(0)

        ptr_neg = sum(element < 0 for element in unit_contribution_margins)

        # Check for negative input values
        if(sum([mc_neg, ucm_neg, ptr_neg]) > 0):
            raise ValueError(F"Please use only non-negative values as input.")

        # Check if machine dimensions match
        elif(n_constraints != len(product_time_requirement)):
            raise ValueError(
                F"Machine dimensions dont match (machine_capacities {n_constraints} vs. product_time_requiremnts per machine {len(product_time_requirement)}")

        # Check if product dimensions match
        elif(n_variables != len(product_time_requirement[0])):
            raise ValueError(
                F"Variable dimensions dont match (unit_contribution_margins {n_variables} vs. product_time_requiremnts per product {len(product_time_requirement[0])}")

        else:
            # Create empty table with the needed dimensions
            simplex_table = np.zeros(
                (n_constraints+1, n_variables+n_constraints+1))

            # initialize k_i, g_i and k_i-g_i
            for j in range(0, n_variables):
                simplex_table[-1, j] = unit_contribution_margins[j]

            for i in range(0, n_constraints):

                # Fills y1 to y_n_constraints
                simplex_table[i, n_variables+i] = 1

                simplex_table[i, -1] = machine_capacities[i]

                for j in range(0, n_variables):
                    simplex_table[i, j] = product_time_requirement[i][j]

        optimal_solution = False

        # Creates dummy variable that is used to break infinite loop
        break_condition = 0

        # Calls the function recursion until optimal solution is reached
        while(optimal_solution == False):

            if(break_condition < 1000):
                simplex_table, optimal_solution = self.recursion(
                    simplex_table, optimal_solution)

            # Raise error if algorithm took too long
            else:
                raise RecursionError(
                    "The algorithm took too long to terminate.")

            break_condition = break_condition + 1

        # Creates empty list for optimal product quantities
        product_quantities = np.zeros(len(unit_contribution_margins))

        # Fill list with optimal product quantities
        for j in range(0, len(unit_contribution_margins)):
            if((1 in simplex_table[:, j]) & (sum(simplex_table[:, j]) == 1)):
                index = simplex_table[:, j].tolist().index(1)
                product_quantities[j] = simplex_table[index, -1]
            else:
                continue

        # Creates empty list for remaining machine time
        remaining_machine_time = np.zeros(len(machine_capacities))

        # Fill list with remaining machine time
        for k in range(len(unit_contribution_margins), len(unit_contribution_margins) + len(machine_capacities)):
            c_index = k - len(unit_contribution_margins)
            if((1 in simplex_table[:, k]) & (sum(simplex_table[:, k]) == 1)):
                remaining_machine_time[c_index] = simplex_table[c_index, -1]
            else:
                continue

        # Write class variables
        self.production_quantities = product_quantities
        self.remaining_machine_time = remaining_machine_time
        self.profit = -1*simplex_table[-1, -1]

    def recursion(self, simplex_table, optimal_solution):
        """
        Prints simplex attributes.

        Args: 
        - simplex_table: Current state of simplex_table
        - optimal_solution: Current state of optimal_solution


        Returns:
        - Updated simplex_table 
        - Updated optimal_solution
        """

        # Get column index for column with the highest value in the bottom row
        bottom_row = simplex_table[-1, ].tolist()
        col_index = bottom_row.index(max(bottom_row))

        # Create bottleneck list and fill values
        bottleneck = []

        for i in range(0, simplex_table.shape[0]):
            if(simplex_table[i, col_index] != 0):
                value = simplex_table[i, -1] / simplex_table[i, col_index]
                if(value < 1):
                    value = value*-1
                bottleneck.append(value)

            else:
                bottleneck.append(None)

        # Get row index for lowest non negative value in bottlenecks
        row_index = bottleneck.index(min(bottleneck[:-1]))

        # Get pivot element and divide pivot row through pivot_element to get pivot_element = 1
        pivot_element = simplex_table[row_index, col_index]
        simplex_table[row_index, ] = simplex_table[row_index, ] / pivot_element

        # Get pivot row
        pivot_row = simplex_table[row_index, ]

        # Iterate through rows and substract pivot row and multiplikator to get 0
        for i in range(0, simplex_table.shape[0]):
            if(i == row_index):
                continue
            else:
                multiplicator = simplex_table[i, col_index] / \
                    simplex_table[row_index, col_index]

                simplex_table[i, ] = simplex_table[i, ] - \
                    multiplicator * pivot_row

        # Count number of positives in bottom row, if > 0 there is not a optimal solution reached yet
        n_positives = sum(element > 0 for element in simplex_table[-1, ])

        if(n_positives > 0):
            optimal_solution = False
        else:
            optimal_solution = True

        return simplex_table, optimal_solution
