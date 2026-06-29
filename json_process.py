#This program is used to process JSON files.

def read_Data(data, temp):
    for i in data:
        value = data[i]
        if type(value) != str:
            temp[i] = [j for j in value]
            read_Data(value, temp)
        else:
            temp[i] = value
    return temp

def process_Data(data, rawData):
    t = {}
    for i in data:
        value = rawData[i]
        if type(value) != str:
            t[i] = process_Data(value, rawData)
        else:
            t[i] = value
    return t