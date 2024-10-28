from core.utils import constants
from core.utils.logs import logger
from core.utils.errors import error_handler
from core.clients.config import config
import os


class Refinement:
    """
    Refinement
    -----------
    Reads file contents as python object.
    Defaults to the current file if no path is provided.
    """
    def __init__(self, env, file_path=None):
        self.env = env
        self.file_path = file_path or __file__
        self.cfg = config(env=self.env)
        self.client = self.cfg.openai_client

        self.description = constants.DESCRIPTION
        self.instructions = constants.INSTRUCTIONS

    @error_handler
    def read(self):
        """
        Read
        ----
        Reads file path or current file contents.
        """

        with open(self.file_path, 'r') as file:
            file_contents = file.read()
        logger.info(f"Read {len(file_contents)} bytes from {self.file_path}")
        return file_contents
    
    @error_handler
    def write(self, data):
        """
        Write
        -----
        Rewrites content to the same file.
        """

        with open(self.file_path, 'a', encoding='utf-8') as file:
            file.write(data)
        logger.info(f"Wrote data to {self.file_path}")

    @error_handler
    def refine(self):
        """
        Refine
        ------
        Passes file content to chat completion. If file-path is not passed
        as a parameter, it uses the current file.
        """
        
        original_content = self.read()

        if original_content is not None:
            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.1,
                messages=[
                    {"role": "system", "content": self.description},
                    {"role": "system", "content": self.instructions},
                    {"role": "user", "content": original_content}
                ], 
                stream=True
            )
            # refined_content = completion.choices[0].message.content
            # self.write(data=refined_content)
            
            for chunk in completion: 
                refined_content = chunk.choices[0].delta.content
                if refined_content is not None: 
                    self.write(data=refined_content)
                else: 
                    logger.info("Moving on -- no content found")


if __name__ == "__main__":
    
    Refinement()
    
    # env = "staging"
    # file_path = "/Users/teraearlywine/Engineering/Consulting/auto_code/core/cli/cli.py"
    # cf = Refinement(env=env, file_path=file_path)
    # cf.refine()