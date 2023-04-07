from exception import db_read_error
#from Objects import 


numli = ["1","2","3","4","5","6","7","8","9","0"]

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
        e2 = e2.replace("[","")
        e2 = e2.replace("]","")
        maindict.update({"FOREIGN_KEY":e2.split(";")})
    elif e1 == "foreign_key" and e2 == "[None]":
        maindict.update({"FOREIGN_KEY":e2})
    return maindict
    

def tag_spill(char:str,tag1,tag2):
    if (tag1 not in char) or (tag2 not in char):
        db_read_error.notag(f"{tag1} or {tag2} is not in database.")
    e1,char = char.split(tag1)
    e2,e3 = char.split(tag2)
    return [e1,e2,e3]

def get_sc_dic(char:str,sep=":",fkey=False):
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

def get_fruit_dic(char:str):
    maindic = dict()
    key = char[:3]
    char = char[4:]
    char = char.replace("{","")
    char = char.replace(f"${key[2]}>","")
    char = char.replace("}","")
    char = char.replace(f"<${key[2]}","")
    char = char.split(",")
    for i in char:
        w = i.split(":")
        if w[1][-1] == '"' and w[1][0] == '"':
            w[1] = w[1].replace('"',"")
        else:
            if "." in w[1]:
                w[1] = float(w[1])
            elif w[1] == "True" or w[1] == "False":
                w[1] = bool(w[1])
            elif w[1][0] in numli:
                w[1] = int(w[1])
            else:
                raise db_read_error.DataisNotinSchm
        maindic.update({w[0]:w[1]})
    return {key: maindic}



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
            if (("{" in i) or ("}" in i)) and (i[0:11] != 'foreign_key'):
                dic_st = i
                continue
            if i[0:11] == "primary_key":
                l.update({"PRIMARY_KEY":(prim_for_key(i)['PRIMARY_KEY'])})
                continue
            if i[0:11] == "foreign_key":
                l.update({"FOREIGN_KEY":(prim_for_key(i))['FOREIGN_KEY']})
                continue
            l.update(get_sc_dic(i))

        maindict = dict()
        if dic_st[0:7] == "slices:":
            sep = "|"
            #print(dic_st)
            dic_st = dic_st[7:]
            #print(dic_st)
            dic_st = dic_st.replace("{","")
            dic_st = dic_st.replace("}","")
            li = dic_st.split(sep)
            maindict.update({"slices":dict()})
            for i in li:
                maindict['slices'].update(get_sc_dic(i))
            l.update(maindict)
    # var "l" is the output var of the above code.
    # process data
    raw = giv_raw(fp)
    raw = (tag_spill(raw,"{main>","<main}"))[1]
    parts = raw.split(";~")
    data = parts[1]
    if data[0:11] != "$mainfruit:":
        raise db_read_error.nohull
    else:
        data = data[11:]
        data = (tag_spill(data,"{infu>","<infu}"))[1]
        data = data.split(";")
        dict1 = dict()
        for i in data:
            dict1.update(get_fruit_dic(i))
        print(dict1)
        pass



read_berrybase(".\\text.berrybase")