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

        self.challenge = link['href']
        instructions = requests.get('http://'+self.host+self.challenge,
                                    headers=self.header)
        self.binary_data = instructions.content

        with open('binary_assembley.temp.bin', 'wb+') as file:
            file.write(self.binary_data)

    def parse(self):
        """Parse the given byte code and returns the instructions hexdump."""
        hexstring = binascii.hexlify(self.binary_data)
        program = [hexstring[i:i + 2] for i in range(0, len(hexstring), 2)]
        return program

    def submit(self, registers):
        """Submit the solution to the challenge."""
        url = 'http://'+self.host+self.challenge
        data = {'reg0': registers[0],
                'reg1': registers[1],
                'reg2': registers[2],
                'reg3': registers[3]}
        response = requests.post(url, data=data, headers=self.header)
        print response.content


class VM(object):
    """A simple VM to solve the challenge."""

    OPERATIONS = ['MOVE', 'OR', 'XOR', 'AND', 'NOT', 'ADD', 'SUB', 'MUL',
                  'SH_L', 'SH_R', 'INC', 'DEC', 'PUSH', 'POP', 'CMP', 'JMP',
                  'JP']

    def __init__(self, registers, stack, program, ip=0):
        """Initialize the VM registers, stack, counter and code."""
        self._registers = registers
        self._stack = stack
        self._program = program
        self._ip = ip

    def __str__(self):
        """Print the VM status during execution."""
        _string = 'VM(IP({}),\n   REG{},\n   STACK{}\n)'
        return _string.format(self._ip, self._registers, self._stack)

    def program(self):
        """Return the byte code as hex."""
        return self._program

    def registers(self):
        """Return the registers."""
        return self._registers

    def execute(self):
        """Start processing the byte code."""
        print('Running 0x0ACE VM\n{}').format(self)

        program_lenght = len(self.program())
        while self._ip < program_lenght:
            self._ip += 1

        print('\n\nFinished running 0x0ACE VM\n{}').format(self)

    def move(self, code):
        """0x00 move."""
        pass


if __name__ == '__main__':
    controller = Controller()

    vm = VM([0, 0, 0, 0], [], ['00', '12', '9f', '1a'])
    vm.execute()

    controller.submit(vm.registers())
