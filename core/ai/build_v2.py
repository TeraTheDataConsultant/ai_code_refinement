import rich
from core.utils.logs import logger
from core.clients.config import config
from core.files.file_management import FileManagement


class Build: 

    def __init__(self, assistant_name, assistant_description, assistant_instructions, dir, env):
        self.assistant_name = f"assistant_resource_{assistant_name}"
        self.vector_name = f"vector_store_{self.assistant_name}"

        self.assistant_description = assistant_description
        self.assistant_instructions = assistant_instructions
        self.assistant_id = None 
        self.vector_id = None 
        self.file_ids = None 

        self.dir = dir
        self.env = env
        self.cfg = config(env=self.env)
        self.client = self.cfg.openai_client

    def create_assistant(self):
        # 1. Creates a new assistant

        new_assistant = self.client.beta.assistants.create(
            name=f'assistant_resource_{self.assistant_name}',
            description=self.assistant_description, 
            instructions=self.assistant_instructions, 
            
            # Presets: 
            model="gpt-4o-mini", 
            temperature=0.1,  # For more consistent results
            tools=[
                    {"type": "file_search"},
                    {"type": "code_interpreter"},
            ]
        )
        self.assistant_id = new_assistant.id
        logger.info(f"New assistant created named assistant_resource_{self.assistant_name} & {self.assistant_id}")

    def create_vector(self): 
        # 2. Creates a new vector object

        new_vector = self.client.beta.vector_stores.create(
            name=f'vector_store_{self.assistant_name}' 
        )
        self.vector_id = new_vector.id 
        logger.info(f"New vector created named vector_store_{self.assistant_name} & {self.vector_id}")

    def upload_files(self, dir, vector_id): 
        # 3. Uploads files to general storage
        
        fm = FileManagement(env='staging', root_directory=dir)
        fm.upload_files_io(in_memory=True)
        fm.get_uploaded_files()

        logger.info(f"Attaching {len(fm.file_ids)} files to {vector_id}")

        for file_id in fm.file_ids: 
            self.client.beta.vector_stores.files.create(
                vector_store_id=vector_id, 
                file_id=file_id
            )
        logger.info("Files successfully attached")
            
    def new_assistant_resource(self): 
        """
        Tying it all together the new_assistant_resource method 
        first checks if either assistant_id or vector_id has a string assignment
        """
        
        # TODO: Refactor this so that it first checks to see if an assistant and vector 
        # exist. If they do, just pass the assistant_id and vector_id to the file upload 
        
        # assistants = self.client.beta.assistants.list()
        # for a in assistants.data:
        #     if a.name == self.assistant_name:
        #         self.assistant_id = a.id
        #         logger.info(f"assistant exists: {self.assistant_name} * {self.assistant_id}")

        if self.assistant_id is None and self.vector_id is None:             
            self.create_assistant()
            self.create_vector()

        # Updates the new assistant to reference the new vector with files attached
        self.client.beta.assistants.update(
            assistant_id=self.assistant_id, 
            tool_resources={
                "file_search": {"vector_store_ids": [self.vector_id]}
            }
        )

        # Updates vector to reference any newly uploaded files 
        # if self.file_ids is None: 
        #     self.upload_files(dir=self.dir, vector_id=self.vector_id)


if __name__ == "__main__": 

    # Pass environment and user input data to build 
    
    env = 'staging'

    build = Build(
        assistant_name='format_text_assistant', 
        assistant_description='Process uploaded data that was captured via an audio transcript.',
        assistant_instructions=(
            'fix any grammar related issues'
            'streamline the text, look for patterns and summarize'
            'if a user requests a templatized output, reference uploaded files prefixed template_'
        ), 
        dir=dir, 
        env=env
    )

    # build.new_assistant_resource()

    # dir = '/Users/teraearlywine/Engineering/AI/audio/mnt/transcripts'
    # dir = '/Users/teraearlywine/Engineering/AI/audio/mnt/templates'
    vector_id = build.vector_id

    # Upload transcript files to assistant
    if build.file_ids is None: 
        build.upload_files(dir=dir, vector_id="vs_d18uzfWihHpwjsjKzTAerZTa")