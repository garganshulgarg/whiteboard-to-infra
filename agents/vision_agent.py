from strands import Agent
from strands.models import BedrockModel
from core.config import MODEL_ID

def get_vision_agent():
    model = BedrockModel(model_id=MODEL_ID)
    system_prompt = """You are an expert Cloud Architect Vision AI.
    Your job is to analyze uploaded architecture diagrams or whiteboard sketches.
    Extract the AWS topology and output it strictly as a JSON list of dictionaries.
    Each dictionary should represent a resource and its connections.
    Example: [{"resource": "API Gateway", "connects_to": ["Lambda Function"]}, {"resource": "Lambda Function", "connects_to": ["DynamoDB"]}]
    Do not output any other text or markdown formatting, just the raw JSON."""
    
    return Agent(model=model, system_prompt=system_prompt)