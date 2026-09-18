
import socket
import struct
import time

# NTP_SERVER = "pool.ntp.org"
NTP_SERVER = "iotcore-ntp-v1.pre.eu.iotcore.liebherr.eu"
NTP_PORT = 123
NTP_PACKET_SIZE = 48

# NTP client request: LI=0, VN=4, Mode=3
packet = bytearray(NTP_PACKET_SIZE)
packet[0] = 0x23

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.settimeout(5)
    sock.sendto(packet, (NTP_SERVER, NTP_PORT))

    response, addr = sock.recvfrom(512)

print(f"Received {len(response)} bytes from {addr}")

# Extract NTP header fields
li_vn_mode = response[0]
stratum = response[1]

li = (li_vn_mode >> 6) & 0x03
vn = (li_vn_mode >> 3) & 0x07
mode = li_vn_mode & 0x07

print(f"Leap indicator: {li}")
print(f"NTP version:    {vn}")
print(f"Mode:           {mode}")
print(f"Stratum:        {stratum}")