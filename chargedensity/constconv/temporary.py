import re

parametr = 'gegegeg'

def handle_uploaded_file(file):
    data = []

    for line in file:

        line = line.decode('utf-8')
        search = re.search(r'^\((.*?)\)s', line)
        if search:
            text = search.group(1)
            if text == '' or text.startswith('Symmetry') or text.startswith('structure'):
                continue
            data.append(text)

        print(data)

handle_uploaded_file('gegegeg')