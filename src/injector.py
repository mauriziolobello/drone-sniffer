from scapy.all import sendp, IP, UDP, Raw

def craft_command(drone_ip, dport, payload_bytes):
    """
    Costruisce lo stack di rete necessario per inviare il colpo.
    Basato sull'ipotesi frequente TCP/IP -> UDP -> Raw Payload.
    """
    # Esempio di struttura, personalizzabile dopo il reverse engineering
    # packet = IP(dst=drone_ip) / UDP(dport=dport) / Raw(load=payload_bytes)
    pass

def send_command(interface, packet):
    """
    Esegue l'iniezione (spoofing) del pacchetto forgiato nell'interfaccia.
    """
    # verbose=False nasconde il log di scapy dell'invio ad ogni frame
    sendp(packet, iface=interface, verbose=False)
