#
# Informed Search Methods
#
# Simple-CSP solver.  Run with '-h' command-line argument to see usage.
# You do not want to change anything in here!
#
#
import argparse
import re
import constraintnetwork
import solvers
from timeit import default_timer as timer


def log_string(text):
    with open('output.txt', 'a') as f:
        f.write(text)
        f.write('\n')


def domain_from_str(text):
    d = set()
    for match in re.finditer(r'\d+', text):
        d.add(int(match.group()))
    return d


def read_domains_of_instances(filename):
    instances_domains = []
    try:
        with open(filename) as f:
            domains = []
            for line in f:
                if line.strip() == '#':
                    instances_domains.append(domains)
                    domains = []
                else:
                    domains.append(domain_from_str(line))
            instances_domains.append(domains)
    except FileNotFoundError:
        print("File", "'"+name+"'", "not found.")
    return instances_domains


def read_binary_constraints(filename):
    constraints = []
    try:
        with open(filename) as f:
            for line in f:
                iterator = re.finditer(r'\d+', line)
                c = []
                for match in iterator:
                    c.append(int(match.group()))
                assert len(c) == 2
                constraints.append((c[0], c[1]))
    except FileNotFoundError:
        print("File", "'" + name + "'", "not found.")
    return constraints


def make_constraint_network(constraints, domains, ac):
    network = constraintnetwork.ConstraintNetwork(len(domains))
    for c in constraints:
        network.add_ne_constraint(c[0], c[1])
    for j in range(len(domains)):
        network.set_domain(j, domains[j])
    if ac:
        solvers.make_arc_consistent(network)
    return network


def solution_str(sol, max_elem):
    n = min(max_elem, len(sol))
    # print(sol, max_elem, n)
    if max_elem > 0:
        s = '[' + ','.join(str(s) for s in sol[0:max_elem//2]) + ",...," +\
                   ','.join(str(s) for s in sol[-(max_elem-max_elem//2):]) + ']'
    else:
        s = '[' + ','.join(str(s) for s in sol) + ']'
    return s


# Main program
#

# Set up and parse command-line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-g", "--gtbt", choices=['on', 'off'], default='on', help="Run the GTBT solver.")
ap.add_argument("-b", "--bt",   choices=['on', 'off'], default='on', help="Run the the BT solver.")
ap.add_argument("-j", "--bj",   choices=['on', 'off'], default='on', help="Run the BJ solver.")
ap.add_argument("-c", "--cbj",  choices=['on', 'off'], default='on', help="Run the CBJ solver.")
ap.add_argument("-i", "--instance", type=int, action='append', help="Run only specified puzzle instance.")
ap.add_argument("-t", "--time",  choices=['on', 'off'], default='on', help="Display runtime (in seconds).")
ap.add_argument("-a", "--arc",  choices=['on', 'off'], default='off', help="Make constraint network arc consistent.")
ap.add_argument("-l", "--len",  type=int, choices=range(0, 1000), default=0, help="Display solution with max n elem")
ap.add_argument("-name", default='sudoku', help="Basename of constraint and instances files (e.g. sudoku).")

args = vars(ap.parse_args())
print(args)
solvers_to_run = []
if args['gtbt'] == 'on':
    solvers_to_run.append(solvers.SolverType.GTBT)
if args['bt'] == 'on':
    solvers_to_run.append(solvers.SolverType.BT)
if args['bj'] == 'on':
    solvers_to_run.append(solvers.SolverType.BJ)
if args['cbj'] == 'on':
    solvers_to_run.append(solvers.SolverType.CBJ)
if args['instance']:
    specific_instances_to_run = args['instance']
else:
    specific_instances_to_run = []
do_display_time = (args['time'] == 'on')
do_arc_consistent = (args['arc'] == 'on')
len_sol = args['len']
name = args['name']
input_cnstr_file = name + "_cst.txt"
input_domain_file = name + "_dom.txt"

# Read in CSP problem specification.
problem_constraints = read_binary_constraints(input_cnstr_file)
print('Read', len(problem_constraints), 'constraints.')
problem_instances = read_domains_of_instances(input_domain_file)
print('Read', len(problem_instances), 'problem instances.')

# Run the specified solvers on the given problem instances and log results (output.txt).
for solver_type in solvers_to_run:
    for i, instance in enumerate(problem_instances):
        if not specific_instances_to_run or i in specific_instances_to_run:
            csp = make_constraint_network(problem_constraints, instance, do_arc_consistent)
            start = timer()
            (solution, nodes) = solvers.solve(solver_type, csp)
            end = timer()
            if do_display_time:
                output = "{:3d} {:15s} {:10d} {:9.4f} {:s}".format(i, str(solver_type), nodes, end-start,
                                                                   solution_str(solution, len_sol))
            else:
                output = "{:3d} {:15s} {:10d} {:s}".format(i, str(solver_type), nodes, solution_str(solution, len_sol))
            print(output)
            log_string(output)
