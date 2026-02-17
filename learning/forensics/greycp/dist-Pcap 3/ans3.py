import pandas as pd
from base64 import b64decode

# Load the dataset
df = pd.read_csv("pcap3.csv")

msg = ""
seen_queries = set()

# 1. Filter for DNS protocols only
# 2. Extract only Standard queries (not responses) to avoid duplication
for i in df[df["Protocol"] == "DNS"]["Info"].dropna():
    if "Standard query " in i and ".welc0mectf.gr3yh4ts.com" in i:
        # Extract the base64 part
        # Format: "Standard query 0x... A [B64_DATA].welc0mectf..."
        try:
            parts = i.split(".welc0mectf.gr3yh4ts.com")[0].split()
            query = parts[-1] # The last token is the B64 string
            
            # Use a set to prevent adding the same chunk twice if retransmitted
            if query not in seen_queries:
                msg += query
                seen_queries.add(query)
        except IndexError:
            continue

# Decode and clean the output
try:
    decoded_flag = b64decode(msg).decode('utf-8', errors='ignore')
    print(f"Decoded Message: {decoded_flag}")
except Exception as e:
    print(f"Error decoding: {e}")
    print(f"Raw string was: {msg}")
