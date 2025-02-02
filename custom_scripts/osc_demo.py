import numpy as np
import robosuite as suite
from robosuite.utils.placement_samplers import UniformRandomSampler
from robosuite import load_composite_controller_config
import time

for _ in range(3):
    x_position = [-0.3, 0.3]  # forward/backward
    y_position = [-0.3, 0.3]  # left/right
    z_height = 0.8

    controller_config = load_composite_controller_config(controller='BASIC')

    sampler = UniformRandomSampler(
        name="ObjectSampler",
        mujoco_objects=None,
        x_range=x_position,
        y_range=y_position,
        rotation=None,
        rotation_axis='z',
        ensure_object_boundary_in_range=True,
        ensure_valid_placement=True,
        reference_pos=np.array([0.0, 0.0, z_height])
    )

    env = suite.make(
        env_name="Lift",
        robots="Panda",
        has_renderer=True,
        has_offscreen_renderer=False,
        use_camera_obs=False,
        controller_configs=controller_config,
        placement_initializer=sampler,
    )

    obs = env.reset()

    steps_per_action = 75
    steps_per_rest = 75
    print("cube pos:", obs['cube_pos'])
    cube_pos = obs['cube_pos']
    print(f"eef pos: {obs['robot0_eef_pos']}")
    count = 0
    total_action_steps = 3

    displacements = [cube_pos[0] - obs['robot0_eef_pos'][0], cube_pos[1] - obs['robot0_eef_pos'][1],
                     cube_pos[2] - obs['robot0_eef_pos'][2]]

    while count < total_action_steps:
        for i in range(steps_per_action):
            action = np.zeros(env.action_spec[0].shape[0])
            action[count] = displacements[count]
            obs, reward, done, info = env.step(action)

            env.render()
            time.sleep(0.003)

        for i in range(steps_per_rest):
            action = np.zeros(env.action_spec[0].shape[0])
            env.step(action)
            env.render()
        count += 1

    print(f"final hand: {obs['robot0_eef_pos']}")
    env.close()

