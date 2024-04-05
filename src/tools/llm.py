import os
from langchain_community.chat_models import ChatOllama
from dotenv import load_dotenv
load_dotenv('.env')

def get_default_llm_model(temperature=0.5, stop_sequences=[]):
    return ChatOllama(
        base_url=os.environ['LLM_API'],
        model=os.environ['MODEL'],
        temperature=temperature,
        stop=stop_sequences
    )