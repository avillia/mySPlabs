import Sptokens as Tokens
from newLabSP4 import *


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
    tree = []

    operand = rpn.pop()
    restOperands = [order_of_operation(i) for i in rpn]

    if len(rpn) > 3:
        if order_of_operation(operand) < max_operand(restOperands):
            tree += [rpn[0], operand, bifurcation(rpn[1:])]
        else:
            tree += [rpn[-1], operand, bifurcation(rpn[:-1])]
    else:
        tree += [rpn[0], operand, rpn[-1]]

    return tree


def print_tree(tree:list):
    indent = 0
    print(' '*(len(tree[0])+1), end="")
    while type(tree[2]) == list:
        operation = tree[1]
        operand = tree[0]
        tree = tree.pop()
        print(f"{operation.rjust(len(operand))}\n{operand.rjust(indent+1)} | ", end="")
        indent += len(tree[0])+1
    print(f"{tree[1].rjust(len(tree[0]))}\n{tree[0].rjust(indent+1)} | {tree[2]}",)


if __name__ == "__main__":
    codeToProcess = "b = (2*a +c/d) * 2 * a;"

    print("Your input: ", codeToProcess, "\n")

    inputTokens = preprocessing(codeToProcess)
    print("Input by tokens:\n", inputTokens, "\n")

    variables = []
    nums = []
    for instance in inputTokens:
        if is_variable_or_num(instance):
            if is_numeric(instance):
                nums.append(instance)
            else:
                variables.append(instance)

    brackets_check(inputTokens)
    check_indexing(inputTokens, nums, variables)

    RPN = to_RPN(inputTokens, variables, nums)
    print("Reversed Polish Notation for inputted expression:\n", RPN, "\n")

    myTree = bifurcation(RPN)
    print("Nested array representing sequence of operations:\n", myTree, "\n")

    print_tree(myTree)
