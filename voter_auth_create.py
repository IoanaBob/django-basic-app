import csv
import random
from itertools import islice


def CreateAuth(id,voter_id):
    person = [str(id),voter_id,"41","a" ]

    return person #",".join(person)



auths = []

remaining = random.randint(35,47)
numbers = iter(range(4,20303))
for id in numbers:
    remaining -= 1
    print("F4K3BU7K"+str(id))
    auths.append( CreateAuth(id+1000,"F4K3BU7K"+str(id)) )
    if remaining < 1:
        remaining = random.randint(35,47)
        next(islice(numbers, 20, 20), None)
        id += 20


ofile  = open('auths.csv', "w")
writer = csv.writer(ofile, delimiter=',')

for auth in auths:
    writer.writerow(auth)

ofile.close()