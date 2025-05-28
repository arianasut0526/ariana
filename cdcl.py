
import random
import time
from collections import defaultdict, deque

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

def bcp(formula, assignment, trail, decision_level, implication_graph, reason_clauses):
    queue = deque()

    # Start cu toți literal ii deja setați
    for lit in [l for l in assignment if reason_clauses.get(l)]:
        queue.append(lit if assignment[l] else -l)

    while queue:
        current = queue.popleft()
        for clause in formula:
            unassigned = [l for l in clause if abs(l) not in assignment]
            true_lits = [l for l in clause if lit_true(l, assignment)]
            if not true_lits and not unassigned:
                # Conflict!
                return False, clause
            if len(unassigned) == 1 and not true_lits:
                unit = unassigned[0]
                var = abs(unit)
                val = unit > 0
                if var in assignment:
                    continue
                assignment[var] = val
                trail.append((var, decision_level))
                reason_clauses[var] = clause
                implication_graph[var] = [abs(l) for l in clause if abs(l) != var]
                queue.append(unit)
    return True, None

def analyze_conflict(conflict_clause, reason_clauses):
    # Simplificare: rezolvăm toate clauzele care au produs conflictul într-una singură
    learned_clause = set(conflict_clause)
    changed = True
    while changed:
        changed = False
        for lit in list(learned_clause):
            var = abs(lit)
            if var in reason_clauses:
                reason = reason_clauses[var]
                learned_clause.remove(lit)
                learned_clause.update(reason)
                changed = True
                break
    return list(learned_clause)

def backjump(trail, assignment, decision_level_target):
    to_remove = [var for var, level in trail if level > decision_level_target]
    for var in to_remove:
        assignment.pop(var, None)
    trail[:] = [t for t in trail if t[1] <= decision_level_target]

def pick_unassigned_variable(assignment, num_vars):
    for var in range(1, num_vars + 1):
        if var not in assignment:
            return var
    return None

def cdcl(formula, num_vars):
    assignment = {}
    trail = []
    decision_level = 0
    learned_clauses = []
    implication_graph = {}
    reason_clauses = {}

    while True:
        status, conflict_clause = bcp(formula + learned_clauses, assignment, trail, decision_level, implication_graph, reason_clauses)
        if not status:
            if decision_level == 0:
                return False  # Conflict at root level → UNSAT
            learned = analyze_conflict(conflict_clause, reason_clauses)
            learned_clauses.append(learned)
            # simplificare: backjump la nivelul anterior
            decision_level -= 1
            backjump(trail, assignment, decision_level)
            continue
        var = pick_unassigned_variable(assignment, num_vars)
        if var is None:
            return True  # Toate variabilele sunt atribuite → SAT
        # Decizie nouă
        decision_level += 1
        assignment[var] = True
        trail.append((var, decision_level))
        reason_clauses[var] = None  # decizie, nu implicare
        implication_graph[var] = []

for num_clauze in [10, 100, 1000]:
    formula = genereaza_formula(num_clauze)
    num_vars = max(abs(lit) for clause in formula for lit in clause)
    print(f"\nTestare CDCL cu {num_clauze} clauze...")
    start = time.time()
    rezultat = cdcl(formula, num_vars)
    durata = time.time() - start
    print(f"CDCL - {'Satisfiabilă' if rezultat else 'Nesatisfiabilă'} în {durata:.6f} secunde.")
