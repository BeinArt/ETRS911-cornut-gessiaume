# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 13:25:57 2022

@author: armand
"""
import pysnmp as pysnmpdef
import pysnmp.hlapi as pysnmp

auth = pysnmp.CommunityData("passprojet",mpModel=1)
data = pysnmp.ObjectType(pysnmp.ObjectIdentity("iso.org.dod.internet.mgmt.mib-2.2.2.1.16.10101"))
snmpEngine = pysnmp.SnmpEngine()
for (errorIndication, errorStatus, errorIndex, varBinds) in pysnmp.getCmd(snmpEngine,
                                                                    auth,
                                                                    pysnmp.UdpTransportTarget(("192.168.176.2", 161)),
                                                                    pysnmp.ContextData(),
                                                                    data):
    if errorIndication or errorStatus:
        print(errorIndication or errorStatus)
        break
    else:
        for oid,val in varBinds:
            res = str(val)
            print(oid,val)
            print(varBinds)
