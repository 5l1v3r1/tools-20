'''
This script takes a binary assembled shellcode and convert the objdump output and XOR encode it with 0xAA
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
new_array = []
final = []

for line in array:
  if line:
    # opcodes + mnemonics line?
    if re.match("^[ ]*[0-9a-f]*:.*$",line):
       line =line.split(":")[1].lstrip()
       new_array.append(line)
for line in new_array:
    om = line.split("\t")
    # split opcodes
    op = re.findall("[0-9a-f][0-9a-f]",om[0])
    ops = "\""
    for i in op:
     ops += "%s" % i

    # print opcodes and mnemonics
    ops = ops.ljust(30)
    ops = ops.strip(' \t\n\r')
    final.append(ops)


# print joined string from list
shellcode = ''.join(final)
shellcode = shellcode.replace('"','')
shellcode = shellcode.replace('\""','')
shellcode = bytearray.fromhex(shellcode)

print '[*] ORIGINAL SHELLCODE:'

printable_shellcode = ""

for x in bytearray(shellcode) :
	# XOR Encoding
	printable_shellcode += '\\x%02x'  % x
print printable_shellcode + '\n'


encoded = ""
encoded2 = ""



for x in bytearray(shellcode) :
	# XOR Encoding
	y = x^0xAA
	encoded += '\\x'
	encoded += '%02x' % y

	encoded2 += '0x'
	encoded2 += '%02x,' %y

print '\n[*] ENCODED SHELLCODE - format A:'
print encoded
print '\n[*] ENCODED SHELLCODE - format B:'
print encoded2 

print '\nOriginal Shellcode Len: %d' % len(bytearray(shellcode))
