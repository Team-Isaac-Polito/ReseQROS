import definitions
import can
import time
import os

import rospy
from ReseQROS.msg import Motor

print('\n\rCAN Rx test')
print('Bring up CAN0....')



def writeNumbers(addr,vsx,vdx,angle):
    global canbus

    a = vsx & 0xFF
    b = vsx>>8 & 0xFF
	msg = can.Message(arbitration_id=addr,data=[definitions.DATA_TRACTION_LEFT,a,b, 0x0, 0x0, 0x0,0x0, 0x0],extended_id=False)
    canbus.send(msg)

    a = vdx & 0xFF
    b = vdx>>8 & 0xFF
	msg = can.Message(arbitration_id=addr,data=[definitions.DATA_TRACTION_RIGHT, a, b, 0x0, 0x0, 0x0,0x0, 0x0],extended_id=False)
    canbus.send(msg)

    a = angle & 0xFF
    b = angle>>8 & 0xFF
	msg = can.Message(arbitration_id=addr,data=[definitions.DATA_TRACTION_YAW, a, b, 0x0, 0x0, 0x0,0x0, 0x0],extended_id=False)
    canbus.send(msg)






def invio_dati(data):
	rospy.loginfo("DataToSend:\nADDR: " + str(data.address) + "\nVSX: " + str(data.vsx) + "\nVDX: " + str(data.vdx) + "\nANGLE: " + str(data.angle))
	writeNumbers(data.address,int(data.vsx),int(data.vdx),int(data.angle))


if __name__ == '__main__':
    global canbus
	try:

		rospy.init_node('communication')

		rospy.loginfo("Hello! communication node started!")

        # Bring up can0 interface at 125kbps
        os.system("sudo modprobe can")
        os.system("sudo /sbin/ip link set can0 up type can bitrate 125000")
        time.sleep(0.1)	
        canbus = can.interface.Bus(channel='can0', bustype='socketcan_native')


		rospy.Subscriber("motor_topic",Motor,invio_dati)

		rospy.spin()
		

	except rospy.ROSInterruptException:
		pass
