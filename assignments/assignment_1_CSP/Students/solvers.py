#
# Informed Search Methods
#
# Implementation of various backtracking-based solvers.
#

from enum import Enum
import copy


class SolverType(Enum):
    GTBT = 1  # Generate-and-test Backtracking
    BT = 2  # Cronological Backtracking
    BJ = 3  # Backjumping
    CBJ = 4  # Conflict-Directed Backjumping


def make_arc_consistent(cn):
    """
    Makes the cn constraint network arc-consistent (use the AC-3 algorithm).
    (there are no unary-constraints, so you can omit making it first node-consistent).
    """

    # ===> Your task is to implement this routine. Feel free to add sub-routines as needed.

    def remove_inconsistent_values(csp, cell_i, cell_j):

        removed = False

        domain = csp.get_domain(cell_i)

        values_to_remove = []

        for value in csp.get_domain(cell_i):
            to_remove = True
            for poss in csp.get_domain(cell_j):
                if value != poss:
                    to_remove = False
            if to_remove:
                values_to_remove.append(value)
                removed = True
        csp.set_domain(cell_i, domain - set(values_to_remove))

        return removed

    queue = cn.get_constraints()

    while queue:

        (xi, xj) = queue.pop(0)

        if remove_inconsistent_values(cn, xi, xj):

            if len(cn.get_domain(xi)) == 0:
                return False

            for Xk in cn.get_vars_in_constraint_with(xi):
                if Xk != xi:
                    queue.append((Xk, xi))

    return True


def solve(st, cnet):
    """
    Use the specified backtracking algorithm (st) to solve the CSP problem (cnet).
    Returns a tuple (assignment, nodes), where the former is the solution (an empty list if not found)
    and the latter the number of nodes generated.
    """

    def consistent_upto_level(cn, i, A):
        for j in range(0, i):
            if not cn.consistent(i, j, A):
                return j
        return i

    def GTB(cn, i, A):
        # print(A)
        nonlocal num_nodes
        num_nodes += 1
        if i >= cn.num_variables():
            return cn.consistent_all(A)
        for v in cn.get_sorted_domain(i):
            A.append(v)
            solved = GTB(cn, i+1, A)
            if solved:
                return True
            A.pop()
        return False


    def BT(cn, i, A):
        # ===> Your task is to implement this routine.
        nonlocal num_nodes
        num_nodes += 1
        if len(A) == 0:
            A = [0] * cn.num_variables()
        for value in cn.get_domain(i):
            A[i] = value
            consistency_level = consistent_upto_level(cn, i, A)
            if consistency_level == i:
                if i == cn.num_variables() - 1:
                    return True
                else:
                    BT(cn, i + 1, A)
        return False

    def BJ(cn, i, A):
        # ===> Your task is to implement this routine.
        nonlocal num_nodes
        num_nodes += 1
        return_depth = 0
        if len(A) == 0:
            A = [0] * cn.num_variables()
        for val in cn.get_domain(i):
            A[i] = val
            max_check_level = consistent_upto_level(cn, i, A)
            if max_check_level == i:
                if i == 80:
                    print(A)
                if i == cn.num_variables() - 1:
                    return True, num_nodes
                else:
                    (_, max_check_level) = BJ(cn, i + 1, A)
                    if max_check_level < i:
                        return _, max_check_level
            return_depth = max(return_depth, max_check_level)
        return False, return_depth

    def CBJ(cn, i, A, CS):

        # Data structure to track the changes in the domains of variables
        domain_changes = [set() for _ in range(cn.num_variables())]

        def select_value_CBJ(cn, i, A, CS):
            #Increase the number of visited nodes
            nonlocal num_nodes
            num_nodes += 1
            while len(cn.domains[i]) > 0:
                consistent = True
                #Select an arbitrary value from the domain of Xi
                value = cn.domains[i].pop()
                # Track the change
                domain_changes[i].add(value)
                # Add the value to the partial assignment and check consistency with the previous variables
                A.insert(i, value)
                consistency_level = consistent_upto_level(cn, i, A)
                # If the value is not consistent with the previous variables, add the level of the last variable
                # breaking the consistency and remove the value from the partial assignment, else return the value
                if consistency_level != i:
                    consistent = False
                    CS[i].add(consistency_level)
                    A.pop(i)
                if consistent:
                    return value
            return None

        # Variable to track the maximum level reached during this partial assignment to ease the clearing of the
        # changed domains after backtracking
        max_reached_level = 0

        while i < cn.num_variables():
            max_reached_level = i if i > max_reached_level else max_reached_level
            # Select a value for Xi. If there is no value, backtrack
            xi_value = select_value_CBJ(cn, i, A, CS)
            if xi_value is None:
                prev_i = i
                i = max(list(CS[i]))
                # Merge the conflict sets
                CS[i].update(CS[prev_i] - {i})
                # Forget all the changes made below the new i level
                for j in range(i + 1, max_reached_level + 1):
                    CS[j] = set()
                    for value in domain_changes[j]:
                        cn.domains[j].add(value)
                    domain_changes[j].clear()
                max_reached_level = 0
                #Clear the partial assignment below the new i level
                A[i + 1:] = []
            else:
                i = i + 1
        if i == 0:
            return False, num_nodes
        else:
            return True, num_nodes

    num_nodes = 0
    assignment = []
    conflict_set = [set() for _ in range(0, cnet.num_variables())]

    print('Solving ...', st)
    if st == SolverType.GTBT:
        is_solved = GTB(cnet, 0, assignment)
    elif st == SolverType.BT:
        is_solved = BT(cnet, 0, assignment)
    elif st == SolverType.BJ:
        (is_solved, _) = BJ(cnet, 0, assignment)
    elif st == SolverType.CBJ:
        (is_solved, _) = CBJ(cnet, 0, assignment, conflict_set)

    return (assignment, num_nodes)

