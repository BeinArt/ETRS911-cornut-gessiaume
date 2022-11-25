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
import socket

from stat import ST_CTIME

from glob import iglob
app = Flask(__name__)

PATH = "D:\\Users\\user\\Documents\\SupervisionProject\\racine"
"""
print(os.getcwd())
os.chdir("..\\racine")
PATH = os.getcwd()
"""
#print(os.getcwd())
#PATH = "\\192.168.141.222\\racine"
serveur = "http://192.168.141.58:8080"
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
    Clef = request.args.get('Clef','')
    Commentaire = request.args.get('Commentaire','')
    
    
    if(FQDN == ""):
        return redirect(f'{serveur}/ajout?manque=FQDN')
    
    if(NomAffichage == ""):
        NomAffichage = FQDN
        
    if(Marque == ""):
        Marque = ""
        
    if(Modele == ""):
        Modele = ""
        
    if(IP == ""):
        return redirect(f'{serveur}/ajout?manque=IP')
        
    if(Client == ""):
        Client = ""
        
    if(Localisation == ""):
        Localisation = ""
        
    if(VersionSNMP == ""):
        return redirect(f'{serveur}/ajout?manque=VersionSNMP')
        
    if(Communaute == ""):
        return redirect(f'{serveur}/ajout?manque=Communaute')
        
    if(User == ""):
        User = ""
        
    if(Password == ""):
        Password = ""
        
    if(Clef == ""):
        Clef = ""
        
    if(Commentaire == ""):
        Commentaire = ""
    
    
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
    print(Clef)
    print(Commentaire)
    
    
    #on se place dans le repertoire equipements
    print(os.getcwd())
    os.chdir(f"{PATH}\\equipements")
    print(os.getcwd())
    #creation du dossier
    os.mkdir(FQDN)
    
    #on rentre dans le dossier que l'on vient de créer
    os.chdir(".\\" + FQDN)
    print(os.getcwd())
    
    equipementJSON = f"{FQDN}.json"
    print(f"file name : {equipementJSON}")
    
    equipementjsonString = {"FQDN" : FQDN,"NomAffichage" : NomAffichage,"Marque" : Marque,"Modele" : Modele,"IP" : IP,"Client" : Client,"OS" : OS,"Localisation" : Localisation,"Commentaire" : Commentaire}
    
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
    connexionjsonString = {"FQDN" : FQDN ,"Version" : VersionSNMP,"Communaute" : Communaute,"User" : User,"Password" : Password,"Key" : Clef}

    
    file = open(connexionjson, "w")
    json.dump(connexionjsonString, file)
    file.close()
    
    #creation fichier test-ping.json dans procedures
    testpingjson = "test-ping.json"
    print("creation test-ping.json")
    testpingjsonString = {"FQDN procedure" : FQDN,"Frequence" : 2 ,"Nbvaleurs" : 1,"Unite" : "Bool"}
    
    file = open(testpingjson, "w")
    json.dump(testpingjsonString, file)
    file.close()

    os.chdir("..\\resultats")
    
    #creation fichier test-ping.json dans resultats
    testpingjson = "test-ping.json"
    print("creation test-ping.json dans resultat")

    testpingjsonString = {"FQDN procedure" : FQDN,"Frequence" : 2 ,"Nbvaleurs" : 1,"Unite" : "Bool","Result": [0]}
    
    #testpingjson = json.loads(testpingjsonString)
    
    #print (testpingjsonString)
    
    file = open(testpingjson, "w")
    json.dump(testpingjsonString, file)
    file.close()
    
    os.chdir(f"{PATH}")
    print(os.getcwd())
    return redirect(f'{serveur}/')

@app.route('/suppression')
def suppression():
    return render_template('suppression.html')

@app.route('/actionSuppression')
def actionSuppression():
    listeFichiers = []
    equipementSuppr = request.args.get('EquipementSuppr','')
    #for (repertoire) in walk("G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements"):
    for (repertoire) in walk(f"{PATH}\\equipements"):
        listeFichiers.extend(repertoire)
 
    print(listeFichiers)
    listeFinal = listeFichiers[1]
    for i in listeFinal:
        if equipementSuppr == i:
            #shutil.rmtree(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{equipementSuppr}")
            shutil.rmtree(f"{PATH}\\equipements\\{equipementSuppr}")
            return redirect(f'{serveur}/suppression?creation=ok')
    return redirect(f'{serveur}/suppression?creation=erreur')

