import random
import csv

# Define at least 10 protocols and their associated port ranges
protocols_ports = {
    "tcp": [20, 21, 22, 23, 25, 80, 110, 143, 443, 3389, 993],
    "udp": [53, 67, 68, 69, 123, 161, 162, 500, 520],
    "icmp": [0, 8, 31, 128],
    "http": [80],
    "https": [443],
    "ftp": [20, 21],
    "dns": [53],
    "dhcp": [67, 68],
    "snmp": [161, 162],
    "ntp": [123],
    "smtp": [25],
    "pop3": [110],
    "imap": [143]
}

# Define possible tags (at least 20 different tags)
tags = [
    "sv_P1", "sv_P2", "sv_P3", "sv_P4", "sv_P5", "email", "web", 
    "dns", "dhcp", "vpn", "ftp", "remote", "snmp", "ntp", 
    "firewall", "load_balancer", "database", "monitor", 
    "security", "iot"
]

# Function to generate a random mapping of port, protocol, and tag
def generate_data(num_records=100):
    data = []
    
    for _ in range(num_records):
        # Randomly choose a protocol
        protocol = random.choice(list(protocols_ports.keys()))
        
        # Randomly choose a port from the protocol's port list
        port = random.choice(protocols_ports[protocol])
        
        # Randomly choose a tag
        tag = random.choice(tags)
        
        # Append the generated record to the data list
        data.append([port, protocol, tag])
    
    return data

# Function to save the generated data to a CSV file
def save_to_csv(filename, data):
    header = ['dstport', 'protocol', 'tag']
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

# Generate 100 records of data
data = generate_data(100)

# Save to a CSV file
save_to_csv('generated_lookup_table.csv', data)

print("Data generation complete. Saved to 'protocol_lookup.csv'.")