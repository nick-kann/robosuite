import os
import trimesh
import numpy as np
import xml.etree.ElementTree as ET

def scene_to_xml(scene, filename="custom_scripts/hook.xml"):
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
    print(f"C hook saved to {filename}")


def generate_mjcf(scene, filename="robosuite/models/assets/robots/ur5e/custom_meshes/hook.xml"):
    """
    Convert a trimesh scene to MJCF (MuJoCo XML) format

    Args:
        scene (trimesh.Scene): Input trimesh scene
        filename (str): Output MJCF file path
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Create the root MuJoCo element
    mujoco = ET.Element("mujoco", model="hook_gripper")

    # Create compiler options
    compiler = ET.SubElement(mujoco, "compiler",
                             angle="radian",
                             meshdir="./")

    # Create assets section for mesh definitions
    assets = ET.SubElement(mujoco, "asset")

    # Export mesh to STL if not already done
    mesh_filename = filename.replace('.xml', '.stl')
    scene.export(file_obj=mesh_filename, file_type='stl')

    # Create mesh asset
    mesh_asset = ET.SubElement(assets, "mesh",
                               name="hook_mesh",
                               file=os.path.basename(mesh_filename))

    # Create worldbody section
    worldbody = ET.SubElement(mujoco, "worldbody")

    # Create a body for the mesh
    body = ET.SubElement(worldbody, "body", name="hook_body")

    # Create geom for the mesh
    geom = ET.SubElement(body, "geom",
                         type="mesh",
                         mesh="hook_mesh",
                         name="hook_geom",
                         group="0",
                         rgba="1 0 0 1")  # Red color

    # Write the XML file
    tree = ET.ElementTree(mujoco)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"MJCF file saved to {filename}")

    return filename


def generate_hook():
    scale = 1
    # edit these variables
    width = np.random.uniform(0.05*scale, 0.5*scale) # [0.05, 0.5]
    height = np.random.uniform(0.5*scale, 1*scale) # [0.5, 1]
    length = np.random.uniform(0.5*scale, 1*scale) # [0.5, 1]
    cylinder_height = np.random.uniform(0.2*scale, 1*scale)
    # --------------------
    cylinder_radius = 0.06*scale

    print(f"width = {width}")
    print(f"height = {height}")
    print(f"length = {length}")
    print(f"cylinder_height = {cylinder_height}")

    extents = [width, height, length]

    # translate to shift origin to bottom left
    shift = np.array([[1, 0, 0, width / 2],
                      [0, 1, 0, height / 2],
                      [0, 0, 1, length / 2],
                      [0, 0, 0, 1]])

    original_cube = trimesh.creation.box(extents=extents, transform=shift)



    # red cube properties
    red_cube_extents = [width, height * 0.8, length - height*0.1]  # Width, Height, Depth
    red_shift = np.array([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 1, height * 0.05],
                          [0, 0, 0, 1]])

    # apply the same shift with red cube
    red_shift = shift @ red_shift

    red_cube = trimesh.creation.box(extents=red_cube_extents, transform=red_shift)

    red_cube.visual.face_colors = [255, 0, 0, 255]

    axis = trimesh.creation.axis(origin_size=0.1, transform=np.eye(4))

    c_cube = original_cube.difference(red_cube)

    c_shift = np.array([[1, 0, 0, -width/2],
                          [0, 1, 0, -height/2],
                          [0, 0, 1, cylinder_height],
                          [0, 0, 0, 1]])

    c_cube.apply_transform(c_shift)

    cylinder = trimesh.creation.cylinder(radius=cylinder_radius, height=cylinder_height)

    cylinder_transform = np.array([[1, 0, 0, 0],
                                   [0, 1, 0, 0],
                                   [0, 0, 1, cylinder_height/2],
                                   [0, 0, 0, 1]])

    cylinder.apply_transform(cylinder_transform)

    # Merge with handle
    c_cube = c_cube.union(cylinder)
    # add back axis for debugging

    # t_cube = trimesh.creation.box(extents=extents)

    scene = trimesh.Scene([c_cube])

    output_stl = "robosuite/models/assets/grippers/meshes/hook.stl"
    # output_obj = "robosuite/models/assets/robots/ur5e/custom_meshes/hook.obj"
    # output_mjcf = "robosuite/models/assets/robots/ur5e/custom_meshes/hook.xml"

    scene.export(file_obj=output_stl, file_type='stl')
    # t_cube.export(file_obj=output_obj, file_type='obj')
    # generate_mjcf(t_cube, output_mjcf)
    print("C hook generated")

    scene.show()
