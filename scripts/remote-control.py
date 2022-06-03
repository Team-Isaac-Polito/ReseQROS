#!/usr/bin/env python3

import rospy
from ReseQROS.msg import Remote
#from std_msgs.msg import String

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import math
from multiprocessing import Process, Queue
import time

import os
clear = lambda: os.system('clear')

_debug = True

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
CORS(app)
socketio = SocketIO(app)

#msg = Remote()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on_error_default
def default_error_handler(e):
    print ("======================= ERROR")
    print(e)
#    print(request.event["message"])
#    print(request.event["args"])


@socketio.on('control', namespace='/control')
def control(message):
	global pub
	if "left" in message["data"].keys():
		global data
		data = message["data"]["left"]
		msg = Remote()
		msg.vel_avanzamento = float(data[0])
		msg.curvatura = float(data[1])

		str = "Remote control: Left joystick: ",data[0],",",data[1]
		if _debug: rospy.loginfo (str)
		pub.publish(msg)


class MapTool(object):
    def __init__(self):
        self.thread = None

    def start_server(self):
        rospy.loginfo('starting remote control server')
        socketio.run(app,host='0.0.0.0', port=5000, debug=True, use_reloader=False)

    def start(self):
        self.thread = socketio.start_background_task(self.start_server)

    def wait(self):
        self.thread.join()



def talker():
	global pub
	rospy.init_node('controllo-remoto')

	pub = rospy.Publisher('remote_topic', Remote, queue_size=10)


	rospy.loginfo("Hello! remote-control node started!")


	maptool = MapTool()
	maptool.start()

	#	rospy.spin()
	while True:
		socketio.sleep(.00000100)


if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
