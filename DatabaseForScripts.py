import json


def start():
    data = {
        'employees' : [
            {
                'name' : 'John Doe',
                'department' : 'Marketing',
                'place' : 'Remote'
            },
            {
                'name' : 'Jane Doe',
                'department' : 'Software Engineering',
                'place' : 'Remote'
            },
            {
                'name' : 'Don Joe',
                'department' : 'Software Engineering',
                'place' : 'Office'
            }
        ]
    }
    json_string = json.dumps(data)
    # Using a JSON string
    with open('json_data.json', 'w') as outfile:
        outfile.write(json_string)

    # Directly from dictionary
    with open('json_data.json', 'w') as outfile:
        json.dump(json_string, outfile)

    with open('json_data.json') as json_file:
        data = json.load(json_file)
        print(data)