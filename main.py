from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as in_file:
    rows = csv.reader(in_file, delimiter=",")
    contacts_list = list(rows)
    contacts_list_updated = []

def names_moving():
    name_pattern = r'([А-Я])'
    name_substitution = r' \1'
    for column in contacts_list[1:]:
        line = column[0] + column[1] + column[2]
        if len((re.sub(name_pattern, name_substitution, line).split())) == 3:
            column[0] = re.sub(name_pattern, name_substitution, line).split()[0]
            column[1] = re.sub(name_pattern, name_substitution, line).split()[1]
            column[2] = re.sub(name_pattern, name_substitution, line).split()[2]
        elif len((re.sub(name_pattern, name_substitution, line).split())) == 2:
            column[0] = re.sub(name_pattern, name_substitution, line).split()[0]
            column[1] = re.sub(name_pattern, name_substitution, line).split()[1]
            column[2] = ''
        elif len((re.sub(name_pattern, name_substitution, line).split())) == 1:
            column[0] = re.sub(name_pattern, name_substitution, line).split()[0]
            column[1] = ''
            column[2] = ''
    return
def phone_number_formatting():
    phone_pattern = re.compile(
        r'(\+7|8)?\s*\(?(\d{3})\)?\s*\D?(\d{3})[-\s+]?(\d{2})-?(\d{2})((\s)?\(?(доб.)?\s?(\d+)\)?)?')
    phone_substitution = r'+7(\2)\3-\4-\5\7\8\9'
    for column in contacts_list:
        column[5] = phone_pattern.sub(phone_substitution, column[5])
    return


def duplicates_combining():
    contact_list = {}
    for column in contacts_list[1:]:
        last_name = column[0]
        first_name = column[1]
        for contact in contacts_list[1:]:
            new_last_name = contact[0]
            new_first_name = contact[1]
            if last_name == new_last_name and first_name == new_first_name:
                for item in range(2, 7):
                    if contact[item] == '':
                        contact[item] = column[item]
        if last_name not in contact_list:
            contact_list[last_name] = column
        else:
            for ind, item in enumerate(contact_list[last_name]):
                if item == '':
                    contact_list[last_name][ind] = column[ind]

    for contact in contacts_list:
        if contact not in contacts_list_updated:
            contacts_list_updated.append(contact)
    for last_name, contact in contact_list.items():
        for contacts in contact:
            if contact not in contacts_list_updated:
                contacts_list_updated.append(contact)
    return contacts_list_updated


if __name__ == '__main__':
    names_moving()
    phone_number_formatting()
    duplicates_combining()

# код для записи файла в формате CSV
with open("phonebook.csv", "w") as out_file:
    datawriter = csv.writer(out_file, delimiter=',')
    datawriter.writerows(contacts_list_updated)
pprint(contacts_list_updated)
with open("phonebook_raw.csv") as in_file:
    rows = csv.reader(in_file, delimiter=",")
    contacts_list = list(rows)
    contacts_list_updated = []
    names_moving()
    phone_number_formatting()
    duplicates_combining()
with open("phonebook.csv", "w") as out_file:
    datawriter = csv.writer(out_file, delimiter=',')
    datawriter.writerows(contacts_list_updated)
pprint(contacts_list_updated)
