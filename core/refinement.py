from core.utils.logs import logger
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
        assert isinstance(env, str), "Environment must be a string"
        self.env = env
        self.file_path = file_path or __file__
        self.cfg = config(env=self.env)
        self.client = self.cfg.openai_client

        self.description = "Generalized programming assistant bot for generation and optimization."
        self.instructions = (
            "No chat response needed, just respond with the code. "
            "Focus on instruction following TODO: or FIX: "
            "If none provided, just write comments at the end of doc to improve code. "
            "Implement using software engineering development best practices. "
            "Include new features or libraries that would improve functionality. "
            "Add assertions and logging where necessary."
        )

    def read(self):
        """
        Read
        ----
        Reads file path or current file contents.
        """
        try:
            with open(self.file_path, 'r') as file:
                file_contents = file.read()
            logger.info(f"Read {len(file_contents)} bytes from {self.file_path}")
            return file_contents
        except FileNotFoundError:
            logger.error(f"File {self.file_path} not found.")
            return None
        except Exception as e:
            logger.error(f"An error occurred while reading file: {e}")
            return None

    def write(self, data):
        """
        Write
        -----
        Rewrites content to the same file.
        """

        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write(data)
            logger.info(f"Wrote data to {self.file_path}")
        except FileNotFoundError:
            logger.error(f"File {self.file_path} not found.")
            return False
        except Exception as e:
            logger.error(f"An error occurred while writing to file: {e}")
            return False

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
                model="gpt-4-turbo",
                temperature=0.1,
                messages=[
                    {"role": "system", "content": self.description},
                    {"role": "system", "content": self.instructions},
                    {"role": "user", "content": original_content}
                ]
            )
            refined_content = completion.choices[0].message.content
            self.write(data=refined_content)

if __name__ == "__main__":
    
    Refinement()
    
    # env = "staging"
    # cf = Refinement(env=env)
    # cf.refine()