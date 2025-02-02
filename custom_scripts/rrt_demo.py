import numpy as np
import robosuite as suite
from robosuite.utils.placement_samplers import UniformRandomSampler
from robosuite import load_composite_controller_config
import time
from rrt_planner import RRT3D, Obstacle

controller_config = load_composite_controller_config(controller='BASIC')

env = suite.make(
    env_name="PickPlace",
    robots="UR5e",
    has_renderer=True,
    has_offscreen_renderer=False,
    use_camera_obs=False,
    controller_configs=controller_config,
)

obs = env.reset()

milk_x, milk_y, milk_z = obs['Milk_pos']
print(f"Initial EEF position: {obs['robot0_eef_pos']}")
print(f"Milk position: {obs['Milk_pos']}")
print(f"Initial Distance to milk: {np.linalg.norm(obs['robot0_eef_pos'] - obs['Milk_pos'])}")

# Parameters for movement
steps_per_action = 20
approach_speed = 2

rrt_params = {
    "start": obs['robot0_eef_pos'],
    "goal": obs['Can_pos'],
    "bounds": [[-1, 1], [-1, 1], [0.6, 1.0]],
    "step_size": 0.01,
    "max_iter": 3000,
    "safety_margin": 0.04,
    "obstacles": [
        Obstacle(obs['Milk_pos'], [0.002, 0.002, 0.002]),
        Obstacle(obs['Cereal_pos'], [0.01, 0.12, 0.03]),
        Obstacle(obs['Bread_pos'], [0.0001, 0.0001, 0.0001])
    ]
}

rrt = RRT3D(rrt_params["start"], rrt_params["goal"], rrt_params["bounds"], rrt_params["step_size"],
            rrt_params["max_iter"], rrt_params["obstacles"], rrt_params["safety_margin"])

path = rrt.plan()


if path:
    print(f"Path found with {len(path)} waypoints")
else:
    print("No path found.")
    for _ in range(500):
        action = np.zeros(env.action_spec[0].shape[0])
        obs, reward, done, info = env.step(action)
        env.render()
        time.sleep(0.01)
    exit(0)

def is_colliding(eef_pos, milk_pos, threshold=0.05):
    distance = np.linalg.norm(eef_pos - milk_pos)
    return distance < threshold

for i in range(len(path)):
    # print(f"Moving to point {i+1}/{len(path)}")
    for step in range(steps_per_action):
        current_pos = obs['robot0_eef_pos']

        # neutral vec
        action = np.zeros(env.action_spec[0].shape[0])

        # action vec
        action[0] = approach_speed * (path[i][0] - current_pos[0])
        action[1] = approach_speed * (path[i][1]- current_pos[1])
        action[2] = approach_speed * (path[i][2] - current_pos[2])

        obs, reward, done, info = env.step(action)

        env.render()
        time.sleep(0.001)

# for step in range(steps_per_action):
    # current_pos = obs['robot0_eef_pos']
    #
    # # neutral vec
    # action = np.zeros(env.action_spec[0].shape[0])
    #
    # # action vec
    # action[0] = approach_speed * (milk_x - current_pos[0])
    # action[1] = approach_speed * (milk_y - current_pos[1])
    # action[2] = approach_speed * (milk_z - current_pos[2])
    #
    # obs, reward, done, info = env.step(action)
    #
    # env.render()
    # time.sleep(0.01)

print(f"Final EEF position: {obs['robot0_eef_pos']}")
print(f"Final Distance to milk: {np.linalg.norm(obs['robot0_eef_pos'] - obs['Milk_pos'])}")

env.close()