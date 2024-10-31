import rich
from openai import OpenAI
from core.utils.logs import logger
from core.clients.config import config


class CleanUp: 
    """
    Deletes either all vectors or all files depending on the environment. 
    Use with caution, this class just helps development proliferation
    """
    def __init__(self, env):
        self.env = env
        self.cfg = config(env=self.env)
        self.client = self.cfg.openai_client

    def delete_all_files(self):

        files = self.client.files.list()
        for file in files:
            file_id = file.id
            try:
                self.client.files.delete(file_id=file_id)
                logger.info(f"Deleted {file_id}")
            except Exception as err: 
                logger.error(f"Issue deleting {file_id} -- see {err}")

    def delete_all_vectors(self):

        vectors = self.client.beta.vector_stores.list()

        for vector in vectors: 
            vector_id = vector.id 
            try: 
                self.client.beta.vector_stores.delete(vector_store_id=vector_id)
                logger.info(f"Deleted {vector_id}")
            except Exception as err: 
                logger.error(f"Issue deleting {vector_id} -- see {err}")


if __name__ == "__main__":
    
    CleanUp()