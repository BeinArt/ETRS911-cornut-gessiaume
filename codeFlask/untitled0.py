# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 16:08:19 2022

@author: Jean-Baptiste
"""

import os.path, time

from datetime import datetime
def get_creation_date(file):
    stat = os.stat(file)
    try:
        return stat.st_birthtime
    except AttributeError:
        # Nous sommes probablement sous Linux. Pas de moyen pour obtenir la date de création, que la dernière date de modification.
        return stat.st_mtime
# Convertir Timestamp en datetime
creation_date = datetime.fromtimestamp(get_creation_date('E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\cisco.usmb.asa\\resultats\\test-ping.json'))
print("%s" % creation_date)
creation = str(creation_date).split('.')
print(creation)
creation = creation[0]
"""
liste = []
liste.append(int(creation[0]))
liste.append(int(creation[1]))
creation = creation[2].split(' ')
liste.append(int(creation[0]))
creation = creation[1].split(':')
liste.append(int(creation[0]))
liste.append(int(creation[1]))
creation = creation[2].split('.')
liste.append(int(creation[0]))
print(liste)
"""
#print("Dernière modification: %s" % time.ctime(os.path.getmtime("E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\cisco.usmb.asa\\resultats\\test-ping.json")))
#date_fichier = time.ctime(os.path.getmtime("E:\\Master2\\Semestre 9\\SupervisionProject\\racine\\equipements\\cisco.usmb.asa\\resultats\\test-ping.json"))

from datetime import datetime
date_actuelle = datetime.now()
print(date_actuelle)
date_actuelle = str(date_actuelle).split('.')
date_actuelle = date_actuelle[0]

import datetime
from datetime import datetime
first = time.strptime(creation, "%Y-%m-%d %H:%M:%S")
second = time.strptime(str(date_actuelle), "%Y-%m-%d %H:%M:%S")

if first < second:
    print('First date is less than the second date.')
elif first > second:
    print('First date is more than the second date.')
else:
    print('Both dates are the same.')