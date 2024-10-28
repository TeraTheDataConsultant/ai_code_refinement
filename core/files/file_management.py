"""
File Management Class
---------------------
TODO: map allowed ext + mime_types, refactor as KV pair

This script automatically handles searching a local directory, reading the files as bytes into memory
and uploading in chunks to OpenAIs' file storage feature. 

This class / this process is important to influencing the assistant's biases (files = context),
fine tuning assistants or even just capturing user data. 
"""

import rich
import os 
from core.clients.config import config
from core.utils.logs import logger
from core.files.file_upload import FileUpload


class FileManagement: 
    """
    File Management
    ---------------

    This class starts at a given root directory for a codebase or project and manages file processing. 
    The hard coded allowed extensions focus on projects relating to python programming. 
    The directories the methods ignore are also hard coded, a future improvement could involve storing 
    these in a constants file for easier management
    """
    def __init__(self, env, root_directory):
        self.env = env
        self.root_directory = root_directory
        self.cfg = config(env=self.env)
        self.client = self.cfg.openai_client

        self.allowed_ext = (
            '.py', 
            '.md', 
            '.txt', 
        )
        self.file_ids = []  # Set in upload_files_io method

    def get_files(self, ignore_dirs=None):
        """
        Get Files 
        ---------

        Recursively walk through a directory and return full file paths in a list of files. 

        Usage::

            >>> root_directory = '.'
            >>> fm = FileManagement(root_directory=root_directory)
            >>> file_paths = fm.get_files()
            >>> print(file_paths)
        ---
        """

        if ignore_dirs is None:
            ignore_dirs = {'.venv', '.git', '__pycache__', 'pytest', 'node_modules'}
            logger.debug(f"Bypassed {ignore_dirs}")

        file_paths = []
        for dirpath, dirnames, filenames in os.walk(self.root_directory):
            dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
            for file in filenames:
                if file.endswith(self.allowed_ext) and file != "__init__.py" and file != '[]':
                    full_path = os.path.join(dirpath, file)
                    file_paths.append(full_path)

        logger.info(f"{len(file_paths)} files ready to process")
        return file_paths

    def read_io(self, file, in_memory: bool = False):
        """
        Read IO

        Using python builtin, reads the object into a python serialized file 
        for iteration

        Usage::

            fm = FileManagement('.')
            files = fm.get_files()

            for file in files: 
                fm.read_io(file, in_memory=True)

        """

        if in_memory: 
            with open(file, 'rb') as f: 
                logger.info(f"{file} is {len(file)} bytes")
                return f.read()
        else:
            logger.info(f"{file} is {len(file)} bytes")
            return file

    def write_io(self, file, data, in_memory: bool = False):
        """
        Write IO

        Using Python's built-in functions, writes data to the specified file. Can write in binary mode or text mode
        based on the `in_memory` flag.

        Usage::

            fm = FileManagement('.')
            files = fm.get_files()

            for file in files: 
                data = fm.read_io(file, in_memory=True)
                fm.write_io('output_file', data, in_memory=True)

        Parameters:
        - file: The path to the file where data should be written.
        - data: The data to write to the file.
        - in_memory: If True, write in binary mode; otherwise, write in text mode.
        ---
        """

        if in_memory:
            # Write in binary mode
            with open(file, 'wb') as f:
                logger.debug(f"Writing binary data to {file}, {len(data)} bytes")
                return f.write(data)
        else:
            # Write in text mode
            with open(file, 'w') as f:
                logger.debug(f"Writing text data to {file}, {len(data)} characters")
                return f.write(data)

    def upload_files_io(self, in_memory: bool = False):
        """
        Upload Files IO
        ----------------

        Upload Files to Open AI in Memory.
        Currently only supports python files, in the future this should map the allowed extensions to the mime type

        Usage::

            >>> env = 'staging'
            >>> root_directory = './front_end'
            >>> fm = FileManagement(env=env, root_directory=root_directory)
            >>> fm.upload_files_io(in_memory=True)

        ---
        """

        try: 
            if in_memory:
                files = self.get_files()
                for file in files: 
                    if file.endswith('.txt') and file != '__init__.py':  # Only upload python files for the time being
                        data = self.read_io(file=file, in_memory=in_memory)
                        fu = FileUpload(env=self.env)
                        fu.upload(
                            file_name=file,
                            data=data, 
                            mime_type='text/plain', 
                            # mime_type='application/msword',
                            purpose='assistants'
                        )
            else: 
                logger.info("In Memory is set to False, try again!")
        except Exception as err: 
            logger.error(f"Issue uploading files, see error {err}")

    def get_uploaded_files(self):
        """
        Get Uploaded Files
        ------------------

        Makes API request, gets a list of all uploaded files.
        This would also be a good place to log records to a table for later 
        retrieval.
        
        Usage::

            env = 'staging'
            root_directory = './core'
            fm = FileManagement(env=env, root_directory=root_directory)
            files = fm.get_uploaded_files()
            rich.print(fm.file_ids)
        ---
        """

        files = self.client.files.list()
        for file in files: 
            self.file_ids.append(file.id)  # Appends the id to the file_ids attr
        logger.info(f"There are currently {len(self.file_ids)} total files uploaded to {self.env}")
        return files
    

if __name__ == "__main__":

    FileManagement()