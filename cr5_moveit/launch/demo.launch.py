from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch
from ament_index_python.packages import get_package_share_directory
import yaml
import os
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution,FindExecutable,Command
from launch import LaunchDescription
def load_yaml(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)

    try:
        with open(absolute_file_path) as file:
            return yaml.safe_load(file)
    except OSError:  # parent of IOError, OSError *and* WindowsError where available
        return None

def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("cr5_robot", package_name="cr5_moveit").to_moveit_configs()
    nodes = generate_demo_launch(moveit_config)
    servo_yaml = load_yaml("cr5_moveit", "config/cr5_servo.yaml")
    servo_params = {"moveit_servo": servo_yaml}
    
    print(  moveit_config.robot_description_kinematics)
    servo_node = Node(
        package="moveit_servo",
        
        executable="servo_node_main",
        parameters=[
            
            
            moveit_config.robot_description_kinematics,
            servo_params,
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
        ],
        output="screen",
    )
    nodes.add_action(servo_node)

    return nodes

