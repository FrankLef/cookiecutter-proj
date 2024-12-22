class FileNamer:
    
    def __init__(self, name: str):
        if not name:
            raise ValueError("The name of the file is empty.")
        self._name = name
    
    def fname(self, *suffix, ext: str = ".xlsx", sep: str = "_"):
        a_join = (self._name,) + suffix
        fn = sep.join(a_join) + ext
        return fn
        
    