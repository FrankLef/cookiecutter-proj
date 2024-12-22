class FileNamer:
    
    def __init__(self, ext: str = ".xlsx", sep: str = "_"):
        self._ext = ext
        self._sep = sep
    
    def fname(self, name: str, *suffix):
        if not name:
            raise ValueError("The name of the file is empty.")
        a_join = (name,) + suffix
        fn = self._sep.join(a_join) + self._ext
        return fn
