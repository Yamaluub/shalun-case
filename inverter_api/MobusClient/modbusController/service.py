#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import Flask,request, Response

import json
import datetime
import os
import time
import logging
import traceback

import threading
import modbusCtrl

app = Flask(__name__)


def initService(app):
	print "init"
	
	#mobus client start
	try:
		th = threading.Thread(target=modbusCtrl.controlThread)
		th.start() 
		print "thread client start"
	except:
		print "Error: unable to start thread Client"

	
initService(app)

			
@app.route("/")
def hello():
	global fanControllerLogger
	data={}
	data['product']="Modbus Client"
	data['success']=True
	return Response(json.dumps(data),  mimetype='application/json')

@app.route("/cakes")
def cakes():
    return 'Yummy cakes!'
    
 
@app.route("/getInfo")
def getInfo():
	data={}
	data=modbusCtrl.getInfo()
	return Response(json.dumps(data),  mimetype='application/json')
	
@app.route("/getStatus")
def getStatus():
	data={}
	data=modbusCtrl.getStatus()
	return Response(json.dumps(data),  mimetype='application/json')
	

@app.route("/setInverter",methods=['POST'])
def setMeterReal():
	jsonObj=request.json
	data=modbusCtrl.setInverter(jsonObj)
	return Response(json.dumps(data),  mimetype='application/json')


if __name__ == "__main__":
	app.run('0.0.0.0',6688)

