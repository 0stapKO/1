def execute(f):
    def resop(op, mem):
        if '#' in op:
            name, index = op.split('#')
            if index.isdigit():
                index = int(index)
            else:
                index = int(mem[index])
            if name not in mem:
                mem[name] = []
            while len(mem[name]) <= index:
                mem[name].append(0)
            return mem[name][index]
        elif op.replace(".", "", 1).isdigit():
            return float(op)
        else:
            return mem[op]
    l = []
    for i in f:
         l.append(i)
    ind = 0
    mem = {}
    while ind < len(l):
        command = l[ind].split()
        if command[0] == 'READ':
            value = float(input())
            if '#' in command[1]:
                name, index = command[1].split('#')
                index = int(index)
                if name not in mem:
                    mem[name] = []
                while len(mem[name]) <= index:
                    mem[name].append(0)
                mem[name][index] = value
            else:
                mem[command[1]] = value
        elif command[0] == 'WRITE':
            print(resop(command[1], mem))
        elif command[0] == 'GOTOIF':
            if resop(command[1], mem) > 0:
                ind = int(command[2])
        elif command[0] == 'GOTOIFNOT':
            if resop(command[1], mem) <= 0:
                ind = int(command[2])
        elif command[0] == 'GOTO':
            ind = int(command[1])
        elif command[0] == 'ADD':
            value = resop(command[1], mem) + resop(command[2], mem)
            if '#' in command[2]:
                name, index = command[3].split('#')
                index = int(index)
                if name not in mem:
                    mem[name] = []
                while len(mem[name]) <= index:
                    mem[name].append(0)
                mem[name][index] = value
            else:
                command[3] = value
        elif command[0] == 'SUB':
            mem[command[3]] = resop(command[1], mem) - resop(command[2], mem)
        elif command[0] == 'MUL':
            mem[command[3]] = resop(command[1], mem) * resop(command[2], mem)

        elif command[0] == 'DIV':
            divisor = resop(command[2], mem)
            if divisor == 0:
                raise ZeroDivisionError("Division by zero")
            mem[command[3]] = resop(command[1], mem) / divisor


        elif command[0] == 'COPY':
            value = resop(command[1], mem)
            if '#' in command[2]:
                name, index = command[2].split('#')
                index = int(index)
                if name not in mem:
                    mem[name] = []
                while len(mem[name]) <= index:
                    mem[name].append(0)
                mem[name][index] = value
            else:
                mem[command[2]] = value

        ind += 1

def checkIfNumber(command, mem):
    if command[1].replace(".", "", 1).isdigit():
        mem[command[1]] = float(command[1])
    if command[2].replace(".", "", 1).isdigit():
        mem[command[2]] = float(command[2])

