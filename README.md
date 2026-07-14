# Risoluzione del Capacitated Vehicle Routing Problem tramite algoritmo ACO
Questa repository contiene il codice e le istanze dei problemi relative al progetto di esame del corso 
di Heuristics and Meta-Heuristics tenuto dal professore Mario Pavone dell'Università di Catania.

E' stato implementato un algoritmo ACO _ibrido_ (in quanto vi si applica _2-Opt_ ai singoli mini-tour) basato su quanto presentato dall'articolo [Applying the ANT System to the Vehicle Routing Problem](https://www.researchgate.net/publication/2798782_Applying_the_ANT_System_to_the_Vehicle_Routing_Problem).

È stata inoltre adottata la strategia di _clamping_ dei feromoni da [MAX-MIN Ant System](https://www.sciencedirect.com/science/article/pii/S0167739X00000431), al fine di non stagnare la ricerca di soluzioni migliori, ed evitare fastidiosi problemi di stabilità numerica.

Infine, poiché eseguire l'algoritmo con Python è come andare alle poste il primo del mese, è stata implementata una semplice variante che usa la libreria `multiprocessing` per distribuire il lavoro su più core, nonostante ciò il programma non usa a pieno le risorse, ma meglio che eseguire su un unico core. Idea fantasiosamente ispirata da [Using the Ant Colony Optimization algorithm for the Capacitated Vehicle Routing Problem](https://ieeexplore.ieee.org/document/7018311/).

> Todo: completare il readme


## Installazione
Si raccomanda l'uso del software `uv`.
### Installazione con uv
Installare le dipendenze
```sh
uv sync
```
Eseguire la raccolta di informazione per i profili già predisposti ( NN, HAS, HAS-SAV, HAS-CAP, HAS-1, HAS-5 ) sulle istanze del problema.
```sh
uv run main.py output.csv
```