class Token:
    def __init__(self, s):
        self.lexeme = s
        if s in '*/':
            self.priority = 2
        elif s in '+-':
            self.priority = 1
        else:
            self.priority = 0

    def __str__(self):
        return self.lexeme

    def is_command(self):
        return self.lexeme in ['read', 'write', '=']

    def is_operator(self):
        return self.lexeme in ['if', 'ifnot', 'while', 'whilenot']


class Stack:
    def __init__(self):
        self.list = []

    def pop(self):
        t = self.list[-1]
        self.list.pop()
        return t

    def pop_front(self):
        t = self.list[0]
        self.list.pop(0)
        return t

    def top(self):
        if len(self.list) == 0:
            return None
        return self.list[-1]

    def push(self, x):
        self.list.append(x)

    def is_empty(self):
        return len(self.list) == 0

    def empty(self):
        self.list = []

    def len(self):
        return len(self.list)

    def __str__(self):
        t = ''
        for i in self.list:
            t += str(i) + ', '
        return t


class Command:
    def __init__(self, name, rhs, lhs='', res=''):
        self.name = name
        self.rhs = rhs
        self.lhs = lhs
        self.res = res

    def __str__(self):
        return self.name + ' ' + self.rhs + ' ' + self.lhs + ' ' + self.res