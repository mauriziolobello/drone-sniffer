def parse_payload(packet):
    """
    Isola il payload raw dal pacchetto.
    L'implementazione finale dependerà dall'analisi del protocollo Sanrock U52.
    """
    if packet.haslayer("Raw"):
        # Estraiamo i byte grezzi
        raw_data = packet.getlayer("Raw").load
        # TODO: Aggiungere logica di analisi differenziale 
        # (es. individuare header fisso e byte di comando)
        return raw_data
    return None
