import serial
import socket
import time
from pymavlink import mavutil
import parser
import math

port=1801
IP='0.0.0.0'
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((IP, port))
# ser = serial.Serial(
#  port='/dev/ttyACM1',
#  baudrate = 9600,
#  parity=serial.PARITY_NONE,
#  stopbits=serial.STOPBITS_ONE,
#  bytesize=serial.EIGHTBITS,
#  timeout=1
# )

master = mavutil.mavlink_connection("udpin:10.0.1.111:14552")

master.wait_heartbeat()
print("recieved heartbeat")

class NmeaMessage(object):

	def __init__(self):
		self.stamp=0 # Time Stamp
		self.gps_id=0 # GPS ID
		self.gps_time=0 # GPS time
		self.gps_week_number=20912 # GPS Week number
		self.fix_type=0 # fix type
		self.lat=0 # Lat
		self.long=0 # Long
		self.alt=0 # Altitude
		self.hdop=1 # HDOP
		self.vdop=1 # VDOP
		self.vn=0 # vn
		self.ve=0 # ve
		self.vd=0 # vd
		self.speed_acc=0.0001 # speed accuracy
		self.hori_acc=0.01 # hori accuracy
		self.vert_acc=0.01 # vertical accuracy
		self.number=7 # number of satellites
		self.yaw=4000 # yaw (cdeg)

	def add_message(self, nmea_string):

	    parsed_sentence = parser.parse_nmea_sentence(
	        nmea_string)
	    if not parsed_sentence:
	        
	        return False

	    else:
			if 'GGA' in parsed_sentence:
				data = parsed_sentence['GGA']
				if not math.isnan(data['utc_time']):
					self.gps_time=data['utc_time']
				self.fix_type = 3 #data['fix_type']
				latitude = data['latitude']
				if data['latitude_direction'] == 'S':
				    latitude = -latitude
				self.lat =1e7 * latitude

				longitude = data['longitude']
				if data['longitude_direction'] == 'W':
				    longitude = -longitude
				self.long =1e7 * longitude

				self.alt = data['altitude']
				self.hdop = data['hdop']
                                #print("hdop=", self.hdop)
                                self.vdop = data['hdop']
				self.number=data['num_satellites']
                                #print"n_sat=", (self.number)

			if 'VTG' in parsed_sentence:
			    data = parsed_sentence['VTG']
			    self.vn=data['speed'] * math.cos(data['true_course'])
			    self.ve=data['speed'] * math.sin(data['true_course'])

			   	

			if 'RMC' in parsed_sentence:
			    data = parsed_sentence['RMC']

			    #print("utc_time=", data['utc_time'])
			    if not math.isnan(data['utc_time']):
			    	self.gps_time=data['utc_time']

			    latitude = data['latitude']
			    if data['latitude_direction'] == 'S':
			        latitude = -latitude
			    self.lat = 1e7 * latitude
			    #print("latitude=", latitude)

			    longitude = data['longitude']
			    if data['longitude_direction'] == 'W':
			        longitude = -longitude
			    #print("longitude=", longitude)
			    self.long =1e7 * longitude
			    self.vn=data['speed']
			    self.ve=data['speed']
			    #print("ve=", data['speed'])
			    #self.alt = float('NaN')



			if 'HDT' in parsed_sentence:
				data = parsed_sentence['HDT']
				self.yaw=100*data['heading']
				


			else:
			    return False

if __name__ == '__main__':

	msg_mav=NmeaMessage()
	while True:
	   msg, adress=s.recvfrom(65515)
	   #msg=ser.readline()
	   #print(msg)

	   msg_mav.add_message(msg)
           #print("yaw=",msg_mav.yaw)
	   master.mav.gps_input_send(
	      msg_mav.stamp, # Timestamp
	      msg_mav.gps_id, # GPS ID
	      0, # Flags
	      msg_mav.gps_time, # GPS time
	      msg_mav.gps_week_number, # GPS Week number
	      msg_mav.fix_type, # fix type
	      msg_mav.lat, # Lat
	      msg_mav.long, # Long
	      0, #msg_mav.alt, # Altitude
	      msg_mav.hdop, # HDOP
	      msg_mav.vdop, # VDOP
	      msg_mav.vn, # vn
	      msg_mav.ve, # ve
	      msg_mav.vd, # vd
	      msg_mav.speed_acc, # speed accuracy
	      msg_mav.hori_acc, # hori accuracy
	      msg_mav.vert_acc, # vertical accuracy
	      msg_mav.number, # number of satellites
	      msg_mav.yaw # yaw (cdeg)
	   )
	   time.sleep(0.1)

	s.close()

