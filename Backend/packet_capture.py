from scapy.all import sniff
import pandas as pd
import time
from pandas.io.common import file_exists

packets_data = []
CSV_FILE = "traffic_log.csv"

def capture_packet(packet):
    global packets_data

    # Extract packet details
    packets_data.append([time.time(), packet.src, packet.dst, len(packet)])

    # Save after every 100 packets
    if len(packets_data) >= 100:
        df = pd.DataFrame(packets_data, columns=["Time", "Source", "Destination", "Size"])
        
        # Append instead of overwriting
        df.to_csv(CSV_FILE, mode='a', header=not file_exists(CSV_FILE), index=False)
        packets_data.clear()  # Clear in-memory data

try:
    print("[+] Starting Packet Capture... Press Ctrl+C to stop.")
    sniff(prn=capture_packet, store=False, iface="Wi-Fi", filter="ip")
except KeyboardInterrupt:
    print("\n[+] Stopping Capture. Saving remaining packets...")
    if packets_data:
        df = pd.DataFrame(packets_data, columns=["Time", "Source", "Destination", "Size"])
        df.to_csv(CSV_FILE, mode='a', header=not file_exists(CSV_FILE), index=False)
    print("[+] Capture Stopped. Data Saved to 'traffic_log.csv'.")
except Exception as e:
    print(f"[!] An error occurred: {e}")