@app.route('/modifier')
def modifier():
    return render_template('modifier.html')

@app.route('/recupFQDN')
def recupFQDN():
    listeFichiers = os.listdir(f"{PATH}\\equipements")
    print(listeFichiers)
    return jsonify(fqdn=listeFichiers)
    
@app.route('/modifFQDN')
def modifFQDN():
    FQDN = request.args.get('equipement','')
    if os.path.exists(f"{PATH}\\equipements\\{FQDN}"):
        file = open(f"{PATH}\\equipements\\{FQDN}\\{FQDN}.json", "r")
        #file = open(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{i}\\resultats\\test-ping.json", "r")
        InfosEquipement = json.load(file)
        file.close()
        FQDNRetour = InfosEquipement["FQDN"]
        nom = InfosEquipement["NomAffichage"]
        marque = InfosEquipement["Marque"]
        modele = InfosEquipement["Modele"]
        ip = InfosEquipement["IP"]
        client = InfosEquipement["Client"]
        OSRetour = InfosEquipement["OS"]
        localisation = InfosEquipement["Localisation"]
        try:
            commentaire = InfosEquipement["Commentaire"]
        except:
            commentaire = InfosEquipement["commentaire"]
            
        file = open(f"{PATH}\\equipements\\{FQDN}\\procedures\\connexion.json", "r")
        #file = open(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{i}\\resultats\\test-ping.json", "r")
        InfosConnexionEquipement = json.load(file)
        file.close()
        version = InfosConnexionEquipement["Version"]
        #print(version)
        communaute = InfosConnexionEquipement["Communaute"]
        try:
            user = InfosConnexionEquipement["User"]
        except:
            user = ""
        
        try:
            password = InfosConnexionEquipement["Password"]
        except:
            password = ""
        
        try:
            key = InfosConnexionEquipement["Key"]
        except:
            key = ""
        
        
        
        return jsonify(FQDN=FQDNRetour, Nom=nom, Marque=marque, Modele=modele, IP=ip, Client=client, OS=OSRetour, Localisation=localisation, Commentaire=commentaire, Version=version, Communaute=communaute, User=user, Password=password, Key=key)

@app.route('/actionModif')
def actionModif():
    #ecrire dans les deux fichiers json connexion.json et fqdn.json
    FQDNOld = request.args.get('equipementold','')
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
    Clef = request.args.get('Clef','')
    Commentaire = request.args.get('Commentaire','')
    
    
    if(FQDN == ""):
        return redirect(f'{serveur}/modifier?manque=FQDN')
    
    if(NomAffichage == ""):
        NomAffichage = FQDN
        
    if(Marque == ""):
        Marque = ""
        
    if(Modele == ""):
        Modele = ""
        
    if(IP == ""):
        return redirect(f'{serveur}/modifier?manque=IP')
        
    if(Client == ""):
        Client = ""
        
    if(Localisation == ""):
        Localisation = ""
        
    if(VersionSNMP == ""):
        return redirect(f'{serveur}/modifier?manque=VersionSNMP')
        
    if(Communaute == ""):
        return redirect(f'{serveur}/modifier?manque=Communaute')
        
    if(User == ""):
        User = ""
        
    if(Password == ""):
        Password = ""
        
    if(Clef == ""):
        Clef = ""
        
    if(Commentaire == ""):
        Commentaire = ""
    
    
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
    print(Clef)
    print(Commentaire)
    
    if FQDN != FQDNOld:
        os.rename(f"{PATH}\\equipements\\{FQDNOld}", f"{PATH}\\equipements\\{FQDN}")
    #on se place dans le repertoire equipements
    print(os.getcwd())
    os.chdir(f"{PATH}\\equipements\\{FQDN}")
    print(os.getcwd())
    
    
    os.remove(f"{FQDNOld}.json")
    
    equipementJSON = f"{FQDN}.json"
    print(f"file name : {equipementJSON}")
    
    equipementjsonString = {"FQDN" : FQDN,"NomAffichage" : NomAffichage,"Marque" : Marque,"Modele" : Modele,"IP" : IP,"Client" : Client,"OS" : OS,"Localisation" : Localisation,"Commentaire" : Commentaire}
    
    file = open(equipementJSON, "w")
    json.dump(equipementjsonString, file)
    file.close()
    
    #on rentre dans procedures
    os.chdir(".\\procedures")
    
    os.remove("connexion.json")
    #creation fichier connexion.json
    connexionjson = "connexion.json"
    print("creation connexion.json")
    if VersionSNMP == "V2":
        connexionjsonString = {"FQDN" : FQDN ,"Version" : VersionSNMP,"Communaute" : Communaute,"User" : "","Password" : "","Key" : ""}
    else:
        connexionjsonString = {"FQDN" : FQDN ,"Version" : VersionSNMP,"Communaute" : Communaute,"User" : User,"Password" : Password,"Key" : Clef}

    
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
    
    os.chdir(f"{PATH}")
    print(os.getcwd())
    return redirect(f'{serveur}/')

