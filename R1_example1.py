#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 14:28:24 2024

@author: marcelomolinari
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 14:20:26 2023.

@author: Marcelo M. Molinari
"""

import warnings
from R1_API import R1_API_calls
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

HOST = 'base url for your region'
USERNAME = 'your email'
PASSWORD = 'password'

r1 = R1_API_calls()
r = r1.getToken(HOST, USERNAME, PASSWORD)
jwt = r['jwt']
tenantId = r['tenantId']
print('jwt:', jwt)

tenantDetails = r1.getTenantDetails(HOST, jwt)
print('tenant details:', tenantDetails)

venues = r1.getVenues(HOST, tenantId, jwt)
print('venues:', venues)

response = r1.configure_802_11k(HOST, False, jwt)

#The following calls is an example to access a delelegate account
#The MSP needs to contain at least one MSP-EC

mspEcTenantId = r1.getMspECs(HOST, tenantId, jwt)[0]['tenant_id']
print('MSP-EC tenantId:', mspEcTenantId)

mspEcVenues = r1.getVenues(HOST, mspEcTenantId, jwt)
print('MSP-EC venues:', mspEcVenues)