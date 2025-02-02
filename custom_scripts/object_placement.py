import numpy as np
import robosuite as suite
from robosuite.utils.placement_samplers import UniformRandomSampler

# Customize these values to adjust placement for random sampling
x_position = [0.0, 0.2]  # [min, max] for forward/backward
y_position = [-0.2, 0.2]  # [min, max] for left/right
z_height = 0.8  # Height above ground

# Configure the sampler with your desired positions
sampler = UniformRandomSampler(
    name="ObjectSampler",
    mujoco_objects=None,
    x_range=x_position,  # Forward/backward range
    y_range=y_position,  # Left/right range
    rotation=None,
    rotation_axis='z',
    ensure_object_boundary_in_range=True,
    ensure_valid_placement=True,
    reference_pos=np.array([0.0, 0.0, z_height])  # Base height
)

env = suite.make(
    env_name="Lift",
    robots="Panda",
    has_renderer=True,
    has_offscreen_renderer=False,
    use_camera_obs=False,
    placement_initializer=sampler,
)

env.reset()

for i in range(1000):
    action = np.random.randn(*env.action_spec[0].shape) * 0.1
    obs, reward, done, info = env.step(action)
    env.render()