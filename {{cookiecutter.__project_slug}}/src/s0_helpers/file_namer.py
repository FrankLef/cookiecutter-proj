class FileNamer:
    """Write a file name to a string.
    """
    
    def __init__(self, ext: str = ".xlsx", sep: str = "_"):
        """Create a file namer.

        Args:
            ext (str, optional): File extension, mustinclude the dot. Defaults to ".xlsx".
            sep (str, optional): Separator. Defaults to "_".
        """
        self._ext = ext
        self._sep = sep
    
    def fname(self, name: str, *suffix) -> str:
        """Create a file name.

        Args:
            name (str): Base name for the file.

        Raises:
            ValueError: The base file name is empty.

        Returns:
            str: File name.
        """
        if not name:
            raise ValueError("The name of the file is empty.")
        a_join = (name,) + suffix
        fn = self._sep.join(a_join) + self._ext
        return fn
