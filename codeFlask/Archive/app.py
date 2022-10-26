# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 13:59:21 2022

@author: user
"""
from datetime import datetime
from flask import Flask, request, make_response, abort, redirect, render_template, jsonify
app = Flask(__name__)
 
tempc = 0.0
temp_sensor = "/sys/bus/w1/devices/28-000007013b3f/w1_slave"
 
 
 
def temp_raw():
    f = open(temp_sensor, "r")
    lines = f.readlines()
    f.close()
    return lines
 
def read_tempc():
    lines = temp_raw()
    temp = lines[1].strip()[-5:]
    tempc = float(temp)/1000
    tempc = round(tempc, 1)
    return tempc
 
 
@app.route('/', methods = ['GET'])
def temp():
        temp = datetime.now().time()
 
        return render_template('temp.html', temp=temp)
    
@app.route('/ajax', methods = ['GET'])
def ajax():
        temp = datetime.now().time()
  
        return '{}'.format(temp)
    
app.run(host="localhost", port=int("5000"))