# Guida Offline per il Reverse Engineering del Drone

Questa guida è stata creata per aiutarti a proseguire il lavoro mentre sei collegato alla Wi-Fi del drone (`udirc-FPV-52445E`) e sei temporaneamente scollegato da internet e dall'assistenza dell'IA.

Segui queste casistiche in ordine.

---

## 1. Avvio Normale (Cattura Dati)

Il tuo obiettivo primario è **registrare** cosa si dicono l'app ufficiale e il drone.

1. **Connettiti** al Wi-Fi del drone dal PC e dallo Smartphone. Apri l'app sul telefono.
2. Apri il terminale nella cartella `Drone Sniffer`.
3. Avvia lo sniffer salvando tutto in un file (così se qualcosa va storto avremo i log):
   ```bash
   sudo venv/bin/python main.py --interface wlp2s0 --pcap sessione1.pcap
   ```
   > *Nota: evito di farti usare `--keep-alive` per ora, perché il payload "00 00 00 00" è inventato e potrebbe dare fastidio. Usa il telefono per mantenere il drone attivo.*

4. **Operazione sul campo**: Dal telefono premi UN SOLO comando (es. decollo). Aspetta 5 secondi. Premi un altro comando (es. atterraggio). 

---

## 2. Casistica: Nessun pacchetto a schermo

Se non vedi scorrere nulla a terminale mentre premi i tasti sull'app, significa che l'IP del drone o la porta non sono quelli standard (`192.168.1.1:7080`).

### Workaround: Trovare i veri parametri
Interrompi lo script (`Ctrl+C`) e lancia un raw dump con tcpdump per guardare il traffico UDP grezzo:
```bash
sudo tcpdump -i wlp2s0 -n udp
```
Ora premi i comandi sull'app del cellulare. Vedrai righe simili a:
`192.168.x.x.12345 > 192.168.y.y.7080: UDP, length 14`
Appuntati l'IP di destinazione e la porta. Quando tornerai online, modificheremo `DEFAULT_DRONE_IP` e `DEFAULT_DRONE_PORT` nel file `src/profiles/sanrock_u52.py`.

---

## 3. Casistica: I pacchetti appaiono ma c'è scritto "(CRC FAIL)"

**Questo è il comportamento atteso!**
Significa che la nostra funzione di calcolo XOR per il Checksum è sbagliata per questo modello di drone.

### Workaround: Raccogliere dati per il Reverse Engineering
Se vedi `(CRC FAIL)`, non ti preoccupare, i pacchetti vengono comunque estratti e stampati.
Copia e incolla l'output di almeno 3 o 4 comandi diversi (es. decollo, atterraggio, flip) in un file di testo temporaneo:
```text
[Sanrock U52 - CMD]: Header=cc00 | Payload=... | Checksum=... | INVALID (CRC FAIL)
```
Quando ti ricollegherai a internet, passami questi output. Avendo diversi esempi reali in cui la coppia "Payload" -> "Checksum" è valida (perché generata dall'app originale), potrò dedurre l'algoritmo matematico esatto per il CRC.

---

## 4. Casistica: Vuoi provare a iniettare un comando (Spoofing)

Se sei riuscito a mappare un comando o vuoi testare l'iniezione, puoi dire al PC di inviare lui stesso il segnale di decollo.
Mentre il drone è acceso e l'app del telefono è collegata:
```bash
sudo venv/bin/python main.py --interface wlp2s0 --send takeoff
```

### Se non succede nulla:
1. **CRC Errato**: Il drone scarta il pacchetto perché l'ultimo byte calcolato dalla nostra funzione XOR non coincide con quello che il drone si aspetta.
2. **Conflitto con l'App**: L'app ufficiale sta bombardando il drone di comandi "stai fermo" che sovrascrivono il nostro comando. 

---

## 5. Ritorno Online

Una volta finito di estrarre i log o salvato il file `.pcap`, riconnettiti al Wi-Fi di casa (es. `FRITZ!Box 7590 GS`):
```bash
nmcli dev wifi connect "FRITZ!Box 7590 GS"
```

A questo punto:
1. Incollami gli output testuali dei pacchetti che hanno fallito il CRC.
2. Eventualmente, fammi analizzare il file `sessione1.pcap` generato, mi aiuterà a capire anche come funziona il pacchetto di Heartbeat/Keep-Alive per far volare il drone da PC senza usare lo smartphone in futuro.
