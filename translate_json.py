#This program is used to process JSON files.

def get_Child(parent):
    for i in parent:
        if type(parent[i]) != str:
            get_Child(parent[i])
        else:
            return(parent[i])

