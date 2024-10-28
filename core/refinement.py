from core.utils.logs import logger
from core.clients.config import config
import os


class Refinement: 
    """
    Refinement 
    -----------


    Reads file contents as python object. 
    Defaults to the current file if no path is provided
    """
    def __init__(self, env, file_path=None): 
        self.env = env
        self.file_path = file_path or __file__  
        self.cfg = config(env=self.env)
        self.client = self.cfg.openai_client

        # TODO: these are hardcoded, replace with assistant 
        # TODO: shore these up to be more specific to coding lines? 
        self.description = "Generalized programming assistant bot for generation and optimization bot. Just write code"
        self.instructions = (
            "No chat response needed, just respond with the code. No backticks needed"
            "Focus on instruction following TODO: or FIX:"
            "If none provided, just write comments at the end of doc to improve code"
            "Implement using software engineering development best practices."
            "Include new features or libraries that would improve functionality."
            "Add assertions and logging where necessary."

        )

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

    def write(self, data): 
        """
        Write
        -----

        Rewrites content to same file
        """

        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write(data)
            logger.info("Wrote file content to current file")
        except FileNotFoundError:
            return False
            logger.info(f"File {self.file_path} not found.")
        except Exception as e:
            logger.info(f"An error occurred: {e}")
            return False

    def refine(self): 
        """ 
        Refine
        ------

        Passes file content to chat completion. If file-path is not passed 
        as a parameter, it uses the current file
        """

        original_content = self.read()
        if original_content is not None:

            completion = self.client.chat.completions.create(
                model="chatgpt-4o-latest",
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
    # cf = CurrentFile(env=env)
    # cf.refine()