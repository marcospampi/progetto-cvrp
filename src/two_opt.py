import numpy as np

def cost_change(D, n1, n2, n3, n4):
    return (D[n1, n3] + D[n2, n4]) - (D[n1, n2] + D[n3, n4])

def two_opt(customer_tour, D):
    """
    Accetta un tour di soli clienti (es. [3, 1, 2, 4])
    Restituisce il tour ottimizzato (di soli clienti)
    """
    # 1. Inietta il deposito all'inizio e alla fine
    tour = [0] + list(customer_tour) + [0]
    tour = np.asarray(tour)
    
    improved = True
    n = len(tour)
    savings = 0
    while improved:
        improved = False
        
        # Facciamo girare il 2-opt bloccando gli zeri agli estremi
        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                
                n1 = tour[i - 1]
                n2 = tour[i]
                n3 = tour[j]
                n4 = tour[j + 1]
                
                delta = cost_change(D, n1, n2, n3, n4)
                
                if delta < -1e-9:
                    tour[i:j + 1] = tour[i:j + 1][::-1]
                    improved = True
                    savings -= delta
                    break
            if improved:
                break
                
    # 2. Rimuove il deposito prima di restituire il vettore
    return tour[1:-1].tolist(), savings