import json
from anytree import Node, RenderTree, AnyNode
from anytree.exporter import JsonExporter

counter = 0
haha = 0
x = 0

def Datafromscripts(Name, option, text):
    if option == 0:
        option = "Phishing"
    else:
        option = "Vishing"

    global counter
    counter += 1
    if counter == 0:
        data = {
            'Scripts': [
                {
                    'id': counter,
                    'name': Name,
                    'option': option,
                    'text': text
                },
            ]
        }
        json_string = json.dumps(data)

        # Using a JSON string
        with open('json_data.json', 'w') as outfile:
            outfile.write(json_string)
    else:

        dictObj = {'id': counter, 'name': Name, 'option': option, 'text': text}


        with open('json_data.json', 'r+') as fp:
            data = json.load(fp)
            data["Scripts"].append(dictObj)
            fp.seek(0)
            json.dump(data, fp, indent=4)



def ReadDataFromDatabase(number,name):
    with open('json_data.json', 'r+') as fp:
        data = json.load(fp)
        v = data['Scripts'][number]['name']
        if v == name:
            p = data['Scripts'][number]['id'] -1
            number=p
            number = number - 1
            return data['Scripts'][number]["text"]
        else:
            global haha
            haha = number + 1
            return ReadDataFromDatabase(haha, name)
