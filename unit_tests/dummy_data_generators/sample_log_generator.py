import random
import time

protocols_ports = {
    "tcp": [20, 21, 22, 23, 25, 80, 110, 143, 443, 3389, 993, 8000, 9000],
    "udp": [53, 67, 68, 69, 123, 161, 162, 500, 520, 460, 780, 900, 730],
    "icmp": [0, 8, 31, 128, 80, 90, 3939],
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

number_of_items = 100000

def generate_data():
    # Generating example values
    version = 2
    packet_id = random.randint(100000000000, 999999999999)
    eni_id = f"eni-{random.randint(1000000000, 9999999999)}"
    src_ip = f"10.0.{random.randint(0, 255)}.{random.randint(1, 254)}"
    dest_ip = f"198.51.100.{random.randint(1, 254)}"
    src_port = random.choice([443, 80, 53, 49153, 8083])  # Common ports
    dest_port_array = []
    for _, value in protocols_ports.items():
        dest_port_array.extend(value)
    dest_port_index = random.randint(0, len(dest_port_array)-1)
    dest_port = dest_port_array[dest_port_index]
    protocol_num = random.randint(1, 20)
    packet_size = random.randint(20, 1500)
    total_bytes = random.randint(20000, 50000)
    start_time = int(time.time())
    end_time = start_time + random.randint(1, 10)
    action = random.choice(['ACCEPT', 'DROP'])
    status = random.choice(['OK', 'FAIL'])

    return f"{version} {packet_id} {eni_id} {src_ip} {dest_ip} {src_port} {dest_port} {protocol_num} {packet_size} {total_bytes} {start_time} {end_time} {action} {status}"

# Generate 100 lines of data
data_lines = []
for _ in range(number_of_items):
    data_lines.append(generate_data())

# Write the generated data to a .log file
with open('generated_data.log', 'w') as log_file:
    for line in data_lines:
        log_file.write(line + '\n')

print("Data written to generated_data.log")
