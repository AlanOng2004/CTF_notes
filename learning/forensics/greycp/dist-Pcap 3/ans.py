import pandas as pd
from base64 import b64decode

df = pd.read_csv("pcap3.csv")

msg = ""

for i in df["Info"].dropna():
    if ".welc0mectf.gr3yh4ts.com" in i:
        query = i.split(".welc0mectf.gr3yh4ts.com")[0]
        query = query.split()[-1]   # get last token before domain
        msg += query

print(b64decode(msg))

