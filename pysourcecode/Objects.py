from exception import  db_update_error

class slices:
    class primary_keys:
        def __init__(self,head,lis=[],datatype=str) -> None:
            self.head = head
            self.vals = lis
            self.datatype = datatype
        def add(self,data):
            if type(data) != self.datatype:
                raise db_update_error.column_datatype_err()
            else:
                self.vals.append(data)
    class foreign_keys:
        def __init__(self,head,lis=[],reference_table_name=None,datatype=str) -> None:
            self.head = head
            self.vals = lis
            self.datatype = datatype
            self.reference = reference_table_name
        def add(self,data):
            if type(data) != self.datatype:
                raise db_update_error.column_datatype_err()
            else:
                self.vals.append(data)
    class column:
        def __init__(self,head,lis=[],datatype=str) -> None:
            self.vals = lis
            self.datatype = datatype
            self.head = head
        def add(self,data):
            if type(data) != self.datatype:
                raise db_update_error.column_datatype_err()
            else:
                self.vals.append(data)

class StrawBerry:
    def __init__(self,data:dict,schema:dict):
        self.PRIMARY_KEY = schema['PRIMARY_KEY']
        self.FOREIGN_KEY = schema['FOREIGN_KEY']
        self.schrows = []
        self.row = []
        for i in (schema['slices']).keys():
            if i == self.PRIMARY_KEY:
                self.schrows.append(slices.primary_keys(i,datatype=schema['slices'][i]))
            if i in schema['slices']:
                self.schrows.append(slices.foreign_keys(i[0],reference_table_name=[1],datatype=schema['slices'][i]))
            else:
                self.schrows.append(slices.column(i,datatype=schema['slice'][i]))
        self.add_row(data)

        def add_slice(self,head,datatype=str):
            self.rows.append(slices.column(head,datatype=datatype))
'''
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
            return {"hull":l,"mainfruit":dict1}

        def add_row(self,data:dict):
            for i in data:
                for e in self.rows:
                    if e == self.PRIMARY_KEY:
                        for o in self.rows:
                            if o.head == e:
                                o.add(i[e])
                                break
                    elif e == self.FOREIGN_KEY:
                        for o in self.rows:
                            if o.head == e:
                                o.add(i[e])
                                break
                    else:
                        for o in self.rows:
                            if o.head == e:
                                o.add(i[e])
'''
        

            


