from os import makedirs,rmdir,remove
from copy import copy
import prettytable

# Global Variables
strawberry_logo = r"""
                 \\\\\\\\  ||||||||||  ////////
                   \\\\\\   ||||||||   //////
                     \\\\\   ||||||   /////
                        \\\   ||||   ///
                       _______:___:_______
                      /|||||||||||||||||||\
                     / , , , , , , , , , , \
                    | , , , , , , , , , , , |
                    |, , , , , , , , , , , ,|
                    \ , , , , , , , , , , , /
                     \ , , , , , , , , , , /
                      \ , , , , , , , , , /
                       \ , , , , , , , , /
                        \ , , , , , , , /
                         \ , , , , , , /
(>O w O)>  Welcome to     \ , , , , , /        Created by
          StrawberryDB     \ , , , , /      Amrut Kumar Meher
                            \ , , , /
                             \ , , /
                              \___/
"""


# All independent functions
def _clean(raw: str):
    raw = raw.replace("\n", "")
    raw = raw.replace(" ", "")
    return raw

def charty(char):
    typ = None
    try:
        int(char)
        typ = int
    except:
        if char == "True" or char == "False":
            typ = bool
        elif len(char.split(".")) == 2:
            typ = float
        else:
            typ = str
    return typ

def find_dataty(char):
    if "'" in char or '"' in char:
        dataty = str
    else:
        if "." in char:
            dataty = float
        elif char == "True" or char == "False":
            dataty = bool
        else:
            dataty = int
    return dataty

def prim_for_key(char: str, sep=":"):
    maindict = dict()
    e1, e2 = char.split(sep, maxsplit=1)
    e1 = e1.replace('"', "")
    if e1 == 'primary_key' and e2 != "[None]":
        maindict.update({"primary_key": e2})
    elif e1 == 'primary_key' and e2 == "[None]":
        maindict.update({"primary_key": None})
    elif e1 == "foreign_key" and e2 != "[None]":
        e2 = e2.replace("[", "")
        e2 = e2.replace("]", "")
        maindict.update({"foreign_key": e2.split(";")})
    elif e1 == "foreign_key" and e2 == "[None]":
        maindict.update({"foreign_key": e2})
    else:
        raise db_read_error.MissingPrimOrForkeys
    return maindict

def tag_spill(char: str, tag1, tag2):
    if (tag1 not in char) or (tag2 not in char):
        db_read_error.notag(f"{tag1} or {tag2} is not in database.")
    e1, char = char.split(tag1)
    e2, e3 = char.split(tag2)
    return [e1, e2, e3]

def get_sc_dic(char: str, sep=":", fkey=False):
    "please use | as a sep if processing an array."
    maindict = dict()
    e1, e2 = char.split(sep, maxsplit=1)
    e1 = e1.replace('"', "")
    if e2 == "char":
        maindict.update({e1: str})
    elif e2 == "int":
        maindict.update({e1: int})
    elif e2 == "bool":
        maindict.update({e1: bool})
    elif e2 == 'None' or e2 == "[None]":
        maindict.update({e1: None})
    elif e2 == "decimal":
        maindict.update({e1: float})
    elif fkey == True:
        maindict.update({e1: e2})
    return maindict

def get_fruit_dic(char: str):
    maindic = dict()
    key = char.split(":")[0].replace("*&", "")
    char = char.replace(f"*&{key}:", "")
    char = char.replace(f"<${key}", "")
    char = char.replace("{", "")
    char = char.replace(f"${key}>", "")
    char = char.replace("}", "")
    char = char.split(",")
    for i in char:
        w = i.split(":")
        if w[1][-1] == '"' and w[1][0] == '"':
            w[1] = w[1].replace('"', "")
        else:
            if charty(w[1]) == float:
                w[1] = float(w[1])
            elif charty(w[1]) == bool:
                w[1] = bool(w[1])
            elif charty(w[1]) == int:
                w[1] = int(w[1])
            elif charty(w[1]) == str:
                pass
            else:
                raise db_read_error.DataisNotinSchm
        maindic.update({w[0]: w[1]})
    return {key: maindic}

def newcol(cla, head):
    l = copy(cla(head))
    return l

def giv_raw(fp):
    with open(fp, "r") as file:
        raw = file.read()
    raw = _clean(raw)
    return raw

# Classes Exceptions
class syntaxerror(Exception):
    def __init__(self,msg="You have written wrong syntax!"):
        self.msg = msg
        super().__init__(self.msg)
    class objectCreationErr(Exception):
        def __init__(self,msg):
            self.msg = msg
            super().__init__(self.msg)
    class FormatErr(Exception):
        def __init__(self,msg="Please enter the syntax with correct syntax format."):
            self.msg = msg
            super().__init__(self.msg)
    class UnknownOperation(Exception):
        def __init__(self,msg="This operation is unknown!"):
            self.msg = msg
            super().__init__(self.msg)

