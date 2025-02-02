# First, create your custom gripper class
from robosuite.models.grippers import Gripper
from robosuite.utils.mjcf_utils import array_to_string, string_to_array
import numpy as np


class HookGripper(Gripper):
    def __init__(self, idn=0):
        super().__init__(idn=idn)

        # Set initialization values
        self.gripper_name = "hook_gripper"

        # Path to gripper XML
        self.gripper_path = "hook.xml"

        # Initialize joints
        self.joints = ["hook_joint"]  # Update with your joint names

        # Initialize actuators
        self.actuators = ["hook_actuator"]  # Update with your actuator names

        # Initialize sensors
        self.contact_sensors = ["hook_contact_sensor"]  # Update with your sensor names

    def init_qpos(self):
        """Initialize default joint positions"""
        return np.array([0.0])  # Adjust default position as needed


# Example implementation in your environment
def create_environment():
    from robosuite.environments import Environment
    from robosuite.robots import UR5e

    # Create environment configuration
    config = {
        "robots": "UR5e",
        "controller_configs": {
            "type": "OSC_POSE",
            "input_max": 1,
            "input_min": -1,
            "output_max": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            "output_min": [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5],
            "kp": 150,
            "damping_ratio": 1,
            "impedance_mode": "fixed",
            "kp_limits": [0, 300],
            "damping_ratio_limits": [0, 10],
            "position_limits": None,
            "orientation_limits": None,
            "uncouple_pos_ori": True,
            "control_delta": True,
            "interpolation": None,
            "ramp_ratio": 0.2
        },
    }

    # Initialize robot with custom gripper
    robot = UR5e(
        gripper=HookGripper(),
        has_base=False,
        control_freq=20
    )

    # Create and return environment
    env = Environment(
        robots=[robot],
        **config
    )

    return env