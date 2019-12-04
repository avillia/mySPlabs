import Sptokens as Tokens
from newLabSP4 import *



def split_input(tokens):
    variables = []
    nums = []
    service = []

    for instance in tokens:
        if is_variable_or_num(instance):
            if is_numeric(instance):
                nums.append(instance)
            else:
                if instance in Tokens.serviceWords:
                    service.append(instance)
                else:
                    variables.append(instance)

    return variables, nums, service


def order_of_operation(token):
    for operations in Tokens.operationOrder:
        if token in operations:
            return Tokens.operationOrder.index(operations)
    return None


def max_operand(operands: list):
    order = 0
    for operand in operands:
        if not operand:
            pass
        elif operand > order:
            order = operand
    return order


def to_RPN(tokens, variables, nums):
    stack = []
    output = []

    for token in tokens:
        if token in variables or token in nums or token in Tokens.incrementDecrement:
            output.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()
        elif token in Tokens.possibleOperations:
            if stack:
                while order_of_operation(stack[-1]) >= order_of_operation(token) and stack[-1] != "(":
                    output.append(stack.pop())
                stack.append(token)
            else:
                stack.append(token)

    while stack:
        output.append(stack.pop())

    return output


def bifurcation(rpn: list):
    tree = rpn

    i = 0
    while i < len(tree)-1:
        if rpn[i] in Tokens.possibleOperations:
            tree[i] = tree[i-2:i+1]
            tree.pop(i-1)
            tree.pop(i-2)
            i -= 2
        i += 1

    return tree


def split_per_semicolon(tokens):
    allLines = []
    i = 0
    j = 0
    while i < len(tokens):
        if tokens[i] == ";":
            allLines.append(tokens[j:i])
            j = i+1
        i += 1
    return allLines


def Grammar(lines, service):
    for line in lines:
        i = 0
        serviceWordsCounter = [0 for i in Tokens.serviceWords]

        while i < len(line):
            if line[i] in service:
                serviceWordsCounter[Tokens.serviceWords.index(line[i])] += 1

                if line[i] == "if":
                    if line[i+1] == "(":
                        pass


            i += 1


if __name__ == "__main__":

    codeToProcess = "if (a>b) then begin print(a) else b = 3 end;"
    print("Your input: ", codeToProcess, "\n")

    inputTokens = preprocessing(codeToProcess)
    print("Input by tokens:\n", inputTokens, "\n")

    inputVariables, inputNums, inputServiceWords = split_input(inputTokens)

    no_missing_operands(inputTokens, inputVariables, inputNums)

    brackets_check(inputTokens)
    check_indexing(inputTokens, inputVariables, inputNums)

    inputGrammar = split_per_semicolon(inputTokens)
    for i in inputGrammar:
        print(i)

    Grammar(inputGrammar, inputServiceWords)

    # RPN = to_RPN(inputTokens, inputVariables, inputNums)
    # print("Reversed Polish Notation for inputted expression:\n", RPN, "\n")


    # myTree = bifurcation(RPN)
    # print("Nested array representing sequence of operations:\n", myTree, "\n")

    # print_tree(myTree)
