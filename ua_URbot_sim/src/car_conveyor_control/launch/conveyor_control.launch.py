from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Path to your SDF world
    default_world_path = (
        '/home/mowito/ujwal/ur_gz/src/custom_worlds/worlds/car_conveyor.sdf'
    )

    world_arg = DeclareLaunchArgument(
        'world',
        default_value=default_world_path,
        description='Full path to car_conveyor.sdf'
    )

    world = LaunchConfiguration('world')

    # 1) Start Ignition Gazebo (Fortress) with your SDF
    gz_process = ExecuteProcess(
        cmd=[
            'ign', 'gazebo',
            world,        # SDF path
            '-r',         # start running
            '-v', '4'     # verbose
        ],
        output='screen'
    )

    # 2) Bridge for the conveyor car cmd_vel topic
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='conveyor_bridge',
        output='screen',
        arguments=[
            '/model/conveyor_car/cmd_vel'
            '@geometry_msgs/msg/Twist'
            '@ignition.msgs.Twist'
        ],
    )

    # 3) Your conveyor controller node
    controller = Node(
        package='car_conveyor_control',
        executable='conveyor_controller',
        name='conveyor_controller',
        output='screen',
        parameters=[
            {'cmd_topic': '/model/conveyor_car/cmd_vel'},
            {'default_speed': 0.3},
        ],
    )

    return LaunchDescription([
        world_arg,
        gz_process,
        bridge,
        controller,
    ])