@app.route('/returnList')
def returnList():
    listeFichiers = os.listdir(f"{PATH}\\equipements")
    #listeFichiers = os.listdir("G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements")
    
    listePing = []
    nbUp = 0
    nbDown = 0
    for i in listeFichiers:
        #print(i)
        os.chdir(f"{PATH}\\equipements\\{i}\\resultats")
        file = open(f"{PATH}\\equipements\\{i}\\resultats\\test-ping.json", "r")
        #file = open(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{i}\\resultats\\test-ping.json", "r")
        resultPing = json.load(file)
        file.close()
        #print(resultPing)
        resultPing = resultPing['Result']
        #print(resultPing)
        listePing.append(resultPing)
        
        if resultPing[0]!=0:
            nbUp = nbUp + 1
        
            
    nbDown = len(listeFichiers) - nbUp

    IP = []
    for i in listeFichiers:
        if os.path.exists(f"{PATH}\\equipements\\{i}\\{i}.json"):
        #if os.path.exists(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{i}\\{i}.json"):
            file = open(f"{PATH}\\equipements\\{i}\\{i}.json", "r")
            #file = open(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{i}\\{i}.json", "r")
            lectureIP = json.load(file)
            file.close()
            IP.append(lectureIP['IP'])

    #print(IP)
    nbServices = 0
    for i in listeFichiers:
        if os.path.exists(f"{PATH}\\equipements\\{i}\\{i}.json"):
            listeServices = os.listdir(f"{PATH}\\equipements\\{i}\\procedures")
            nbServices = nbServices + len(listeServices) - 1
            
            
    os.chdir(f"{PATH}")
    
    listeLogs = os.listdir(f"{PATH}\\logs")
    Logs = []
    for i in range(len(listeLogs)):
        for nom in listeFichiers:
            if str(nom) in listeLogs[i] :
            #if os.path.exists(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{i}\\{i}.json"):
                file = open(f"{PATH}\\logs\\{listeLogs[i]}", "r")
                #file = open(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{i}\\{i}.json", "r")
                lectureLogs = json.load(file)
                file.close()
                Logs.append(lectureLogs['Analyse'])
                
    nbequipements = len(listeFichiers)
    
    os.chdir(f"{PATH}")
    return jsonify(result=listeFichiers, resultPing=listePing, TouteIP=IP, resultLogs=Logs, resultnbequipements=nbequipements, resultnbServices=nbServices, resultnbup=nbUp, resultnbdown=nbDown)
    #return jsonify(result=listeFichiers, resultPing=listePing, """uniteCPU="%", resultCPU=listeCPU, uniteRAM=listeUniteRam, resultRAM=listeRAM, TouteIP=IP,""" resultLogs=Logs, resultnbequipements=nbequipements, resultnbServices=nbServices, resultnbup=nbUp, resultnbdown=nbDown)
@app.route('/detail')
def detail():
    FQDN = request.args.get('equipement','')
    if FQDN != "":
        
        return render_template('equipement.html')
    else:
        return redirect(f'{serveur}/')
    
@app.route('/ajoutProcedure')
def ajoutProcedure():
    return render_template('ajout_procedure.html')

