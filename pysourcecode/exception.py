class db_read_error(Exception):
    def __init__(self, msg):
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

