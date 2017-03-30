"""Lets solve this one too."""
import requests
import binascii
import BeautifulSoup as bs

"""
0x00	move
0x01	logical or
0x02	logical xor
0x03	logical and
0x04	logical not
0x05	addition
0x06	subtraction
0x07	multiplication
0x08	logical shift left
0x09	logical shift right
0x0a	increment
0x0b	decrement
0x0c	push on stack
0x0d	pop from stack
0x0e	compare
0x0f	jump to nth opcode when not zero*
0x10	jump to nth opcode when zero*
"""

operations = {'00': 'move', '01': '^or', '02': '^xor', '03': '^and',
              '04': '^not', '05': 'add', '06': 'sub', '07': 'mul',
              '08': '^lsh', '09': '^rsh', '0a': 'inc', '0b': 'dec',
              '0c': 'push', '0d': 'pop', '0e': 'compare', '0f': 'jump',
              '10': 'jump*'}

host = '80.233.134.207'
url = 'http://'+host+'/0x00000ACE.html'
with open('.key', 'r') as keyfile:
    key = keyfile.read()
header = {'X-0x0ACE-Key': key.strip()}

response = requests.get(url, headers=header)
html = response.content
soup = bs.BeautifulSoup(html)
link = soup.find('a')

challenge = link['href']
instructions = requests.get('http://'+host+challenge, headers=header)
binary_data = instructions.content

with open('binary_assembley.temp.bin', 'wb+') as file:
    file.write(binary_data)
hexstring = binascii.hexlify(instructions.content)
program = [hexstring[i:i+2] for i in range(0, len(hexstring), 2)]

for code in program:
    print code,
    if code in operations.keys():
        print operations[code],
    else:
        print int(code, 16)
