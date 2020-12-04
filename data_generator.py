import json
import csv
from random import seed
from random import randint


def generatePhone():
    phone = []
    for _ in range(9):
        value = str(randint(0, 9))
        phone.append(value)
    return "07" + ("".join(phone))


def generateSubjects():
    subs = []
    abbrs = ["BI", "CH", "EN", "FL", "GE", "HI", "IT", "MA", "PH", "PR"]
    for _ in range(4):
        value = randint(0, 9)
        subs.append(abbrs[value])
    return "".join(subs)


with open('data.json') as f:
    data = json.load(f)
    DB = []

    for row in data:
        [f_name, l_name] = row["name"].split(" ")
        dob = row["dob"]
        phone = generatePhone()
        email = row["email"]
        subjects = generateSubjects()

        row_obj = {
            "f_name": f_name,
            "l_name": l_name,
            "phone": phone,
            "subjects": subjects,
            "dob": dob,
            "email": email
        }
        DB.append(row_obj)


with open("data_1", 'w', newline='') as csvfile:
    fieldnames = ['f_name', 'l_name', "phone", "subjects", "dob", "email"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in DB:
        writer.writerow(row)
