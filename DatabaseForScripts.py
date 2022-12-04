import json

counter = 0
haha = -1

def Datafromscripts(Name, option, text):
    if option == 0:
        option = "Phishing"
    else:
        option = "Vishing"

    global counter
    counter += 1
    # data = {
    #     'Scripts': [
    #         {
    #             'id': counter,
    #             'name': Name,
    #             'option': option,
    #             'text': text
    #         },
    #     ]
    # }
    # json_string = json.dumps(data)
    #
    # # Using a JSON string
    # with open('json_data.json', 'w') as outfile:
    #     outfile.write(json_string)
    dictObj = {'id': counter, 'name': Name, 'option': option, 'text': text}
    print(dictObj)
    with open('json_data.json', 'r+') as fp:
        data = json.load(fp)
        data["Scripts"].append(dictObj)
        fp.seek(0)
        json.dump(data, fp, indent=4)

def ReadDataFromDatabase(number):
    with open('json_data.json', 'r+') as fp:
        data = json.load(fp)

        print (number)
    return data['Scripts'][number]["text"]
