import numpy as np
import robosuite as suite
from robosuite.utils.placement_samplers import UniformRandomSampler
from robosuite import load_composite_controller_config
import time

controller_config = load_composite_controller_config(controller='BASIC')
env = suite.make(
    env_name="Lift",
    robots="UR5e",
    has_renderer=True,
    has_offscreen_renderer=False,
    use_camera_obs=False,
    controller_configs=controller_config,
)

obs = env.reset()


for i in range(10000):
    action = np.random.randn(*env.action_spec[0].shape)
    obs, reward, done, _ = env.step(action)
    env.render()
    time.sleep(0.1)

