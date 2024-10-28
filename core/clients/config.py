import os
from dotenv import load_dotenv
from openai import OpenAI


class config:
    """
    Environment set up, loads either staging or production
    for any ETL tools
    """
    def __init__(self, env=None):
        if not env:
            env = os.getenv("ENV", "staging")
        if env == "production":
            load_dotenv(".env.production")
        else:
            load_dotenv(".env.staging")
        self.env = env

        # Keys / Tokens
   
        self.organization_id = self.__get_open_ai_organization_id()
        self.project_id = self.__get_open_ai_project_id()
        self.api_key = self.__get_open_ai_api_key()

        # Clients
        self.openai_client = OpenAI(
            organization=self.organization_id,
            project=self.project_id,
            api_key=self.api_key,
        )

    def __get_open_ai_organization_id(self):
        return os.getenv("open_ai_organization_id")

    def __get_open_ai_project_id(self):
        return os.getenv("open_ai_project_id")

    def __get_open_ai_api_key(self):
        return os.getenv("open_ai_api_key")

    def get_environment(self):
        """
        Checks the environment that's initialized
        """
        return self.env


if __name__ == "__main__":
    config()