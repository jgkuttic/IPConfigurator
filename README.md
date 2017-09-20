# IPConfigurator
This script generates subnet information about the IP addresses passed in through command line arguments or typed in

## Instructions

### How to run the script
```sh
$ python3 ipconfigurator.py
```

### Passing in command line arguments
```sh
$ python3 ipconfigurator.py 10.23.32.23
```

### Example run
```sh
$ python3 ipconfigurator.py 10.23.32.23

Calculating IP information for: 10.23.32.23
============================================
Network Address: 10.0.0.0
Broadcast Address: 10.255.255.255
Subnet Address: 255.0.0.0
Wildcard Address: 0.255.255.255
Host Range: 10.0.0.1 - 10.255.255.254
IP Address Class: A
Number of Subnetworks: 1
Hosts/Network: 16777214
Private IP:  True
--------------------------------------------

Enter IP address: 192.23.233.4/26

Calculating IP information for: 192.23.233.4
============================================
Network Address: 192.23.233.0
Broadcast Address: 192.23.233.63
Subnet Address: 255.255.255.192
Wildcard Address: 0.0.0.63
Host Range: 192.23.233.1 - 192.23.233.62
IP Address Class: C
Number of Subnetworks: 4
Hosts/Network: 62
Private IP:  False
--------------------------------------------

Enter IP address: 
```



