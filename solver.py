from z3 import *
from system_parser import Parser
from itertools import chain, combinations

p = Parser()
p.parse()
d = p.dimension
max = p.max

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))

def new_letter_matrix(var_name):
      return [ [Int(f"{var_name}_{i}_{j}") for j in range(d) ] 
              for i in range(d) ]

def mul(m1, m2):
      result = []
      for i in range(d):
            result.append([])
            for j in range(d):
                  result[i].append(m1[i][0] * m2[0][j])
                  for k in range(1,d):
                        result[i][j] += m1[i][k] * m2[k][j]
      return result

def sub(m1, m2):
      return [[m1[i][j] - m2[i][j] for j in range (d)]
          for i in range(d)]

def greater_than_zero(solver, m):
      bools = []
      for i in range(d):
            for j in range(d):
                  solver.add(m[i][j] >= 0)
                  bools.append(m[i][j] > 0)
      solver.add(Or(bools))
      
def greater_than_or_equal_to_zero(solver, m):
      for i in range(d):
            for j in range(d):
                  solver.add(m[i][j] >= 0)

def less_than_max(solver, m):
      for i in range(d):
            for j in range(d):
                  solver.add(m[i][j] <= max)

def new_term_matrix(term, matrices):
    result = matrices[term[0]]
    for i in range(1, len(term)): 
        result = mul(result, matrices[term[i]])
    return result

def print_model(key, dictionary):
    for key in dictionary: 
        matrix = dictionary[key]
        result = [ [ m.evaluate(matrix[i][j]) for j in range(d) ] for i in range(d) ]
        
        print(f'{key}:')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in result]))
        
def get_formula_E_I(matrix, I):
    f = []
    for i in I: 
        f.append(matrix[i][i] > 0)
    return And(f)

def get_formula_P_I(matrix, I):
    f = []
    for i in I:
        for j in I:
            f.append(matrix[i][j] > 0)
    return Or(f)
    
def enforce_I(letter_to_matrix, rule_to_matrix):
    I = range(d)
    power = list(powerset(I))
    # subset = [0, (d-1)]
    # power = [subset]
    final_f = []
    for subset in power: 
        subset_f = []
            
        for letter in letter_to_matrix:
            matrix = letter_to_matrix[letter]
            subset_f.append(get_formula_E_I(matrix, subset))
            
        for rule in rule_to_matrix:
            matrix = rule_to_matrix[rule]
            subset_f.append(get_formula_P_I(matrix, subset))
            
        final_f.append(And(subset_f))
        
    return Or(final_f)

 
s = Solver()

# create a matrix for each letter + basic constraints
letter_to_matrix = dict()
for letter in p.alphabet:
    letter_to_matrix[letter] = new_letter_matrix(letter)
    greater_than_or_equal_to_zero(s, letter_to_matrix[letter] )
    less_than_max(s, letter_to_matrix[letter] )
    
# create a matrix for each term (no constraints needed)
term_to_matrix = dict()
for term in p.terms: 
    term_to_matrix[term] = new_term_matrix(term, letter_to_matrix)
    # print(term_to_matrix[term])


# create a matrix for each rule + basic constraints
rule_to_matrix = dict()
for rule in p.rules: 
    rule_to_matrix[rule] = sub(term_to_matrix[rule[0]], term_to_matrix[rule[1]])
    greater_than_or_equal_to_zero(s, rule_to_matrix[rule])
    
# enforce that I is the same for both the alphabet and the rules
s.add(enforce_I(letter_to_matrix, rule_to_matrix))

# run solver 
satisfiable = s.check()
if satisfiable == sat:
      print("A matrix interpretation which proves termination was found:")
      m = s.model()
      print_model(letter, letter_to_matrix)
      print_model(term, term_to_matrix)
      print_model(rule, rule_to_matrix)
else:
      print("No matrix interpretation which proves termination was found, given the constraints. The system may or may not be terminating.")