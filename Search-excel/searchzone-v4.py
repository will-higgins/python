## this Python script will find which zone your IP address is located behind
## the zones are head on an excel document 
## the excel doc is called firewall-zone.xlsx
## in this version the user will input the IPs that they want to search for

import pandas as pd
import ipaddress

## Here willl read the excel doc into the pandas Data frame 

df=pd.read_excel("firewall-zone.xlsx")

# Prompt the user for the a list of IP address
#ip_input = input("enter a comma-separated list of IP adddresses to search: ")
ip_input = input("Enter an IP address or subnet to search")

# check if the input is valid IP Address or subnet
try:
   ip_network = ipaddress.ip_network(ip_input)
   #If the input is a subnet, get a list of all IP addresses in the subnet
   ip_list = [str(ip) for ip in ip_network.hosts()]
except ValueError:
   #if the input is not valid subnet, assume its a single IP address
   ip_list = [ip_input]

# split the input string into a list of IP addresses
#ip_list = [ip.strip() for ip in ip_input.split(",")]

# define an empty list to store the results

results = []

#loop over the list of IPs to the find the zone
for ip_address_str in ip_list:
    #find the row in the document to the IP address
    row = df.loc[df['IP address'] == ip_address_str]

## If the row exists, print the name of the zone

    if not row.empty:
        zone = row['zone'].values[0]
        firewall = row['firewall'].values[0]
        results.append({'zone': zone, 'firewall': firewall, 'IP address': ip_address_str})
    else:
    #if not exact match is found, check if it matches with a larger subnet
        for index, row in df.iterrows():
         if "/" in row["IP address"]:
            network = ipaddress.IPv4Network(row["IP address"])
            if ipaddress.IPv4Address(ip_address_str) in network:
                zone = row["zone"]
                firewall = row['firewall']
                results.append({'zone': zone, 'firewall': firewall, 'IP address': ip_address_str})
                ##print(f"The IP adderess {ip_address_str} belongs to the {zone} zone")
                break
        else:
            results.append({'zone': 'unkown', 'firewall': 'unkown', 'IP address': ip_address_str})

#Create a new panads dataframe to store the results
results_df = pd.DataFrame(results, columns=['firewall', 'zone', 'IP address'])

#print the results as a table
print(results_df)