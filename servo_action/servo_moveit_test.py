#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped


class TwistZPublisher(Node):
    def __init__(self):
        super().__init__('twist_z_publisher')

        # Parameters (override with --ros-args -p key:=value)
        self.declare_parameter('topic', '/servo_node/delta_twist_cmds')
        self.declare_parameter('rate_hz', 30.0)
        self.declare_parameter('value', -0.1)          # magnitude for Z
        self.declare_parameter('component', 'linear') # 'linear' or 'angular'
        self.declare_parameter('frame', 'camera_color_optical_frame')

        self.topic = self.get_parameter('topic').get_parameter_value().string_value
        self.rate_hz = float(self.get_parameter('rate_hz').value)
        self.value = float(self.get_parameter('value').value)
        self.component = self.get_parameter('component').get_parameter_value().string_value
        self.frame = self.get_parameter('frame').get_parameter_value().string_value

        if self.component not in ('linear', 'angular'):
            self.get_logger().warn("Parameter 'component' must be 'linear' or 'angular'. Defaulting to 'linear'.")
            self.component = 'linear'

        if self.rate_hz <= 0:
            self.get_logger().warn("rate_hz must be > 0. Defaulting to 30.0")
            self.rate_hz = 30.0

        self.pub = self.create_publisher(TwistStamped, self.topic, 10)
        self.timer = self.create_timer(1.0 / self.rate_hz, self._tick)

        self.get_logger().info(
            f"Publishing TwistStamped on {self.topic} at {self.rate_hz} Hz | "
            f"{self.component}.z = {self.value} | frame = {self.frame}"
        )

    def _tick(self):
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.frame

        # Only set Z, everything else stays 0
        if self.component == 'linear':
            msg.twist.linear.y = self.value
            msg.twist.linear.z = 0.0
        else:
            msg.twist.angular.x = 1.45

        self.pub.publish(msg)


def main():
    rclpy.init()
    node = TwistZPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
