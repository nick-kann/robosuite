import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load XML file
tree = ET.parse('scene.xml')
root = tree.getroot()

# Extract vertices
vertices = []
for vertex in root.findall('.//Vertex'):
    x = float(vertex.get('x'))
    y = float(vertex.get('y'))
    z = float(vertex.get('z'))
    vertices.append((x, y, z))

# Convert to NumPy array
vertices = np.array(vertices)

# Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], c='blue', marker='o')

# Labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Mesh Visualization')

plt.show()
