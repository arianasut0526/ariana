
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
            continue
        new_clause = [l for l in cl if l != -lit]
        new_formula.append(new_clause)
    return new_formula

def dp(formula):
    if not formula:
        return True
    if any(not c for c in formula):
        return False
    for cl in formula:
        if len(cl) == 1:
            return dp(simplifica(formula, cl[0]))
    lit = formula[0][0]
    return dp(simplifica(formula, lit)) or dp(simplifica(formula, -lit))

for num_clauze in [10, 100, 1000]:
    formula = genereaza_formula(num_clauze)
    print(f"\nTestare DP cu {num_clauze} clauze...")
    start = time.time()
    rezultat = dp(formula)
    durata = time.time() - start
    print(f"DP - {'Satisfiabilă' if rezultat else 'Nesatisfiabilă'} în {durata:.4f} secunde.")
