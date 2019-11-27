import Sptokens as Tokens


def is_variable_or_num(token):
    if is_special_symbol(token)\
    or token in Tokens.incrementDecrement \
    or token in Tokens.comparison \
    or token in Tokens.dot \
    or token in Tokens.assignment:
        return False
    else:
        is_adequate_variable(token)

    return True


def is_special_symbol(token):
    return True if token in "=-+/&()[]<>:;*" else False


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
        if variable[0] != "!" and variable[0] != "*" and variable[0] not in Tokens.alphabet:
            if not is_numeric(variable[1:]):
                print("Error occurred!\n",
                      "Variable or reference {} begins with inappropriate symbol.".format(variable))
                exit()
    return True


def brackets_check(tokens):

    openCounter   = 0
    closedCounter = 0
    i = 0
    while i < len(tokens):

        if closedCounter == 1 and openCounter == 0:
            print("Error occurred!\n"
                  "Invalid statement: ", " ".join(tokens[:i]))
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
              "Missing end of statement:\n", " ".join(tokens[j:]))
        exit()
    elif closedCounter > openCounter:
        print("Error occurred!\n"
              "Missing beginning of statement:\n", " ".join(tokens[:j + 1]))
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


if __name__ == "__main__":

    codeToProcess = "b = abra.cadabra +(c/d) * 22 * a;"
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

    print("No error occurred!")
