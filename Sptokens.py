alphabet = "".join([chr(i) for i in range (65, 91)] + [chr(i) for i in range (97, 123)])

nums = "1234567890"


serviceWords = ['if', 'then', 'else',
                'for', 'to', 'do',
                'begin', 'end']

allTokens = {'=': 'assign', ':': 'colon', '?': 'question_mark',
          '*': 'mul', '[': 'left_square_bracket', ']': 'right_square_bracket',
          ';': 'semi_colon', '/': 'divide', '%': 'module',
          '-': 'subtract', '+': 'add', '+=': 'sum_assign',
          '-=': 'sub_assign', '&': 'logic_and', '|': 'logic_or',
          '^': 'logic_exclusive_or', '++': 'inc', '--': 'dec'}


assignment = ['+=', '-=', '=']

bracketsOpen = ['(', '[']
bracketsClose = [')', ']']
parenBrackets = ['(', ')']

incrementDecrement = ['++', '--']

simpleOperations = ['&', '|', '^', '+', '-', '*', '/', ]

lowOperations = ['&', '|', '^', ]
middleOperations = ['+', '-', ]
highOperations = ['*', '/', ]

comparison = [">", "<", "==", "=<", "=>"]
nextStep = [";", ":"]

infixOperation = ["!"]
invariableDelimeters = [".", "_"]

operationOrder = [assignment,lowOperations, middleOperations, highOperations, incrementDecrement, parenBrackets]

possibleOperations = assignment + lowOperations + middleOperations + highOperations + incrementDecrement + parenBrackets

