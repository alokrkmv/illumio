import random
import time

def generate_data(protocol):
    # Generating example values
    version = 2
    packet_id = random.randint(100000000000, 999999999999)
    eni_id = f"eni-{random.randint(1000000000, 9999999999)}"
    src_ip = f"10.0.{random.randint(0, 255)}.{random.randint(1, 254)}"
    dest_ip = f"198.51.100.{random.randint(1, 254)}"
    src_port = random.choice([443, 80, 53, 49153, 8083])  # Common ports
    dest_port = random.randint(1024, 65535, 8080)
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
for _ in range(100):
    protocol = random.choice(['TCP', 'UDP'])  # Randomly choose between TCP and UDP
    data_lines.append(generate_data(protocol))

# Write the generated data to a .log file
with open('data/generated_data.log', 'w') as log_file:
    for line in data_lines:
        log_file.write(line + '\n')

print("Data written to generated_data.log")
