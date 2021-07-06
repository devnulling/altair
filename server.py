import zmq
import time
import threading
import json

from pylibs.rotator import rotator, keep_alive

def main():
	run_event = threading.Event()
	run_event.set()

	az_ip = "10.10.10.168"
	el_ip = "10.10.10.169"
	port = 5000

	zmq_server = "127.0.0.1"
	zmq_port = 9005
	zmq_endpoint = "tcp://" + zmq_server + ":" + str(zmq_port)
	print("[INFO] - Connecting to: %s" % zmq_endpoint)

	zsock = zmq.Context().socket(zmq.REP)
	zsock.bind(zmq_endpoint)

	print("[INFO] - init AZ ip: %s" % az_ip)
	az = rotator(az_ip, port)

	print("[INFO] - init el ip: %s" % el_ip)
	el = rotator(el_ip, port)


	t1 = threading.Thread(target=keep_alive, args=(az, run_event))
	t1.start()
	print("[INFO] - az hb thread started")

	t2 = threading.Thread(target=keep_alive, args=(el, run_event))
	t2.start()
	print("[INFO] - el hb thread started")

	try:
		while 1:
			rxdata = zsock.recv()
			print("RX: %s"  % rxdata.decode())
			zsock.send(rxdata)

			rxj = json.loads(rxdata.decode())
			cmd = rxj['cmd']
			val = rxj['value']

			if cmd == "moveaz":
				print("[INFO] - Moving az to: %s" % val)
				resp = az.move(val, 20)
				print("resp: %s" % resp)
			elif cmd == "moveel":
				print("[INFO] - Moving el to: %s" % val)
				resp = el.move(val, 20)
				print("resp: %s" % resp)
			elif cmd == "servoaz":
				if val == "on":
					print("[INFO] - turning az servo on")
					resp = az.transact(az.cmds['servo_on'])
					print("[INFO] - resp: %s" % resp)
				else:			
					print("[INFO] - turning az servo off")
					resp = az.transact(az.cmds['servo_off'])
					print("[INFO] - resp: %s" % resp)

			elif cmd == "servoel":
				if val == "on":
					print("[INFO] - turning el servo on")
					resp = el.transact(el.cmds['servo_on'])
					print("[INFO] - resp: %s" % resp)
				else:			
					print("[INFO] - turning el servo off")
					resp = el.transact(el.cmds['servo_off'])
					print("[INFO] - resp: %s" % resp)

			elif cmd == "getpos":

				if val == "az":
					print("[INFO] - AZ POS: %s" % az.get_pos())
				elif val == "el": 
					print("[INFO] - EL POS: %s" % el.get_pos())
				
			else: 
				print("[INFO] - command no found")

			
			
			
	except KeyboardInterrupt:
		print("[INFO] - killing threads....")
		run_event.clear()
		t1.join()
		t2.join()
		print("[INFO] - done")

if __name__ == '__main__':
    main()