from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # Paths
    description_file = "/home/mowito/ujwal/ur_gz/install/ur10e_with_camera_description/share/ur10e_with_camera_description/urdf/ur10e_with_camera.urdf.xacro"

    # UR simulation + MoveIt launch
    ur_sim_moveit = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('ur_simulation_gz'),
                'launch',
                'ur_sim_moveit.launch.py'
            )
        ]),
        launch_arguments={
            'ur_type': 'ur10e',
            'description_file': description_file
        }.items()
    )

    # Bridge the camera image topic (GZ → ROS2)
    gz_bridge_image = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            # GZ topic maps to ROS topic with sensor_msgs/Image
            "/wrist_camera/image@sensor_msgs/msg/Image@gz.msgs.Image"
        ],
        output='screen'
    )

    # Start rqt_image_view
    rqt_image = Node(
        package="rqt_image_view",
        executable="rqt_image_view",
        output="screen"
    )

    return LaunchDescription([
        ur_sim_moveit,
        gz_bridge_image,
        rqt_image,
    ])
