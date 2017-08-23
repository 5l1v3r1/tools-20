'''
This script takes a binary assembled shellcode, onvert the objdump output and XOR encode it 
with the given hex byte value, after veryfing the shellcode contains no similar byte.
'''
import sys
import re
import subprocess

try:
    dump = sys.argv[1]
    encoder = sys.argv[2]
    encoder_int = int(encoder, 16)
except IndexError:
    print "[+] Usage %s <binary_assembled_shellcode> + <encoder in hex format> - Example: 0xAA\n   " % sys.argv[0]
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

#exit if byte-encoder is aready present in the shellcode
if encoder_int in shellcode:
  print "[-] found same encoder %s in the shellcode - cannot proceed" % (encoder)
  sys.exit()
else:
  printable_shellcode = ""
  encoded = ""
  encoded2 = ""

  print '\n[*] ORIGINAL SHELLCODE:'

  for x in bytearray(shellcode) :
  	printable_shellcode += '\\x%02x'  % x
  print printable_shellcode 

  for x in bytearray(shellcode) :
    # XOR Encoding
    y = x^encoder_int
    encoded += '\\x'
    encoded += '%02x' % y

    encoded2 += '0x'
    encoded2 += '%02x,' %y

  print '\n[*] ENCODED SHELLCODE - hexformat A:'
  print encoded
  print '\n[*] ENCODED SHELLCODE - hexformat B:'
  print encoded2 
  print '\nOriginal Shellcode Len: %d' % len(bytearray(shellcode))
