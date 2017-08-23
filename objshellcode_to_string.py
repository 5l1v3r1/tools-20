'''
This script takes a binary assembled shellcode and convert the objdump output to
as a ready-to-use hex string

'''
import sys
import re
import subprocess

try:
    dump = sys.argv[1]
except IndexError:
    print "[+] Usage %s <binary_shellcode> " % sys.argv[0]
    sys.exit()

output = subprocess.Popen(['objdump', '-d', dump], stdout=subprocess.PIPE).communicate()[0]
array = output.splitlines()
final = []

for line in array:
  if line:
    # opcodes + mnemonics line?
    if re.match("^[ ]*[0-9a-f]*:.*$",line):
       line =line.split(":")[1].lstrip()
    # split opcodes and mnemonics
    om = line.split("\t")
    # split opcodes
    op = re.findall("[0-9a-f][0-9a-f]",om[0])
    ops = "\""
    for i in op:
     ops += "\\x%s" % i
    ops += "\""
    # print opcodes and mnemonics
    ops = ops.ljust(30)
    ops = ops.strip(' \t\n\r')
    final.append(ops)

# print joined string from list
hex_string = ''.join(final)
hex_string = hex_string.strip('"')
hex_string = hex_string.replace('\""','')
print '"%s"' % (hex_string)