class db_read_error(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)
    class MissingPrimOrForkeys(Exception):
        def __init__(self,msg='Primary Key or Foreign key is not in database or not in proper position.'):
            self.msg = msg
            super().__init__(self.msg)
    class nohull(Exception):
        def __init__(self,msg="hull is not in the database.") -> None:
            self.msg = msg
            super().__init__(self.msg)
    class noMainFruit(Exception):
        def __init__(self,msg="MainFruit is not in the database."):
            self.msg = msg
            super().__init__(self.msg)
    class notag(Exception):
        def __init__(self,msg="The tag is missing.") -> None:
            self.msg = msg
            super().__init__(self.msg)
    class DataisNotinSchm(Exception):
        def __init__(self,msg="All data in database are not according to the data scheme."):
            self.msg = msg
            super().__init__(self.msg)

class db_update_error(Exception):
    def __int__(self,msg):
        self.msg = msg
        super().__int__(self.msg)
    class column_datatype_err(Exception):
        def __init__(self,msg="Given value doesn't match with column datatype."):
            self.msg = msg
            super().__init__(self.msg)

# Classes
class slices:
    class primary_keys:
        def __init__(self, head, datatype=str) -> None:
            self.head = head
            self.vals = copy(list())
            self.datatype = datatype
        def add(self, data):
            if type(data) != self.datatype:
                raise db_update_error.column_datatype_err()
            else:
                self.vals.append(data)

    class foreign_keys:
        def __init__(self, head, reference_table_name=None, datatype=str) -> None:
            self.head = head
            self.vals = copy(list())
            self.datatype = datatype
            self.reference = reference_table_name
        def add(self, data):
            if type(data) != self.datatype:
                raise db_update_error.column_datatype_err()
            else:
                self.vals.append(data)

    class columnint:
        def __init__(self, head):
            self.head = head
            self.vals = copy(list())
            self.datatype = int
        def add(self, data):
            self.vals.append(data)

    class columnbool:
        def __init__(self, head):
            self.head = head
            self.vals = copy(list())
            self.datatype = bool
        def add(self, data):
            self.vals.append(data)

    class columnstr:
        def __init__(self, head):
            self.head = head
            self.vals = copy(list())
            self.datatype = str
        def add(self, data):
            self.vals.append(data)

    class columnflo:
        def __init__(self, head):
            self.head = head
            self.vals = copy(list())
            self.datatype = float
        def add(self, data):
            self.vals.append(data)



