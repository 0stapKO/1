from compiler import *
from machine import *
code_file = open('code.txt', 'r')
code = code_file.read()
code_file.close()
code_list = text_to_code(code)
handleBlock(code_list)
machine_code_file = open('machine_code.txt', 'w')
for obj in machine_commands:
    machine_code_file.write(str(obj))
    machine_code_file.write('\n')
machine_code_file.close()
machine_code_file = open('machine_code.txt', 'r')
execute(machine_code_file)

