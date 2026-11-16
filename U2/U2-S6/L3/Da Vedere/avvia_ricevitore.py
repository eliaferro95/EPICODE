import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("192.168.50.100", 137))
print("Ascolto sulla porta 137...")
while True:
    data, addr = s.recvfrom(1024)
    print(f"Ricevuti {len(data)} byte da {addr}")
