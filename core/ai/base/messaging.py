from core.utils.logs import logger
from core.clients.config import config


class Messaging:
    """
    Messaging Class
    ---------------

    Manages sending and receiving data from the user & assistant
    """

    def __init__(self, env=None, content=None, assistant_id=None):
        self.env = env
        self.content = content
        self.assistant_id = assistant_id
        self.thread_id = None
        self.cfg = config(env=env)
        self.client = self.cfg.openai_client

    def create_thread(self):

        thread = self.client.beta.threads.create()  # Create new empty thread obj
        # self.thread_id = thread.id  # Store in class variable
        logger.info(f"Created thread: {thread.id}")
        return thread 
    
    def update_message(self, thread_id, message_id, **kwargs):
        """
        Update a message instance for a user
        """

        return self.client.beta.threads.messages.update(
            thread_id=thread_id, 
            message_id=message_id,
            **kwargs
        )

    def send_user_message(self, thread_id):
        """
        Send User Message 
        -----------------

        Method to process the content via class attribute.
        Sends to the initialized thread
        """
        
        thread_message = self.client.beta.threads.messages.create(
            thread_id=thread_id,  # Send message to new thread
            role="user",
            content=self.content,
        )
        logger.info(f"Sending user message to {thread_message.id}")
        return thread_message
        
    def get_assistant_response(self, thread_id):
        """
        Get Assistant Response
        ----------------------

        Technically the "main" function of the app persists in 
        get_assistant_response() method. This a) triggers the user message and
        b) processes a run and returns the text data 
        """

        self.send_user_message(thread_id=thread_id)
        self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
            # max_completion_tokens=256,
            # max_prompt_tokens=256  # Dev minimum is 256
        )

        logger.info("Run completed successfully. Retrieving assistant's messages...")

        try:
            messages = self.client.beta.threads.messages.list(thread_id=thread_id)
            if messages.data:
                # Find the last assistant message
                for message in reversed(messages.data):
                    if message.role == 'assistant':
                        assistant_message = message.content[0].text.value
                        return assistant_message
                logger.warning("No assistant message found in the thread.")
        except Exception as err: 
            logger.error(f"Unforseen issue, PTAL: {err}")
            return False


if __name__ == "__main__":
    Messaging()