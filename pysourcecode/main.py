from exception import db_read_error

def _clean(raw:str):
    raw = raw.replace("\n","")
    raw = raw.replace(" ","")
    return raw



def tag_spill(char:str,tag1,tag2):
    if (tag1 not in char) or (tag2 not in char):
        db_read_error.notag(f"{tag1} or {tag2} is not in database.")
    e1,char = char.split(tag1)
    e2,e3 = char.split(tag2)
    return [e1,e2,e3]

def get_dic(char:str,sep=":"):
    "please use | as a sep if processing an array."
    maindict = dict()
    if char[0:7] == "slices:":
        sep = "|"
        char = char[7:]
        char = char.replace("{","")
        char = char.replace("}","")
        l = char.split(sep)
        for i in l:
            maindict.update(get_dic(i,sep=":"))
        return maindict
    else:
        e1, e2 = char.split(sep,maxsplit=1)
        e1 = e1.replace('"',"")
        if e2 == "char":
            maindict.update({e1:str})
        elif e2 == "int":
            maindict.update({e1:int})
        elif e2 == "bool":
            maindict.update({e1:bool})
        elif e2 == 'None' or e2 == "[None]":
            maindict.update({e1:None})
        elif e2 == "decimal":
            maindict.update({e1:float})
        return maindict
        # Have to put operations for primary key.


def read_berrybase(fp):
    #opening file
    with open(fp,"r") as file:
        raw = file.read()
    # processing schema
    raw = _clean(raw)
    raw = (tag_spill(raw,"{main>","<main}"))[1]
    parts = raw.split(";~")
    schema = parts[0]
    if schema[0:6] != "$hull:":
        raise db_read_error.nohull
    else:
        schema = schema[6:]
        schema = (tag_spill(schema,"{hulltag>","<hulltag"))[1]
        schema = schema.split(",")
        l = dict()
        for i in schema:
            l.update(get_dic(i))
    

        

    

read_berrybase(".\\pysourcecode\\text.berrybase")