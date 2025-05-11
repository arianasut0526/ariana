

import random
import time

def genereaza_formula(num_clauze, num_literali=10, max_lungime=4):
    formula = []
    for _ in range(num_clauze):
        lungime = random.randint(1, max_lungime)
        clauza = random.sample(range(1, num_literali + 1), lungime)
        clauza = [lit if random.random() < 0.5 else -lit for lit in clauza]
        formula.append(clauza)
    return formula

def rezolva_clauze(C1, C2):
    resolvents = set()
    for l in C1:
        if -l in C2:
            new_clause = (C1 | C2) - {l, -l}
            resolvents.add(frozenset(new_clause))
    return resolvents

def rezolutie(formula):
    clauze = [set(cl) for cl in formula]
    new = set()
    while True:
        n = len(clauze)
        for i in range(n):
            for j in range(i + 1, n):
                resolvents = rezolva_clauze(clauze[i], clauze[j])
                if frozenset() in resolvents:
                    return False
                new |= resolvents
        if new.issubset(set(map(frozenset, clauze))):
            return True
        for cl in new:
            if cl not in clauze:
                clauze.append(set(cl))

for num_clauze in [10, 100, 1000]:
    formula = genereaza_formula(num_clauze)
    print(f"\nTestare Rezolutie cu {num_clauze} clauze...")
    start = time.time()
    rezultat = rezolutie(formula)
    durata = time.time() - start
    print(f"Rezolutie - {'Satisfiabilă' if rezultat else 'Nesatisfiabilă'} în {durata:.6f} secunde.")
