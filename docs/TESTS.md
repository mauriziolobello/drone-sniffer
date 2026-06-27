# Log dei Test sul Campo e Risoluzione Problemi (Linux)

Questo documento traccia i problemi riscontrati passando dallo sviluppo su Windows (con l'IDE Antigravity e l'AI gemella) ai test pratici su Linux, includendo i suggerimenti dell'IA e i workaround applicati dall'utente. È pensato per mantenere sincronizzato il contesto tra le sessioni.

## Difficoltà 1: Setup dell'Ambiente Python su Ubuntu/Debian
**Problema**: Su Windows bastava un `pip install`, ma su Linux il comando `python3 -m venv venv` falliva con l'errore `ensurepip is not available`.
**Soluzione**: Su sistemi Debian-based il supporto ai virtual environment non è incluso di default nel pacchetto base. L'utente ha dovuto prima lanciare `sudo apt install python3-venv` (o `python3.14-venv` a seconda della versione), poi ha creato il `venv` e installato i `requirements.txt`. Inoltre, `scapy` richiede l'esecuzione tramite `sudo`, cosa che costringe a lanciare esplicitamente l'eseguibile Python del venv (es. `sudo venv/bin/python main.py`).

## Difficoltà 2: Il PC non vedeva la rete Wi-Fi del drone
**Problema**: L'app ufficiale sullo smartphone rilevava l'SSID del drone (`udirc-FPV-52445E`), ma la scheda di rete del portatile Linux (`wlp2s0`) inizialmente non la mostrava.
**Analisi e Suggerimenti**:
1. **Rescan forzato**: Le schede dei PC a volte sono lente ad aggiornare le reti a 2.4 GHz. È stato suggerito `sudo nmcli dev wifi list --rescan yes`.
2. **Distanza**: Le antenne dei droni entry-level sono deboli, avvicinare il PC a 15-20 cm.
3. **Dominio Regolatorio (Regdomain)**: Su Linux la scheda potrebbe bloccare di default i canali 12/13. Suggerito di controllare con `iw reg get` e impostare su Italia (`sudo iw reg set IT`).
**Risoluzione**: Dopo una passata con `nmcli dev wifi list --rescan yes`, l'SSID `udirc-FPV-52445E` è comparso con segnale forte (95) sul Canale 1 (quindi non era un problema di canali alti), rendendo possibile la connessione.

## Difficoltà 3: Errore nel Push del Codice su GitHub
**Problema**: L'agente IA in background non aveva i permessi/credenziali per effettuare il `git push` in automatico (errore `fatal: could not read Username for 'https://github.com'`).
**Soluzione**: L'utente ha sfruttato la GitHub CLI (`gh`). È bastato eseguire `gh auth login` sul terminale per autenticare in modo sicuro Git tramite browser, impostando `gh` come credential helper. Successivamente, l'IA ha potuto fare push e commit in completa autonomia.

---
*Status attuale*: Attesa dei log `.pcap` reali per effettuare il reverse engineering dell'algoritmo di Checksum (attualmente implementato come finto XOR che dà esito `CRC FAIL`).
