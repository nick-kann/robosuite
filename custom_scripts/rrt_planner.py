import numpy as np
import random
import matplotlib.pyplot as plt


class Obstacle:
    def __init__(self, center, dimensions):
        self.center = np.array(center)
        self.dimensions = np.array(dimensions)

    def is_collision(self, point, safety_margin=0):
        point = np.array(point)
        return np.all(np.abs(point - self.center) <= (self.dimensions / 2 + safety_margin))


class Node:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.parent = None


class RRT3D:
    def __init__(self, start, goal, bounds, step_size, max_iter, obstacles=None, safety_margin=0.5):
        self.start = Node(*start)
        self.goal = Node(*goal)
        self.bounds = bounds
        self.step_size = step_size
        self.max_iter = max_iter
        self.tree = [self.start]
        self.obstacles = obstacles or []
        self.safety_margin = safety_margin

    def distance(self, node1, node2):
        return np.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2 + (node1.z - node2.z) ** 2)

    def get_random_node(self):
        if random.random() < 0.1:
            return self.goal

        x = random.uniform(*self.bounds[0])
        y = random.uniform(*self.bounds[1])
        z = random.uniform(*self.bounds[2])
        return Node(x, y, z)

    def nearest_node(self, random_node):
        return min(self.tree, key=lambda node: self.distance(node, random_node))

    def is_collision_free(self, from_node, to_node):
        for t in np.linspace(0, 1, 10):
            point = [
                from_node.x + t * (to_node.x - from_node.x),
                from_node.y + t * (to_node.y - from_node.y),
                from_node.z + t * (to_node.z - from_node.z)
            ]
            for obstacle in self.obstacles:
                if obstacle.is_collision(point, self.safety_margin):
                    return False
        return True

    def steer(self, from_node, to_node):
        direction = np.array([to_node.x - from_node.x, to_node.y - from_node.y, to_node.z - from_node.z])
        distance = np.linalg.norm(direction)
        if distance < self.step_size:
            return to_node
        direction = direction / distance * self.step_size
        new_node = Node(from_node.x + direction[0], from_node.y + direction[1], from_node.z + direction[2])
        new_node.parent = from_node
        return new_node

    def is_in_bounds(self, node):
        return (self.bounds[0][0] <= node.x <= self.bounds[0][1] and
                self.bounds[1][0] <= node.y <= self.bounds[1][1] and
                self.bounds[2][0] <= node.z <= self.bounds[2][1])

    def plan(self):
        for _ in range(self.max_iter):
            random_node = self.get_random_node()
            nearest_node = self.nearest_node(random_node)
            new_node = self.steer(nearest_node, random_node)

            if (self.is_in_bounds(new_node) and
                    self.is_collision_free(nearest_node, new_node)):
                self.tree.append(new_node)

                if (self.distance(new_node, self.goal) < self.step_size or
                        self.distance(new_node, self.goal) <= self.step_size * 1.5):
                    self.goal.parent = new_node
                    self.tree.append(self.goal)
                    return self.extract_path()
        return None

    def extract_path(self):
        path = []
        current = self.goal
        while current is not None:
            path.append([current.x, current.y, current.z])
            current = current.parent
        path.reverse()
        return path

    def plot(self, path):
        if not path:
            print("No path to plot.")
            return

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        for node in self.tree:
            if node.parent is not None:
                ax.plot([node.x, node.parent.x], [node.y, node.parent.y], [node.z, node.parent.z], 'g-', linewidth=0.5,
                        alpha=0.5)

        for obstacle in self.obstacles:
            half_dims = obstacle.dimensions / 2
            x_min = obstacle.center[0] - half_dims[0]
            x_max = obstacle.center[0] + half_dims[0]
            y_min = obstacle.center[1] - half_dims[1]
            y_max = obstacle.center[1] + half_dims[1]
            z_min = obstacle.center[2] - half_dims[2]
            z_max = obstacle.center[2] + half_dims[2]

            vertices = np.array([
                [x_min, y_min, z_min], [x_max, y_min, z_min],
                [x_max, y_max, z_min], [x_min, y_max, z_min],
                [x_min, y_min, z_max], [x_max, y_min, z_max],
                [x_max, y_max, z_max], [x_min, y_max, z_max]
            ])

            edges = [
                [0, 1], [1, 2], [2, 3], [3, 0],
                [4, 5], [5, 6], [6, 7], [7, 4],
                [0, 4], [1, 5], [2, 6], [3, 7]
            ]

            for edge in edges:
                ax.plot3D(vertices[edge, 0], vertices[edge, 1], vertices[edge, 2], 'r-', linewidth=2)

        path = np.array(path)
        ax.plot(path[:, 0], path[:, 1], path[:, 2], 'b-', linewidth=3, label='Path')

        ax.scatter(self.start.x, self.start.y, self.start.z, c='g', marker='o', s=100, label='Start')
        ax.scatter(self.goal.x, self.goal.y, self.goal.z, c='r', marker='x', s=100, label='Goal')

        ax.set_xlim(self.bounds[0])
        ax.set_ylim(self.bounds[1])
        ax.set_zlim(self.bounds[2])

        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_zlabel('Z-axis')
        ax.legend()
        plt.title('RRT 3D Path Planning with Obstacles')
        plt.show()


if __name__ == "__main__":

    obs = {
        'robot0_eef_pos': [-0.01705325, -0.10517212, 0.92201174],
        'Milk_pos': [0.12761573, -0.08847043, 0.885]
    }
    rrt_params = {
        "start": obs['robot0_eef_pos'],
        "goal": obs['Milk_pos'],
        "bounds": [[-1, 1], [-1, 1], [0.6, 1.0]],
        "step_size": 0.01,
        "max_iter": 3000,
        "safety_margin": 0.5,
        "obstacles": [

        ]
    }
    rrt = RRT3D(rrt_params["start"], rrt_params["goal"], rrt_params["bounds"], rrt_params["step_size"],
                rrt_params["max_iter"], rrt_params["obstacles"], rrt_params["safety_margin"])
    path = rrt.plan()

    if path:
        print("Path found:")
        # for point in path:
        #     print(point)
    else:
        print("No path found.")

    # rrt.plot(path)