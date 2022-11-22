# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 16:37:10 2022

@author: armand
"""

from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import cmdgen
import pysnmp.hlapi as pysnmp

tmp = ''

snmpEngine = engine.SnmpEngine()

config.addV3User(
    snmpEngine, 'user1',
    config.usmHMACSHAAuthProtocol, 'miracle2022',
    config.usmAesCfb128Protocol, 'power2022'
)

config.addTargetParams(snmpEngine, 'controleur', 'user1', 'authPriv')
config.addTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpSocketTransport().openClientMode()
)

config.addTargetAddr(
    snmpEngine, 'equipement',
    udp.domainName, ('192.168.140.140', 161),
    'controleur'
)

data = pysnmp.ObjectType(pysnmp.ObjectIdentity("iso.3.6.1.2.1.2.2.1.16.10101"))

def cbFun(snmpEngine, sendRequestHandle, errorIndication,
          errorStatus, errorIndex, varBinds, cbCtx):
    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

    else:
        for oid, val in varBinds:
            print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))
            print(valeur)
            with open("tmp","w") as outfile:
                outfile.write(val.prettyPrint())
            outfile.close()
          
valeur = "Hello world"
cmdgen.GetCommandGenerator().sendVarBinds(
    snmpEngine,
    'equipement',
    None, '',
    [([1, 3, 6, 1, 2, 1,2,2,1,16,10101], None)],
    # valeur,
    cbFun
)

snmpEngine.transportDispatcher.runDispatcher()

config.delTransport(
    snmpEngine,
    udp.domainName
).closeTransport()

with open("tmp","r") as outfile:
    tmp = outfile.readline()
outfile.close()

print("tmp = "+tmp)
print(int(tmp)+1)
