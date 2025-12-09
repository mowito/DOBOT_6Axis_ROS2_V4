# from launch import LaunchDescription
# from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
# from launch_ros.actions import Node
# from launch_ros.substitutions import FindPackageShare


# def generate_launch_description():
#     # ---- Launch configurations ----
#     ur_type = LaunchConfiguration("ur_type")
#     world_file = LaunchConfiguration("world_file")

#     # Use camera URDF only for the simulation
#     sim_description_package = LaunchConfiguration("sim_description_package")
#     sim_description_file = LaunchConfiguration("sim_description_file")

#     # Use stock UR description for MoveIt (has all YAML configs)
#     moveit_description_package = LaunchConfiguration("moveit_description_package")
#     moveit_description_file = LaunchConfiguration("moveit_description_file")

#     moveit_config_package = LaunchConfiguration("moveit_config_package")
#     moveit_config_file = LaunchConfiguration("moveit_config_file")
#     prefix = LaunchConfiguration("prefix")

#     # ---- 1) UR sim + Gazebo (camera URDF + conveyor world) ----
#     ur_control_launch = IncludeLaunchDescription(
#         PythonLaunchDescriptionSource(
#             PathJoinSubstitution([
#                 FindPackageShare("ur_simulation_gz"),
#                 "launch",
#                 "ur_sim_control_world.launch.py",
#             ])
#         ),
#         launch_arguments={
#             "ur_type": ur_type,
#             "safety_limits": "true",
#             "runtime_config_package": "ur_simulation_gz",
#             "controllers_file": "ur_controllers.yaml",
#             "description_package": sim_description_package,
#             "description_file": sim_description_file,
#             "prefix": prefix,
#             "launch_rviz": "false",      # RViz via MoveIt
#             "world_file": world_file,    # conveyor world here
#         }.items(),
#     )

#     # ---- 2) MoveIt + RViz (stock UR description) ----
#     ur_moveit_launch = IncludeLaunchDescription(
#         PythonLaunchDescriptionSource(
#             PathJoinSubstitution([
#                 FindPackageShare("ur_moveit_config"),
#                 "launch",
#                 "ur_moveit.launch.py",
#             ])
#         ),
#         launch_arguments={
#             "ur_type": ur_type,
#             "safety_limits": "true",
#             "description_package": moveit_description_package,
#             "description_file": moveit_description_file,
#             "moveit_config_package": moveit_config_package,
#             "moveit_config_file": moveit_config_file,
#             "prefix": prefix,
#             "use_sim_time": "true",
#             "launch_rviz": "true",
#         }.items(),
#     )

#     # ---- 3) Conveyor bridge + controller (NO Gazebo here) ----
#     conveyor_bridge = Node(
#         package="ros_gz_bridge",
#         executable="parameter_bridge",
#         name="conveyor_bridge",
#         output="screen",
#         arguments=[
#             "/model/conveyor_car/cmd_vel"
#             "@geometry_msgs/msg/Twist"
#             "@ignition.msgs.Twist",
#         ],
#     )

#     conveyor_controller = Node(
#         package="car_conveyor_control",
#         executable="conveyor_controller",  # from your setup.py console_scripts
#         name="conveyor_controller",
#         output="screen",
#         parameters=[
#             {"cmd_topic": "/model/conveyor_car/cmd_vel"},
#             {"default_speed": 0.3},
#         ],
#     )

#     # ---- 4) Wrist camera bridge + rqt_image_view ----
#     wrist_cam_bridge = Node(
#         package="ros_gz_bridge",
#         executable="parameter_bridge",
#         arguments=[
#             "/wrist_camera/image@sensor_msgs/msg/Image@gz.msgs.Image",
#         ],
#         output="screen",
#     )

#     rqt_image = Node(
#         package="rqt_image_view",
#         executable="rqt_image_view",
#         output="screen",
#     )

#     # ---- Declare arguments + defaults ----
#     declared_arguments = [
#         DeclareLaunchArgument(
#             "ur_type",
#             default_value="ur10e",
#             description="UR robot type.",
#         ),
#         DeclareLaunchArgument(
#             "world_file",
#             default_value="/home/mowito/ujwal/ur_gz/src/custom_worlds/worlds/car_conveyor.sdf",
#             description="Full path to the Gazebo SDF world (car + conveyor).",
#         ),

#         # Simulation robot (with camera)
#         DeclareLaunchArgument(
#             "sim_description_package",
#             default_value="ur10e_with_camera_description",
#             description="Description package for sim (UR10e with camera).",
#         ),
#         DeclareLaunchArgument(
#             "sim_description_file",
#             default_value="ur10e_with_camera.urdf.xacro",
#             description="URDF/Xacro file in sim_description_package/urdf.",
#         ),

#         # MoveIt robot (stock UR description, with all YAML configs)
#         DeclareLaunchArgument(
#             "moveit_description_package",
#             default_value="ur_description",
#             description="Description package used by MoveIt.",
#         ),
#         DeclareLaunchArgument(
#             "moveit_description_file",
#             default_value="ur.urdf.xacro",
#             description="URDF/Xacro file used by MoveIt.",
#         ),

#         DeclareLaunchArgument(
#             "moveit_config_package",
#             default_value="ur_moveit_config",
#             description="MoveIt config package.",
#         ),
#         DeclareLaunchArgument(
#             "moveit_config_file",
#             default_value="ur.srdf.xacro",
#             description="MoveIt SRDF/Xacro file.",
#         ),
#         DeclareLaunchArgument(
#             "prefix",
#             default_value='""',
#             description="Joint name prefix.",
#         ),
#     ]

#     return LaunchDescription(
#         declared_arguments
#         + [
#             ur_control_launch,
#             ur_moveit_launch,
#             conveyor_bridge,
#             conveyor_controller,
#             wrist_cam_bridge,
#             rqt_image,
#         ]
#     )

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    # 1) Reuse your existing "UR + MoveIt + camera + world" launch
    ur10_camera_sim_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ur10e_with_camera_description'),
                'launch',
                'ur10_camera_sim_world.launch.py',  # <- your working launch
            )
        )
    )

    # # 2) Conveyor bridge (ROS <-> Gazebo Twist)
    # conveyor_bridge = Node(
    #     package="ros_gz_bridge",
    #     executable="parameter_bridge",
    #     name="conveyor_bridge",
    #     output="screen",
    #     arguments=[
    #         "/model/conveyor_car/cmd_vel"
    #         "@geometry_msgs/msg/Twist"
    #         "@ignition.msgs.Twist",
    #     ],
    # )

    # # 3) Conveyor controller node (just the Python node, NO Gazebo here)
    # conveyor_controller = Node(
    #     package="car_conveyor_control",
    #     executable="conveyor_controller",  # from your setup.py
    #     name="conveyor_controller",
    #     output="screen",
    #     parameters=[
    #         {"cmd_topic": "/model/conveyor_car/cmd_vel"},
    #         {"default_speed": 0.3},
    #     ],
    # )

    return LaunchDescription([
        ur10_camera_sim_world,
        # conveyor_bridge,
        # conveyor_controller,
    ])
