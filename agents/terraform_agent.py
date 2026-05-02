import os
from strands import Agent, tool
from strands.models import BedrockModel
from core.config import MODEL_ID
from core.logger import logger

@tool
def save_tf_code(code: str, filename: str = "main.tf") -> str:
    """Saves the generated Terraform code to a local output directory."""
    output_dir = "output_infra"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w") as f:
        f.write(code)
    
    logger.info(f"Success: Terraform code saved to {filepath}")
    return f"File saved successfully to {filepath}."

def get_terraform_agent():
    model = BedrockModel(model_id=MODEL_ID)
    system_prompt = """You are an expert Platform Engineer.
    Take the provided AWS topology JSON and write production-grade, secure Terraform code.
    Ensure you use AWS best practices like least privilege IAM roles.
    Once the code is generated, you MUST use the `save_tf_code` tool to save it to a file named 'main.tf'.
    Output a brief, professional summary of the resources you provisioned."""
    
    return Agent(
        model=model,
        system_prompt=system_prompt,
        tools=[save_tf_code]
    )