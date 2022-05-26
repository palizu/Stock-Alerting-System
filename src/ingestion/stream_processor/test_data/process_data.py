import json

with open("data.json", 'r') as f:
    lines = f.readlines()
    c = 1
    for line in lines:
        with open("file" + str(c // 500) + ".json", 'a+') as fo:
            json.dump(json.loads(line), fo)
            if  c % 500 != 0:
                fo.write('\n')
            c = c+1