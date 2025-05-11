
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

def simplifica(formula, lit):
    new_formula = []
    for cl in formula:
        if lit in cl:
            continue  # Clauza este satisfăcută
        new_clause = [l for l in cl if l != -lit]
        if not new_clause:  # Dacă clauza devine goală, avem contradicție
            return None
        new_formula.append(new_clause)
    return new_formula

def dpll(formula, assignments={}):
    if not formula:  # Dacă toate clauzele sunt satisfăcute, formula este satisfiabilă
        return True
    if any(not c for c in formula):  # Dacă există o clauză goală (contradicție), formula nu este satisfiabilă
        return False

    # Propagare unitară: găsește clauzele unitare
    unit = [cl[0] for cl in formula if len(cl) == 1]
    while unit:
        lit = unit.pop()
        formula = simplifica(formula, lit)
        if formula is None:
            return False
        assignments[lit] = True
        # Căutăm din nou clauze unitare după simplificare
        unit = [cl[0] for cl in formula if len(cl) == 1]

    # Dacă formula este satisfăcută (fără clauze rămase), întoarcem True
    if not formula:
        return True

    # Alegem un literal pentru backtracking (alegere arbitrară)
    lit = formula[0][0]
    # Testăm cazul în care îl setăm la True
    formula_true = simplifica(formula, lit)
    if formula_true is not None and dpll(formula_true, {**assignments, lit: True}):
        return True
    # Dacă nu am găsit soluție, testăm cazul în care îl setăm la False
    formula_false = simplifica(formula, -lit)
    if formula_false is not None and dpll(formula_false, {**assignments, lit: False}):
        return True

    return False

# Testare DPLL pentru formule cu 10, 100 și 1000 clauze
for num_clauze in [10, 100, 1000]:
    formula = genereaza_formula(num_clauze)
    print(f"\nTestare DPLL cu {num_clauze} clauze...")
    start = time.time()
    rezultat = dpll(formula)
    durata = time.time() - start
    print(f"DPLL - {'Satisfiabilă' if rezultat else 'Nesatisfiabilă'} în {durata:.6f} secunde.")
