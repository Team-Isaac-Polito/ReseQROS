#!/usr/bin/python3

import definitions
import can

canbus = can.interface.Bus(channel='can0', bustype='socketcan')
kp,ki,kd = sys.argv[1:]

data = list(struct.pack('f', kp))
msg = can.Message(arbitration_id=int(addr),data=[definitions.DATA_PID_KP]+data,is_extended_id=False)
canbus.send(msg)

data = list(struct.pack('f', ki))
msg = can.Message(arbitration_id=int(addr),data=[definitions.DATA_PID_KI]+data,is_extended_id=False)
canbus.send(msg)

data = list(struct.pack('f', kd))
msg = can.Message(arbitration_id=int(addr),data=[definitions.DATA_PID_KD]+data,is_extended_id=False)
canbus.send(msg)

