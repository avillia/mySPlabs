import Sptokens as Tokens


def order_of_operation(token):
    for operations in Tokens.operationOrder:
        if token in operations:
            return Tokens.operationOrder.index(operations)
    return None


def maxOperand(operands:list):
    order = 0
    for operand in operands:
        if not operand:
            pass
        elif operand > order:
            order = operand
    return order


def is_variable_or_num(token):
    if is_special_symbol(token)\
    or token in Tokens.incrementDecrement \
    or token in Tokens.comparison \
    or token in Tokens.assignment:
        return False
    else:
        is_adequate_variable(token)

    return True


def is_special_symbol(token):
    for symbol in "=-+/&()[]<>:;*":
        if symbol == token:
            return True
    return False


def is_numeric(token):
    for char in token:
        if char not in Tokens.nums and char != ".":
            return False
    return True


def is_float(token):
    return False if "." not in token else True


def preprocessing(rawInput):
    tokens = []

    i = 0
    while i < len(rawInput):
        if rawInput[i] == " ":
            i += 1
        elif rawInput[i] in Tokens.alphabet:
            j = i + 1
            while j < len(rawInput):
                if  rawInput[j] not in Tokens.alphabet \
                and rawInput[j] not in Tokens.nums     \
                and rawInput[j] != ".":
                    break
                j += 1

            tokens.append(rawInput[i:j])
            i = j
        elif rawInput[i] in Tokens.nums:
            j = i + 1
            while j < len(rawInput):
                if  rawInput[j] not in Tokens.nums \
                and rawInput[j] != ".":
                    break
                j += 1
            tokens.append(rawInput[i:j])
            i = j
        elif rawInput[i:i + 2] in Tokens.assignment \
          or rawInput[i:i + 2] in Tokens.comparison \
          or rawInput[i:i + 2] in Tokens.incrementDecrement:
            tokens.append(rawInput[i:i + 2])
            i += 2
        else:
            tokens.append(rawInput[i])
            i += 1

    return tokens


def is_adequate_variable(variable):

    for char in variable:
        if is_special_symbol(char):
            print("Error occurred: ", variable)
            exit()

    subVariableSet = variable.split(".")
    if len(subVariableSet) != 1:
        for subVariable in subVariableSet:
            is_adequate_variable(subVariable)
    else:
        if variable[0] not in Tokens.alphabet:
            if not is_numeric(variable[1:]):
                print("Error occurred: ", variable)
                exit()
    return True


def brackets_check(tokens):

    openCounter   = 0
    closedCounter = 0
    i = 0
    while i < len(tokens):

        if closedCounter == 1 and openCounter == 0:
            print("Error occurred!\n"
                  "Invalid statement: ", " ".join(tokens[i - 1:]))
            exit()

        if tokens[i] in Tokens.bracketsClose:
            closedCounter += 1
            j = i
        elif tokens[i] in Tokens.bracketsOpen:
            openCounter += 1
            j = i
        i += 1

    if closedCounter < openCounter:
        print("Error occurred!\n"
              "Missing end of statement: ", " ".join(tokens[j:]))
        exit()
    elif closedCounter > openCounter:
        print("Error occurred!\n"
              "Missing beginning of statement:\n", " ".join(tokens[:j+1]))
        exit()


def check_indexing(tokens):
    indexes = []
    i = 0
    while i < len(tokens):
        if tokens[i] in nums:
            if tokens[i - 2] in variables or tokens[i - 4: i - 1] in indexes:
                if tokens[i - 1] == "[" and tokens[i + 1] == "]":
                    if is_float(tokens[i]):
                        print("Error occurred!\n"
                              "Invalid indexing:\n", " ".join(tokens[i - 1: i + 2]))
                        exit()
                indexes.append(tokens[i - 1: i + 2])
        i += 1


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
            try:
                if stack[-1] == "(":
                    stack.append(token)
                else:
                    while order_of_operation(stack[-1]) >= order_of_operation(token):
                        if stack[-1] != "(":
                            output.append(stack.pop())
                        else:
                            stack.pop()
                    stack.append(token)
            except IndexError:
                stack.append(token)

    while stack:
        output.append(stack.pop())

    return output


def bifurcation(rpn: list):
    tree = []

    operand = rpn.pop()
    restOperands = [order_of_operation(i) for i in rpn]

    if len(rpn) > 3:
        if order_of_operation(operand) < maxOperand(restOperands):
            tree += [rpn[0], operand, bifurcation(rpn[1:])]
        else:
            tree += [rpn[-1], operand, bifurcation(rpn[:-1])]
    else:
        tree += [rpn[0], operand, rpn[-1]]

    return tree


def print_tree(tree, indent=0):
    if len(tree[-1]) > 1:
        print(f"{tree[1].rjust(len(tree[0])+2)}\n{tree[0].rjust(indent)} | {print_tree(tree[-1], len(tree[0])+3)}")
    else:
        print(f"{tree[1].rjust(len(tree[0])+2)}\n{tree[0].rjust(indent)} | {tree[2]}")


if __name__ == "__main__":
    codeToProcess = "b = gay +(c/d)* 22 * a;"

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
    check_indexing(inputTokens)

    RPN = to_RPN(inputTokens, variables, nums)
    print(RPN)

    myTree = bifurcation(RPN)
    print(myTree)
    print_tree(myTree)

    print("No error occurred!")
