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
        self.github_token = self.__get_github_token()
        self.gmail_app_username = self.__get_gmail_app_username()
        self.gmail_app_password = self.__get_gmail_app_password()
        
        self.organization_id = self.__get_open_ai_organization_id()
        self.project_id = self.__get_open_ai_project_id()
        self.api_key = self.__get_open_ai_api_key()

        # Clients
        self.openai_client = OpenAI(
            organization=self.organization_id,
            project=self.project_id,
            api_key=self.api_key,
        )

    def __get_github_token(self):
        """
        Get the github token
        """
        return os.getenv("github_token")
    
    def __get_gmail_app_username(self):
        """
        Email username corresponds to the full email/gmail account
        """
        return os.getenv("gmail_app_username")

    def __get_gmail_app_password(self):
        """
        Gets the user defined gmail app specific password 
        api key
        """

        return os.getenv("gmail_app_password")

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