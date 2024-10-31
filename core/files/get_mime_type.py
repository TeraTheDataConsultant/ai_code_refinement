import mimetypes
import os
from core.utils.logs import logger


class GetMimeType:
    """
    Get Mime Type 
    -------------

    Makes a call to the builtin mimetypes library, if a file is a certain type 
    sets the class attribute mime_type to that string, otherwise returns the mime type 
    unknown response: 'application/octet-stream'. 

    This is important for uploading files to the OpenAI api, 
    the mime_type is required for a given file_path, this streamlines the process 
    when batch uploading something
    
    Attributes
    ----------
        + env: str - pass the environment (i.e. staging) configuration to use 
        + file_path: str - full filepath or relative filepath to make the mime type inference from 

    Usage::

        >>> try:
        >>>     file_path = input("Enter the file path: ")
        >>>     gmt = GetMimeType(env='staging', file_path=file_path)
        >>>     print(f"The MIME type of the file is: {gmt.mime_type}")
        >>> except Exception as e:
        >>>     logger.error(f"An error occurred: {e}")
    
    ---
    """

    def __init__(self, env, file_path):
        self.env = env
        self.file_path = file_path 

        if not os.path.isfile(self.file_path): 
            logger.error(f"File not found: {self.file_path}")

        self.mime_type, _ = mimetypes.guess_type(self.file_path)

        if self.mime_type is None:
            logger.warning(f"Could not determine MIME type for: {self.file_path}")
            self.mime_type = 'application/octet-stream'  


if __name__ == "__main__":

    GetMimeType()

# TODO: Add unit tests for get_mime_type function.
# TODO: Consider adding support for URLs or remote files.