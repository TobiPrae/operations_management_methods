# operations_management_methods (version == 0.8.1)

# 1 Overview

This is a package for operations management that I am currently working on. The following packages are used:
- numpy
- math
- scipy.stats
- matplotlib.pyplot

The package can be installed as follows:

`pip install -i https://test.pypi.org/simple/ operations-management-methods==version`

# 2 Details

The package currently contains 2 classes that can be imported:

**Simplex**

This class contains the simplex method. This makes it possible to solve a production planning problem with several machine bottlenecks. Please note that in this implementation not all special cases of the method are caught yet.

The following inputs are necessary:
- *unit_contribution_margins*: Uni contribution margin for each product 
- *machine_capacities*: Capacities for each given machine
- *product_time_requirement*: Time requirement for each product on each machine

The outputs are:
- *production_quantities*: Optimal order quantities for given products
- *remaining_machine_time*: Remaining capacities for given machines
- *profit*: Overall profit

Following class methods are important:
- *print_simplex()*: Print instance attributes
- *solve()*: Solve problem
- *plot_production_quantities()*: Plot optimal production quantities for each product

![demo_pq](demo_pq.png)

- *plot_capacities(): Plot initial and remaining capacities after optimization

![demo_cap](demo_cap.png)

**InventoryManagement**

With this class it is possible to determine a sq-policy, where s denotes the re-order point and q the economic order quantity. The procedure implemented here takes uncertainty into account by including an in-stock rate and the standard deviations of demand and lead times. The Class can be used either for optimal production quantities or for optimal order quantities.

The following inputs are necessary:
- *demand*: Demand for the upcoming period
- *holding_cost_per_unit*: Variable costs per product unit
- *setup_cost*: Setup cost for machine or costs per order
- *instock_rate*: The ration between theoretical assortment and actual stock level
- *past_demands*: List of past demands
- *past_leadtimes*: List of past lead times
- *period_length* (not required, default = 7): Period length in days
- *daily_working_hours* (not required, default = 10): Working hours per day

The outputs are:
- *quantity*
- *safety_stock*
- *reorder_point*
- *order_cost*
- *holding_cost*
- *total_cost*

Following class methods are important:
- *print_sq_policy()*: Print instance attributes
- *calculate_sq_policy()*: Calculate outputs
- *plot_sql_policty()*: Plot costs

![demo_sq](demo_sq.png)

# 3 Literature/Acknowledgements

Bloech, J., Bogaschewsky, R., Götze, U., & Roland, F. (2014). Einführung in die Produktion. Heidelberg: Physica-Verlag.

Package on TestPyPi: https://test.pypi.org/project/operations-management-methods/0.5/
