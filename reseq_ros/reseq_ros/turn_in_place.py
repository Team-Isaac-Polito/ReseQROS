#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from reseq_msgs.msg import Motor


class Turn_In_Place(Node):

    def __init__(self):
        super().__init__('turn_in_place')
        self.publisher_ = self.create_publisher(Motor,"motor_topic",10)
        self.get_logger().info("Hello! turn_in_place node started!")
        timer_freq = 50 # hertz
        self.timer = self.create_timer(1/timer_freq, self.node_callback)
        
    def node_callback(self):
        motor_msg=Motor() #Motor.msg={wdx,wsx,angle}
        vel = 500
        
        motor_msg.wdx = -vel
        motor_msg.wsx = -vel
        motor_msg.angle = 0.0
        motor_msg.address = 21 # head
        self.publisher_.publish(motor_msg)

        motor_msg.wdx = vel
        motor_msg.wsx = -vel
        motor_msg.angle = 0.0
        motor_msg.address = 22 # middle
        self.publisher_.publish(motor_msg)

        motor_msg.wdx = vel
        motor_msg.wsx = vel
        motor_msg.angle = 0.0
        motor_msg.address = 23 # tail
        self.publisher_.publish(motor_msg)


def main(args=None):
    rclpy.init(args=args)
    
    turn_in_place = Turn_In_Place()
    
    rclpy.spin(turn_in_place)


if __name__ == '__main__':
    main()
