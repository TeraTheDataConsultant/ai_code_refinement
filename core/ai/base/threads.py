from core.utils.logs import logger
from core.clients.config import config


class Threads:
    # (2024-10-08 TE NOTE): replace with a database model for assistant_id/thread_id mapping
    # file to store the thread_id

    thread_id = None  # Class attribute to store thread_id across instances

    def __init__(self, env=None):
        self.env = env
        self.cfg = config(env=env)
        self.client = self.cfg.openai_client
        self.thread_id = Threads.thread_id
    
    def delete_thread(self, thread_id):
        """
        Deletes a thread
        """

        if not thread_id:
            logger.info("No thread to delete.")
            return None
        
        self.client.beta.threads.delete(thread_id)
        logger.info(f"Thread with id {thread_id} has been deleted.")
        self.thread_id = None  # Reset class variable
        Threads.thread_id = None  # Reset the class attribute as well

    def update_thread(self, thread_id, **kwargs):
        """
        Modifys a thread resource. 
        Used for mapping vector / file / assistant to the newly minted thread later on.
        """

        logger.info(f"Updating {thread_id}")
        updated_thread = self.client.beta.threads.update(thread_id, **kwargs)
        self.thread_id = updated_thread.id 
        Threads.thread_id = updated_thread.id
        return updated_thread


if __name__ == "__main__":
    Threads()
