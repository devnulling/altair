import socket
import struct
import time

class rotator:
	def __init__(self, ipaddr, port=5000):
		
		self.cmds = {
			"servo_on": b'\x07',
			"servo_off": b'\x08', 
			"nsr": b'\x33',
			"move": b'\x3a',
			"timeout_off": b'\x88'
		}

		self.addr = (ipaddr, port)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.settimeout(0.2)
		self.transact(self.cmds['timeout_off'])
		self.transact(self.cmds['servo_off'])
		self.transact(self.cmds['servo_on'])
		self.transact(self.cmds['timeout_off'])

	def cleanup(self):
		print("cleaning up")
		self.sock.close()

	#TODO FIXME need to deal with partial and unsolicited responses.
	def transact(self, cmd):
		#try:
		#    self.sock.recvfrom(1024)
		#except:
		#    pass
		self.sock.sendto(cmd, self.addr)
		#sometimes when the thing just wakes up or something it only sends back one byte, the
		#command you sent to it. not sure if that's a NACK or a "hang on a minute" or what.
		return self.sock.recvfrom(1024)[0]

	def parse_status(self, cmd=b'\x33'):
		#byte 5 lower 3 bits appears to be 7 for "servo disabled", 0 (also maybe 8) for "servo enabled"
		kv = 763.55
		lsb = 360/(2**24)
		status = self.transact(cmd)
		print("Status: [%s]" % " ".join(["%02x" % b for b in status]))
		err = status[0] == b'\x77'
		if err:
			self.transact(self.cmds['servo_off'])
			raise Exception("Shit has gone bad!")

		pos_int = struct.unpack('>i', b'\x00' + status[1:4])[0]
		pos_deg = pos_int * lsb

		return pos_deg

	def get_pos(self):
		return self.parse_status()

	def hb(self):
		resp = self.transact(self.cmds['nsr'])
		# self.parse_status(resp)
		# time.sleep(0.1)
		return resp

	# rate is not working. always about 30deg/s
	# if you pull the stow pin, though, or it goes into fault,
	# that el drive moves WAY faster than 30d/s.
	def move(self, pos, rate=20):
		kv = 763.55
		lsb = 360/(2**24)

		pos_cmd = struct.pack('>i', round(pos/lsb))[1:]
		rate_cmd = struct.pack('>h', round(rate*kv))
		cmd = self.cmds['move'] + pos_cmd + rate_cmd + b'\x00\x08'
		print("move: %s" % cmd)
		return self.parse_status(cmd)

def keep_alive(obj, run_event):
	ct = 0
	while run_event.is_set():
		print("[INFO] - sending hb %s" % ct)
		resp = obj.hb()
		print("Status: [%s]" % " ".join(["%02x" % b for b in resp]))
		ct += 1
		time.sleep(0.3)