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
        new_clause = [l for l in cl if l != -lit]  # Elimină literalul negativ
        if not new_clause:  # Dacă clauza devine goală, avem contradicție
            return None
        new_formula.append(new_clause)
    return new_formula

def dp(formula):
    if not formula:
        return True  # Dacă formula nu are clauze, este satisfiabilă
    if any(not c for c in formula):
        return False  # Dacă există o clauză goală, formula nu este satisfiabilă

    # Propagare unitară: caută clauze unitare
    for cl in formula:
        if len(cl) == 1:  # Dacă găsești o clauză unitară
            return dp(simplifica(formula, cl[0]))  # Simplifică formula și continuă recursiv

    # Dacă nu există clauze unitare, alegem un literal arbitrar și încercăm ambele ramuri (backtracking)
    lit = formula[0][0]
    formula_true = simplifica(formula, lit)
    if formula_true is not None and dp(formula_true):
        return True
    # Dacă nu am găsit soluție, încercăm complementul literalului
    formula_false = simplifica(formula, -lit)
    if formula_false is not None and dp(formula_false):
        return True

    return False  # Dacă nu găsește o soluție, formula este nesatisfiabilă

# Testare DP pentru formule cu 10, 100 și 1000 clauze
for num_clauze in [10, 100, 1000]:
    formula = genereaza_formula(num_clauze)
    print(f"\nTestare DP cu {num_clauze} clauze...")
    start = time.time()
    rezultat = dp(formula)
    durata = time.time() - start
    print(f"DP - {'Satisfiabilă' if rezultat else 'Nesatisfiabilă'} în {durata:.6f} secunde.")