class StrawBerry:
    def __init__(self, have_data=True, data: dict = None, schema: dict = None, fp=None):
        if have_data == True:
            try:
                self.PRIMARY_KEY = schema['primary_key']
            except:
                self.PRIMARY_KEY = schema["PRIMARY_KEY"]
            try:
                self.FOREIGN_KEY = schema['FOREIGN_KEY']
                if self.FOREIGN_KEY == '[None]':
                    self.FOREIGN_KEY = None
            except:
                self.FOREIGN_KEY = schema["foreign_key"]
                if self.FOREIGN_KEY == '[None]':
                    self.FOREIGN_KEY = [None]
            self.schpunnet = {}
            self.punnet = {}
            for i in (schema['slices']).keys():
                if i == self.PRIMARY_KEY:
                    self.schpunnet.update({i: slices.primary_keys(i, datatype=schema['slices'][i])})
                elif self.FOREIGN_KEY:
                    self.schpunnet.update(
                        {i: slices.foreign_keys(i, reference_table_name=[1], datatype=schema['slices'][i])})
                elif schema['slices'][i] == bool:
                    self.schpunnet.update({i: slices.columnbool(i)})
                elif schema['slices'][i] == int:
                    self.schpunnet.update({i: slices.columnint(i)})
                elif schema['slices'][i] == float:
                    self.schpunnet.update({i: slices.columnflo(i)})
                elif schema['slices'][i] == str:
                    self.schpunnet.update({i: slices.columnstr(i)})

            self.init_punnet()
            for i in data:
                self.add_row(data[i])
        else:
            data = self.read_berrybase(fp)
            schema = data['hull']
            self.PRIMARY_KEY = schema["primary_key"]
            self.FOREIGN_KEY = schema["foreign_key"]
            self.schpunnet = {}
            self.punnet = {}
            for i in (schema['slices']).keys():
                if i == self.PRIMARY_KEY:
                    self.schpunnet.update({i: slices.primary_keys(i, datatype=schema['slices'][i])})
                elif i == self.FOREIGN_KEY[0]:
                    self.schpunnet.update(
                        {i: slices.foreign_keys(i, reference_table_name=[1], datatype=schema['slices'][i])})
                elif schema['slices'][i] == bool:
                    self.schpunnet.update({i: slices.columnbool(i)})
                elif schema['slices'][i] == int:
                    self.schpunnet.update({i: slices.columnint(i)})
                elif schema['slices'][i] == float:
                    self.schpunnet.update({i: slices.columnflo(i)})
                elif schema['slices'][i] == str:
                    self.schpunnet.update({i: slices.columnstr(i)})

            self.init_punnet()
            for i in data['mainfruit']:
                self.add_row(data["mainfruit"][i])

    def add_slice(self, head, datatype=str):
        self.punnet.append(slices.column(head, datatype=datatype))

    def add_row(self, data: dict):
        for i in data:
            if i == self.PRIMARY_KEY:
                self.punnet[i].vals.append(data[i])
            elif i == self.FOREIGN_KEY[0]:
                self.punnet[i].vals.append(data[i])
            elif type(data[i]) == bool:
                self.punnet[i].vals.append(data[i])
            elif type(data[i]) == int:
                self.punnet[i].vals.append(data[i])
            elif type(data[i]) == float:
                self.punnet[i].vals.append(data[i])
            elif type(data[i]) == str:
                self.punnet[i].vals.append(data[i])

    def init_punnet(self):
        self.punnet = self.schpunnet

    def read_berrybase(self, fp):
        # opening file
        # process schema
        raw = giv_raw(fp)
        raw = (tag_spill(raw, "{main>", "<main}"))[1]
        parts = raw.split(";~")
        schema = parts[0]
        if schema[0:6] != "$hull:":
            raise db_read_error.nohull
        else:
            schema = schema[6:]
            schema = (tag_spill(schema, "{hulltag>", "<hulltag"))[1]
            schema = schema.split(",")
            l = dict()
            dic_st = str()
            for i in schema:
                if (("{" in i) or ("}" in i)) and (i[0:11] != 'foreign_key'):
                    dic_st = i
                    continue
                if i[0:11] == "primary_key":
                    l.update({"primary_key": (prim_for_key(i)['primary_key'])})
                    continue
                elif i[0:11] == "foreign_key":
                    l.update({"foreign_key": (prim_for_key(i))['foreign_key']})
                    continue
                else:
                    db_read_error.MissingPrimOrForkeys
                l.update(get_sc_dic(i))

            maindict = dict()
            if dic_st[0:7] == "slices:":
                sep = "|"
                # print(dic_st)
                dic_st = dic_st[7:]
                # print(dic_st)
                dic_st = dic_st.replace("{", "")
                dic_st = dic_st.replace("}", "")
                li = dic_st.split(sep)
                maindict.update({"slices": dict()})
                for i in li:
                    maindict['slices'].update(get_sc_dic(i))
                l.update(maindict)
        # var "l" is the output var of the above code.
        # process data
        raw = giv_raw(fp)
        raw = (tag_spill(raw, "{main>", "<main}"))[1]
        parts = raw.split(";~")
        data = parts[1]
        if data[0:11] != "$mainfruit:":
            raise db_read_error.noMainFruit
        else:
            data = data[11:]
            data = (tag_spill(data, "{infu>", "<infu}"))[1]
            data = data.split(";")
            dict1 = dict()
            for i in data:
                dict1.update(get_fruit_dic(i))  #
            return {"hull": l, "mainfruit": dict1}

    def alter(self, primary_key, col, colval):
        for i in self.punnet[self.PRIMARY_KEY].vals:
            if type(colval) != self.punnet[col].datatype:
                raise db_update_error.column_datatype_err
            if i == primary_key:
                self.punnet[col].vals[(self.punnet[self.PRIMARY_KEY].vals).index(i)] = colval

    def show_norm(self,col:list=None,row:list=None):
        if col == None and row == None:
            head = [i for i in self.punnet]
            l = []
            for i in range(len(self.punnet[self.PRIMARY_KEY].vals)):
                li = []
                for e in self.punnet:
                    li.append(self.punnet[e].vals[i])
                l.append(li)
            table = [head]
            table.append(l)
            return table
        elif col != None and row == None:
            head = []
            for i in col:
                for e in self.punnet:
                    if self.punnet[e].head == i:
                        head.append(e)
            l = []
            for i in range(len(self.punnet[self.PRIMARY_KEY].vals)):
                li = []
                for e in self.punnet:
                    if e not in col:
                        continue
                    li.append(self.punnet[e].vals[i])
                l.append(li)
            table = [head]
            table.append(l)
            return table
        elif col != None and row != None:
            head = []
            for i in col:
                for e in self.punnet:
                    if self.punnet[e].head == i:
                        head.append(e)
            l = []
            for i in range(len(self.punnet[self.PRIMARY_KEY].vals)):
                if i not in row:
                    continue
                li = []
                for e in self.punnet:
                    if e not in col:
                        continue
                    li.append(self.punnet[e].vals[i])
                l.append(li)
            # print(l)
            table = [head]
            table.append(l)
            return table
        elif col == None and row != None:
            head = [i for i in self.punnet]
            l = []
            for i in range(len(self.punnet[self.PRIMARY_KEY].vals)):
                if str(i) not in row:
                    continue
                li = []
                for e in self.punnet:
                    li.append(self.punnet[e].vals[i])
                l.append(li)
            # print(l)
            table = [head]
            table.append(l)
            return table

    def show(self, col:list=None, row:list=None):
        if col == None and row == None:
            head = [i for i in self.punnet]
            l = []
            for i in range(len(self.punnet[self.PRIMARY_KEY].vals)):
                li = []
                for e in self.punnet:
                    li.append(self.punnet[e].vals[i])
                l.append(li)
            table = prettytable.PrettyTable(head)
            table.add_rows(l)
            return table
        elif col != None and row == None:
            head = []
            for i in col:
                for e in self.punnet:
                    if self.punnet[e].head == i:
                        head.append(e)
            l = []
            for i in range(len(self.punnet[self.PRIMARY_KEY].vals)):
                li = []
                for e in self.punnet:
                    if e not in col:
                        continue
                    li.append(self.punnet[e].vals[i])
                l.append(li)
            # print(l)
            table = prettytable.PrettyTable(head)
            table.add_rows(l)
            return table
        elif col != None and row != None:
            head = []
            for i in col:
                for e in self.punnet:
                    if self.punnet[e].head == i:
                        head.append(e)
            l = []
            for i in range(len(self.punnet[self.PRIMARY_KEY].vals)):
                if i not in row:
                    continue
                li = []
                for e in self.punnet:
                    if e not in col:
                        continue
                    li.append(self.punnet[e].vals[i])
                l.append(li)
            # print(l)
            table = prettytable.PrettyTable(head)
            table.add_rows(l)
            return table
        elif col == None and row != None:
            head = [i for i in self.punnet]
            l = []
            for i in range(len(self.punnet[self.PRIMARY_KEY].vals)):
                if (find_dataty(i)(i)) not in row:
                    continue
                li = []
                for e in self.punnet:
                    li.append(self.punnet[e].vals[i])
                l.append(li)
            table = prettytable.PrettyTable(head)
            table.add_rows(l)
            return table

    def insert(self, data: dict):
        for i in data:
            self.add_row(data[i])

    def seal(self, indent=4):
        mainstr = str()
        slic = dict()
        for i in self.schpunnet:
            slic.update({i: self.schpunnet[i].datatype})
        schema = {"primary_key": self.PRIMARY_KEY, "foreign_key": self.FOREIGN_KEY, "slices": slic}
        # for i in self.schpunnet:
        # schema.update({i:self.schpunnet[i]})
        l = {}
        for i in range(len(self.punnet[self.PRIMARY_KEY].vals)):
            li = {}
            for e in self.punnet:
                li.update({e: self.punnet[e].vals[i]})
            i = f"*&{self.punnet[self.PRIMARY_KEY].vals[i]}"
            l.update({i: li})
        mainstr = mainstr.__add__("{main>\n")
        mainstr = mainstr.__add__((" " * indent).__add__("$hull: {hulltag>\n"))
        mainstr = mainstr.__add__((" " * indent * 2).__add__(f"primary_key: {schema['primary_key']},\n"))
        mainstr = mainstr.__add__((" " * indent * 2).__add__(f"foreign_key: {schema['foreign_key']},\n"))
        mainstr = mainstr.__add__((" " * indent * 2).__add__(f"slices: {schema['slices']},\n"))
        mainstr = mainstr.__add__((" " * indent).__add__("<hulltag};~\n"))
        mainstr = mainstr.__add__((" " * indent).__add__("$mainfruit: {infu>\n"))
        for i in l:
            mainstr = mainstr.__add__((" " * indent * 2).__add__(f"{i}: {{${l[i][self.PRIMARY_KEY]}>\n"))
            for z in l[i]:
                mainstr = mainstr.__add__((f" " * indent * 3).__add__(f"{z}: {l[i][z]}\n"))
            mainstr = mainstr.__add__((" " * indent * 2).__add__(f"<${l[i][self.PRIMARY_KEY]}}}\n"))
        mainstr = mainstr.__add__((" " * indent * 2).__add__("}\n"))
        mainstr = mainstr.__add__((" " * indent * 1).__add__("<infu}\n"))
        mainstr = mainstr.__add__("<main}\n")
        return mainstr

    def seal_deliver(self, dbpath, filename, indent=4, createdb=False):
        if createdb:
            with open(dbpath.__add__(filename), "x") as f:
                f.write(self.seal(indent))
        else:
            with open(dbpath.__add__(filename), "w") as f:
                f.write(self.seal(indent))

