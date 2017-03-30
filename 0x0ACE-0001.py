"""Script for solving the 0x0ACE challenge."""
import requests
import BeautifulSoup as bs
import math


def is_prime(n):
    """Check if number is prime."""
    if n == 2:
        return True
    if n % 2 == 0 or n <= 1:
        return False

    sqr = int(math.sqrt(n)) + 1

    for divisor in range(3, sqr, 2):
        if n % divisor == 0:
            return False
    return True


url = 'http://5.9.247.121/d34dc0d3'

with open('.key', 'r') as keyfile:
    key = keyfile.read()

header = {'X-0x0ACE-Key': key.strip()}

soup = bs.BeautifulSoup(requests.get(url, headers=header).content)
challenge = soup.find("span", {"class": "challenge"})

digits = int(filter(str.isdigit, str(challenge.text)))
val1 = int(str(digits)[:len(str(digits))/2])
val2 = int(str(digits)[len(str(digits))/2:])

verif = soup.find("input")
verification = verif['value']

nums = []
for num in range(val1+2, val2+1, 2):
    if is_prime(num):
        nums.append(str(num))

solution = ', '.join(nums)

r = requests.post("http://5.9.247.121/d34dc0d3",
                  headers={"X-0x0ACE-Key": key.strip()},
                  data={"verification": verification, "solution": solution})

print r.content
