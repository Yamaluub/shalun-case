#import pymodbus
#import serial

from pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU cient instance
from pymodbus.register_read_message import ReadInputRegistersResponse

import time
import traceback
import logging
import json
import random

connStatus = "init"  
connection = False   
InverterOn = False
InverterPath='./Inverter.json'
MobusLogPath  = '../log/MobusClient.log'

logging.basicConfig(
	level=logging.WARNING,
	format='%(asctime)s]:%(message)s', 
	datefmt='%Y-%m-%d %H:%M:%S',
	filename=MobusLogPath
	)


def getInfo():
	global connection,connStatus,InverterOn
	data={}
	data['connection']= connection
	data['InverterOn']= InverterOn
	data['connStatus']= connStatus
	print 'data=',data
	
	try:	
		with open('../version', 'r') as verfile:
			version=verfile.read().replace('\n', '')
		data['version']=version
	except:
		data['version']="N/A"
		
	return data	
	
def getStatus():
	global pwr,volt,ampr
	data={}
	data['LoadPower']  = pwr
	data['LoadVolt']   = volt
	data['LoadCurrent']= ampr
	print 'data=',data
			
	return data	


def startClient():
	global client, connection
	logging.basicConfig()
	log = logging.getLogger()
	log.setLevel(logging.DEBUG)	
	
	logging.warning('Mobus Client Start')

	client = ModbusClient(
		method='rtu',
		port='/dev/ttyUSB0',
		stopbits=1,
		bytesize=8,
		party ='N',
		baudrate=9600,
		timeout=1
		)

	#connect to the serial modbus server
	connection = client.connect()
	time.sleep(0.2)
	print "connection :",connection
	
	return True
	

def controlThread():
	global client, connStatus, InverterOn
	connStatus="init"	
				
	while True:
		try:
			if connStatus=="init":
				if startClient():
					connStatus="hacker"
			elif connStatus=="hacker":
				if sendHacker():
					connStatus="display"
					time.sleep(2)
			elif connStatus=="display":
				if sendDisplay():
					time.sleep(2)
					connStatus="hacker"
					#time.sleep(2)
			
		except:
			print traceback.format_exc()				
			time.sleep(1)
	
	
def setInverter(jsonObj):
	global InverterOn
	print jsonObj
	data={}
	try:		
		if jsonObj['InverterOn']==True:		
			if InverterOn:
				print "InverterOn already Power ON"
				logging.warning('InverterOn already Power ON')
				data['InverterOn']=True
				data['success']=True
				data['note']=""
			else:				
				InverterOn = True
				data['InverterOn']=True
				with open(InverterPath, 'w') as outfile:
					json.dump(data, outfile)
						
				data['success']=True
				data['note']=""
		else :
			if not InverterOn:
				print "InverterOn already Power OFF"
				logging.warning('InverterOn already Power OFF')
				data['InverterOn']=False				
				data['success']=True
				data['note']=""
			else:				
				InverterOn = False
				data['InverterOn']=False
				with open(InverterPath, 'w') as outfile:
					json.dump(data, outfile)
					
				data['success']=True
				data['note']=""
	except:
		data['success']=False
		data['note']=traceback.format_exc()

	return data
	
def sendHacker():	
	global client, InverterOn	
	
	# read the Inverter status from Inverter.json
	try:
		InverterContent = json.load(open(InverterPath))
		InverterOn = InverterContent['InverterOn']
		print "InverterOn", InverterOn
		logging.warning('InverterOn is Power ON')
	except:
		traceback.print_exc()
		
	try:		
		if (InverterOn):
			value=client.write_register(271,1,unit=0x01) #address=0x010F(271D),data=1,slave id=0x01
			
			print "inverter is remote power on"
			return True
		else :
			value=client.write_register(271,2,unit=0x01)
			print "inverter is remote power off"
			logging.warning('InverterOn is Power OFF')
			return True
	except:
		print "inverter is control fail"		
		logging.warning('InverterOn is control fail')
		return False


def sendDisplay():
	global client,pwr,volt,ampr
	# Start add, num of reg to read, slave unit
	#value=client.read_input_registers(300,4,unit=0x01)
	
	value1=client.read_holding_registers(271,1,unit=0x01)  #remote power on/off
	value2=client.read_holding_registers(4613,4,unit=0x01) #address=1205H,number=4,slave id=0x01
																											   	#Protect Load Voltage/current/Watt(H,L)
	print(value1.registers)
	print(value2.registers)
	logging.warning(value1.registers)
	logging.warning(value2.registers)
	
	
	volt = value2.registers[0]
	amp = value2.registers[1]
	phw = value2.registers[2]<<8 
	plw = value2.registers[3]
	power =phw + plw 
	
	print(volt)
	'''
	print(amp)
	print(power)
	logging.warning(volt)
	logging.warning(amp)
	logging.warning(power)
	'''
		
	num = random.randint(1,12)
	ampr = amp + num
	logging.warning(ampr)
	print(ampr)
	
	pwr =  ampr * volt 
	logging.warning(pwr)
	
	if (amp < 30):
		pwr = 0
	else:	
		pwr = pwr / 100
	
	logging.warning(pwr)
	print(pwr)	
	
	time.sleep(1)	
			
	try:		
		value=client.write_register(9984,pwr,unit=2) #address=2700H,data=power,slave id=0x02
		value=client.write_register(9984,volt,unit=3) #address=2700H,data=amp,slave id=0x03
		value=client.write_register(9984,ampr,unit=4) #address=2700H,data=volt,slave id=0x04
	except:
		traceback.print_exc()
	
	return True																						
	
	   
#closes the underlying socket connection
#client.close()

#controlThread()
