import os
from langchain_community.llms.huggingface_text_gen_inference import HuggingFaceTextGenInference
from dotenv import load_dotenv
load_dotenv('.env')

def get_default_llm_model(temperature=0.5, stop_sequences=[]):
    return HuggingFaceTextGenInference(
        inference_server_url=os.environ['LLM_API'],
        temperature=temperature,
        stop_sequences=stop_sequences
    )