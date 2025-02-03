import robosuite as suite
from robosuite import load_composite_controller_config
from robosuite.models.grippers import GripperModel
from robosuite.models.robots import RobotModel
import robosuite.models.grippers as grippers
import numpy as np
import time
import os


# Create a custom gripper class
class CustomGripper(GripperModel):
    def __init__(self):
        super().__init__(
            fname="hoeok.xml",  # Path to your gripper XML file
            name="custom_gripper"  # Name for your gripper
        )

    def format_action(self, action):
        """
        Maps raw input actions to gripper-specific actions.
        """
        return action

    def init_qpos(self):
        """
        Return default qpos for this gripper.
        """
        return np.zeros(self.dof)


# Register the custom gripper using the module-level registration
grippers.GRIPPER_MAPPING["CustomGripper"] = CustomGripper

# Load controller config
controller_config = load_composite_controller_config(controller='BASIC')

# Create environment with custom gripper
env = suite.make(
    env_name="Lift",
    robots="UR5e",
    has_renderer=True,
    has_offscreen_renderer=False,
    use_camera_obs=False,
    controller_configs=controller_config,
    gripper_types="CustomGripper",  # Use our custom gripper
)

# Reset and run simulation loop
env.reset()
for i in range(1000):
    action = np.random.randn(*env.action_spec[0].shape)
    obs, reward, done, _ = env.step(action)
    env.render()
    time.sleep(0.01)