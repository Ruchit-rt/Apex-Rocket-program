import socket
import struct
import random
import sys

IP = "35.7897"
UDP_PORT = 8080

if __name__ == '__main__':
    assert len(sys.argv) == 2
    with open(sys.argv[1], "r") as f:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.sendto(bytes("start", "ascii"), (IP, UDP_PORT))
        data = (list(map(float, i.split(","))) for i in f.readlines())

        for vals in data:
            arr = bytearray(45)
            struct.pack_into("b", arr, 0, 97)
            struct.pack_into("f", arr, 1+0, vals[0]) #time
            struct.pack_into("f", arr, 1+4, vals[1]) #i
            struct.pack_into("f", arr, 1+8, vals[2]) #j
            struct.pack_into("f", arr, 1+12, vals[3]) #k
            struct.pack_into("f", arr, 1+16, vals[4]) #w
            struct.pack_into("f", arr, 1+20, vals[5]) #p
            struct.pack_into("f", arr, 1+24, vals[6]) #t
            struct.pack_into("f", arr, 1+28, vals[7]) #a_x
            struct.pack_into("f", arr, 1+32, vals[8]) #a_y
            struct.pack_into("f", arr, 1+40, alt(i) + random.uniform(-3, 3))
            sock.sendto(bytes(arr), (IP, UDP_PORT))

        sock.sendto(bytes("end", "ascii"), (IP, UDP_PORT))
