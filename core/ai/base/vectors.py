from core.utils.logs import logger
from core.clients.config import config


class Vectors:
    """
    Vectors
    -------------

    Creates a vector store to upload files too, 
    will later be integrated with assistants and threads 
    """

    vector_id = None 

    def __init__(self, env=None, vector_name=None):
        self.env = env
        self.vector_name = vector_name
        self.cfg = config(env=env)
        self.client = self.cfg.openai_client
        self.vector_id = Vectors.vector_id

    def get_vectors(self):
        """
        Get all vector store(s)
        """
        return self.client.beta.vector_stores.list()

    def get_vector(self, vector_id): 
        """
        Gets a single vector store resource
        """

        return self.client.beta.vector_stores.retrieve(vector_id)
    
    def update_vector(self, vector_id, **kwargs):
        """
        Updates vector store after passing keyword arguments 
        """

        return self.client.beta.vector_stores.update(vector_id, **kwargs)

    def create_vector(self):
        """
        Create New
        ----------

        Check to see if vector store exists, if not
        create a new vector store using the provided name.

        Usage::

            >>> env='staging'
            >>> vector_name=f"{env}_vector_resource"
            >>> vs = Vectors(env, vector_name=vector_name)
            >>> vs.create_new()
        ----
        """

        vectors = self.get_vectors()
        for vs in vectors.data:
            if vs.name == self.vector_name:
                logger.info(f"Vector store exists: {vs.name}")
                self.vector_id = vs.id
                Vectors.vector_id = vs.id
                return vs

        logger.info(f"Vector store doesn't exist, creating vector store: {self.vector_name}")
        vector = self.client.beta.vector_stores.create(name=self.vector_name)
        self.vector_id = vector.id
        Vectors.vector_id = vector.id
        return vector
    

if __name__ == "__main__":
    Vectors()
