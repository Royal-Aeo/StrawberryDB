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
        self.rows = []
        for i in (schema['slices']).keys():
            if i == self.PRIMARY_KEY:
                self.rows.append(slices.primary_keys(i,datatype=schema['slices'][i]))
            if i in schema['slices']:
                self.rows.append(slices.foreign_keys(i[0],reference_table_name=[1],datatype=schema['slices'][i]))
            else:
                self.rows.append(slices.column(i,datatype=schema['slice'][i]))
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
        def add_slice(self,head,datatype=str):
            self.rows.append(slices.column(head,datatype=datatype))


            


