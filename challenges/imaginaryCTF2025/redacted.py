cipher = "kfÁgÌyot\\jÄ^Öfe_cbÐXÐo`r{uÁhØo}".encode("latin1")

for shift in range(1, len(cipher)):
    recovered = bytes([cipher[i] ^ cipher[(i+shift) % len(cipher)] for i in range(len(cipher))])
    if b"ictf{" in recovered:
        print("Possible flag:", recovered.decode(errors="ignore"))
