import re
import math
import requests
 
def is_prime(n):
	if n % 2 == 0 and n > 2: 
		return False
	return all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2))
 
key = 'jq1Og5wWzvkqlMRjeDQdyrAOLZ2oJBovx47nxa6VwYPb0p1ENG5g894KmRzQyZ8W'
site = requests.get("http://5.9.247.121/d34dc0d3", headers={"X-0x0ACE-Key": key.strip()})
low = int(re.findall("(\d+), ...,", site.text)[0])
high = int(re.findall(", ..., (\d+)", site.text)[0])
verification = re.findall("value=\"(.+)\"", site.text)[0]
print verification
out = []
for i in range(low + 2, high, 2):
	if is_prime(i):
		out.append(str(i))
solution = ", ".join(out)
print len(solution)
print solution
res = requests.post("http://5.9.247.121/d34dc0d3", headers={"X-0x0ACE-Key": key.strip()}, data={"verification": verification, "solution": solution})
print("\nReply from the site:\n")
print(res.text)
print()