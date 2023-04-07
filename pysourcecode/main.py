from exception import db_read_error


def _clean(raw:str):
    raw = raw.replace("\n","")
    raw = raw.replace(" ","")
    return raw

def prim_for_key(char:str,sep=":"):
    maindict = dict()
    e1, e2 = char.split(sep,maxsplit=1)
    e1 = e1.replace('"',"")
    if e1 == 'primary_key' and e2 != "[None]":
        maindict.update({"PRIMARY_KEY":e2})
    elif e1 == 'primary_key' and e2 == "[None]":
        maindict.update({"PRIMARY_KEY":None})
    if e1 == "foreign_key" and e2 != "[None]":
        e2 = e2.replace("{","")
        e2 = e2.replace("}","")
        maindict.update({"FOREIGN_KEY":get_dic(e2,":",fkey=True)})
    elif e1 == "foreign_key" and e2 == "[None]":
        maindict.update({"FOREIGN_KEY":e2})
    return maindict
    

def tag_spill(char:str,tag1,tag2):
    if (tag1 not in char) or (tag2 not in char):
        db_read_error.notag(f"{tag1} or {tag2} is not in database.")
    e1,char = char.split(tag1)
    e2,e3 = char.split(tag2)
    return [e1,e2,e3]

def get_dic(char:str,sep=":",fkey=False):
    "please use | as a sep if processing an array."
    maindict = dict()
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
    elif fkey == True:
        maindict.update({e1:e2})
    return maindict

def giv_raw(fp):
    with open(fp,"r") as file:
        raw = file.read()
    raw = _clean(raw)
    return raw

def read_berrybase(fp):
    #opening file
    #process schema
    raw = giv_raw(fp)
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
        dic_st = str()
        for i in schema:
            if "{" in i or "}" in i:
                dic_st = i
                continue
            if i[0:11] == "primary_key":
                l.update({"PRIMARY_KEY":(prim_for_key(i)['PRIMARY_KEY'])})
                continue
            if i[0:11] == "foreign_key":
                l.update({"FOREIGN_KEY":(prim_for_key(i))['FOREIGN_KEY']})
                continue
            l.update(get_dic(i))

        maindict = dict()
        if dic_st[0:7] == "slices:":
            sep = "|"
            dic_st = dic_st[7:]
            dic_st = dic_st.replace("{","")
            dic_st = dic_st.replace("}","")
            li = dic_st.split(sep)
            maindict.update({"slices":dict()})
            for i in li:
                maindict['slices'].update(get_dic(i,sep=":"))
            l.update(maindict)
    # var "l" is the output var of the above code.
    # process data
    raw = giv_raw(fp)
    raw = (tag_spill(raw,"{main>","<main}"))[1]
    parts = raw.split(";~")
    schema = parts[1]
    if schema[0:11] != "$mainfruit:":
        raise db_read_error.nohull
    else:
        print(l,type(l))
        pass

    

        

    

read_berrybase(".\\pysourcecode\\text.berrybase")