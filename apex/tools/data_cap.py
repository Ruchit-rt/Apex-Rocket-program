import struct
import sys

LINE_SIZE = 16 * 4

if __name__ == '__main__':
    assert len(sys.argv) == 2
    log_file = sys.argv[1]
    with open(log_file, "rb") as log_file, open("data.csv", "w") as csv:
        csv.write("Time,i,j,k,w,Pressure,Temperature,Acc_x,Acc_y,Acc_z,Gyro_x,Gyro_y,Gyro_z,Mag_x,Mag_y,Mag_z\n")

        buf = log_file.read()
        for line in range(0, len(buf), LINE_SIZE):
            for i in range(0, LINE_SIZE, 4):
                csv.write(f"{struct.unpack('f', buf[line+i:line+i+4])[0]},")
            csv.write("\n")