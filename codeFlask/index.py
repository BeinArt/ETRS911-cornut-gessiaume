# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 08:09:12 2022

@author: jbgessiaume
"""
#import pour Flask
from flask import Flask, render_template, request, redirect, jsonify

#import pour traitement
import os
from os import walk
import shutil
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
    #return 'Hello, World!'
    
@app.route('/ajout')
def ajout():
    return render_template('ajout.html')
    
@app.route('/actionAjout')
def actionAjout():
    FQDN = request.args.get('FQDN','')
    NomAffichage = request.args.get('NomAffichage','')
    Marque = request.args.get('Marque','')
    Modele = request.args.get('Modele','')
    IP = request.args.get('IP','')
    Client = request.args.get('Client','')
    OS = request.args.get('OS','')
    Localisation = request.args.get('Localisation','')
    VersionSNMP = request.args.get('VersionSNMP','')
    Communaute = request.args.get('Communaute','')
    User = request.args.get('User','')
    Password = request.args.get('Password','')
    Commentaire = request.args.get('Commentaire','')
    
    if(FQDN == ""):
        return redirect('http://localhost:5000/ajout?manque=FQDN')
    
    if(NomAffichage == ""):
        NomAffichage = FQDN
        
    if(Marque == ""):
        Marque = "Vide"
        
    if(Modele == ""):
        Modele = "Vide"
        
    if(IP == ""):
        return redirect('http://localhost:5000/ajout?manque=IP')
        
    if(Client == ""):
        Client = "Vide"
        
    if(Localisation == ""):
        Localisation = "Vide"
        
    if(VersionSNMP == ""):
        return redirect('http://localhost:5000/ajout?manque=VersionSNMP')
        
    if(Communaute == ""):
        return redirect('http://localhost:5000/ajout?manque=Communaute')
        
    if(User == ""):
        User = "Vide"
        
    if(Password == ""):
        Password = "Vide"
        
    if(Commentaire == ""):
        Commentaire = "Vide"
    
    
    print(FQDN)
    print(NomAffichage)
    print(Marque)
    print(Modele)
    print(IP)
    print(Client)
    print(OS)
    print(Localisation)
    print(VersionSNMP)
    print(Communaute)
    print(User)
    print(Password)
    print(Commentaire)
    
    #on se place dans le repertoire equipements
    print(os.getcwd())
    os.chdir("..\\racine\\equipements")
    print(os.getcwd())
    #creation du dossier
    os.mkdir(FQDN)
    
    #on rentre dans le dossier que l'on vient de créer
    os.chdir(".\\" + FQDN)
    print(os.getcwd())
    
    equipementJSON = f"{FQDN}.json"
    print(f"file name : {equipementJSON}")
    
    equipementjsonString = {"FQDN" : FQDN,"NomAffichage" : NomAffichage,"Marque" : Marque,"Modele" : Modele,"IP" : IP,"Client" : Client,"OS" : OS,"Localisation" : Localisation,"commentaire" : Commentaire}
    
    file = open(equipementJSON, "w")
    json.dump(equipementjsonString, file)
    file.close()
    
    #creation du dossier procedures
    os.mkdir("procedures")
    
    #creation du dossier resultats
    os.mkdir("resultats")
    
    #on rentre dans procedures
    os.chdir(".\\procedures")
    
    #creation fichier connexion.json
    connexionjson = "connexion.json"
    print("creation connexion.json")
    connexionjsonString = {"FQDN" : FQDN ,"Version" : VersionSNMP,"Communaute" : Communaute,"User" : User,"Password" : Password}

    
    file = open(connexionjson, "w")
    json.dump(connexionjsonString, file)
    file.close()
    
    #creation fichier test-ping.json dans procedures
    testpingjson = "test-ping.json"
    print("creation test-ping.json")
    testpingjsonString = {"FQDN procedure" : FQDN,"Frequence" : 10 ,"Nbvaleurs" : 1,"Unite" : "Bool"}
    
    file = open(testpingjson, "w")
    json.dump(testpingjsonString, file)
    file.close()

    os.chdir("..\\resultats")
    
    #creation fichier test-ping.json dans resultats
    testpingjson = "test-ping.json"
    print("creation test-ping.json dans resultat")

    testpingjsonString = {"FQDN procedure" : FQDN,"Frequence" : 10 ,"Nbvaleurs" : 1,"Unite" : "Bool","Result": []}
    
    #testpingjson = json.loads(testpingjsonString)
    
    #print (testpingjsonString)
    
    file = open(testpingjson, "w")
    json.dump(testpingjsonString, file)
    file.close()
    
    os.chdir("..\\..\\..\\")
    print(os.getcwd())
    return redirect('http://localhost:5000/ajout?creation=ok')

@app.route('/infoSuppression')
def infoSuppression():
    listeFichiers = []
    #for (repertoire) in walk("G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements"):
    for (repertoire) in walk("E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements"):
        listeFichiers.extend(repertoire)
 
    print(listeFichiers[1])
    listeFinal = listeFichiers[1]
    equipementURL = 0
    count = 0
    longueur = len(listeFinal)
    for equipement in listeFinal:
        if equipementURL == 0 and count == 0:
            equipementURL = f"Equipement={equipement}&"
            count = count + 1
        elif (count == longueur-1):
            equipementURL = equipementURL + f"Equipement{count}={equipement}"
            count = count + 1
        else:
            equipementURL = equipementURL + f"Equipement{count}={equipement}&"
            count = count + 1
    
    print(equipementURL)
    
    creation = request.args.get('creation','')
    if creation == "":
        return redirect(f"http://localhost:5000/suppression?{equipementURL}")
    elif creation == "ok" or creation == "erreur":
        return redirect(f"http://localhost:5000/suppression?{equipementURL}&creation={creation}")
    #return redirect(f"http://localhost:5000/actionSuppression?Liste={listeFinal}")

@app.route('/suppression')
def suppression():
    return render_template('suppression.html')

@app.route('/actionSuppression')
def actionSuppression():
    listeFichiers = []
    equipementSuppr = request.args.get('EquipementSuppr','')
    #for (repertoire) in walk("G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements"):
    for (repertoire) in walk("E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements"):
        listeFichiers.extend(repertoire)
 
    print(listeFichiers)
    listeFinal = listeFichiers[1]
    for i in listeFinal:
        if equipementSuppr == i:
            #shutil.rmtree(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{equipementSuppr}")
            shutil.rmtree(f"E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{equipementSuppr}")
            return redirect('http://localhost:5000/infoSuppression?creation=ok')
    return redirect('http://localhost:5000/infoSuppression?creation=erreur')

@app.route('/returnList')
def returnList():
    listeFichiers = os.listdir("E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements")
    
    listePing = []
    for i in listeFichiers:
        #print(i)
        #os.chdir(f"E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{i}\\resultats")
        file = open(f"E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{i}\\resultats\\test-ping.json", "r")
        resultPing = json.load(file)
        file.close()
        #print(resultPing)
        resultPing = resultPing['Result']
        #print(resultPing)
        listePing.append(resultPing)
        
    listeCPU = []
    for i in listeFichiers:
        #print(i)
        #os.chdir(f"E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{i}\\resultats")
        if os.path.exists(f"E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{i}\\resultats\\test-cpu.json"):
            file = open(f"E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{i}\\resultats\\test-cpu.json", "r")
            resultCPU = json.load(file)
            file.close()
            #print(resultPing)
            resultCPU = resultCPU['Result']
            #print(resultPing)
            longueur = len(resultCPU)
            listeCPU.append(resultCPU[longueur -1][0])
        else:
            listeCPU.append("None")
            
    listeRAM = []
    listeUniteRam = []
    for i in listeFichiers:
        #print(i)
        #os.chdir(f"E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{i}\\resultats")
        if os.path.exists(f"E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{i}\\resultats\\test-ram.json"):
            file = open(f"E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{i}\\resultats\\test-ram.json", "r")
            resultRAM = json.load(file)
            file.close()
            #print(resultPing)
            listeUniteRam.append(resultRAM['Unite'])
            resultRAM = resultRAM['Result']
            #print(resultPing)
            longueur = len(resultRAM)
            listeRAM.append(resultRAM[longueur -1][0])
        else:
            listeRAM.append("None")
            listeUniteRam.append("None")
    #print(listeUniteRam)
    
    IP = []
    for i in listeFichiers:
        if os.path.exists(f"E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{i}\\{i}.json"):
            file = open(f"E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{i}\\{i}.json", "r")
            lectureIP = json.load(file)
            file.close()
            IP.append(lectureIP['IP'])

    #print(IP)
    return jsonify(result=listeFichiers, resultPing=listePing, uniteCPU="%", resultCPU=listeCPU, uniteRAM=listeUniteRam, resultRAM=listeRAM, TouteIP=IP)

@app.route('/detail')
def detail():
    FQDN = request.args.get('equipement','')
    if FQDN != "":
        
        return render_template('equipement.html')
    else:
        return redirect('http://localhost:5000/')
    
@app.route('/ajoutProcedure')
def ajoutProcedure():
    return render_template('ajout_procedure.html')

@app.route('/actionAjoutProcedure')
def actionAjoutProcedure():
    FQDN = request.args.get('equipement','')
    OID = request.args.get('OID','')
    frequence = request.args.get('frequence','')
    Unite = request.args.get('Unite','')
    valeur = request.args.get('valeur','')
    
    dicoOIDConnu = {
        '1.3.6.1.4.1.9.9.109.1.1.1.1.24': 'cpu',
        '1.3.6.1.4.1.9.9.221.1.1.1.1.18': 'ram',
        '1.3.6.1.2.1.2.2.1.10': 'octet-in'    
        }
    
    
    if(FQDN != "" and OID!= "" and frequence != "" and Unite != "" and valeur != ""):
        os.chdir(f"E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{FQDN}\\procedures")
        nom = dicoOIDConnu[OID]
        
        nomProcedure = f"test-{nom}.json"
        if os.path.exists(f"E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{FQDN}\\procedures\\{nomProcedure}"):
            return redirect('http://localhost:5000/detail?equipement=cisco.usmb.asa&ajout=alredyExist')
        else:
            print(f"file name : {nomProcedure} pour {FQDN}")
            
            FQDNfinal = f"{FQDN}.test.{nom}"
            procedurejsonString = {"FQDN" : FQDNfinal,"OID" : OID,"frequence" : frequence,"Unite" : Unite,"Nbvaleurs" : valeur}
            
            file = open(nomProcedure, "w")
            json.dump(procedurejsonString, file)
            file.close()
            return redirect('http://localhost:5000/detail?equipement=cisco.usmb.asa&ajout=ok')
    else:
        return redirect('http://localhost:5000/')

@app.route('/modifierProcedure')
def modifierProcedure():
    return render_template('modifier_procedure.html')

@app.route('/retourListProcedure')
def retourListProcedure():
    listeApop= []
    FQDN = request.args.get('equipement','')
    if(FQDN !=""):
        listeProcedure = os.listdir(f"E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{FQDN}\\procedures")
        
        for i in range(len(listeProcedure) - 1):
            if listeProcedure[i] == "connexion.json" or listeProcedure[i] == "test-ping.json":
                listeApop.append(i)
                
        for pop in reversed(listeApop):
            listeProcedure.pop(pop)
            
        print(listeProcedure)
        return jsonify(listeProcedure=listeProcedure)
    else:
        return redirect('http://localhost:5000/')

@app.route('/retourProcedure')
def retourProcedure():
    FQDN = request.args.get('equipement','')
    procedure = request.args.get('procedure','')
    if(FQDN !="" and procedure !=""):
        print(f"E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{FQDN}\\procedures\\{procedure}")
        file = open(f"E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{FQDN}\\procedures\\{procedure}", "r")
        procedure = json.load(file)
        file.close()
        return procedure 
    else:
        return redirect('http://localhost:5000/')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    c = [1,2,3,4]
    return jsonify(result=c, result2=a+b)

app.run(host="localhost", port=int("5000"))
