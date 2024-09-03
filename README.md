# RUCKUS-One-Python
Python scripts examples for RUCKUS One.

**R1_example1** uses the account credentials to retrieve the jwt token, using the function **getToken**.

**R1_example2** uses an API KEY to retrieve the jwt token. This is the recommended method. First you need to create an API KEY in the RUCKUS One UI, then use the client id and client secret to generate a jwt token using the function **getJWT**.

**R1_example3** is an example on how to manage delegated accounts.

**R1_hospitality_edition** retrieves Properties, Spaces, APs, AP parameters and clients from a R1 Hospitality Edition instance and writes that data in a .csv file (R1 Hospitality Edition uses delegated accounts in a way that is similar to MSP/MSP-ECs.

**R1_API** is the module with all the API calls used in the examples above.
