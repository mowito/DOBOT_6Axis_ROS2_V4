from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # Bridge /model/conveyor_car/cmd_vel between ROS2 and Gazebo
    cmd_vel_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="conveyor_bridge",
        arguments=[
            "/model/conveyor_car/cmd_vel"
            "@geometry_msgs/msg/Twist"
            "@ignition.msgs.Twist",
        ],
        output="screen",
    )

    # Conveyor speed controller (publishes to /model/conveyor_car/cmd_vel)
    conveyor_controller = Node(
        package="car_conveyor_control",
        executable="conveyor_controller",
        name="conveyor_controller",
        output="screen",
    )

    return LaunchDescription([
        cmd_vel_bridge,
        conveyor_controller,
    ])