@app.route('/actionAjoutProcedure')
def actionAjoutProcedure():
    FQDN = request.args.get('equipement','')
    OID = request.args.get('OID','')
    Instance = request.args.get('instance','')
    frequence = request.args.get('frequence','')
    Unite = request.args.get('Unite','')
    valeur = request.args.get('valeur','')
    
    oldOID = OID
    OID = f"{OID}.{Instance}"
    
    dicoOIDConnu = {
        '1.3.6.1.2.1.2.2.1.16': 'octet_out'
        }
    
    
    if(FQDN != "" and OID!= "" and frequence != "" and Unite != "" and valeur != ""):
        os.chdir(f"{PATH}\\equipements\\{FQDN}\\procedures")
        #os.chdir(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{FQDN}\\procedures")
        nom = dicoOIDConnu[oldOID]
        
        nomProcedure = f"test-{nom}.json"
        if os.path.exists(f"{PATH}\\equipements\\{FQDN}\\procedures\\{nomProcedure}"):
        #if os.path.exists(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{FQDN}\\procedures\\{nomProcedure}"):    
            return redirect(f'{serveur}/detail?equipement=cisco.usmb.asa&ajout=alredyExist')
        else:
            print(f"file name : {nomProcedure} pour {FQDN}")
            
            FQDNfinal = f"{FQDN}.test.{nom}"
            procedurejsonString = {"FQDN" : FQDNfinal,"OID" : OID,"Frequence" : int(frequence),"Nbvaleurs" : int(valeur),"Unite" : Unite}
            
            file = open(nomProcedure, "w")
            json.dump(procedurejsonString, file)
            file.close()
            
            os.chdir("..\\resultats")
            FQDNfinal = f"{FQDN}.test.{nom}"
            procedurejsonString = {"FQDN" : FQDNfinal,"Frequence" : int(frequence),"Nbvaleurs" : int(valeur),"Unite" : Unite,"Result" : []}
            
            nomResultat = f"test-{nom}.json"
            file = open(nomResultat, "w")
            json.dump(procedurejsonString, file)
            file.close()
            os.chdir(f"{PATH}")
            return redirect(f'{serveur}/detail?equipement={FQDN}&ajout=ok')
    else:
        
        return redirect(f'{serveur}/')

@app.route('/modifierProcedure')
def modifierProcedure():
    return render_template('modifier_procedure.html')

@app.route('/actionModifProcedure')
def actionModifProcedure():
    FQDN = request.args.get('equipement','')
    OID = request.args.get('OID','')
    frequence = request.args.get('frequence','')
    Unite = request.args.get('Unite','')
    valeur = request.args.get('valeur','')
    nomProcedure = request.args.get('nom','')
    
    if(FQDN != "" and OID!= "" and frequence != "" and Unite != "" and valeur != "" and nomProcedure != ""):
        os.chdir(f"{PATH}\\equipements\\{FQDN}\\procedures")
        #os.chdir(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{FQDN}\\procedures")
        
        
        
        if os.path.exists(f"{PATH}\\equipements\\{FQDN}\\procedures\\{nomProcedure}"):
            with open(nomProcedure, "r") as file:
                data = json.load(file)
                
            file.close()
            print(data)
            data["OID"] = OID
            data["Unite"] = Unite
            data["Frequence"] = int(frequence)
            data["Nbvaleurs"] = int(valeur)
             
            with open(nomProcedure, 'w') as file:
                json.dump(data, file, indent=4)
            file.close()
            with open(nomProcedure, "r") as file:
                data = json.load(file)
            file.close()
            print(data)
        os.chdir(f"{PATH}")
        return redirect(f'{serveur}/detail?equipement={FQDN}&modifProcedure=ok')
    else:
        return redirect(f'{serveur}/detail?equipement={FQDN}')

@app.route('/retourListProcedure')
def retourListProcedure():
    listeApop= []
    FQDN = request.args.get('equipement','')
    if(FQDN !=""):
        listeProcedure = os.listdir(f"{PATH}\\equipements\\{FQDN}\\procedures")
        #listeProcedure = os.listdir(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{FQDN}\\procedures")
        
        for i in range(len(listeProcedure) - 1):
            if listeProcedure[i] == "connexion.json" or listeProcedure[i] == "test-ping.json":
                listeApop.append(i)
                
        for pop in reversed(listeApop):
            listeProcedure.pop(pop)
            
        print(listeProcedure)
        return jsonify(listeProcedure=listeProcedure)
    else:
        return redirect(f'{serveur}/')

@app.route('/retourProcedure')
def retourProcedure():
    FQDN = request.args.get('equipement','')
    procedure = request.args.get('procedure','')
    if(FQDN !="" and procedure !=""):
        #print(f"{PATH}\\equipements\\{FQDN}\\procedures\\{procedure}")
        file = open(f"{PATH}\\equipements\\{FQDN}\\procedures\\{procedure}", "r")
        #file = open(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{FQDN}\\procedures\\{procedure}", "r")
        procedure = json.load(file)
        file.close()
        print(procedure)
        return procedure 
    else:
        return redirect(f'{serveur}/')
    
    
    
@app.route('/supprProcedure')
def supprProcedure():
    return render_template('suppression_procedure.html')
    
