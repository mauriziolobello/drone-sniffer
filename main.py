import argparse
import sys
from src.sniffer import get_interfaces, start_sniffing
from src.parser import get_profile
from src.injector import craft_command, send_command, KeepAliveThread

def main():
    parser = argparse.ArgumentParser(description="Drone Packet Sniffer & Injector")
    parser.add_argument("--list-interfaces", action="store_true", help="List available network interfaces")
    parser.add_argument("--interface", type=str, help="Network interface to listen on")
    parser.add_argument("--filter", type=str, default="", help="Optional BPF filter (e.g. 'udp')")
    parser.add_argument("--profile", type=str, default="sanrock_u52", help="Drone profile to use (default: sanrock_u52)")
    parser.add_argument("--send", type=str, help="Action to send (e.g. 'takeoff')")
    parser.add_argument("--pcap", type=str, help="File to save captured packets (e.g. 'capture.pcap')")
    parser.add_argument("--keep-alive", action="store_true", help="Start background keep-alive thread")

    args = parser.parse_args()

    if args.list_interfaces:
        print("[*] Detected network interfaces:")
        for iface in get_interfaces():
            print(f" - {iface}")
        sys.exit(0)

    if not args.interface:
        print("Specify an interface with --interface, or list available ones with --list-interfaces.")
        sys.exit(1)

    profile = get_profile(args.profile)
    if not profile:
        print(f"[X] Profile '{args.profile}' not found in src/profiles/")
        sys.exit(1)

    keep_alive_thread = None
    if args.keep_alive:
        heartbeat_payload = profile.get_predefined_command("heartbeat")
        if heartbeat_payload:
            packet = craft_command(profile.DEFAULT_DRONE_IP, profile.DEFAULT_DRONE_PORT, heartbeat_payload)
            keep_alive_thread = KeepAliveThread(args.interface, packet, interval=0.05)
            keep_alive_thread.start()
            print("[*] Keep-alive thread started in background.")
        else:
            print("[!] Profile does not define a 'heartbeat' payload.")

    try:
        if args.send:
            action = args.send
            payload = profile.get_predefined_command(action)
            if payload:
                print(f"[*] Sending '{action}' using profile '{args.profile}'...")
                packet = craft_command(profile.DEFAULT_DRONE_IP, profile.DEFAULT_DRONE_PORT, payload)
                send_command(args.interface, packet)
                print("[+] Command sent successfully.")
            else:
                print(f"[X] Action '{action}' not found in profile '{args.profile}'.")
            sys.exit(0)

        start_sniffing(args.interface, args.filter, profile_name=args.profile, pcap_file=args.pcap)
    except KeyboardInterrupt:
        print("\n[!] Capture interrupted by user.")
    except Exception as e:
        print(f"\n[X] Error during execution: {e}")
    finally:
        if keep_alive_thread:
            keep_alive_thread.stop()
            keep_alive_thread.join()
            print("[*] Keep-alive thread stopped.")

if __name__ == "__main__":
    main()
