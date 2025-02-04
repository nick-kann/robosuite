import trimesh
import numpy as np
import xml.etree.ElementTree as ET
def scene_to_xml(scene, filename="custom_scripts/hoeok.xml"):
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
    print(f"L hook saved to {filename}")

def generate_hook():

    # edit these variables
    length = np.random.uniform(0.2, 1)
    width = np.random.uniform(0.1, 0.5)
    theta = np.random.uniform(30, 90)
    cylinder_height = np.random.uniform(0.2, 1)
    # --------------------

    print(f"length = {length}")
    print(f"width = {width}")
    print(f"theta = {theta}")
    print(f"cylinder_height = {cylinder_height}")

    """
    order:
    create side one
    create side two
    shift both sides to origin
    rotate side two
    combine sides into hook
    rotate hook to make middle lined up with Z-axis
    shift hook by cylinder length
    create cylinder
    shift cylinder to origin
    """

    cylinder_radius = 0.06


    extents = [width, 0.1*length, length]  # Width, thickness, Depth

    # translate to shift origin to bottom left
    shift_one = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, length / 2],
                      [0, 0, 0, 1]])

    side_one = trimesh.creation.box(extents=extents, transform=shift_one)

    side_two = trimesh.creation.box(extents=extents, transform=shift_one)

    angle = np.radians(-theta)
    t_axis = np.array([1, 0, 0])

    rotation_matrix = trimesh.transformations.rotation_matrix(angle, t_axis)

    side_two.apply_transform(rotation_matrix)

    hook = side_one.union(side_two)

    shift_hook = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, cylinder_height],
                      [0, 0, 0, 1]])

    angle = np.radians(theta/2)
    t_axis = np.array([1, 0, 0])

    hook_rotation_matrix = trimesh.transformations.rotation_matrix(angle, t_axis)
    hook.apply_transform(hook_rotation_matrix)

    hook.apply_transform(shift_hook)

    axis = trimesh.creation.axis(origin_size=0.1, transform=np.eye(4))

    cylinder = trimesh.creation.cylinder(radius=cylinder_radius, height=cylinder_height)

    cylinder_transform = np.array([[1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, cylinder_height/2],
    [0, 0, 0, 1]])

    cylinder.apply_transform(cylinder_transform)

    # add back axis for debugging
    scene = trimesh.Scene([hook, cylinder])
    print("L hook generated")
    scene_to_xml(scene)
    output_stl = "robosuite/models/assets/grippers/meshes/hook.stl"
    scene.export(file_obj=output_stl, file_type='stl')
    scene.show()
