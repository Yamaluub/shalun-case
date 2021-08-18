import os
import json
import traceback

InverterPath='./Inverter.json'
	
def setInverterON():
	global InverterOn	
	data={}
	try:	
		InverterOn = True
		data['InverterOn']=True
		with open(InverterPath, 'w') as outfile:
			json.dump(data, outfile)
				
		print "InverterOn", InverterOn
		
		data['success']=True
		data['note']=""
	except:
		data['success']=False
		data['note']=traceback.format_exc()

	return data

setInverterON()	
