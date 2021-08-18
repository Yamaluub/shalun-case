import os
import json
import traceback

InverterPath='./Inverter.json'
	
def setInverterOFF():
	global InverterOn	
	data={}
	try:	
		InverterOn = False
		data['InverterOn']=False
		with open(InverterPath, 'w') as outfile:
			json.dump(data, outfile)
				
		print "InverterOn", InverterOn
		
		data['success']=True
		data['note']=""
	except:
		data['success']=False
		data['note']=traceback.format_exc()

	return data

setInverterOFF()	