@app.route('/actionSupprProcedure')
def actionSupprProcedure():
    FQDN = request.args.get('equipement','')
    nomProcedure = request.args.get('nom','')
    
    if(FQDN != "" and nomProcedure!= "" ):
        os.chdir(f"{PATH}\\equipements\\{FQDN}\\procedures")
        #os.chdir(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{FQDN}\\procedures")

        if os.path.exists(f"{PATH}\\equipements\\{FQDN}\\procedures\\{nomProcedure}"):
            os.remove(nomProcedure)
            os.chdir(f"{PATH}\\equipements\\{FQDN}\\resultats")
            os.remove(nomProcedure)
        os.chdir(f"{PATH}")
        return redirect(f'{serveur}/detail?equipement={FQDN}&supprProcedure=ok')
    else:
        return redirect(f'{serveur}/detail?equipement={FQDN}')
    
    
@app.route('/returnInfoEquipement')
def returnInfoEquipement():
    FQDN = request.args.get('equipement','')
    procedure = request.args.get('procedures','')
    
    file = open(f"{PATH}\\equipements\\{FQDN}\\resultats\\{procedure}", "r")
    #file = open(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{FQDN}\\procedures\\{procedure}", "r")
    procedure = json.load(file)
    result_procedures = procedure["Result"]
    unite = procedure["Unite"]
    frequence = procedure["Frequence"]
    absyss = []
    ordonnee = []
    for i in range(len(result_procedures)):
        test = result_procedures[i][1]
        test = test.split('-')
        #print(test)
        
        recup = test[3]
        test[3] = f"{recup}h"
        recup = test[4]
        test[4] = f"{recup}m"
        recup = test[5]
        test[5] = f"{recup}s"
        test = " ".join(test)
        #nombres = f'{result_procedures[i][0]} {unite}'
        #absyss.append(result_procedures[i][1])
        absyss.append(test)
        ordonnee.append(result_procedures[i][0])
        #ordonnee.append(nombres)
    #print(absyss)
    #print(ordonnee)
    return jsonify(retoura=absyss, retourb=ordonnee, unite=unite, frequence=frequence)

@app.route('/returnProceduresEquipement')
def returnProceduresEquipement():
    FQDN = request.args.get('equipement','')
    if(FQDN != ""):
        os.chdir(f"{PATH}\\equipements\\{FQDN}\\procedures")
        #os.chdir(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{FQDN}\\procedures")
        ListeNomCompletProcedure = []
        if os.path.exists(f"{PATH}\\equipements\\{FQDN}\\procedures"):
            procedures = os.listdir(f"{PATH}\\equipements\\{FQDN}\\procedures")
            #print(procedures)
            procedures.remove("connexion.json")
            procedures.remove("test-ping.json")
            for i in range(len(procedures)):
                nom_procedure = []
                ListeNomCompletProcedure.append(procedures[i])
                nom_procedure = procedures[i].split(".")
                
                nom_procedure.remove("json")
                
                nom_procedure = nom_procedure[0]
                nom_procedure = nom_procedure.split("-")
                nom_procedure.remove("test")
                nom_procedure = nom_procedure[0]
                procedures[i] = nom_procedure
                
                
            
            #print(procedures)
                
            os.chdir(f"{PATH}")
            return jsonify(procedures=procedures, nomprocedures=ListeNomCompletProcedure)
        else:
            print("")
    else:
        return 0

@app.route('/logsdashboard')
def logsdashboard():
    return render_template('logsDashboard.html')

