
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

def lit_true(lit, assignment):
    var = abs(lit)
    if var not in assignment:
        return None
    return assignment[var] if lit > 0 else not assignment[var]

def bcp(formula, assignment):
    changed = True
    while changed:
        changed = False
        for clause in formula:
            unassigned = [l for l in clause if abs(l) not in assignment]
            true_lits = [l for l in clause if lit_true(l, assignment)]
            if not true_lits and not unassigned:
                return False
            if len(unassigned) == 1 and not true_lits:
                unit = unassigned[0]
                assignment[abs(unit)] = unit > 0
                changed = True
    return True

def pick_unassigned_variable(formula, assignment):
    for clause in formula:
        for lit in clause:
            if abs(lit) not in assignment:
                return abs(lit)
    return None

def cdcl_recursive(formula, assignment, learned):
    if not bcp(formula + learned, assignment):
        return False
    if all(abs(l) in assignment for clause in formula for l in clause):
        return True
    var = pick_unassigned_variable(formula, assignment)
    for value in [True, False]:
        new_assign = assignment.copy()
        new_assign[var] = value
        result = cdcl_recursive(formula, new_assign, learned)
        if result:
            return True
        else:
            learned.append([-var if value else var])
    return False

def cdcl(formula):
    assignment = {}
    learned = []
    return cdcl_recursive(formula, assignment, learned)

for num_clauze in [10, 100, 1000]:
    formula = genereaza_formula(num_clauze)
    print(f"\nTestare CDCL cu {num_clauze} clauze...")
    start = time.time()
    rezultat = cdcl(formula)
    durata = time.time() - start
    print(f"CDCL - {'Satisfiabilă' if rezultat else 'Nesatisfiabilă'} în {durata:.4f} secunde.")
