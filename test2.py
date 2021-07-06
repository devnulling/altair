import zmq 
import time
import json

zmq_server = "127.0.0.1"
zmq_port = 9005
zmq_endpoint = "tcp://" + zmq_server + ":" + str(zmq_port)
print("[INFO] - Connecting to: %s" % zmq_endpoint)

def sendcmd(mysocket, mycmd):
	print("sending: %s" % mycmd)
	mysocket.send(mycmd.encode())
	rxdata = mysocket.recv()
	return rxdata.decode()

try:
	zsock = zmq.Context().socket(zmq.REQ)
	zsock.setsockopt( zmq.RCVTIMEO, 1000 )
	zsock.connect(zmq_endpoint)




	# cmd = json.dumps({ "cmd": "servoaz", "value": "off" })
	# resp = sendcmd(zsock, cmd)
	# print("server response: %s" % resp)

	cmd = json.dumps({ "cmd": "getpos", "value": "az" })
	resp = sendcmd(zsock, cmd)
	print("server response: %s" % resp)
	
	cmd = json.dumps({ "cmd": "getpos", "value": "el" })
	resp = sendcmd(zsock, cmd)
	print("server response: %s" % resp)
	time.sleep(5)

	cmd = json.dumps({ "cmd": "servoaz", "value": "on" })
	resp = sendcmd(zsock, cmd)
	print("server response: %s" % resp)

	cmd = json.dumps({ "cmd": "servoel", "value": "on" })
	resp = sendcmd(zsock, cmd)
	print("server response: %s" % resp)

	
	cmd = json.dumps({ "cmd": "moveel", "value": 0 })
	resp = sendcmd(zsock, cmd)
	print("server response: %s" % resp)
	time.sleep(5)

	cmd = json.dumps({ "cmd": "moveel", "value": -45 })
	resp = sendcmd(zsock, cmd)
	print("server response: %s" % resp)
	time.sleep(5)

	cmd = json.dumps({ "cmd": "moveel", "value": 0 })
	resp = sendcmd(zsock, cmd)
	print("server response: %s" % resp)
	time.sleep(5)

	cmd = json.dumps({ "cmd": "moveel", "value": 45 })
	resp = sendcmd(zsock, cmd)
	print("server response: %s" % resp)
	time.sleep(5)

	cmd = json.dumps({ "cmd": "moveel", "value": 0 })
	resp = sendcmd(zsock, cmd)
	print("server response: %s" % resp)
	time.sleep(5)


	# cmd = json.dumps({ "cmd": "moveaz", "value": 90 })
	# resp = sendcmd(zsock, cmd)
	# print("server response: %s" % resp)
	# time.sleep(5)

	# cmd = json.dumps({ "cmd": "moveaz", "value": 45 })
	# resp = sendcmd(zsock, cmd)
	# print("server response: %s" % resp)
	# time.sleep(5)

	# cmd = json.dumps({ "cmd": "moveaz", "value": 180 })
	# resp = sendcmd(zsock, cmd)
	# print("server response: %s" % resp)
	# time.sleep(5)

	# cmd = json.dumps({ "cmd": "moveaz", "value": 90 })
	# resp = sendcmd(zsock, cmd)
	# print("server response: %s" % resp)
	# time.sleep(5)

	# cmd = json.dumps({ "cmd": "moveaz", "value": 0 })
	# resp = sendcmd(zsock, cmd)
	# print("server response: %s" % resp)
	# time.sleep(5)

	

	
	


	cmd = json.dumps({ "cmd": "servoaz", "value": "off" })
	resp = sendcmd(zsock, cmd)
	print("server response: %s" % resp)

	cmd = json.dumps({ "cmd": "servoel", "value": "off" })
	resp = sendcmd(zsock, cmd)
	print("server response: %s" % resp)

except zmq.Again:
	print("[ERROR] - Unable to connect or timeout.")
