# operations_management_methods (version == 0.5)

# 1 Overview

This is a package for operations management that I am currently working on. The following packages are used:
- numpy
- math
- scipy.stats
- matplotlib.pyplot

The package can be installed as follows:

`pip install -i https://test.pypi.org/simple/ operations-management-methods==version`

# 2 Content

The package currently contains 2 classes that can be imported:

**Simplex:**

This class contains the simplex method. This makes it possible to solve a production planning problem with several machine bottlenecks.

The following inputs are necessary:
- unit_contribution_margins: Uni contribution margin for each product 
- machine_capacities: Capacities for each given machine
- product_time_requirement: Time requirement for each product on each machine

The outputs are:
- production_quantities: Optimal order quantities for given products
- remaining_machine_time: Remaining capacities for given machines
- profit: Overall profit


**InventoryManagement:**



# 3 Literature/Acknowledgements

Bloech, J., Bogaschewsky, R., Götze, U., & Roland, F. (2001). Einführung in die Produktion (pp. 176-178). Heidelberg: Physica-Verlag.
