# Specifica Protocollo: Sanrock U52

Questo documento raccoglie il reverse engineering parziale del protocollo relativo al drone *Sanrock U52*.

## Dati di Connessione (Hotspot Wi-Fi mode)
- **App Ufficiale**: SAN AIR
- **Frequenza**: 2.4 GHz
- **Indirizzo IP Drone (Target)**: `192.168.x.1` (Di solito `192.168.1.1` o `192.168.0.1`)
- **Porta UDP Drone (RX)**: `7080`
- **Porta UDP PC/App (TX)**: `7060`
- **Protocollo Trasporto**: `UDP`

## Struttura del Profilo di Rete
I comandi impartiti dall'app originale viaggiano in chiaro senza cifratura tramite pacchetti UDP binari di dimensione fissa (spesso ~14 byte). 

### Esempi Mappati (Hex)
- **Decollo (Takeoff)**: `cc 00 40 00 68 00 00 00 00 00 00 00 00 00`

### Note Tecniche
- Il drone espone direttamente il network a cui l'operatore (o lo script Python) deve agganciarsi come Client.
- Non avendo un SDK ufficiale, il comportamento meccanico dipende da questi byte generati.
- **Attenzione**: Potrebbe esserci un "heartbeat" (Keep-Alive) o il calcolo di un CRC. Le tracce `.pcap` riveleranno se sono presenti checksum dinamici nell'ultimo byte del frame.
