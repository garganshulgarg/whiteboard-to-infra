import base64
import argparse
from agents.vision_agent import get_vision_agent
from agents.terraform_agent import get_terraform_agent
from core.logger import logger

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def main(image_path):
    logger.info(f"Starting Whiteboard-to-Infra pipeline for: {image_path}")
    
    # 1. Initialize Agents
    vision_agent = get_vision_agent()
    tf_agent = get_terraform_agent()

    # 2. Vision Phase
    logger.info("Phase 1: Analyzing whiteboard image...")
    base64_image = encode_image(image_path)
    
    # Constructing the multimodal payload for Claude 3
    vision_prompt = [
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": base64_image
            }
        },
        {
            "type": "text",
            "text": "Analyze this architecture diagram and output the JSON topology."
        }
    ]
    
    topology_json = vision_agent(vision_prompt)
    logger.info("Phase 1 Complete: Topology extracted successfully.")

    # 3. Terraform Builder Phase
    logger.info("Phase 2: Generating Infrastructure as Code...")
    tf_prompt = f"Build Terraform for this topology and save the file: {topology_json}"
    final_result = tf_agent(tf_prompt)
    
    logger.info("Pipeline completed successfully!")
    print("\n" + "="*40)
    print("AGENT EXECUTION SUMMARY")
    print("="*40)
    print(final_result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert whiteboard sketches to Terraform.")
    parser.add_argument("--image", type=str, required=True, help="Path to the whiteboard image (JPEG/PNG).")
    args = parser.parse_args()
    
    main(args.image)