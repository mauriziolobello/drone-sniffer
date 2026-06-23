import os
import sys
from scapy.all import sniff, get_if_list, conf

def get_interfaces():
    """Rileva in modo multipiattaforma le interfacce di rete supportate da scapy."""
    return get_if_list()

def packet_callback(packet):
    """Callback di base per la visualizzazione a CLI dei pacchetti in arrivo."""
    # TODO: Invocare il modulo parser.py qui per analizzare payload specifici
    print(packet.summary())

def start_sniffing(interface, bpf_filter="", count=0):
    """
    Avvia il processo di sniffing asincrono.
    Gestisce controlli basilari per il cross-platform e privilegi di root.
    """
    print(f"[*] Inizio cattura sull'interfaccia: {interface}...")
    
    if sys.platform.startswith("win"):
        print("[i] Ambiente Windows. Assicurati che Npcap sia installato.")
    elif sys.platform.startswith("linux") or sys.platform == "darwin":
        if os.geteuid() != 0:
            print("[!] ATTENZIONE: Potresti necessitare dei permessi di root (sudo) per catturare correttamente.")
            
    if bpf_filter:
        print(f"[*] Filtro BPF applicato: '{bpf_filter}'")

    sniff(iface=interface, filter=bpf_filter, count=count, prn=packet_callback, store=0)
