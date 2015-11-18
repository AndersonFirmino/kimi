import unittest
from kimi import *

class TestTokenize(unittest.TestCase):

    def test_numbers(self):
        # Valid number literals
        self.assertEqual(tokenize("3"), [('literal', 3)])
        self.assertEqual(tokenize("+3"), [('literal', 3)])
        self.assertEqual(tokenize("-4"), [('literal', -4)])
        # Not valid (considered symbols)
        self.assertEqual(tokenize("2.5"), [('symbol', '2.5')])
        self.assertEqual(tokenize("-2-4"), [('symbol', '-2-4')])

    def test_strings(self):
        # Valid string literals
        self.assertEqual(tokenize('"some string"'), [('literal', 'some string')])
        self.assertEqual(tokenize('"some (string)"'), [('literal', 'some (string)')])
        self.assertEqual(tokenize('''"some 'string'"'''), [('literal', "some 'string'")])
        # Not valid
        self.assertEqual(tokenize('"some \"string\""'), [('literal', 'some '), ('symbol', 'string'), ('literal', '')])

    def test_symbols(self):
        # Valid symbols
        self.assertEqual(tokenize("x"), [('symbol', 'x')])
        self.assertEqual(tokenize("123abc123"), [('symbol', '123abc123')])
        self.assertEqual(tokenize("--thing--"), [('symbol', '--thing--')])
        # Not valid
        self.assertEqual(tokenize("x y"), [('symbol', 'x'), ('symbol', 'y')])
        self.assertEqual(tokenize("z(x)"), [('symbol', 'z'), ('opening', None), ('symbol', 'x'), ('closing', None)])


    def test_apply(self):
        self.assertEqual(tokenize("(- 1 2)"), [('opening', None), ('symbol', '-'), ('literal', 1), ('literal', 2), ('closing', None)])
        self.assertEqual(tokenize("(define square (lambda x (* x x)))"),
            [('opening', None), ('symbol', 'define'), ('symbol', 'square'),
             ('opening', None), ('symbol', 'lambda'), ('symbol', 'x'),
             ('opening', None), ('symbol', '*'), ('symbol', 'x'), ('symbol', 'x'),
             ('closing', None), ('closing', None), ('closing', None)])

class TestParse(unittest.TestCase):

    def test_parse(self):
        self.assertEqual(parse(tokenize("(+ 1 2)")),
             {'type': 'apply',
              'operator': {'type': 'symbol', 'value': '+'},
              'arguments': ({'type': 'literal', 'value': 1},
                            {'type': 'literal', 'value': 2})})
        self.assertEqual(parse(tokenize("(define square (lambda x (* x x)))")),
             {'type': 'apply',
              'operator': {'type': 'symbol', 'value': 'define'},
              'arguments': ({'type': 'symbol', 'value': 'square'},
                            {'type': 'apply',
                             'operator': {'type': 'symbol', 'value': 'lambda'},
                             'arguments': ({'type': 'symbol', 'value': 'x'},
                                           {'type': 'apply',
                                            'operator': {'type': 'symbol', 'value': '*'},
                                            'arguments': ({'type': 'symbol', 'value': 'x'},
                                                          {'type': 'symbol', 'value': 'x'})})})})

class TestExecute(unittest.TestCase):

    def test_atoms(self):
        self.assertEqual(execute("-10"), -10)
        self.assertEqual(execute("true"), True)
        self.assertEqual(execute('"string"'), "string")

    def test_arithmetic(self):
        # Addition
        self.assertEqual(execute("(+ 1 2)"), 3)
        self.assertEqual(execute("(+ -1 2)"), 1)
        # Subtraction
        self.assertEqual(execute("(- 2 1)"), 1)
        self.assertEqual(execute("(- 1 -2)"), 3)
        # Multiplication
        self.assertEqual(execute("(* 2 4)"), 8)
        self.assertEqual(execute("(* 3 -2)"), -6)
        # Floor division
        self.assertEqual(execute("(/ 6 2)"), 3)
        self.assertEqual(execute("(/ 7 2)"), 3)
        self.assertEqual(execute("(/ 1 2)"), 0)
        self.assertEqual(execute("(/ 6 -2)"), -3)
        self.assertEqual(execute("(/ -3 -2)"), 1)
        # Modulo
        self.assertEqual(execute("(% 7 2)"), 1)
        self.assertEqual(execute("(% 6 -4)"), -2)
        self.assertEqual(execute("(% 2 3)"), 2)

    def test_logic(self):
        # And
        self.assertEqual(execute("(& true true)"), True)
        self.assertEqual(execute("(& true false)"), False)
        self.assertEqual(execute("(& false true)"), False)
        self.assertEqual(execute("(& false false)"), False)
        # Or
        self.assertEqual(execute("(| true true)"), True)
        self.assertEqual(execute("(| true false)"), True)
        self.assertEqual(execute("(| false true)"), True)
        self.assertEqual(execute("(| false false)"), False)
        # Not
        self.assertEqual(execute("(! true)"), False)
        self.assertEqual(execute("(! false)"), True)




if __name__ == '__main__':
    unittest.main()
