from pprint import pprint
import csv
import re

def names_moving():
    name_pattern = r'([А-ЯЁ][а-яё]+)'
    name_substitution = r'\1'
    for column in contacts_list[1:]:
        full_name = ' '.join(column[0:3])
        names = re.findall(name_pattern, full_name)
        if len(names) == 3:
            column[0], column[1], column[2] = names
        elif len(names) == 2:
            column[0], column[1], column[2] = names[0], names[1], ''
        elif len(names) == 1:
            column[0], column[1], column[2] = names[0], '', ''

def phone_number_formatting():
    phone_pattern = re.compile(
        r'(\+7|8)?\s*\(?(\d{3})\)?\s*\D?(\d{3})[-\s+]?(\d{2})-?(\d{2})((\s)?\(?(доб.)?\s?(\d+)\)?)?'
    )
    phone_substitution = r'+7(\2)\3-\4-\5\7\8\9'
    for column in contacts_list:
        column[5] = phone_pattern.sub(phone_substitution, column[5])

def duplicates_combining():
    contact_list = {}
    for column in contacts_list[1:]:
        last_name = column[0]
        first_name = column[1]
        if (last_name, first_name) not in contact_list:
            contact_list[(last_name, first_name)] = column
        else:
            for index, item in enumerate(contact_list[(last_name, first_name)]):
                if not item:
                    contact_list[(last_name, first_name)][index] = column[index]

    return [contacts_list[0]] + list(contact_list.values())

if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding="utf-8") as in_file:
        rows = csv.reader(in_file, delimiter=",")
        contacts_list = list(rows)

    names_moving()
    phone_number_formatting()
    contacts_list_updated = duplicates_combining()

    with open("phonebook.csv", "w", encoding="utf-8", newline='') as out_file:
        datawriter = csv.writer(out_file, delimiter=',')
        datawriter.writerows(contacts_list_updated)

    pprint(contacts_list_updated)
