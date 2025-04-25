from classes import *


def generateCommand():
    global temp_count
    op = OP.pop()
    rhs = ARG.pop()
    lhs = ARG.pop()
    name = None
    if str(op) == '+':
        name = 'ADD'
    elif str(op) == '-':
        name = 'SUB'
    elif str(op) == '*':
        name = 'MUL'
    elif str(op) == '/':
        name = 'DIV'

    res = 't' + str(temp_count)
    machine_commands.append(Command(name, lhs, rhs, res))
    ARG.push(res)
    temp_count += 1


def minus_temp():
    global temp_count
    temp_count -= 1


ARG = Stack()
OP = Stack()
temp_count = 0
machine_commands = []