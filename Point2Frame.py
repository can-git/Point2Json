import open3d as o3d
import numpy as np
from file_paths import Paths as p
import time

# Load camera poses from the text file
camera_poses = []
with open(p.pose_txt.value, "r") as pose_file:
    for line in pose_file:
        new_line = line.split(":")[1]
        pose_data = list(map(float, new_line.strip().split()))
        camera_poses.append(pose_data)

# Load the PCD file (replace "path_to_pcd_file.pcd" with your PCD file path)
point_cloud = o3d.io.read_point_cloud(p.pcd.value)

# Create an Open3D visualization window
visualizer = o3d.visualization.Visualizer()
visualizer.create_window()

visualizer = o3d.visualization.Visualizer()
visualizer.create_window()

# Add the point cloud to the visualization
visualizer.add_geometry(point_cloud)


# Iterate through each frame and visualize
for camera_pose in camera_poses:
    # Extract orientation and position from the camera pose
    camera_orientation = camera_pose[:4]
    camera_position = camera_pose[4:]

    # Create a transformation matrix from the camera pose
    transformation_matrix = np.eye(4)
    transformation_matrix[:3, :3] = o3d.geometry.get_rotation_matrix_from_quaternion(camera_orientation)
    transformation_matrix[:3, 3] = camera_position

    # Calculate the inverse transformation matrix
    inverse_transformation_matrix = np.linalg.inv(transformation_matrix)

    # Transform the point cloud using the inverse transformation matrix
    transformed_point_cloud = point_cloud.transform(transformation_matrix)

    # Clear previous geometry
    visualizer.clear_geometries()

    # Add the transformed point cloud to the visualization
    visualizer.add_geometry(transformed_point_cloud)

    # Update the visualization
    visualizer.poll_events()
    visualizer.update_renderer()

    # Pause for visualization (adjust as needed)
    time.sleep(0.1)

# Clean up
visualizer.destroy_window()