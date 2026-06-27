# Drone Packet Sniffer & Injector

A cross-platform (Windows, Linux, macOS) Python packet sniffer and injector for capturing,
analysing, and replaying the control protocols of various drones (including the Sanrock U52).

## Project Structure
- `src/sniffer.py`: Interface detection and asynchronous packet capture.
- `src/parser.py`: Reverse engineering of hex payloads extracted from packets.
- `src/injector.py`: Frame crafting and command forwarding (spoofing) to the drone.
- `main.py`: CLI entry point.

## Prerequisites
- **Windows**: Install [Npcap](https://npcap.com/) (make sure to select
  "Install Npcap in WinPcap API-compatible Mode" and the raw 802.11 support options if needed).
- **Linux**: You need root privileges to sniff/inject (use `sudo python3 main.py ...`).
  Install the requirements via system package manager or create a `venv`:
  ```bash
  sudo apt update
  sudo apt install python3-scapy python3-colorama python3-pytest
  ```

Install Python dependencies (if on Windows or using venv):
```bash
pip install -r requirements.txt
```

## First Capture (Quick Start)

### Scenario A — Drone as Access Point (recommended on Windows)
The drone creates its own Wi-Fi network. Both the PC and the smartphone connect to that network,
allowing the PC to intercept UDP traffic between the official app and the drone.

**1. Connect the PC to the drone's Wi-Fi**
Find the drone's network in the Windows Wi-Fi list and connect (usually no password or a fixed one).
Do not use your home network.

**2. Discover the interface name**
```bash
python main.py --list-interfaces
```
Look for the name matching your Wi-Fi adapter (typically `Wi-Fi` on Windows).

**3. Start a broad capture to explore the traffic**
```bash
python main.py --interface "Wi-Fi"
```
Open the official app on the phone and press **one single command** (e.g. takeoff).
Observe in the console the UDP source/destination ports and the length of the Raw payloads shown.

**4. Restart with a targeted filter**
Once you have identified the port (e.g. `7080`), reduce noise:
```bash
python main.py --interface "Wi-Fi" --filter "udp port 7080"
```
Press one command at a time in the app and note the hex payload displayed.
That payload is the raw command to map inside the drone's profile.

> **Note:** for a parallel visual analysis, launch Wireshark on the same interface
> with the same BPF filter.
