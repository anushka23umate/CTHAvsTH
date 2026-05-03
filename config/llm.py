import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_groq import ChatGroq

load_dotenv()

def get_llm():
    """
    Returns a ChatModel. Switch between HuggingFace and Groq by commenting/uncommenting.
    """
    
    # --- CHOICE 1: HuggingFace (DeepSeek-V4-Pro) ---
    # huggingfacehub_api_token = os.getenv("HUGGINGFACE_API_KEY")
    # if not huggingfacehub_api_token:
    #     raise ValueError("HUGGINGFACE_API_KEY is missing.")
    #
    # llm = HuggingFaceEndpoint(
    #     repo_id="deepseek-ai/DeepSeek-V4-Pro",
    #     huggingfacehub_api_token=huggingfacehub_api_token,
    #     max_new_tokens=4096,
    #     temperature=0.1,
    #     task="text-generation"
    # )
    # return ChatHuggingFace(llm=llm)

    # --- CHOICE 2: Groq / "Grok" (Using DeepSeek-R1) ---
    # This uses the GROK_API_KEY (which is a Groq gsk_... key)
    grok_api_key = os.getenv("GROK_API_KEY")
    if not grok_api_key:
        raise ValueError("GROK_API_KEY is missing from environment variables.")
        
    return ChatGroq(
        model_name="openai/gpt-oss-120b", 
        api_key=grok_api_key,
        temperature=0.1,
        max_tokens=4096
    )