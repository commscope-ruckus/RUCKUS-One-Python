#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R1 API Integration Script

This script demonstrates the usage of the R1 API for retrieving 
JWT tokens, MSP-EC tenant IDs, and venue information.

Created on Fri Jan 26 14:28:24 2024
@author: marcelomolinari
"""

import warnings
from R1_API import R1_API_calls

# Suppress unverified HTTPS request warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# Configuration
CONFIG = {
    'HOST': 'base your for your region',
    'TENANT_ID': 'your tenant id',
    'CLIENT_ID': 'your client id',
    'SECRET_ID': 'your secret id'
}

def main():
    """Main function to execute the R1 API calls."""
    r1 = R1_API_calls()
    
    # Get JWT token
    jwt = get_jwt(r1)
    print('JWT:', jwt)
    
    # Get MSP-EC tenant ID
    msp_ec_tenant_id = get_msp_ec_tenant_id(r1, jwt)
    print('MSP-EC tenant ID:', msp_ec_tenant_id)
    
    # Get MSP-EC venues
    msp_ec_venues = get_msp_ec_venues(r1, msp_ec_tenant_id, jwt)
    print('MSP-EC venues:', msp_ec_venues)

def get_jwt(r1):
    """Retrieve JWT token."""
    response = r1.getJWT(CONFIG['HOST'], CONFIG['TENANT_ID'], 
                         CONFIG['CLIENT_ID'], CONFIG['SECRET_ID'])
    return response['access_token']

def get_msp_ec_tenant_id(r1, jwt):
    """Retrieve MSP-EC tenant ID."""
    response = r1.getMspECs(CONFIG['HOST'], CONFIG['TENANT_ID'], jwt)
    return response[0]['tenant_id']

def get_msp_ec_venues(r1, msp_ec_tenant_id, jwt):
    """Retrieve MSP-EC venues."""
    return r1.getVenues(CONFIG['HOST'], msp_ec_tenant_id, jwt)

if __name__ == "__main__":
    main()