# Argument parser
def argu(argument):
    arguments = argument.split("\n")
    for i in arguments:
        if i == "":
            del arguments[arguments.index(i)]

    for argu in arguments:
        argus = argu.split(" ")
        if argus[0][0] == "*":
            continue
        if argus[0].lower() == "create":
            if argus[1].lower() == "database":
                makedirs(f"{argus[2]}.BerryBase")
                return f"database {argus[2]} has been successfully created!"
            elif argus[1].lower() == "table":
                name = argus[2]
                if argus[3].lower() == "in":
                    if argus[4].lower() == "database":
                        db = argus[5]
                        open(f".\\{db}.BerryBase\\{name}.berrybase","x")
                        return f"table {name} in database {db} has been successfully created!"
                    else:
                        syntaxerror.FormatErr("Mention database please: create table <name> in database <dbname>")
                else:
                    syntaxerror.FormatErr("Mention database please: create table <name> in database <dbname>")
            else:
                raise syntaxerror.objectCreationErr(f"Unrecognized object: {argus[1]}")
        elif argus[0].lower() == "alter":
            if argus[1].lower() == "database":
                return f"database {argus[2]} has successfully altered!"
            elif argus[1].lower() == "table":
                return f"table {argus[2]} has successfully altered!"
            else:
                raise syntaxerror.objectCreationErr(f"Unrecognized object: {argus[1]}")
        elif argus[0].lower() == "drop":
            if argus[1].lower() == "database":
                rmdir(f"{argus[2]}.BerryBase")
                return f"database {argus[2]} has been successfully droped!"
            elif argus[1].lower() == "table":
                if argus[3] == "in":
                    if argus[4] == "database":
                        remove(f".\\{argus[5]}.BerryBase\\{argus[2]}.berrybase")
                        return f"table {argus[2]} has been successfully droped!"
                    else:
                        raise syntaxerror.FormatErr("format: drop table <name> in database <dbname>")
                else:
                    raise syntaxerror.FormatErr("format: drop table <name> in database <dbname>")
            else:
                raise syntaxerror.objectCreationErr(f"Unrecognized object: {argus[1]}")
        elif argus[0].lower() == "grab":
            if argus[1].lower() == "from":
                if argus[2].lower() == "table":
                    table = argus[3]
                    if argus[4].lower() == "from":
                        if argus[5].lower() == "database":
                            db = argus[6]
                            ins = StrawBerry(have_data=False,fp=f".\\{db}.BerryBase\\{table}.berrybase")
                            if argus[7][:3].lower() == "row":
                                rows = argus[7]
                                rows = rows.replace("row(","")
                                rows = rows.replace(")","")
                                rows = rows.split(",")
                                return ins.show_norm(row=rows)
                            elif argus[7][:3].lower() == "col":
                                col = argus[7]
                                col = col.replace("col(","")
                                col = col.replace(")","")
                                col = col.split(",")
                                return ins.show_norm(col=col)
                            else:
                                raise syntaxerror.FormatErr(
                                    "format: grab from table <name> from database <dbname> col(col1,col)/row(row,row2)")
                        else:
                            raise syntaxerror.FormatErr(
                                "format: grab from table <name> from database <dbname> col(num)/row(num)")
                    else:
                        raise syntaxerror.FormatErr(
                            "format: grab from table <name> from database <dbname> col(num)/row(num)")
                else:
                    raise syntaxerror.FormatErr(
                        "format: grab from table <name> from database <dbname> col(num)/row(num)")
            else:
                raise syntaxerror.FormatErr(
                    "format: grab from table <name> from database <dbname> col(num)/row(num)")
        else:
            raise syntaxerror.UnknownOperation(f"Operation {argus[0]} is unknown!")
        
def main():
    print(strawberry_logo)
    while True:
        inpu = input(">")
        if inpu == "exit":
            break
        print(argu(inpu))
main()