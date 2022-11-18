# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 16:37:10 2022

@author: armand
"""

from twisted.internet.task import react
from pysnmp.hlapi.v3arch.twisted import *


def success(args, reactor, snmpEngine):
    errorStatus, errorIndex, varBindTable = args

    if errorStatus:
        print('%s: %s at %s' % (hostname,
                                errorStatus.prettyPrint(),
                                errorIndex and varBindTable[0][int(errorIndex) - 1][0] or '?'))

    else:
        for varBindRow in varBindTable:
            for varBind in varBindRow:
                print(' = '.join([x.prettyPrint() for x in varBind]))

        if not isEndOfMib(varBindTable[-1]):
            return getbulk(reactor, snmpEngine, *varBindTable[-1])


def failure(errorIndication):
    print(errorIndication)


def getbulk(reactor, snmpEngine, varBinds):
    deferred = bulkCmd(
        snmpEngine,
        UsmUserData('usr-none-none'),
        UdpTransportTarget(('192.168.176.2', 161)),
        ContextData(),
        0, 50,
        varBinds
    )

    deferred.addCallback(success, reactor, snmpEngine).addErrback(failure)

    return deferred


react(getbulk, [SnmpEngine(), ObjectType(ObjectIdentity('SNMPv2-MIB', 'system'))])