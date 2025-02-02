import numpy as np
import trimesh
from shapes import trimesh_L, trimesh_C, trimesh_ellipse

choice = np.random.randint(1, 4)
if choice == 1:
    trimesh_L.generate_hook()
elif choice == 2:
    trimesh_C.generate_hook()
elif choice == 3:
    trimesh_ellipse.generate_hook()

