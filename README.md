# Risoluzione del Capacitated Vehicle Routing Problem tramite algoritmo ACO
Questa repository contiene il codice e le istanze dei problemi relative al progetto di esame del corso 
di Heuristics and Meta-Heuristics tenuto dal professore Mario Pavone dell'Università di Catania.

E' stato implementato un algoritmo ACO _ibrido_ (in quanto vi si applica _2-Opt_ ai singoli mini-tour) basato su quanto presentato dall'articolo [Applying the ANT System to the Vehicle Routing Problem](https://www.researchgate.net/publication/2798782_Applying_the_ANT_System_to_the_Vehicle_Routing_Problem).

È stata inoltre adottata la strategia di _clamping_ dei feromoni da [MAX-MIN Ant System](https://www.sciencedirect.com/science/article/pii/S0167739X00000431), al fine di non stagnare la ricerca di soluzioni migliori, ed evitare fastidiosi problemi di stabilità numerica.

Infine, poiché eseguire l'algoritmo con Python incorre a penalità di performance, è stata implementata una semplice variante che usa la libreria `multiprocessing` per distribuire il lavoro su più core. 
> Todo: completare il readme


## Installazione
Si raccomanda l'uso del gestore di progetto Python [uv](https://docs.astral.sh/uv/).
### Installazione con uv
Installare le dipendenze
```sh
uv sync
```
## Uso
Vi sono due programmi richiamabili:
- `main.py` permette di eseguire l'algoritmo su di un file `.vrp`, permettendo la configurazione dei parametri.
- `grind.py` permette di eseguire l'algoritmo in batch su un insieme di file `.vrp` utilizzando i profili presentati dalla relazione.

### main.py

È possibile richiamare interrogare i parametri di `main.py`:

```bash
uv run main.py --help
usage: main.py [-h] [--iterations ITERATIONS] [--runs RUNS] [--seed SEED] [--alpha ALPHA] [--beta BETA] [--gamma GAMMA] [--lambda LAMBDA] [--rho RHO] [--sigma SIGMA]
               [--mmas MMAS] [--mmas-smoothing MMAS_SMOOTHING] [--two-opt TWO_OPT] [--save SAVE] [--show-plot SHOW_PLOT]
               instance

positional arguments:
  instance              File di istanza .vrp

options:
  -h, --help            show this help message and exit
  --iterations ITERATIONS
                        Numero di iterazioni
  --runs RUNS           Numero di prove
  --seed SEED           Seed per il generatore pseudorandom
  --alpha ALPHA         Influenza del feromone
  --beta BETA           Influenza della visibilità
  --gamma GAMMA         Influenza del risparmio
  --lambda LAMBDA       Influenza della capacità
  --rho RHO             Costante di evaporazione
  --sigma SIGMA         Numero di formiche elitarie. Default numero di clienti.
  --mmas MMAS           Applica MAX-MIN
  --mmas-smoothing MMAS_SMOOTHING
                        Applica MAX-MIN smoothing
  --two-opt TWO_OPT     Applica 2-Opt
  --save SAVE           Salva la soluzione in formato JSON
  --show-plot SHOW_PLOT
                        Mostra la soluzione a schermo
```
Un possibile esempio di invocazione può essere:
```bash
uv run main.py instances/CMT1.vrp.ignore --iterations 1000 --seed 1234 --rho 0.25 --alpha 1 --beta 5 --gamma 5 --lambda 5 --save results/CMT.json
```

Il seguente comando esegue l'algoritmo sull'istanza `instances/CMT1.vrp.ignore`, usando il seed `1234` con i parametri:
- Coefficiente di evaporazione $\rho = 0.25$.
- Influenza del feromone $\alpha = 1$. 
- Influenza della visibilità $\beta = 5$. 
- Influenza della misura di risparmio $\gamma = 6$ 
- Influenza della misura di capacità $\lambda = 6$ 
- Formiche elitarie $\sigma=K$, _2-Opt_ e _MAX-MIN_. 

A fine esecuzione, mostrerà a schermo la soluzione migliore trovata, e salverà la soluzione in formato JSON nel file `results.json`.

### grind.py
Eseguire la raccolta di informazione per i profili già predisposti ( NN, HAS, HAS-SAV, HAS-CAP, HAS-1, HAS-5 ) sulle istanze del problema.

È possibile richiamare interrogare i parametri di `grind.py`:
```sh
uv run grind.py --help
usage: grind.py [-h] [--instances INSTANCES] [--fe FE] [--runs RUNS] [--seed SEED] output

positional arguments:
  output                File di output (.csv)

options:
  -h, --help            show this help message and exit
  --instances INSTANCES
                        Percorso delle istanze .vrp
  --fe FE               Numero di fitness evaluation
  --runs RUNS           Esecuzioni per istanza
  --seed SEED           Seed per il generatore pseudorandom
```
Il seguente esempio genera tutti i risultati usati nella relazione.
```sh
uv run main.py output.csv
```

Si fa presente che i tempi di elaborazioni potrebbero superare le 24 ore.

![E questa immagine è stata uno spreco di token.](relazione/spreco-di-token.png)