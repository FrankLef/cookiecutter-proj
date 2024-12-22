class FileNamer:
    def fname(self, name: str, *suffix, ext: str = ".xlsx", sep: str = "_"):
        if not name:
            raise ValueError("The name of the file is empty.")
        a_join = (name,) + suffix
        fn = sep.join(a_join) + ext
        return fn
