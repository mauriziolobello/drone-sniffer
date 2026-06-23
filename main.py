import argparse
import sys
from src.sniffer import get_interfaces, start_sniffing

def main():
    parser = argparse.ArgumentParser(description="Sanrock U52 Packet Sniffer & Injector")
    parser.add_argument("--list-interfaces", action="store_true", help="Elenca le interfacce di rete disponibili")
    parser.add_argument("--interface", type=str, help="L'interfaccia di rete su cui mettersi in ascolto")
    parser.add_argument("--filter", type=str, default="", help="Filtro BPF opzionale (es. 'udp')")

    args = parser.parse_args()

    if args.list_interfaces:
        print("[*] Interfacce di rete rilevate:")
        for iface in get_interfaces():
            print(f" - {iface}")
        sys.exit(0)

    if args.interface:
        try:
            start_sniffing(args.interface, args.filter)
        except KeyboardInterrupt:
            print("\n[!] Cattura interrotta dall'utente.")
        except Exception as e:
            print(f"\n[X] Errore durante la cattura: {e}")
    else:
        print("Specifica un'interfaccia per eseguire lo sniffing con --interface, oppure visualizza la lista con --list-interfaces.")

if __name__ == "__main__":
    main()
