import csv
from serializer import PickleStorage
from addressbook import Birthday, Phone, Email, AddressBook

contacts = AddressBook()


def import_csv(filename):
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header row
        for row in reader:
            name = row[0]
            birthday = [Birthday("10.10.1234")]
            phones = [Phone(number) for number in row[2].split(";")]
            emails = [Email(email) for email in row[3].split("|")]

            address = row[4]
            contacts.add_record(
                name=name,
                birthday=birthday,
                phones=phones,
                emails=emails,
                address=address,
            )


import_csv("./data.csv")

contacts.show_contact()

PickleStorage.export_file(contacts, "contacts.bin")


contacts.update(PickleStorage.import_file("contacts.bin"))

print(contacts)
