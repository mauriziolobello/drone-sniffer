import os
import sys
from scapy.all import sniff, get_if_list, PcapWriter
from src.parser import parse_payload

def get_interfaces():
    """Return network interfaces supported by scapy on all platforms."""
    return get_if_list()

def start_sniffing(interface, bpf_filter="", count=0, profile_name="sanrock_u52", pcap_file=None):
    """
    Start asynchronous sniffing on the given interface.
    Handles basic cross-platform checks and root privilege warnings.
    """
    print(f"[*] Starting capture on interface: {interface}...")
    print(f"[*] Using profile: {profile_name}")

    if sys.platform.startswith("win"):
        print("[i] Windows environment. Make sure Npcap is installed.")
    elif sys.platform.startswith("linux") or sys.platform == "darwin":
        if os.geteuid() != 0:
            print("[!] WARNING: You may need root permissions (sudo) to capture traffic correctly.")

    if bpf_filter:
        print(f"[*] BPF filter applied: '{bpf_filter}'")

    writer = None
    if pcap_file:
        print(f"[*] Saving capture to: {pcap_file}")
        writer = PcapWriter(pcap_file, append=True, sync=True)

    def packet_callback(packet):
        """Basic callback for CLI display of incoming packets."""
        parsed_info = parse_payload(packet, profile_name=profile_name)
        if parsed_info:
            print(f"Payload extracted -> {parsed_info}")
        else:
            print(packet.summary())
        
        if writer:
            writer.write(packet)

    sniff(iface=interface, filter=bpf_filter, count=count, prn=packet_callback, store=0)

    if writer:
        writer.close()
