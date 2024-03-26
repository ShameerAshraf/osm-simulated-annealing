
# osm-simulated-annealing
*Salesmen don't even travel like that anymore*

## In short
The goal of this project is to plot and visualize the progress of the simulated annealing algorithm in arriving at a good enough solution for the travelling salesman problem.
For path-finding between a source and destination node, the code mostly relies on algorithms from the NetworkX python library.
For a number of points in the graph, a custom simulated annealing and plotting is implemented.

## Environment
requirements_pip.txt or requirements_conda.txt
Major libraries used: pyrosm, osmnx, NetworkX

## Code
The files contain a lot of commented out code left in for plotting and debugging, in case someone wants to expand on the code or verify the results.

[main.py](main.py) has the POINTS_IN_ROUTE constant at the top to adjust number of random points on the graph used for the problem. It also has [TARGET_FILE](main.py#L42) to define the path to the **openstreepmap dataset in pbf format**.

[routes.py](routes.py) has parameters to tune for the simulated annealing algorithm itself, which also requires adjusting the [loop iteration values](main.py#L139) in main.py


## Demo

![Iteration 0](demo-resources/labels1.png?raw=true "Iteration 0")


![Iteration 60](demo-resources/labels2.png?raw=true "Iteration 60")


![Iteration 200](demo-resources/labels3.png?raw=true "Iteration 200")

#### Bookmarks
[pyrosm reference](https://pyrosm.readthedocs.io/en/latest/reference.html)
[osmnx reference](https://osmnx.readthedocs.io/en/stable/getting-started.html)
[NetworkX shortest path algorithm](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.shortest_path.html#networkx.algorithms.shortest_paths.generic.shortest_path)
[travel time calculation based on speed limit and distance](https://access-ucl.readthedocs.io/en/latest/notebooks/spatial_network_analysis.html)
[pandas GeoDataFrame reference](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.html)