from src.profiles import sanrock_u52

def parse_payload(packet, profile_name="sanrock_u52"):
    """
    Isola il payload raw dal pacchetto.
    L'implementazione finale dependerà dall'analisi del protocollo.
    Se richiamata per un profilo noto, formatta l'output.
    """
    if packet.haslayer("Raw"):
        # Estraiamo i byte grezzi
        raw_data = packet.getlayer("Raw").load
        
        # Delegazione al profilo per parser specifico
        if profile_name == "sanrock_u52":
            return sanrock_u52.parse(raw_data)
            
        return f"[Byte Raw Non Mappati]: {raw_data.hex(' ')}"
    return None
