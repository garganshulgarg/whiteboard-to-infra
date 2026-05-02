import os
from strands import Agent, tool
from strands.models import BedrockModel
from core.config import MODEL_ID
from core.logger import logger

@tool
def save_tf_code(code: str, filename: str) -> str:
    """Saves a single Terraform file to the output directory.
    
    Call this tool once per file. Expected filenames:
    - providers.tf  (terraform block, required_providers, provider config)
    - variables.tf  (all variable declarations)
    - main.tf       (all resource blocks)
    - outputs.tf    (all output blocks)
    """
    allowed = {"providers.tf", "variables.tf", "main.tf", "outputs.tf"}
    if filename not in allowed:
        return f"Error: filename must be one of {sorted(allowed)}, got '{filename}'."

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

    Split the code across exactly four files and call `save_tf_code` once for each:
    1. providers.tf  — terraform block (required_version, required_providers) and provider configuration
    2. variables.tf  — all variable declarations with descriptions and defaults
    3. main.tf       — all resource and data source blocks
    4. outputs.tf    — all output blocks

    Do NOT merge content across files. Call the tool four times, one per file.
    Output a brief, professional summary of the resources you provisioned."""
    
    return Agent(
        model=model,
        system_prompt=system_prompt,
        tools=[save_tf_code]
    )