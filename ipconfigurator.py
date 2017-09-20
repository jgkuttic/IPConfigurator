import sys
import re

#Function that gets user input
def get_user_input():
    user_input = input("Enter IP address: ")
    return user_input

#Function takes in an IP address and converts into binary
def dec_to_binary(ip_address):
    return map(lambda x: bin(x)[2:].zfill(8), ip_address)
    
#Function that takes in the IP address and checks if it is valid
def validate_ip(ip_address):
    ip = ip_address.split(".")
    if len(ip) != 4:
        return False
    for i in ip:
        if not i.isdigit():
            return False
        num = int(i)
        if num < 0 or num > 255:
            return False
    return True

#Function that takes in the network mask and checks if it is valid
def validate_subnet_mask(network_mask):
    if not network_mask.isdigit():
        return False
    num = int(network_mask)
    if num < 0 or num > 32:
        return False
    return True

#Function that takes in the IP address and checks if it is a private IP
def is_private_ip(ip_address):
    pattern = "(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^192\.168\.)"
    if re.match(pattern, ip_address):
        return True
    return False

#Function that calculates the maximum number of hosts from the network mask
def get_max_hosts(mask):
    if mask >= 2:
        mask = 2**(32-network_mask)
    return mask - 2

#Function that calculates the maximum number of subnets from the network mask
def get_max_subnets(mask):
    mask = mask % 8
    return 2**mask

#Function that calculates the wildcard/cicso address from the network mask
def get_wildcard_address(mask):
    mask = ~(~0 << (32 - mask))
    return "%d.%d.%d.%d" % (mask >> 24 & 255,
                            mask >> 16 & 255,
                            mask >> 8 & 255,
                            mask & 255)

#Function that calculates the subnet address from the network mask
def get_subnet_address(mask):
    mask = ~0 << (32 - mask)
    return "%d.%d.%d.%d" % (mask >> 24 & 255,
                            mask >> 16 & 255,
                            mask >> 8 & 255,
                            mask & 255)

#Function that calculates the network address from anding the binary ip address and binary subnet address
def get_network_address(binary_ip, binary_subnet_address):
    network_address = []
    for x, y in zip(binary_ip, binary_subnet_address):
        network_address.append(int(x, 2) & int(y, 2))
    return network_address

#Function that calculates the network address from anding the binary ip address and binary wildcard address
def get_broadcast_address(binary_ip, binary_wildcard_address):
    broadcast_address = []
    for x, y in zip(binary_ip, binary_wildcard_address):
        broadcast_address.append(int(x, 2) | int(y, 2))
    return broadcast_address

#Function that returns binary IP address
def get_binary_ip(ip_address):
    return dec_to_binary(map(int, ip_address.split(".")))

#Function that determines that class of an IP
def get_class_type(ip_address):
    first_octet = int(ip_address.split(".")[0])

    if first_octet >= 0 and first_octet <= 126:
        return "A"
    elif first_octet == 127:
        return "Loopback address"
    elif first_octet >= 128 and first_octet <= 191:
        return "B"
    elif first_octet >= 192 and first_octet <= 223:
        return "C"
    elif first_octet >= 224 and first_octet <= 239:
        return "D"
    else:
        return "E"

#Function takes in the network address and broadcast address and returns the host range.
def get_host_range(network_address, broadcast_address):
    min_range = network_address[:]
    min_range[-1] += 1
    max_range = broadcast_address[:]
    max_range[-1] -= 1
    return "%s - %s" % (".".join(map(str, min_range)), ".".join(map(str, max_range)))

#Function takes in all the information and prints them out all the information
def print_ip_information(ip_address, subnet_address, wildcard_address, broadcast_address, network_address, ip_address_class,
number_of_subnets, number_of_hosts, private_ip, host_range):
    print("")
    print("Calculating IP information for:", ip_address)
    print("============================================")
    print("Network Address:", ".".join(map(str, network_address)))
    print("Broadcast Address:", ".".join(map(str, broadcast_address)))
    print("Subnet Address:", subnet_address)
    print("Wildcard Address:", wildcard_address)
    print("Host Range:", host_range)
    print("IP Address Class:", ip_address_class)
    print("Number of Subnetworks:", number_of_subnets)
    print("Hosts/Network:", number_of_hosts)
    print("Private IP: ", private_ip)
    print("--------------------------------------------")
    print("")

run = True
user_input = None

#Checking for passed in arguments
if len(sys.argv) <= 1:
    user_input = get_user_input()
else:
    user_input = sys.argv[1]

while run:
    if user_input == "q" or user_input == "quit":
        run = False
    else:
        args = user_input.split("/")
        ip_address = args[0]
        if len(args) > 1:
            network_mask = args[1]
            if not validate_ip(ip_address):
                print("Please Enter Valid IP Address")
                print("")
            elif not validate_subnet_mask(network_mask):
                print("Please Enter Valid Subnet Mask")
                print("")
            else:
                ip_address_class = get_class_type(ip_address)
                network_mask = int(network_mask)
                subnet_address = get_subnet_address(network_mask)
                wildcard_address = get_wildcard_address(network_mask)
                number_of_hosts = get_max_hosts(network_mask)
                number_of_subnets = get_max_subnets(network_mask)
                private_ip = is_private_ip(ip_address)
                network_address = get_network_address(get_binary_ip(ip_address), get_binary_ip(subnet_address))
                broadcast_address = get_broadcast_address(get_binary_ip(ip_address), get_binary_ip(wildcard_address))
                host_range = get_host_range(network_address, broadcast_address)

                print_ip_information(ip_address, subnet_address, wildcard_address, broadcast_address, network_address, ip_address_class,
                number_of_subnets, number_of_hosts, private_ip, host_range)
        else:
            if not validate_ip(ip_address):
                print("Please Enter Valid IP Address")
                print("")
            else:
                ip_address_class = get_class_type(ip_address)
                if ip_address_class == "A":
                    network_mask = 8
                elif ip_address_class == "B":
                    network_mask = 16
                elif ip_address_class == "C":
                    network_mask = 24
                else:
                    network_mask = 8
                subnet_address = get_subnet_address(network_mask)
                wildcard_address = get_wildcard_address(network_mask)
                number_of_hosts = get_max_hosts(network_mask)
                number_of_subnets = get_max_subnets(network_mask)
                network_address = get_network_address(get_binary_ip(ip_address), get_binary_ip(subnet_address))
                broadcast_address = get_broadcast_address(get_binary_ip(ip_address), get_binary_ip(wildcard_address))
                private_ip = is_private_ip(ip_address)
                host_range = get_host_range(network_address, broadcast_address)

                print_ip_information(ip_address, subnet_address, wildcard_address, broadcast_address, network_address, ip_address_class,
                number_of_subnets, number_of_hosts, private_ip, host_range)

        user_input = get_user_input()
sys.exit()
