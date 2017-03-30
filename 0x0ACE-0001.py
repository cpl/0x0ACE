"""Script for solving the 0x0ACE challenge."""
import requests
import BeautifulSoup as bs
import math


def is_prime(n):
    """Check for prime number."""
    if n % 2 == 0 and n > 2:
        return False
    return all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2))


url = 'http://5.9.247.121/d34dc0d3'

with open('.key', 'r') as keyfile:
    key = keyfile.read()

header = {'X-0x0ACE-Key': key.strip()}

ress = requests.get(url, headers=header)
soup = bs.BeautifulSoup(ress.content)
challenge = soup.find("span", {"class": "challenge"})

val1 = int(filter(str.isdigit, str(challenge.text)[:10]))
val2 = int(filter(str.isdigit, str(challenge.text)[10:]))

print val1, val2

verif = soup.find("input")
verification = verif['value']
print verification

nums = []
for num in range(val1+2, val2, 2):
    if is_prime(num):
        nums.append(str(num))

solution = ', '.join(nums)
print 'sol', len(solution)

r = requests.post(url, headers={"X-0x0ACE-Key": key},
                  data={"verification": verification, "solution": solution})

print r.content