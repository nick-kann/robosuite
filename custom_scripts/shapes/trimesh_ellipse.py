import trimesh
import numpy as np
from shapely.geometry import Polygon
import xml.etree.ElementTree as ET
def scene_to_xml(scene, filename="hook.xml"):
    root = ET.Element("Scene")

    for geometry in scene.geometry.values():
        mesh_element = ET.SubElement(root, "Mesh")

        # Store vertices
        vertices_element = ET.SubElement(mesh_element, "Vertices")
        for v in geometry.vertices:
            ET.SubElement(vertices_element, "Vertex", x=str(v[0]), y=str(v[1]), z=str(v[2]))

        # Store faces
        faces_element = ET.SubElement(mesh_element, "Faces")
        for f in geometry.faces:
            ET.SubElement(faces_element, "Face", v1=str(f[0]), v2=str(f[1]), v3=str(f[2]))

    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"Ellipse hook saved to {filename}")


# major = 0.44010770383677394
# minor = 0.25724638603775096
# height = 0.06454600645177404
# cylinder_height = 1.5996086917714047
# hook_angle = -34.1736038857976
def generate_hook():
    # edit these variables
    major = np.random.uniform(0.2, 1)
    minor = np.random.uniform(0.2, 1)
    height = np.random.uniform(0.03, 0.1)
    cylinder_height = np.random.uniform(0.2, 2)
    hook_angle = np.random.uniform(-40, -30)
    # --------------------
    cylinder_radius = 0.06

    if major < minor:
        major, minor = minor, major

    print(f"major = {major}")
    print(f"minor = {minor}")
    print(f"height = {height}")
    print(f"cylinder_height = {cylinder_height}")
    print(f"hook_angle = {hook_angle}")


    def make_ellipse(a, b): # major, minor, height
        t = np.linspace(0, 2 * np.pi, 100)
        x = a * np.cos(t)
        y = b * np.sin(t)

        ellipse_points = list(zip(x, y))

        ellipse_polygon = Polygon(ellipse_points)
        return ellipse_polygon

    ellipse = trimesh.creation.extrude_polygon(make_ellipse(major, minor), height=height, engine="triangle")
    red_ellipse = trimesh.creation.extrude_polygon(make_ellipse(major * 0.7, minor*0.8), height=height, engine="triangle")
    red_ellipse.visual.face_colors = [255, 0, 0, 255]

    red_shift = np.array([[1, 0, 0, 0],
                          [0, 1, 0, minor*0.8/3],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])

    red_ellipse.apply_transform(red_shift)

    hook = ellipse.difference(red_ellipse)

    t_angle = np.radians(hook_angle)
    t_axis = np.array([0, 0, 1])

    rotation_matrix = trimesh.transformations.rotation_matrix(t_angle, t_axis)

    hook.apply_transform(rotation_matrix)

    t_angle = np.radians(90)
    t_axis = np.array([0, 1, 0])

    rotation_matrix = trimesh.transformations.rotation_matrix(t_angle, t_axis)

    hook.apply_transform(rotation_matrix)

    def dist_to_edge(a, b, angle):
        numerator = (a**2) * (b**2)
        denominator = (b**2) * (np.cos(np.radians(angle)) ** 2) + (a**2) * (np.sin(np.radians(angle)) ** 2)
        return np.sqrt(numerator/denominator)

    hook_shift = np.array([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 1, cylinder_height + dist_to_edge(major, minor, hook_angle)],
                          [0, 0, 0, 1]])

    hook.apply_transform(hook_shift)

    axis = trimesh.creation.axis(origin_size=0.1, transform=np.eye(4))


    cylinder = trimesh.creation.cylinder(radius=cylinder_radius, height=cylinder_height)

    cylinder_transform = np.array([[1, 0, 0, 0],
                                   [0, 1, 0, 0],
                                   [0, 0, 1, cylinder_height/2],
                                   [0, 0, 0, 1]])

    cylinder.apply_transform(cylinder_transform)
    # add back axis for debugging
    scene = trimesh.Scene([hook, cylinder])

    print("Ellipse hook generated")
    scene_to_xml(scene)
    scene.show()

if __name__ == "__main__":
    generate_hook()