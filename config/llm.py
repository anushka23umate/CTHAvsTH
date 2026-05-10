import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_groq import ChatGroq

load_dotenv()

def get_llm():
    """
    Returns a default ChatModel.
    """
    grok_api_key = os.getenv("GROK_API_KEY")
    if not grok_api_key:
        raise ValueError("GROK_API_KEY is missing from environment variables.")
        
    return ChatGroq(
        model_name="openai/gpt-oss-120b", 
        api_key=grok_api_key,
        temperature=0.1,
        max_tokens=4096
    )

def get_layer_llm(layer_name: str):
    """
    Returns an LLM configured specifically for the requested layer based on CTHA parameters.
    """
    grok_api_key = os.getenv("GROK_API_KEY")
    if not grok_api_key:
        raise ValueError("GROK_API_KEY is missing from environment variables.")
        
    # Mapping the exact models from the research paper (Table 8/9)
    configs = {
        "institutional": {"temp": 0.7, "max_tokens": 2048, "model_str": "deepseek-v3.2-speciale"},
        "strategic": {"temp": 0.5, "max_tokens": 1024, "model_str": "kimi-k2"},
        "tactical": {"temp": 0.3, "max_tokens": 512, "model_str": "qwen3-32b"},
        "reflex": {"temp": 0.1, "max_tokens": 256, "model_str": "glm-4.6-9b"}
    }
    
    config = configs.get(layer_name.lower(), {"temp": 0.1, "max_tokens": 4096, "model_str": "openai/gpt-oss-120b"})
    
    print(f"   > [INFRA] LLM Configuration: {layer_name.capitalize()} Layer -> Model: {config['model_str']} | Temp: {config['temp']} | Tokens: {config['max_tokens']}")
    
    # Primary LLM using the theoretical model string from the paper
    primary_llm = ChatGroq(
        model_name=config["model_str"], 
        api_key=grok_api_key,
        temperature=config["temp"],
        max_tokens=config["max_tokens"],
        max_retries=0 # Fail fast to trigger fallback
    )
    
    # Fallback LLM using the functional endpoint
    fallback_llm = ChatGroq(
        model_name="openai/gpt-oss-120b", 
        api_key=grok_api_key,
        temperature=config["temp"],
        max_tokens=config["max_tokens"]
    )
    
    # Use LangChain's native fallback mechanism to handle 404 errors during invoke()
    return primary_llm.with_fallbacks([fallback_llm])