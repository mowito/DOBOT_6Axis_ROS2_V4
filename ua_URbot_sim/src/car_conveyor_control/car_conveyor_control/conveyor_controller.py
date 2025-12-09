#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_srvs.srv import SetBool
from rclpy.qos import QoSProfile


class ConveyorController(Node):
    def __init__(self):
        super().__init__('conveyor_controller')

        # This MUST match what works with bridge + Gazebo
        self.declare_parameter(
            'cmd_topic',
            '/model/conveyor_car/cmd_vel'
        )
        self.declare_parameter('default_speed', 0.5)

        self.cmd_topic = self.get_parameter('cmd_topic').get_parameter_value().string_value
        self.default_speed = self.get_parameter('default_speed').get_parameter_value().double_value

        qos = QoSProfile(depth=10)
        self.pub = self.create_publisher(Twist, self.cmd_topic, qos)

        self.current_speed = 0.0

        # True → run at +default_speed, False → stop
        self.srv = self.create_service(
            SetBool,
            'set_conveyor_running',
            self.handle_set_conveyor_running
        )

        # Publish at 20 Hz so velocity persists
        self.timer = self.create_timer(0.05, self.publish_twist)

        self.get_logger().info(
            f'ConveyorController publishing to [{self.cmd_topic}] '
            f'with default speed {self.default_speed} m/s'
        )

    def handle_set_conveyor_running(self, request, response):
        if request.data:
            self.current_speed = self.default_speed
            response.message = f'Conveyor started at {self.current_speed:.3f} m/s'
        else:
            self.current_speed = 0.0
            response.message = 'Conveyor stopped'

        response.success = True
        self.get_logger().info(response.message)
        return response

    def publish_twist(self):
        msg = Twist()
        msg.linear.x = float(self.current_speed)
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ConveyorController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
