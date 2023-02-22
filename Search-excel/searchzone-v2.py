## this Python script will find which zone your IP address is located behind
## the zones are head on an excel document 
## the excel doc is called firewall-zone.xlsx

import pandas as pd
import ipaddress

## you will define the IP address you want to search for here

ip_address_str = "10.1.1.1"

## Here willl read the excel doc into the pandas Data frame 

df=pd.read_excel("firewall-zone.xlsx")

## Find the row in the data that corresponds to IP address

row = df.loc[df['IP address'] == ip_address_str]

## If the row exists, print the name of the zone

if not row.empty:
    zone = row['zone'].values[0]
    print(f"The IP adderess {ip_address_str} belongs to the {zone} zone")
else:
    #if not exact match is found, check if it matches with a larger subnet
    for index, row in df.iterrows():
        if "/" in row["IP address"]:
            network = ipaddress.IPv4Network(row["IP address"])
            if ipaddress.IPv4Address(ip_address_str) in network:
                zone = row["zone"]
                print(f"The IP adderess {ip_address_str} belongs to the {zone} zone")
                break
    else:
        print(f"unable to find a zone")