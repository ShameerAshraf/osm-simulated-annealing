import pyrosm
import os
import matplotlib.pyplot as plt

dir_path = os.path.dirname(os.path.realpath(__file__))
TARGET_FILE = "micro-Toronto.osm.pbf"

print(os.path.join(dir_path, TARGET_FILE))


# Get filepath to test PBF dataset
#fp = pyrosm.get_data(TARGET_FILE)
#print("Filepath to test data:", fp)

# Initialize the OSM object 
osm = pyrosm.OSM(TARGET_FILE)

# See the type
print("Type of 'osm' instance: ", type(osm))

drive_net = osm.get_network(network_type="driving")
drive_net.plot()
plt.show()