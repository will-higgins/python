## this Python script will find which zone your IP address is located behind
## the zones are head on an excel document 
## the excel doc is called firewall-zone.xlsx

import pandas as pd
import ipaddress


# Define the list IPs that you want to search against the Excel Document 
ip_list = ["10.1.1.1", "10.2.2.3", "10.3.3.3"]

## Here willl read the excel doc into the pandas Data frame 

df=pd.read_excel("firewall-zone.xlsx")

#define an emply list to store the results
results = []

#loop over the list of IPs to the find the zone
for ip_address_str in ip_list:
    #find the row in the document to the IP address
    row = df.loc[df['IP address'] == ip_address_str]

## If the row exists, print the name of the zone

    if not row.empty:
        zone = row['zone'].values[0]
        results.append({'zone': zone, 'IP address': ip_address_str})
    else:
    #if not exact match is found, check if it matches with a larger subnet
        for index, row in df.iterrows():
         if "/" in row["IP address"]:
            network = ipaddress.IPv4Network(row["IP address"])
            if ipaddress.IPv4Address(ip_address_str) in network:
                zone = row["zone"]
                results.append({'zone': zone, 'IP address': ip_address_str})
                ##print(f"The IP adderess {ip_address_str} belongs to the {zone} zone")
                break
        else:
            results.append({'zone': 'unkown', 'IP address': ip_address_str})

#Create a new panads dataframe to store the results
results_df = pd.DataFrame(results, columns=['zone', 'IP address'])

#print the results as a table
print(results_df)