@app.route('/retourlogsdashboard')
def retourlogsdashboard():
    #print("infos relout logs")
    os.chdir(f"{PATH}\\logs")
    #listeFichiersLogs = os.listdir("E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\logs")
    #listeFichiersLogs = [(os.stat(fname)[ST_CTIME], fname) for fname in os.listdir("E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\logs") if os.path.isfile(fname)]
    #print(listeFichiersLogs)
    retourLogs = []
    listeFichiersLogs = []

    fichiers = []
    for fichier in iglob(f"{PATH}\\logs\\*.json"):
        if os.path.isfile(fichier):
            fichiers.append([fichier, os.path.getmtime(fichier)])
    #si la liste de tout les logs est plus grande que 200 donc plus que 200 log
    if len(fichiers) > 200:
        #alors on supprimer tout les fichiers de 200 a la derniere entree
        del fichiers[199:len(fichiers)]
        
    fichiers.sort(key=lambda elem: elem[1], reverse=True) # tri par date avec date récente au début
    #print(fichiers)
    for i in range(len(fichiers)):
        listeFichiersLogs.append(fichiers[i][0])
        
    for i in listeFichiersLogs:
        #print(i)
        #file = open(f"E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\logs\\{i}", "r")
        file = open(f"{i}", "r")
        #file = open(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{FQDN}\\procedures\\{procedure}", "r")
        procedure = json.load(file)
        file.close()
        Log = []
        Log.append(procedure["FQDN procedure"])
        Log.append(procedure["Type"])
        test = procedure["Datetime"]
        test = test.split('-')
        #print(test)
        
        recup = test[3]
        test[3] = f"{recup}h"
        recup = test[4]
        test[4] = f"{recup}m"
        recup = test[5]
        test[5] = f"{recup}s"
        
        #print(test)
        test = " ".join(test)
        #print(test)
        Log.append(test)
        Log.append(procedure["Analyse"])
        retourLogs.append(Log)
    
    #print(retourLogs)
    os.chdir(f"{PATH}")
    return jsonify(retourlogs=retourLogs)

@app.route('/logsequipement')
def logsequipement():
    return render_template('logsEquipement.html')

@app.route('/retourlogsequipement')
def retourlogsequipement():
    FQDN = request.args.get('equipement','')
    #print("infos relout logs")
    os.chdir(f"{PATH}\\logs")
    #listeFichiersLogs = os.listdir("E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\logs")
    #listeFichiersLogs = [(os.stat(fname)[ST_CTIME], fname) for fname in os.listdir("E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\logs") if os.path.isfile(fname)]
    #print(listeFichiersLogs)
    retourLogs = []
    listeFichiersLogs = []

    fichiers = []
    for fichier in iglob(f"{PATH}\\logs\\*.json"):
        if os.path.isfile(fichier):
            fichiers.append([fichier, os.path.getmtime(fichier)])
    
    fichiers.sort(key=lambda elem: elem[1], reverse=True) # tri par date avec date récente au début
    #print(fichiers)
    for i in range(len(fichiers)):
        if FQDN in fichiers[i][0]:
            listeFichiersLogs.append(fichiers[i][0])
        
    for i in listeFichiersLogs:
        #print(i)
        #file = open(f"E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\logs\\{i}", "r")
        file = open(f"{i}", "r")
        #file = open(f"G:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\{FQDN}\\procedures\\{procedure}", "r")
        procedure = json.load(file)
        file.close()
        Log = []
        Log.append(procedure["FQDN procedure"])
        Log.append(procedure["Type"])
        test = procedure["Datetime"]
        test = test.split('-')
        #print(test)
        
        recup = test[3]
        test[3] = f"{recup}h"
        recup = test[4]
        test[4] = f"{recup}m"
        recup = test[5]
        test[5] = f"{recup}s"
        
        #print(test)
        test = " ".join(test)
        #print(test)
        Log.append(test)
        Log.append(procedure["Analyse"])
        retourLogs.append(Log)
    
    #print(retourLogs)
    os.chdir(f"{PATH}")
    return jsonify(retourlogs=retourLogs)

@app.route('/returnEquipement')
def returnEquipement():
    os.chdir(f"{PATH}\\equipements")
    listeEquipements = os.listdir(f"{PATH}\\equipements")
    
    
    os.chdir(f"{PATH}")
    return jsonify(equipements=listeEquipements)

@app.route('/start')
def start():
    
    commande = "Start"
    creationSocket(commande)
    return redirect(f'{serveur}/?supervision=demarrer')

@app.route('/restart')
def restart():

    commande = "Restart"
    creationSocket(commande)
    return redirect(f'{serveur}/?supervision=demarrer')

@app.route('/stop')
def stop():
    commande = "Stop"
    creationSocket(commande)
    return redirect(f'{serveur}/')

@app.route('/reload')
def reload():
    print("reload")
    FQDN = request.args.get('equipement','')
    commande = f"reload@{FQDN}"
    creationSocket(commande)
    return redirect(f'{serveur}/detail?equipement={FQDN}')

def creationSocket(commande):
    print("function socket creation")
    try:
        print("connexion socket")
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(('localhost', 8089))
        data = str(commande)
        print(f"envoie de {str(commande)}")
        clientsocket.send(data.encode(encoding='utf-8'))
    except:
        print("error")
    

app.run(host="192.168.141.58", port=int("8080"))
