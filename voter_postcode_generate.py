

constiuency_dict = {}

# with open("postcode2.csv","r") as postcode_file:

import csv



def CreatePerson(id,post_code):
    voter_id = "F4K3BU7K" + str(id)
    person = [str(id),voter_id,"Mrs",str(id),"bulk-fake","","","","","","","",post_code,"" ]

    return person #",".join(person)


file1reader = csv.reader(open("postcode.txt"), delimiter=",")

for post_code, constituency in file1reader:

    if(not constituency in constiuency_dict):
        constiuency_dict[constituency] = []

    constiuency_dict[constituency].append(post_code)


people = []

total_people_count = 3
for key in constiuency_dict:
    constituency_people_count = 0
    print(key + ": " + str(len(constiuency_dict[key])))

    for postcode in constiuency_dict[key]:
        total_people_count+= 1
        constituency_people_count += 1
        people.append( CreatePerson(total_people_count,postcode) )

        if(constituency_people_count > 49):
            break
    


ofile  = open('people.csv', "w")
writer = csv.writer(ofile, delimiter=',')

for person in people:
    writer.writerow(person)

ofile.close()


