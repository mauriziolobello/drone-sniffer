# Piano di Sviluppo: Drone Sniffer

Progetto per costruire un packet sniffer in Python volto a catturare i pacchetti di droni (via Wi-Fi o rete cablata) per il reverse engineering dei comandi e permetterne la replica via computer.

## Obiettivi
1. Catturare pacchetti di droni in vari scenari (connessione diretta o sniffing passivo su un canale, a seconda dell'hardware/OS).
2. Analizzare i payload per comprendere la struttura dei comandi (diffing).
3. Replicare i comandi al drone tramite computer eseguendo packet injection/spoofing.
4. Supporto multi-piattaforma per i protocolli analizzati.

---

## Fase 1: Setup e Scelta degli Strumenti
La libreria principale scelta per l'implementazione in Python è **Scapy**. Questa permette cattura (sniffing) e forgiatura (spoofing) da zero dei pacchetti.

1. **Installazione librerie**:
   - Installare *Npcap* (su Windows).
   - Pacchetti Python: `scapy`, `colorama`.
   - Strumento raccomandato per analisi manuale visiva: *Wireshark*.
2. **Definizione della struttura del progetto**:
   - `src/sniffer.py` (cattura pacchetti).
   - `src/parser.py` (analisi e reverse engineering dei payload).
   - `src/injector.py` (replica comandi tramite packet crafting).
   - Strutturati come librerie generiche pronte ad espandersi a vari modelli di drone (es. Sanrock U52).

## Fase 2: Sniffer di Base (Rete Cablata / Rete Connessa)
Costruzione del sistema base di ricezione e interazione asincrona con le interfacce.
1. **Rilevamento interfacce**: Enumerazione delle interfacce Ethernet/Wi-Fi attive.
2. **Cattura asincrona**: Sfruttamento della funzione `sniff()` di Scapy integrando i filtri BPF.
3. **Analisi diagnostica base**: Possibilità di leggere traffico direttamente tra PC e drone se in stessa rete o tramite cavo, scartando i layer non utili.
4. **Logging**: Predisposizione per lo switch dei dump su file `.pcap` per analisi in dead-time.

## Fase 3: Sniffing Wi-Fi Specifico
Gestione della cattura pacchetti via aria a seconda dell'interazione hardware.
- **Scenario A (Drone = Access Point)**: PC connesso direttamente alla rete del drone. Cattura diretta del traffico UDP tramite Scapy (metodo standard supportato in modo nativo ovunque).
- **Scenario B (Traffico passivo tra radiocomando e drone)**: Prevede hardware abilitato alla Monitor Mode, generalmente in ambiente linux/WSL2 con airmon-ng.
1. **Filtraggio mirato**: Limitazione dei byte elaborati filtrando per BPF (es. MAC address o porte UDP predefinite).
2. **Estrazione payload**: Navigazione dei layer di rete da Ethernet->IP->UDP fino al layer "Raw".

## Fase 4: Analisi e Reverse Engineering (Modulo Parser)
Fase esplorativa e investigativa.
1. **Mappatura azioni**: Catturare pacchetti isolando singole azioni meccaniche fisiche (es. comando `Pitch`, comando `Throttle`).
2. **Differenziazione (Diffing)**: Confronto dei payload per identificare variazioni esadecimali nel pattern (Tipicamente `[Header Fisso] [Payload Comandi] [Checksum]`).
3. **Validazione Checksum**: Calcolo algoritmi standard (CRC8, CRC16) che spesso vengono usati alla fine del frame dai produttori per la consistenza dei pacchetti.

## Fase 5: Replicazione ed Esecuzione (Modulo Injector)
Creazione e trasmissione degli impulsi sintetici.
1. **Costruzione pacchetti (Forging)**: Modellazione del frame `IP(dst=...) / UDP(dport=...) / Raw(load=...)`.
2. **Injector routines**: Sviluppo funzioni ad alto livello come `takeoff()`, `land()`.
3. **Gestione del Keep-Alive**: Implementazione thread secondario volto all'invio dei pacchetti fittizi/heartbeat costanti necessari ai droni per impedire l'auto-landing d'emergenza, qualora il protocollo testato lo richieda.
