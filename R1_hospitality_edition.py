import warnings
import csv

from datetime import datetime
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# Import classes
from R1_API import R1_API_calls

# Constants
R1HOST = 'api.ruckus.cloud'
TENANT_ID = 'your_tenant_id'
CLIENT_ID = 'your_client_id'
SECRET_ID = 'your_secret_id'
    
csvFileName = 'r1_' + str(datetime.now().strftime("%m%d%Y%H%M")) + '.csv'

def main():
    # Open the csv file
    csv_file = open(csvFileName, mode='w', encoding='UTF8') 
    fieldnames = ['Property', 'Space', 'AP Name', 'AP Model','Serial Number', 'AP Status', 'Client Count']
    writer = csv.writer(csv_file)
    writer.writerow(fieldnames)
    
    # Initialize R1 class and get JWT
    r1 = R1_API_calls()
    jwt = r1.getJWT(R1HOST, TENANT_ID, CLIENT_ID, SECRET_ID)['access_token']
    #print('jwt:', jwt)

    #brandDetails = r1.getBrandDetails(R1HOST, jwt)
    #print('brand details:', brandDetails)
        
    propertyList = r1.getProperties(R1HOST, jwt)['data']
    # print('properties:', propertyList)  
    
    # Loop through each property, get the required values and write .csv file
    for brandProperty in propertyList:
        print (brandProperty['name'])
        spaceList = r1.getVenues(R1HOST, brandProperty['id'], jwt)
        for space in spaceList:
            print(space['name'])
            apList = r1.getAPsByVenueId(R1HOST, brandProperty['id'], 
                                        space['id'], jwt)
            if len(apList) == 0:
                writer.writerow([brandProperty['name'], space['name'], '', '', 
                                 '', '', ''])
            for ap in apList:
                print(ap['name'])
                try:
                    apModel = ap['model']
                except:
                    apModel = 'Never contacted cloud'
                print(apModel)
                print(ap['serialNumber'])
                #print(ap['clientCount'])
                #print(ap['state'])
                writer.writerow([brandProperty['name'], space['name'], 
                                 ap['name'], apModel, ap['serialNumber'], 
                                 ap['state'], ap['clientCount']])
        print()

    # Close the csv file
    csv_file.close()
    print (csvFileName)


if __name__ == '__main__':
    main()
