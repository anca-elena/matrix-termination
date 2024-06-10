import argparse

class Parser():
    def __init__(self):
        self.parser = argparse.ArgumentParser (
            prog='python3 ./solver.py', 
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description='Parses a .txt file into an alphabet, terms, and rules, and provides a solution to the termination problem.',
            epilog='Example usage:\npython3 ./solver.py example.txt 3 1\n' +
                   '- The parsed file is example.txt\n' +
                   '- The dimension of all matrices is 3x3\n' + 
                   '- The maximum value of each entry in the interpretation of the alphabet is 1'
        )
        self.parser.add_argument('filename')
        self.parser.add_argument('dimension', type=int)
        self.parser.add_argument('max', type=int)

        self.alphabet = set()
        self.terms = set()
        self.rules = set()

    def parse(self):
        args = self.parser.parse_args()
        filename = args.filename
        self.dimension = args.dimension
        self.max = args.max

        file = open(filename)
        lines = file.readlines()

        for line in lines: 
            lhs, rhs = line.split("->")
            rhs = rhs.replace('\n', '')

            self.alphabet.update(''.join(set(lhs)))
            self.alphabet.update(''.join(set(rhs)))

            self.terms.add(lhs)
            self.terms.add(rhs)

            self.rules.add((lhs, rhs))

