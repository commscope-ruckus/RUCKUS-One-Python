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
    
    def getBrandDetails(self, host, jwt):
        """Get the tenant details."""
        url = "https://" + host + "/mspLabels"
        auth = {'Authorization': 'Bearer {}'.format(jwt)}
        r = requests.get(url, verify=False, headers=auth).json()
        return r
    
    def getBrandAdmins(self, host, jwt):
        """Get the tenant details."""
        url = "https://" + host + "/tenants/self?deep=true"
        auth = {'Authorization': 'Bearer {}'.format(jwt)}
        r = requests.get(url, verify=False, headers=auth).json()
        return r

    def getMspECs(self, host, tenantID, jwt):
        """Get tall msp customers."""
        url = "https://" + host + "/mspCustomers"
        reqHeaders = {'Authorization': 'Bearer {}'.format(jwt),
                      'Content-Type': 'application/json'}
        r = requests.get(url, verify=False, headers=reqHeaders).json()
        return r
    
    def getMspTechs(self, host, jwt):
        """Get all MSP and Tech partners."""
        url = "https://" + host + "/mspCustomers"
        reqHeaders = {'Authorization': 'Bearer {}'.format(jwt),
                      'Content-Type': 'application/json'}
        r = requests.get(url, verify=False, headers=reqHeaders).json()
        return r
    
    def getProperties(self, host, jwt):
        """Get brand properties."""
        url = "https://" + host + "/mspecs/query"
        body = {
                "searchString": "",
                "filters": {
                    "tenantType": [
                        "MSP_REC"
                    ]
                },
                "fields": [
                    "id",
                    "name",
                    "tenantType",
                    "status",
                    "alarmCount",
                    "mspAdminCount",
                    "mspEcAdminCount",
                    "creationDate",
                    "expirationDate",
                    "wifiLicense",
                    "streetAddress"
                ],
                "searchTargetFields": [
                    "name"
                ],
                "page": 1,
                "pageSize": 10,
                "defaultPageSize": 10,
                "total": 0,
                "sortField": "name",
                "sortOrder": "ASC"
            }
        reqHeaders = {'Authorization': 'Bearer {}'.format(jwt),
                      'Content-Type': 'application/json'}
        r = requests.post(url, verify=False, headers=reqHeaders, json=body).json()
        return r

    def getVenues(self, host, tenantID, jwt):
        """Get all venues."""
        url = "https://" + host + "/venues"
        reqHeaders = {'Authorization': 'Bearer {}'.format(jwt),
                      'x-rks-tenantid': tenantID}
        r = requests.get(url, verify=False, headers=reqHeaders).json()
        return r

    def getVenueById(self, host, tenantID, venueId, jwt):
        """Get venue with provided Id."""
        url = "https://" + host + "/venues"
        reqHeaders = {'Authorization': 'Bearer {}'.format(jwt),
                      'x-rks-tenantid': tenantID}
        r = requests.get(url, verify=False, headers=reqHeaders).json()
        for item in r:
            if item['id'] == venueId:
                return item['name']
        return 'not found'

    def getAPs(self, host, tenantID, jwt):
        """Get all APs."""
        url = "https://" + host + "/venues/aps"
        reqHeaders = {'Authorization': 'Bearer {}'.format(jwt),
                      'x-rks-tenantid': tenantID}
        r = requests.get(url, verify=False, headers=reqHeaders).json()
        return r
    
    def getAPsByVenueId(self, host, tenantID, venueID, jwt):
        """Get all APs in a venue."""
        url = "https://" + host + "/venues/aps"
        reqHeaders = {'Authorization': 'Bearer {}'.format(jwt),
                      'x-rks-tenantid': tenantID}
        r = requests.get(url, verify=False, headers=reqHeaders).json()
        apList = []
        for item in r:
            if item['venueId'] == venueID:
                apList.append(item)             
        return apList
    
    def getNetworks(self, host, tenantID, jwt):
        """Get all networks."""
        url = "https://" + host + "/networks"
        reqHeaders = {'Authorization': 'Bearer {}'.format(jwt),
                      'x-rks-tenantid': tenantID}
        r = requests.get(url, verify=False, headers=reqHeaders).json()
        return r

    def getNetworkDetails(self, host, tenantID, networkID, jwt):
        """Get network details."""
        url = "https://" + host + "/networks/" + networkID + "?deep=true"
        reqHeaders = {'Authorization': 'Bearer {}'.format(jwt),
                      'x-rks-tenantid': tenantID}
        r = requests.get(url, verify=False, headers=reqHeaders).json()
        return r

    def getClients(self, host, tenantID, jwt):
        """Get clients."""
        url = "https://" + host + "/clients"
        reqHeaders = {'Authorization': 'Bearer {}'.format(jwt),
                      'x-rks-tenantid': tenantID}
        r = requests.get(url, verify=False, headers=reqHeaders).json()
        return r
    
    def getClientSessions(self, host, tenantID, clientMac, fromTime, 
                          toTime, jwt):
        """List client sessions."""
        url = "https://" + host + "/reports/clients/sessionHistories"
        body = {
            "filters": {
                "clientMAC": [
                    clientMac
                ],
                "fromTime": fromTime,
                "toTime": toTime
            }
        }
        reqHeaders = {'Authorization': 'Bearer {}'.format(jwt), 
                      'x-rks-tenantid': tenantID, 
                      'Content-Type': 'application/json'}
        r = requests.post(url, verify=False, headers=reqHeaders, 
                          json=body).json()
        return r
    
    def getEvents(self, host, tenantID, jwt):
        """List events."""
        url = "https://" + host + "/events/query"
        body = {
                "fields": [
                    "event_datetime",
                    "severity",
                    "entity_type",
                    "product",
                    "entity_id",
                    "message",
                    "dpName",
                    "apMac",
                    "clientMac",
                    "macAddress",
                    "apName",
                    "switchName",
                    "serialNumber",
                    "networkName",
                    "networkId",
                    "ssid",
                    "radio",
                    "raw_event",
                    "sourceType",
                    "adminName",
                    "clientName",
                    "userName",
                    "hostname",
                    "adminEmail",
                    "administratorEmail",
                    "venueName",
                    "venueId",
                    "apGroupId",
                    "apGroupName",
                    "floorPlanName",
                    "recipientName",
                    "transactionId",
                    "name",
                    "ipAddress",
                    "detailedDescription",
                    "Persona-ID"
                ],
                "page": 1,
                "pageSize": 300,
                "sortField": "event_datetime",
                "sortOrder": "DESC",
                "filters": {
                    "entity_type": [
                        "AP",
                        "SECURITY",
                        "CLIENT",
                        "SWITCH",
                        "NETWORK",
                        "EDGE"
                    ]
                }
            }
        reqHeaders = {'Authorization': 'Bearer {}'.format(jwt), 
                      'x-rks-tenantid': tenantID,
                      'Content-Type': 'application/json'}
        r = requests.post(url, verify=False, headers=reqHeaders, 
                          json=body).json()
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