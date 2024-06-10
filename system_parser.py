import argparse
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring

class Parser():
    def __init__(self):
        self.parser = argparse.ArgumentParser (
            prog='python3 ./solver.py', 
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description='Parses an XML file into an alphabet, terms, and rules, and provides a solution to the termination problem.',
            epilog='Example usage:\npython3 ./solver.py example.xml 3 1\n' +
                   '- The parsed file is example.xml\n' +
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

        tree = ET.parse(filename)
        root = tree.getroot()

        # Extract rules
        for rule in root.findall('.//rule'):
            lhs_string = ''
            rhs_string = ''

            lhs = rule.find('.//lhs')
            for letter in lhs.findall('.//name'):
                lhs_string += letter.text

            rhs = rule.find('.//rhs')
            for letter in rhs.findall('.//name'):
                rhs_string += letter.text

            self.rules.add((lhs_string, rhs_string))
            self.terms.add(lhs_string)
            self.terms.add(rhs_string)

        for funcsym in root.findall('.//signature/funcsym'):
            letter = funcsym.find('.//name').text
            self.alphabet.add(letter)

p = Parser()
p.parse()