from additional import *

def handleOperatorBlock(tokens, i):
    before_expr = len(machine_commands)
    expr = []
    j = i + 2
    if str(tokens[i+1]) != '[':
        raise SyntaxError('Missed "["')
    while str(tokens[j]) != ']':
        expr.append(tokens[j])
        j += 1
        if j == len(tokens) - 1 or str(tokens[j]) == '[':
            raise SyntaxError('Unmatched "["')
    expr_l = len(expr)
    handle_result = handleExpression(expr)

    block = []
    open_count, close_count = 1, 0
    j += 2
    if str(tokens[j-1]) != '{':
        raise SyntaxError('Missed "{"')
    while open_count != close_count:
        if j == len(tokens) - 1:
            raise SyntaxError('Missed "}"')
        block.append(tokens[j])
        if str(tokens[j + 1]) == '{':
            open_count += 1
        if str(tokens[j + 1]) == '}':
            close_count += 1
        j += 1

    ind = len(machine_commands)
    if str(tokens[i]) == 'while' or str(tokens[i]) == 'if':
        machine_commands.append(Command('GOTOIFNOT', str(handle_result)))
    elif str(tokens[i]) == 'whilenot' or str(tokens[i]) == 'ifnot':
        machine_commands.append(Command('GOTOIF', str(handle_result)))

    if 'while' in str(tokens[i]):
        gotoif_ind = str(handleBlock(block) + 1)
        machine_commands.append('GOTO ' + str(before_expr))
    else:
        gotoif_ind = str(handleBlock(block))
    machine_commands[ind].lhs = gotoif_ind
    i += expr_l + len(block) + 4
    return i

def handleCommand(tokens, i):
    if str(tokens[i]) == 'read':
        if str(tokens[i + 1]) != '>':
            raise SyntaxError('Missed ">"')
        if str(tokens[i + 3]) != ';':
            raise SyntaxError('Missed ";"')
        machine_commands.append('READ ' + str(tokens[i + 2]))
        i += 3
    elif str(tokens[i]) == 'write':
        if str(tokens[i+1]) != '>':
            raise SyntaxError('Missed ">"')
        if str(tokens[i+3]) != ';':
            raise SyntaxError('Missed ";"')
        machine_commands.append('WRITE ' + str(tokens[i + 2]))
        i += 3
    else:
        j = i + 1
        expression = []
        while str(tokens[j]) != ';':
            expression.append(tokens[j])
            j += 1
        expr_l = len(expression)
        if len(expression) == 1:
            machine_commands.append('COPY ' + str(expression[0]) + ' ' + str(tokens[i - 1]))
        else:
            handleExpression(expression)
            machine_commands[-1].res = str(tokens[i - 1])
            minus_temp()
        i += 1 + expr_l
        if str(tokens[i]) != ';':
            raise SyntaxError('Missed ";"')
    return i

def handleBlock(tokens):
    i = 0
    while i < len(tokens):
        while tokens[i].is_command():
            i = handleCommand(tokens, i)
        while tokens[i].is_operator():
            i = handleOperatorBlock(tokens, i)
        i+=1
    return len(machine_commands)

def handleExpression(expression):
    ARG.empty()
    OP.empty()
    global temp_count
    t = Stack()
    t.list = expression
    expression = t
    if len(expression.list) == 1:
        return expression.pop()
    while not expression.is_empty():
        token = str(expression.pop_front())
        if token.replace('.', '').replace('#', '').isalnum() :
            ARG.push(token)
        elif token in '+-*/':
            while OP.top() is not None and Token(OP.top()).priority >= Token(token).priority:
                generateCommand()
            OP.push(token)
        elif token == '(':
            OP.push(token)
        elif token == ')':
            while OP.top() != '(':
                generateCommand()
            OP.pop()
    while not OP.is_empty():
        if str(OP.top()) in '()':
            raise SyntaxError(f'Unmatched "{OP.top()}"')
        generateCommand()
    return machine_commands[-1].res

def text_to_code(text):
    text = text.replace(' ', '')
    text = text.replace('\n', '')
    t = ''
    code = []
    for obj in text:
        if (t == 'read' or t == 'write') and obj != '>':
            raise SyntaxError(f'Missed ">" after "{t}"')
        if obj in '>;=*/+-()[]{}':
            if t != '':
                code.append(Token(t))
                t = ''
            code.append(Token(obj))
        else:
            t += obj
    return code