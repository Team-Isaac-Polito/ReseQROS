#!/usr/bin/python3

import definitions
import can
import sys
import struct

canbus = can.interface.Bus(channel='can1', bustype='socketcan')
addr,kp,ki,kd = sys.argv[1:]

data = list(struct.pack('f', float(kp)))
msg = can.Message(arbitration_id=int(addr),data=[definitions.DATA_PID_KP]+data,is_extended_id=False)
canbus.send(msg)

data = list(struct.pack('f', float(ki)))
msg = can.Message(arbitration_id=int(addr),data=[definitions.DATA_PID_KI]+data,is_extended_id=False)
canbus.send(msg)

data = list(struct.pack('f', float(kd)))
msg = can.Message(arbitration_id=int(addr),data=[definitions.DATA_PID_KD]+data,is_extended_id=False)
canbus.send(msg)
