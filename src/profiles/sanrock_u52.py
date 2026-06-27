"""
Profile for the Sanrock U52 drone.
Contains known network constants and packet extraction/crafting logic.
"""

# Network parameters (to be confirmed via DHCP sniffing)
DEFAULT_DRONE_IP = "192.168.1.1"  # Placeholder, usually ending in .1
DEFAULT_DRONE_PORT = 7080
DEFAULT_APP_PORT = 7060

def calculate_checksum(data_bytes):
    """
    Calculate the XOR checksum for the given bytes (excluding the last byte).
    Note: This is a placeholder standard algorithm. Needs verification with real .pcap traces.
    """
    checksum = 0
    for b in data_bytes[:-1]:
        checksum ^= b
    return checksum

def validate_checksum(data_bytes):
    """Check if the last byte matches the XOR checksum of the preceding bytes."""
    if len(data_bytes) < 2:
        return False
    return calculate_checksum(data_bytes) == data_bytes[-1]

def parse(raw_data):
    """
    Basic formatting decoder for Sanrock U52 payloads.
    Receives bytes extracted from scapy's Raw() layer.
    """
    data_len = len(raw_data)

    # Known base commands are ~14 bytes long
    if data_len == 14:
        header = raw_data[:2]
        payload = raw_data[2:13]
        checksum = raw_data[13:]
        is_valid = validate_checksum(raw_data)
        valid_str = "VALID" if is_valid else "INVALID (CRC FAIL)"
        return f"[Sanrock U52 - CMD]: Header={header.hex()} | Payload={payload.hex(' ')} | Checksum={checksum.hex()} | {valid_str}"
    else:
        return f"[Sanrock U52 - UKN ({data_len} bytes)]: {raw_data.hex(' ')}"

def get_predefined_command(action):
    """Return the hardcoded hex payload for a known action, or None if unmapped."""
    commands = {
        "takeoff": bytes.fromhex("cc 00 40 00 68 00 00 00 00 00 00 00 00 00"),
        "heartbeat": bytes.fromhex("00 00 00 00"),  # PLACEHOLDER: to be found via sniffing
        # Other commands (land, forward, backward...) to be decoded here
    }
    return commands.get(action.lower(), None)
