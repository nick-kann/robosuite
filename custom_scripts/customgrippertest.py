import numpy as np
from robosuite.models.grippers import GripperModel
from robosuite.models.robots import UR5e


class CustomHookGripper(GripperModel):
    def __init__(self, idn=0):
        super().__init__(fname="custom_scripts/hoeok.xml", idn=idn)

    @property
    def bottom_offset(self):
        return np.array([0, 0, -0.05])

custom_gripper = CustomHookGripper()
robot = UR5e(
    gripper_type=custom_gripper,
    controller_config="default",
)

env = suite.make(
    env_name="Lift",
    robots=robot,
    has_renderer=True,
    has_offscreen_renderer=False,
    use_camera_obs=False,
    controller_configs=controller_config,
)


env.reset()

for i in range(1000):
    action = np.random.randn(env.action_dim)
    obs, reward, done, info = env.step(action)
    env.render()

    if done:
        break

env.close()