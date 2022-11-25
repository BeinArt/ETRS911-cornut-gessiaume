# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 16:36:47 2022

@author: armand
"""

import json
import os
import socket
import platform
import datetime
import time
import threading
import subprocess
import pysnmp.hlapi as pysnmp
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import cmdgen

taches = {}
PATH_equipement = "racine/equipements/"

def GenerateOID(OID):
    liste = []
    split = OID.split(".")
    for element in split:
        liste.append(int(element))
    return liste

def FormatTime():
    now = datetime.datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time = now.strftime("%H-%M-%S")
    return day+"-"+month+"-"+year+"-"+time
            
def testping(adresse,procedure,chemin,status):
    if status != 1:
        garbage(chemin)
        print("Process killed : "+chemin)
        return "Process killed : "+chemin
    else:
        time.sleep(procedure["Frequence"])
        param = '-n' if platform.system().lower()=='windows' else '-c'
        command = ['ping',param,'1',adresse]
        res = subprocess.call(command)
        with open(chemin,"r") as outfile:
            try:
                resT0 = json.load(outfile)["Result"][0]
            except:
                resT0 = 0
        outfile.close()
        now = FormatTime()
        if os.path.exists(chemin):
            if resT0 == 0 and res == 0:
                with open("racine/logs/"+procedure["FQDN procedure"]+"."+str(now)+".json","w") as outfile:
                    json.dump({"FQDN procedure" : procedure["FQDN procedure"],"Type" : "Info", "Datetime" : str(now), "Analyse" : "Equipement connected"}, outfile)
                outfile.close()
            elif resT0 == 1 and res != 0:
                with open("racine/logs/"+procedure["FQDN procedure"]+"."+str(now)+".json","w") as outfile:
                    json.dump({"FQDN procedure" : procedure["FQDN procedure"],"Type" : "Critical", "Datetime" : str(now), "Analyse" : "Equipement disconnected"}, outfile)
                outfile.close()
            with open(chemin,"w") as outfile:
                if res == 0:
                    json.dump({"FQDN procedure" : procedure["FQDN procedure"],"Frequence" : procedure["Frequence"],"Nbvaleurs" : procedure["Nbvaleurs"],"Unite" : procedure["Unite"],"Result" : [1]},outfile)
                else:
                    json.dump({"FQDN procedure" : procedure["FQDN procedure"],"Frequence" : procedure["Frequence"],"Nbvaleurs" : procedure["Nbvaleurs"],"Unite" : procedure["Unite"],"Result" : [0]},outfile)
            outfile.close()
            print("Next call : "+chemin)
            return restart(chemin)
        else:
            garbage(chemin)
            return "Non existant path"

def testsnmp(adresse,procedure,connexion,chemin,status):
    if status != 1:
        garbage(chemin)
        print("Process killed : "+chemin)
        return "Process killed : "+chemin
    else:
        if True:
            time.sleep(procedure["Frequence"])
            if connexion["Version"] == "V2":
                try:
                    auth = pysnmp.CommunityData(connexion["Communaute"],mpModel=1)
                    snmpEngine = pysnmp.SnmpEngine()
                    data = pysnmp.ObjectType(pysnmp.ObjectIdentity(procedure["OID"]))
                    for (errorIndication, errorStatus, errorIndex, varBinds) in pysnmp.getCmd(snmpEngine,
                                                                                        auth,
                                                                                        pysnmp.UdpTransportTarget((adresse, 161)),
                                                                                        pysnmp.ContextData(),
                                                                                        data):
                        if errorIndication or errorStatus:
                            print(errorIndication or errorStatus)
                            res = "0"
                            break
                        else:
                            for oid,val in varBinds:
                                if procedure["Unite"] != "String":
                                    res = str(val)
                                    res = int(res)
                                else:
                                    res = str(val)
                except:
                    res = "0"
            elif connexion["Version"] == "V3":
                def cbFun(snmpEngine, sendRequestHandle, errorIndication,
                          errorStatus, errorIndex, varBinds, cbCtx):
                    if errorIndication:
                        print(errorIndication)
                        with open(procedure["FQDN"],"w") as outfile:
                            outfile.write("0")
                        outfile.close()
                    elif errorStatus:
                        print('%s at %s' % (errorStatus.prettyPrint(),
                                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                        with open(procedure["FQDN"],"w") as outfile:
                            outfile.write("0")
                        outfile.close()
                    else:
                        for oid, val in varBinds:
                            with open(procedure["FQDN"],"w") as outfile:
                                outfile.write(val.prettyPrint())
                            outfile.close()
                snmpEngine = engine.SnmpEngine()

                config.addV3User(
                    snmpEngine, connexion["User"],
                    config.usmHMACSHAAuthProtocol, connexion["Password"],
                    config.usmAesCfb128Protocol, connexion["Key"]
                )

                config.addTargetParams(snmpEngine, 'controleur', connexion["User"], 'authPriv')
                config.addTransport(
                    snmpEngine,
                    udp.domainName,
                    udp.UdpSocketTransport().openClientMode()
                )

                config.addTargetAddr(
                    snmpEngine, 'equipement',
                    udp.domainName, (adresse, 161),
                    'controleur'
                )
                
                cmdgen.GetCommandGenerator().sendVarBinds(
                    snmpEngine,
                    'equipement',
                    None, '',
                    [(GenerateOID(procedure["OID"]), None)],
                    cbFun
                )
                
                try:
                    snmpEngine.transportDispatcher.runDispatcher()
                    config.delTransport(
                        snmpEngine,
                        udp.domainName
                    ).closeTransport()
                    
                    with open(procedure["FQDN"],"r") as outfile:
                        res = outfile.readline()
                    outfile.close()
                    
                    os.remove(procedure["FQDN"])
                except:
                    res = "0"

            
            with open(chemin,"r") as outfile:
                results = json.load(outfile)
            outfile.close()
            results["FQDN"] = procedure["FQDN"]
            results["OID"] = procedure["OID"]
            results["Frequence"] = procedure["Frequence"]
            results["Unite"] = procedure["Unite"]
            results["Nbvaleurs"] = procedure["Nbvaleurs"]
            with open(chemin,"w") as outfile:
                while len(results["Result"]) >= procedure["Nbvaleurs"]:
                    results["Result"].pop(0)
                now = FormatTime()
                results["Result"].append((res,now))
                json.dump(results,outfile)
                # for oid, val in varBinds:
                #     results["Result"].append([val,now])
                
            outfile.close()
        else:
            with open(chemin,"r") as outfile:
                results = json.load(outfile)
            outfile.close()
            with open(chemin,"w") as outfile:
                while len(results["Result"]) >= procedure["Nbvaleurs"]:
                    results["Result"].pop(0)
                results["Result"].append((res,now))
                json.dump(results,outfile)
                # for oid, val in varBinds:
                #     results["Result"].append([val,now])
            outfile.close()
        print("Next call : "+chemin)
        return restart(chemin)

def restart(tache):
    chemin = tache.split("/")
    equipement = chemin[2]
    with open(PATH_equipement+equipement+"/"+equipement+".json","r") as file_equipement:
            adresse_ip = json.load(file_equipement)["IP"]
    file_equipement.close()
    with open(PATH_equipement+equipement+"/procedures/connexion.json","r") as file_connexion:
        connexion = json.load(file_connexion)
    file_connexion.close()
    procedure = chemin[4][0:-5]
    if procedure == "test-ping":
        with open(PATH_equipement+equipement+"/procedures/test-ping.json","r") as file_testping:
            test_ping = json.load(file_testping)
        file_testping.close()
        new_thread = threading.Thread(target=testping,args=(adresse_ip,test_ping,PATH_equipement+equipement+"/resultats/test-ping.json",taches[PATH_equipement+equipement+"/procedures/test-ping.json"]))
        new_thread.start()
    else:
        with open(PATH_equipement+equipement+"/procedures/"+procedure+".json","r") as file_proceduresnmp:
            test_snmp = json.load(file_proceduresnmp)
        file_proceduresnmp.close()
        new_thread = threading.Thread(target=testsnmp,args=(adresse_ip,test_snmp,connexion,PATH_equipement+equipement+"/resultats/"+procedure+".json",taches[PATH_equipement+equipement+"/procedures/"+procedure+".json"]))
        new_thread.start()
        
def garbage(tache):
    chemin = tache.split("/")
    equipement = chemin[2]
    procedure = chemin[4][0:-5]
    taches.pop(PATH_equipement+equipement+"/procedures/"+procedure+".json")
    
def LoadProc(secondes,status):
    if status != 1:
        print("Process killed : Load process")
        taches.pop("LoadProcess")
    else:
        time.sleep(secondes)
        liste_equipements = os.listdir(PATH_equipement)
        for equipement in liste_equipements:
            with open(PATH_equipement+equipement+"/"+equipement+".json","r") as file_equipement:
                adresse_ip = json.load(file_equipement)["IP"]
            file_equipement.close()
            for procedure in os.listdir(PATH_equipement+equipement+"/procedures/"):
                if procedure == "connexion.json":
                    with open(PATH_equipement+equipement+"/procedures/connexion.json","r") as file_connexion:
                        connexion = json.load(file_connexion)
                    file_connexion.close()
                elif procedure == "test-ping.json" and (PATH_equipement+equipement+"/procedures/"+procedure not in taches or taches[PATH_equipement+equipement+"/procedures/"+procedure] == 0):
                    with open(PATH_equipement+equipement+"/procedures/test-ping.json","r") as file_testping:
                        test_ping = json.load(file_testping)
                    file_testping.close()
                    taches[PATH_equipement+equipement+"/procedures/test-ping.json"] = 1
                    new_thread = threading.Thread(target=testping,args=(adresse_ip,test_ping,PATH_equipement+equipement+"/resultats/test-ping.json",taches[PATH_equipement+equipement+"/procedures/test-ping.json"]))
                    new_thread.start()
                    print("Starting : "+PATH_equipement+equipement+"/procedures/"+procedure)
                elif PATH_equipement+equipement+"/procedures/"+procedure not in taches or taches[PATH_equipement+equipement+"/procedures/"+procedure] == 0:
                    with open(PATH_equipement+equipement+"/procedures/"+procedure,"r") as file_proceduresnmp:
                        test_snmp = json.load(file_proceduresnmp)
                    file_proceduresnmp.close()
                    taches[PATH_equipement+equipement+"/procedures/"+procedure] = 1
                    new_thread = threading.Thread(target=testsnmp,args=(adresse_ip,test_snmp,connexion,PATH_equipement+equipement+"/resultats/"+procedure,taches[PATH_equipement+equipement+"/procedures/"+procedure]))
                    new_thread.start()
                    print("Starting : "+PATH_equipement+equipement+"/procedures/"+procedure)
        print("Next call : LoadProcess")
        return LoadProc(secondes, taches["LoadProcess"])
                    
def ControlLoadProc(secondes,status):
    if status == 1:
        if "LoadProcess" not in taches or taches["LoadProcess"] == 0:
            print("Starting : Loading process")
            taches["LoadProcess"] = status
            new_thread = threading.Thread(target=LoadProc,args=(secondes,status))
            new_thread.start()
    elif status == 0:
        print("Killing : Loading process")
        taches["LoadProcess"] = status
    
def KillTask(key):
        taches[key] = 0
        
def KillAll():
    print("Killing all process")
    for element in taches:
        print("Killing : "+element)
        taches[element] = 0
        
def CommandCenter():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('0.0.0.0', 8089))
    serversocket.listen(5) # become a server socket, maximum 5 connections
    while True:
        connection, address = serversocket.accept()
        buf = connection.recv(64)
        if len(buf) > 0:
            decode = buf.decode(encoding='utf-8')
            print(decode)
            if decode == "Restart":
                for i in range(0,5):
                    KillAll()
                    time.sleep(1)
                ControlLoadProc(5, 1)
            elif decode == "Stop":
                for i in range(0,5):
                    KillAll()
                    time.sleep(1)
            elif decode == "Start":
                ControlLoadProc(5, 1)
            split = decode.split("@")
            if split[0] == "Reload":
                for procedure in os.listdir(PATH_equipement+"/"+split[1]+"/procedures/"):
                    if procedure != "connexion.json":
                        KillTask(PATH_equipement+split[1]+"/procedures/"+procedure)

# initialisation()
ControlLoadProc(5, 1)
new_thread = threading.Thread(target=CommandCenter)
new_thread.start()