class slices:
    class primary_keys:
        def __init__(self,head,lis=[],datatype=str) -> None:
            self.head =head
            self.vals = lis
            self.datatype = datatype
    class foreign_keys:
        def __init__(self,lis=[],reference_table_name=None,datatype=str) -> None:
            self.vals = lis
            self.datatype = datatype
            self.reference = reference_table_name
    class column:
        def __init__(self,lis=[],datatype=str) -> None:
            self.vals = lis
            self.datatype = datatype



class StrawBerry:
    def __init__(self,data:dict,schema:dict):
        self.PRIMARY_KEY = schema['PRIMARY_KEY']
        self.FOREIGN_KEY = schema['FOREIGN_KEY']
        self.rows = []
        for i in (schema['slices']).keys():
            if i == self.PRIMARY_KEY:
                self.rows.append(slices.primary_keys(i,datatype=schema['slices'][i]))
            if i in schema['slices']:
                self.rows.append(slices.foreign_keys(i,datatype=schema['slices'][i]))
            else:
                self.rows.append(slices.column)
        for i in self.data:
            pass
            


