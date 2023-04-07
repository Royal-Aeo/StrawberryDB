class db_read_error(Exception):
    def __init__(self, msg) -> None:
        self.msg = msg
        super().__init__(self.msg)
    class nohull(Exception):
        def __init__(self,msg="hull is not in the database.") -> None:
            self.msg = msg
            super().__init__(self.msg)
    class notag(Exception):
        def __init__(self,msg="The tag is missing.") -> None:
            self.msg = msg
            super().__init__(self.msg)
    


