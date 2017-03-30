"""Lets solve this one too."""
import requests
import binascii
import BeautifulSoup as bs

"""
0x00    move
0x01    logical or
0x02    logical xor
0x03    logical and
0x04    logical not
0x05    addition
0x06    subtraction
0x07    multiplication
0x08    logical shift left
0x09    logical shift right
0x0a    increment
0x0b    decrement
0x0c    push on stack
0x0d    pop from stack
0x0e    compare
0x0f    jump to nth opcode when not zero*
0x10    jump to nth opcode when zero*
"""


class Controller(object):
    """Manages the connection with the website."""

    def __init__(self):
        """Create a Controller for this problem."""
        self.host = '80.233.134.207'
        self.url = 'http://' + self.host + '/0x00000ACE.html'
        with open('.key', 'r') as keyfile:
            key = keyfile.read()
        self.header = {'X-0x0ACE-Key': key.strip()}

        response = requests.get(self.url, headers=self.header)
        html = response.content
        soup = bs.BeautifulSoup(html)
        link = soup.find('a')

        challenge = link['href']
        instructions = requests.get('http://'+self.host+challenge,
                                    headers=self.header)
        self.binary_data = instructions.content

        with open('binary_assembley.temp.bin', 'wb+') as file:
            file.write(self.binary_data)

    def parse(self):
        """Parse the given byte code and returns the instructions hexdump."""
        hexstring = binascii.hexlify(self.binary_data)
        program = [hexstring[i:i + 2] for i in range(0, len(hexstring), 2)]
        return program


class VM(object):
    """A simple VM to solve the challenge."""

    OPERATIONS = ['MOVE', 'OR', 'XOR', 'AND', 'NOT', 'ADD', 'SUB', 'MUL',
                  'SH_L', 'SH_R', 'INC', 'DEC', 'PUSH', 'POP', 'CMP', 'JMP',
                  'JP']

    def __init__(self, registers, stack, program, pc=0):
        """Initialize the VM registers, stack, counter and code."""
        self._registers = registers
        self._stack = stack
        self._program = program
        self._pc = pc

    def __str__(self):
        """Print the VM status during execution."""
        _string = 'VM(REG{},\n   STACK{}\n)'
        return _string.format(self._registers, self._stack)

    def program(self):
        """Return the byte code as hex."""
        return self._program

    def push(self, value):
        """0x0c    push on stack."""
        self._stack.append(value)

    def pop(self):
        """0x0d    pop from stack."""
        return self._stack.pop()


if __name__ == '__main__':
    controller = Controller()
    vm = VM([0, 0, 0, 0], [], controller.parse())

    operations = {'00': 'move', '01': '^or', '02': '^xor', '03': '^and',
                  '04': '^not', '05': 'add', '06': 'sub', '07': 'mul',
                  '08': '^lsh', '09': '^rsh', '0a': 'inc', '0b': 'dec',
                  '0c': 'push', '0d': 'pop', '0e': 'compare', '0f': 'jump',
                  '10': 'jump*'}

    for code in vm.program():
        if code in operations.keys():
            print operations[code],
        else:
            print code

print vm.program()
