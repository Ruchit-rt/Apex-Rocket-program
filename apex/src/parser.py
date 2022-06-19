import struct

try: 
    with open("datafile", "rb") as f:
        out = open("out.csv", "w")
        out.write("Time, AccX, AccY, AccZ, GyroX, GyroY, GyroZ, MagX, MagY, MagZ, LinAccX, LinAccY, LinAccZ, GRV1, GRV2, GRV3 ,GRV4 ,ROT1, ROT2, ROT3, ROT4, Pressure, Temperature\n")
        bytes = f.read(92)
        while bytes:
            #lol why was this so easy
            out.write(", ".join(map(str, struct.unpack("Iffffffffffffffffffffff", bytes))))
            out.write('\n')
            bytes = f.read(92)
except IOError:
    print('Error While Opening the file!')  

