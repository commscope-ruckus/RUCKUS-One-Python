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

HOST = 'base your for your region'
TENANT_ID = 'your tenant id'
CLIENT_ID = 'your client id'
SECRET_ID = 'your secret id'

r1 = R1_API_calls()
jwt = r1.getJWT(HOST, TENANT_ID, CLIENT_ID, SECRET_ID)['access_token']
print('jwt:', jwt)

mspEcTenantId = r1.getMspECs(HOST, TENANT_ID, jwt)[0]['tenant_id']
print('MSP-EC tenantId:', mspEcTenantId)

mspEcVenues = r1.getVenues(HOST, mspEcTenantId, jwt)
print('MSP-EC venues:', mspEcVenues)


