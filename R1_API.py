#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 14:29:46 2024

@author: marcelomolinari
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 14:18:25 2023.

@author: Marcelo M. Molinari
"""

import requests
import time


class R1_API_calls:
    """R1 and RUCKUS Cloud calls using JWT and the new endpoints."""

    def getToken(self, host, username, password):
        """Use your credentials to retrieve the jwt."""
        url = "https://" + host + "/token"
        body = {'username': username, 'password': password}
        r = requests.post(url, json=body, verify=False).json()
        return r
    
    def getJWT(self, host, tenantID, clientID, clientSecret):
        """Use your API KEY to retrieve the jwt."""
        url = "https://" + host + "/oauth2/token/" + tenantID
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = 'grant_type=client_credentials&client_id=' + clientID +  \
            '&client_secret=' + clientSecret
        r = requests.post(url, headers=headers, data=body, verify=False).json()
        return r
    
    def getTenantDetails(self, host, jwt):
        """Get the tenant details."""
        url = "https://" + host + "/tenants/self?deep=true"
        auth = {'Authorization': 'Bearer {}'.format(jwt)}
        r = requests.get(url, verify=False, headers=auth).json()
        return r

    def getVenues(self, host, tenantID, jwt):
        """Get all venues."""
        url = "https://" + host + "/venues"
        reqHeaders = {'Authorization': 'Bearer {}'.format(jwt),
                      'x-rks-tenantid': tenantID}
        r = requests.get(url, verify=False, headers=reqHeaders).json()
        return r

    def getMspECs(self, host, tenantID, jwt):
        """Get tall msp customers."""
        url = "https://" + host + "/mspCustomers"
        # auth = {'Authorization': 'Bearer {}'.format(jwt)}
        reqHeaders = {'Authorization': 'Bearer {}'.format(jwt),
                      'Content-Type': 'application/json'}
        r = requests.get(url, verify=False, headers=reqHeaders).json()
        # print(r)
        return r

    def configure_802_11k(self, host, enableNeighborReport, jwt):
        """Configure 802_11k in the wlan."""
        url = "https://" + host + "/networks"
        auth = {'Authorization': 'Bearer {}'.format(jwt)}
        r = requests.get(url, verify=False, headers=auth).json()
        print(r)
        for network in r:
            networkId = network['id']
            print('\nNetwork: ', network['name'])
            network['wlan']['advancedCustomization']['enableNeighborReport'] \
                = enableNeighborReport
            url = "https://" + host + "/networks/" + networkId
            auth = {'Authorization': 'Bearer {}'.format(jwt)}
            r = requests.put(url, verify=False, headers=auth, json=network)
            print('change response:', r)
            self.wait_for_async_response(host, r, jwt)
        return 'SUCCESS'

    def wait_for_async_response(self, host, response, jwt,
                                sleep_time=3):
        """Check if the status of the async call."""
        http_response = response.status_code
        if http_response != 202:
            return response
        requestId = response.json()['requestId']
        print('\nWaiting for request to complete:', requestId)
        url = "https://" + host + "/activities/" + requestId
        auth = {'Authorization': 'Bearer {}'.format(jwt)}
        while True:
            try:
                r = requests.get(url, verify=False, headers=auth).json()
                print('\nrequest:', r['status'])
                if r['status'] in ['SUCCESS', 'FAIL']:
                    break
                time.sleep(sleep_time)
            except Exception as ex:
                print(ex)
                print('retrying')
                time.sleep(sleep_time)
        if r['status'] != 'SUCCESS':
            raise Exception(r['status'])