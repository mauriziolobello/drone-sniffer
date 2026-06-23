# Drone Packet Sniffer & Injector

Un packet sniffer e injector cross-platform (Windows, Linux, macOS) scritto in Python per catturare, analizzare e replicare i protocolli di controllo di vari droni (tra cui il Sanrock U52).

## Struttura del Progetto
- `src/sniffer.py`: Modulo per la rilevazione delle interfacce e la cattura asincrona.
- `src/parser.py`: Modulo per il reverse engineering dei payload esadecimali estratti dai pacchetti.
- `src/injector.py`: Modulo per fondere frame di rete e inoltrare i comandi (spoofing) al drone.
- `main.py`: Punto di ingresso dell'applicazione CLI.

## Prerequisiti
- **Windows**: Installare [Npcap](https://npcap.com/) (assicurarsi di selezionare "Install Npcap in WinPcap API-compatible Mode" e le opzioni per il supporto raw 802.11 se richieste).
- **Linux/macOS**: Assicurarsi di eseguire gli script con privilegi di root (`sudo`).

Installare le dipendenze Python:
```bash
pip install -r requirements.txt
```
