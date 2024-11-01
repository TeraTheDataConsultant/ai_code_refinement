from core.utils.logs import logger
from core.clients.config import config


class Assistants:
    """
    Assistant Class
    ---------------

    Creates and deletes new assistant resources from the Open AI API.

    Usage::

        >>> env = "staging"
        >>> assistant_name = f"{env}__assistant_resource"
        >>> assistants = Assistants(env=env, assistant_name=assistant_name)
        >>> assistants.create_new()

    """

    assistant_id = None  # Class attribute to store id across instances

    def __init__(self, env=None, assistant_name=None):
        self.env = env
        self.assistant_name = assistant_name
        self.cfg = config(env=env)
        self.client = self.cfg.openai_client
        self.assistant_id = Assistants.assistant_id

    def get_assistants(self):
        """
        List all created assistants for the environment
        """

        return self.client.beta.assistants.list()
    
    def get_assistant(self, assistant_id):
        """
        Get a assistant object by it's ID
        """

        return self.client.beta.assistants.retrieve(assistant_id)

    def update_assistant(self, assistant_id, **kwargs):
        """
        Update an assistant's details. This is the entry-point for passing vector_store_id later 
        to tool resources.
        
        Args:
            assistant_id (str): The ID of the assistant to update.
            **kwargs: Arbitrary keyword arguments representing fields to update.
        
        Example:
            update_assistant(assistant_id="123", assistant_name="New Name", instructions="New Instructions")
        """

        logger.info(f"Updating {assistant_id}")
        return self.client.beta.assistants.update(assistant_id=assistant_id, **kwargs)

    def create_assistant(self):
        """
        Create New GPT Assistant
        ------------------------
        If assistant already exists, returns the assistant ID
        If the assistant doesn't already exist, create new one

        All assistants come preconfigured with the following settings:
        + assistant_name
        + file_search enabled
        + temperature set to 0.1
        + gpt model 4o mini

        Returns
        -------
            assistant.id: assistant_id
        ---
        """
        assistants = self.get_assistants()

        for a in assistants.data:
            if a.name == self.assistant_name:
                logger.info(f"Assistant already exists: {self.assistant_name}")
                self.assistant_id = a.id  # Set class attr
                Assistants.assistant_id = a.id 
                return a

        assistant = self.client.beta.assistants.create(
            name=self.assistant_name,
            temperature=0.1,
            model="gpt-4o-mini",
            tools=[
                {"type": "file_search"},
            ],
        )
        logger.info(f"created {self.assistant_name}")
        self.assistant_id = assistant.id  # Set class attr
        Assistants.assistant_id
        return assistant  # Return assistant object


if __name__ == "__main__":
    Assistants()

    # import rich

    # assistants = Assistants()
    # response = assistants.get_assistants()

    # assistant_data = response.data[0]
    # assistant_id = assistant_data.id 
    # current_name = assistant_data.name 

    # rich.print(f"Assistant Check: {assistant_id}, {current_name}")

    # assistants.update(assistant_id=assistant_id, name="staging__assistant_resource")