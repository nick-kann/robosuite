import os
from mujoco_py import load_model_from_path, MjSim, MjViewer
from urdf_parser_py.urdf import URDF

def convert_urdf_to_mjcf(urdf_path, output_path):
    robot = URDF.from_xml_file(urdf_path)
    with open(output_path, 'w') as f:
        f.write('<mujoco>\n')
        f.write('<asset>\n')
        for mesh in robot.links:
            if mesh.visual and mesh.visual.geometry.mesh:
                mesh_file = mesh.visual.geometry.mesh.filename
                f.write(f'<mesh file="{mesh_file}" />\n')
        f.write('</asset>\n')
        f.write('<worldbody>\n')
        for link in robot.links:
            f.write(f'<body name="{link.name}">\n')
            if link.visual and link.visual.geometry.mesh:
                mesh_file = link.visual.geometry.mesh.filename
                f.write(f'<geom type="mesh" mesh="{mesh_file}" />\n')
            f.write('</body>\n')
        f.write('</worldbody>\n')
        f.write('</mujoco>\n')

urdf_path = 'custom_scripts/mobility.urdf'
mjcf_path = 'path/to/mobility.xml'
convert_urdf_to_mjcf(urdf_path, mjcf_path)