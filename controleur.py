# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 16:36:47 2022

@author: armand
"""

import json
import os
import platform
import datetime
import time
import threading
import subprocess
from pysnmp.hlapi import *
import pysnmp.hlapi as hlapi

taches = {}
PATH_equipement = "racine/equipements/"

def FormatTime():
    now = datetime.datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time = now.strftime("%H-%M-%S")
    return day+"-"+month+"-"+year+"-"+time

def initialisation():
    liste_equipements = os.listdir(PATH_equipement)
    for equipement in liste_equipements:
        with open(PATH_equipement+equipement+"/equipement.json","r") as file_equipement:
            adresse_ip = json.load(file_equipement)["IP"]
        file_equipement.close()
        for procedure in os.listdir(PATH_equipement+equipement+"/procedures/"):
            if procedure == "connexion.json":
                with open(PATH_equipement+equipement+"/procedures/connexion.json","r") as file_connexion:
                    connexion = json.load(file_connexion)
                file_connexion.close()
            elif procedure == "test-ping.json":
                with open(PATH_equipement+equipement+"/procedures/test-ping.json","r") as file_testping:
                    test_ping = json.load(file_testping)
                file_testping.close()
                taches[PATH_equipement+equipement+"/procedures/test-ping.json"] = 1
                new_thread = threading.Thread(target=testping,args=(adresse_ip,test_ping,PATH_equipement+equipement+"/resultats/test-ping.json",taches[PATH_equipement+equipement+"/procedures/test-ping.json"]))
                new_thread.start()
                print("Starting "+PATH_equipement+equipement+"/procedures/"+procedure)
            else:
                with open(PATH_equipement+equipement+"/procedures/"+procedure,"r") as file_proceduresnmp:
                    test_snmp = json.load(file_proceduresnmp)
                file_proceduresnmp.close()
                taches[PATH_equipement+equipement+"/procedures/"+procedure] = 1
                new_thread = threading.Thread(target=testsnmp,args=(adresse_ip,test_snmp,connexion,PATH_equipement+equipement+"/resultats/"+procedure,taches[PATH_equipement+equipement+"/procedures/"+procedure]))
                new_thread.start()
                print("Starting "+PATH_equipement+equipement+"/procedures/"+procedure)
            
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
            resT0 = json.load(outfile)["Result"][0]
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
                    json.dump({"FQDN procedure" : procedure["FQDN procedure"],"Frequence" : procedure["Frequence"],"Nb valeurs" : procedure["Nb valeurs"],"Unite" : procedure["Unite"],"Result" : [1]},outfile)
                else:
                    json.dump({"FQDN procedure" : procedure["FQDN procedure"],"Frequence" : procedure["Frequence"],"Nb valeurs" : procedure["Nb valeurs"],"Unite" : procedure["Unite"],"Result" : [0]},outfile)
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
        split = chemin.split("/")
        with open(split[0]+"/"+split[1]+"/"+split[2]+"/"+split[3]+"/test-ping.json","r") as resultat_ping:
            res_ping = json.load(resultat_ping)["Result"][0]
        resultat_ping.close()
        if res_ping:
            time.sleep(procedure["Frequence"])
            now = FormatTime()
            if connexion["Version"] == "V2":
                auth = hlapi.CommunityData(connexion["Communaute"],mpModel=1)
            elif connexion["Version"] == "V3":
                auth = hlapi.CommunityData(connexion["Communaute"]) # a faire en V3
            # errorIndication, errorStatus, errorIndex, varBinds = cmdgen.getCmd(cmdgen.SnmpEngine(),auth,cmdgen.UdpTransportTarget((adresse, 161)),cmdgen.ObjectIdentifier(procedure["OID"]),lookupMib=False,)
            data = hlapi.ObjectType(hlapi.ObjectIdentity(procedure["OID"]))
            handler = hlapi.getCmd(hlapi.SnmpEngine()
                , auth
                , hlapi.UdpTransportTarget((adresse, 161))
                , hlapi.ContextData()
                , lookupMib=False
                , *data)
            errorIndication, errorStatus, errorIndex, varBinds = next(handler)
            with open(chemin,"r") as outfile:
                results = json.load(outfile)
            outfile.close()
            with open(chemin,"w") as outfile:
                if len(results["Result"]) == procedure["Nb valeurs"]:
                    results["Result"].pop(0)
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
                if len(results["Result"]) == procedure["Nb valeurs"]:
                    results["Result"].pop(0)
                results["Result"].append((0,now))
                json.dump(results,outfile)
                # for oid, val in varBinds:
                #     results["Result"].append([val,now])
            outfile.close()
        return restart(chemin)

def restart(tache):
    chemin = tache.split("/")
    equipement = chemin[2]
    with open(PATH_equipement+equipement+"/equipement.json","r") as file_equipement:
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
        new_thread = threading.Thread(target=testsnmp(),args=(adresse_ip,test_snmp,connexion,PATH_equipement+equipement+"/resultats/"+procedure,taches[PATH_equipement+equipement+"/procedures/"+procedure]))
        new_thread.start()
        
def garbage(tache):
    chemin = tache.split("/")
    equipement = chemin[2]
    procedure = chemin[4][0:-5]
    taches.pop(PATH_equipement+equipement+"/procedures/"+procedure+".json")
    
def LoadProc(secondes):
    while True:
        time.sleep(secondes)
        liste_equipements = os.listdir(PATH_equipement)
        for equipement in liste_equipements:
            with open(PATH_equipement+equipement+"/equipement.json","r") as file_equipement:
                adresse_ip = json.load(file_equipement)["IP"]
            file_equipement.close()
            for procedure in os.listdir(PATH_equipement+equipement+"/procedures/"):
                if procedure == "connexion.json":
                    with open(PATH_equipement+equipement+"/procedures/connexion.json","r") as file_connexion:
                        connexion = json.load(file_connexion)
                    file_connexion.close()
                elif procedure == "test-ping.json" and [PATH_equipement+equipement+"/procedures/"+procedure,1] not in taches:
                    with open(PATH_equipement+equipement+"/procedures/test-ping.json","r") as file_testping:
                        test_ping = json.load(file_testping)
                    file_testping.close()
                    taches[PATH_equipement+equipement+"/procedures/test-ping.json"] = 1
                    new_thread = threading.Thread(target=testping,args= (adresse_ip,test_ping,PATH_equipement+equipement+"/resultats/test-ping.json",taches[PATH_equipement+equipement+"/procedures/test-ping.json"]))
                    new_thread.start()
                    print("Starting "+PATH_equipement+equipement+"/procedures/"+procedure)
                elif [PATH_equipement+equipement+"/procedures/"+procedure,1] not in taches:
                    with open(PATH_equipement+equipement+"/procedures/"+procedure,"r") as file_proceduresnmp:
                        test_snmp = json.load(file_proceduresnmp)
                    file_proceduresnmp.close()
                    taches[PATH_equipement+equipement+"/procedures/"+procedure] = 1
                    new_thread = threading.Thread(target=testsnmp(),args=(adresse_ip,test_snmp,connexion,PATH_equipement+equipement+"/resultats/"+procedure,taches[PATH_equipement+equipement+"/procedures/"+procedure]))
                    new_thread.start()
                    print("Starting "+PATH_equipement+equipement+"/procedures/"+procedure)
    
def KillTask(key):
        taches[key] = 0
        
def KillAll():
    print("Killing all process")
    for element in taches:
        print("Killing : "+element)
        taches[element] = 0

initialisation()

# LoadProc(10)

time.sleep(20)

KillAll()