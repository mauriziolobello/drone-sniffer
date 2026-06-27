# Development Plan: Drone Sniffer

Python packet sniffer aimed at capturing drone packets (via Wi-Fi or wired network)
for reverse engineering their control commands and replaying them from a PC.

## Goals
1. Capture drone packets in various scenarios (direct connection or passive channel sniffing,
   depending on hardware/OS).
2. Analyse payloads to understand the command structure (diffing).
3. Replay commands to the drone from a PC via packet injection/spoofing.
4. Multi-drone protocol support through a profile-based architecture.

---

## Phase 1: Setup and Tooling
The main library chosen for the Python implementation is **Scapy**, which supports both
packet capture (sniffing) and crafting (spoofing) from scratch.

1. **Install dependencies**:
   - Install *Npcap* (Windows).
   - Python packages: `scapy`, `colorama`.
   - Recommended tool for manual visual analysis: *Wireshark*.
2. **Define the project structure**:
   - `src/sniffer.py` (packet capture).
   - `src/parser.py` (payload analysis and reverse engineering).
   - `src/injector.py` (command replay via packet crafting).
   - Structured as generic libraries ready to expand to multiple drone models (e.g. Sanrock U52).

## Phase 2: Basic Sniffer (Wired / Connected Network)
Build the base system for receiving and asynchronously interacting with interfaces.
1. **Interface detection**: Enumerate active Ethernet/Wi-Fi interfaces.
2. **Asynchronous capture**: Use Scapy's `sniff()` function with BPF filters.
3. **Basic diagnostic analysis**: Read traffic directly between PC and drone on the same network
   or via cable, discarding unused layers.
4. **Logging**: Prepare a switch to dump captures to `.pcap` files for dead-time analysis.

## Phase 3: Wi-Fi-Specific Sniffing
Handle packet capture over the air depending on hardware interaction.
- **Scenario A (Drone = Access Point)**: PC connected directly to the drone's network.
  Direct UDP traffic capture via Scapy (standard method, natively supported everywhere).
- **Scenario B (Passive traffic between remote controller and drone)**: Requires hardware
  with Monitor Mode enabled, typically Linux/WSL2 with airmon-ng.
1. **Targeted filtering**: Limit processed bytes by filtering on BPF (e.g. MAC address
   or predefined UDP ports).
2. **Payload extraction**: Navigate network layers from Ethernet→IP→UDP down to the Raw layer.

## Phase 4: Analysis and Reverse Engineering (Parser Module)
Exploratory and investigative phase.
1. **Action mapping**: Capture packets by isolating single physical mechanical actions
   (e.g. `Pitch` command, `Throttle` command).
2. **Diffing**: Compare payloads to identify hex variations in the pattern
   (typically `[Fixed Header] [Command Payload] [Checksum]`).
3. **Checksum validation**: Calculate standard algorithms (CRC8, CRC16) commonly used
   by manufacturers at the end of the frame for packet consistency.

## Phase 5: Replay and Execution (Injector Module)
Create and transmit synthetic impulses.
1. **Packet crafting (Forging)**: Model the frame `IP(dst=...) / UDP(dport=...) / Raw(load=...)`.
2. **Injector routines**: Develop high-level functions such as `takeoff()`, `land()`.
3. **Keep-Alive management**: Implement a secondary thread for sending periodic
   dummy/heartbeat packets required by drones to prevent emergency auto-landing,
   where the tested protocol requires it.

## Architecture and Multi-Drone Profiles
The project is based on a **profile** architecture (`src/profiles/`) to allow easy extension
to multiple drones and protocols (e.g. `sanrock_u52.py`).
Each profile defines in isolation: the target IP, operational ports, optional custom parsing
logic, and the library of known payloads (hexadecimal).

---

## Current Code State

| File | Responsibility | Status |
|------|----------------|--------|
| `main.py` | CLI: `--list-interfaces`, `--interface`, `--filter` | ✅ Working (listen mode only) |
| `src/sniffer.py` | Interface enumeration + async `sniff()` with callback | ✅ Working |
| `src/parser.py` | Extracts `Raw` layer and delegates to profile | ✅ Working (hardcoded profile) |
| `src/profiles/sanrock_u52.py` | Network constants + `parse()` + known command library | 🟡 Only `takeoff` mapped |
| `src/injector.py` | Spoofing packet construction and sending | ✅ Working (`craft_command` & keep-alive) |
| `src/__init__.py`, `src/profiles/__init__.py` | Package initialisation | ✅ |

---

## Open Gaps

1. **No checksum** — CRC8/CRC16 validation (Phase 4.3) is planned but not implemented. Without a correct checksum, injected packets risk being dropped by the drone.
2. **Zero tests** — No `tests/` folder. Parsing and checksums are byte-deterministic → ideal for TDD with `pytest` without physical hardware.

---

## Next Steps (by priority)

- **A — Checksum Validation**: Implement CRC8/CRC16 calculation in the profile to ensure injected packets are accepted.
- **B — Tests (`pytest`)**: Write deterministic tests for the parser and checksum logic.
- **C — Richer parsing**: Split header/payload/checksum instead of printing flat hex to speed up reverse engineering.

---

## Legal and Ethical Notes

Sniffing and injection must be performed **only on hardware you own** and in authorised contexts
(reverse engineering your own drone, research, educational purposes).

---

## Reverse Engineering Operational Workflow (Field Approach)
To add commands for an unknown drone or test a new one, follow this operational procedure:

1. **Parallel connection**: Connect both the smartphone (using the official app) and the PC
   (with the Sniffer) to the Wi-Fi network/hotspot generated by the drone.
2. **Sniffer / Wireshark setup**: Start the sniffer (or listen via Wireshark) on the Wi-Fi
   interface. Set BPF filters immediately (e.g. `udp port 7080`) to limit packet flow to the
   command channel only.
   *CLI example*:
   ```bash
   python main.py --interface "Wi-Fi" --filter "udp port 7080"
   ```
3. **Event isolation**: From the phone, physically press one and only one command in the app
   (e.g. tap takeoff or push the throttle forward).
4. **Live capture and interpretation**: Read the traffic from the terminal/Wireshark.
   Isolate the last hex payload captured at the Raw/Data layer.
5. **Profile mapping**: Hardcode those bytes inside the Python profile
   (e.g. in `get_predefined_command("takeoff")`), certifying which command that byte sequence
   corresponds to. Repeat from step 3.
