import zmq 
import time
import json

# 72.034*

zmq_server = "127.0.0.1"
zmq_port = 9005
zmq_endpoint = "tcp://" + zmq_server + ":" + str(zmq_port)
print("[INFO] - Connecting to: %s" % zmq_endpoint)

def sendcmd(mysocket, mycmd):
	print("[INFO] - sending: %s" % mycmd)
	mysocket.send(mycmd.encode())
	rxdata = mysocket.recv()
	return rxdata.decode()

try:
	zsock = zmq.Context().socket(zmq.REQ)
	zsock.setsockopt( zmq.RCVTIMEO, 1000 )
	zsock.connect(zmq_endpoint)

	cmd = json.dumps({ "cmd": "servo", "value": "on" })
	resp = sendcmd(zsock, cmd)
	print("[INFO] - server response: %s" % resp)

	for idx in range(0,360):
		cmd = json.dumps({ "cmd": "moveaz", "value": idx })
		resp = sendcmd(zsock, cmd)
		print("[INFO] - server response: %s" % resp)
		time.sleep(1)

	for idx in range(360, -1, -1):
		cmd = json.dumps({ "cmd": "moveaz", "value": idx })
		resp = sendcmd(zsock, cmd)
		print("[INFO] - server response: %s" % resp)
		time.sleep(1)

	cmd = json.dumps({ "cmd": "servo", "value": "off" })
	resp = sendcmd(zsock, cmd)
	print("[INFO] - server response: %s" % resp)

except zmq.Again:
	print("[ERROR] - Unable to connect or timeout.")
