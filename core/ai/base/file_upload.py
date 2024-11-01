from core.clients.config import config
from core.utils.logs import logger
from pathlib import Path


class FileUpload:

    def __init__(self, env):
        self.env = env 
        self.cfg = config(env=self.env)
        self.client = self.cfg.openai_client
        self.in_memory = False

    def upload(self, file_name, data, **kwargs):
        """ 
        Upload Method 
        -------------
        Uploads one file to the open ai file storage client

        For in memory uploads the following fields are required: 

        + filename=data
        + bytes=len(data)
        + mime_type=mime_type 
        + purpose=purpose 

        For non in-memory uploads, all that's needed is the full 
        path for the file, the mime_type and purpose. 
        """
        
        bytes = len(data)
        try: 
            upload = self.client.uploads.upload_file_chunked(
                file=data,
                filename=file_name,
                bytes=int(bytes),
                **kwargs
            )
            return upload 
        except Exception as error: 
            logger.error(f"Error uploading file: {error}")
            return None 


if __name__ == "__main__":
    
    FileUpload()

    # EXAMPLE USAGE: 
    # Non in-memory file uploads:
    
    # file_upload = FileUpload(env='staging')
    # file_upload.upload(
    #     data='path',
    #     mime_type='text/markdown', 
    #     purpose='assistants'
    # )