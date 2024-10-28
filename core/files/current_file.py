from core.utils.logs import logger
import os


class CurrentFile: 
    """
    CurrentFile 
    -----------


    Reads file contents as python object. 
    Defaults to the current file if no path is provided
    """
    def __init__(self, file_path=None): 
        self.file_path = file_path or __file__  

    def read(self): 
        """
        Read
        ----

        Reads file path _or_ current file contents
        """

        try:
            with open(self.file_path, 'r') as file:
                file_contents = file.read()
            return file_contents
            logger.info(f"{len(self.file_path)} bytes")
        except FileNotFoundError:
            return False
            logger.info(f"File {self.file_path} not found.")
        except Exception as e:
            logger.info(f"An error occurred: {e}")
            return False


if __name__ == "__main__":
    cf = CurrentFile()
    file_text = cf.read()
    if file_text:
        # Call the function here that refines or further processes `file_text`
        print(file_text)  # For demonstration, printing the contents