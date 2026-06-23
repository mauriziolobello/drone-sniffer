"""
Profilo per il drone Sanrock U52.
Contiene le costanti note e la logica di estrazione/creazione dei pacchetti.
"""

# Parametri di rete (da confermare tramite sniffing DHCP)
DEFAULT_DRONE_IP = "192.168.1.1" # Segnaposto, solitamente terminante in .1
DEFAULT_DRONE_PORT = 7080
DEFAULT_APP_PORT = 7060

def parse(raw_data):
    """
    Decodifica di formattazione base per il payload del Sanrock U52.
    Riceve i byte estratti dal livello Raw() di scapy.
    """
    hex_string = raw_data.hex(' ')
    data_len = len(raw_data)
    
    # E' noto che i comandi base siano lunghi ~14 byte
    protocol_type = "CMD (~14 bytes)" if data_len == 14 else f"UKN ({data_len} bytes)"
    
    return f"[Sanrock U52 - {protocol_type}]: {hex_string}"

def get_predefined_command(action):
    """
    Ritorna il payload esadecimale hardcoded di azioni già note.
    """
    commands = {
        "takeoff": bytes.fromhex("cc 00 40 00 68 00 00 00 00 00 00 00 00 00"),
        # Altri comandi (land, avanti, indietro...) andranno decifrati qui
    }
    return commands.get(action.lower(), None)
