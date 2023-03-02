import csv
import os
import sys
import time
from pymodbus.client.sync import ModbusTcpClient

def main():

    if (len(sys.argv) != 2):
        print("Usage: python3 capture-from-plc.py <logfile>")
        sys.exit(1)

    print("Writing to log: " + sys.argv[1])
    sys.stdout.flush()

    logfile = "/home/hmi/data-capture/log/" + sys.argv[1]

    plc = ModbusTcpClient("192.168.56.2")
    prevLine = []

    while True:
        with open(logfile, "a+", encoding="utf8") as fp:

            w = csv.writer(fp)

            try:
                input_resp = plc.read_input_registers(100, 2)
                disc_resp = plc.read_discrete_inputs(800, 100)
                coils_resp = plc.read_coils(800, 15)

                if input_resp.isError() or disc_resp.isError() or coils_resp.isError(): continue

                data = []

                for i in range(len(disc_resp.bits)):
                    if disc_resp.bits[i] == True: disc_resp.bits[i] = 1
                    elif disc_resp.bits[i] == False: disc_resp.bits[i] = 0

                for i in range(len(coils_resp.bits)):
                    if coils_resp.bits[i] == True: coils_resp.bits[i] = 1
                    elif coils_resp.bits[i] == False: coils_resp.bits[i] = 0

                if len(prevLine) > 0:
                    # input regs
                    data.append(input_resp.registers[0] / 100)                  # MC01 Progress
                    data.append((input_resp.registers[0] / 100) - prevLine[0])  # MC01 Progress diff
                    data.append(input_resp.registers[1] / 100)                  # MC02 Progress
                    data.append(input_resp.registers[1] - prevLine[2])          # MC02 Progress diff

                    # discretes
                    data.append(disc_resp.bits[0])                      # discrete 0
                    data.append(disc_resp.bits[0] - prevLine[4])        # discrete 0 diff
                    data.append(disc_resp.bits[1])                      # discrete 1
                    data.append(disc_resp.bits[1] - prevLine[6])        # discrete 1 diff
                    data.append(disc_resp.bits[2])                      # discrete 2
                    data.append(disc_resp.bits[2] - prevLine[8])        # discrete 2 diff
                    data.append(disc_resp.bits[3])                      # discrete 3
                    data.append(disc_resp.bits[3] - prevLine[10])       # discrete 3 diff
                    data.append(disc_resp.bits[4])                      # discrete 4
                    data.append(disc_resp.bits[4] - prevLine[12])       # discrete 4 diff
                    data.append(disc_resp.bits[5])                      # discrete 5
                    data.append(disc_resp.bits[5] - prevLine[14])       # discrete 5 diff
                    data.append(disc_resp.bits[6])                      # discrete 6
                    data.append(disc_resp.bits[6] - prevLine[16])       # discrete 6 diff
                    data.append(disc_resp.bits[7])                      # discrete 7
                    data.append(disc_resp.bits[7] - prevLine[18])       # discrete 7 diff
                    data.append(disc_resp.bits[8])                      # discrete 8
                    data.append(disc_resp.bits[8] - prevLine[20])       # discrete 8 diff
                    data.append(disc_resp.bits[9])                      # discrete 9
                    data.append(disc_resp.bits[9] - prevLine[22])       # discrete 9 diff


                    # coils
                    data.append(coils_resp.bits[0])                     # coil 0
                    data.append(coils_resp.bits[1])                     # coil 1
                    data.append(coils_resp.bits[2])                     # coil 2
                    data.append(coils_resp.bits[3])                     # coil 3
                    data.append(coils_resp.bits[4])                     # coil 4
                    data.append(coils_resp.bits[5])                     # coil 5
                    data.append(coils_resp.bits[6])                     # coil 6
                    data.append(coils_resp.bits[7])                     # coil 7
                    data.append(coils_resp.bits[8])                     # coil 8
                    data.append(coils_resp.bits[9])                     # coil 9
                    data.append(coils_resp.bits[10])                    # coil 10
                    data.append(coils_resp.bits[11])                    # coil 11
                    data.append(coils_resp.bits[12])                    # coil 12
                    data.append(coils_resp.bits[13])                    # coil 13
                    data.append(coils_resp.bits[14])                    # coil 14

                # first input
                else:
                # input regs
                    data.append(input_resp.registers[0] / 100)          # MC01 Progress
                    data.append(0)                                      # MC01 Progress diff
                    data.append(input_resp.registers[1] / 100)          # MC02 Progress
                    data.append(0)                                      # MC02 Progress diff

                    # discretes
                    data.append(disc_resp.bits[0])                      # discrete 0
                    data.append(0)                                      # discrete 0 diff
                    data.append(disc_resp.bits[1])                      # discrete 1
                    data.append(0)                                      # discrete 1 diff
                    data.append(disc_resp.bits[2])                      # discrete 2
                    data.append(0)                                      # discrete 2 diff
                    data.append(disc_resp.bits[3])                      # discrete 3
                    data.append(0)                                      # discrete 3 diff
                    data.append(disc_resp.bits[4])                      # discrete 4
                    data.append(0)                                      # discrete 4 diff
                    data.append(disc_resp.bits[5])                      # discrete 5
                    data.append(0)                                      # discrete 5 diff
                    data.append(disc_resp.bits[6])                      # discrete 6
                    data.append(0)                                      # discrete 6 diff
                    data.append(disc_resp.bits[7])                      # discrete 7
                    data.append(0)                                      # discrete 7 diff
                    data.append(disc_resp.bits[8])                      # discrete 8
                    data.append(0)                                      # discrete 8 diff
                    data.append(disc_resp.bits[9])                      # discrete 9
                    data.append(0)                                      # discrete 9 diff


                    # coils
                    data.append(coils_resp.bits[0])                     # coil 0
                    data.append(coils_resp.bits[1])                     # coil 1
                    data.append(coils_resp.bits[2])                     # coil 2
                    data.append(coils_resp.bits[3])                     # coil 3
                    data.append(coils_resp.bits[4])                     # coil 4
                    data.append(coils_resp.bits[5])                     # coil 5
                    data.append(coils_resp.bits[6])                     # coil 6
                    data.append(coils_resp.bits[7])                     # coil 7
                    data.append(coils_resp.bits[8])                     # coil 8
                    data.append(coils_resp.bits[9])                     # coil 9
                    data.append(coils_resp.bits[10])                    # coil 10
                    data.append(coils_resp.bits[11])                    # coil 11
                    data.append(coils_resp.bits[12])                    # coil 12
                    data.append(coils_resp.bits[13])                    # coil 13
                    data.append(coils_resp.bits[14])                    # coil 14

                prevLine = data
                w.writerow(data)
                time.sleep(0.1)

            except KeyboardInterrupt as k:
                plc.close()
                fp.close()
                break

            except Exception as e:
                print(e)
                continue

if __name__ == "__main__":
    main()
