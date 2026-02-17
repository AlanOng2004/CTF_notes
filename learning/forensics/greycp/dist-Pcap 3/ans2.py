import re

hex_pattern = re.compile(r'0x[0-9a-fA-F]+')

hex_values = set()

with open("pcap3.csv", "r") as f:
    for i in f:
        parts = i.split(" ")
        if len(parts) > 3:              # <-- fix
            query = parts[3]
            matches = hex_pattern.findall(query)
            hex_values.update(matches)

print(hex_values)

