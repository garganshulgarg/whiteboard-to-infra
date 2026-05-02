import argparse
import shutil
import os
from agents.vision_agent import get_vision_agent
from agents.terraform_agent import get_terraform_agent
from core.logger import logger

OUTPUT_DIR = "output_infra"

def cleanup_output_dir():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        logger.info(f"Cleaned up existing '{OUTPUT_DIR}' directory.")

def main(image_path):
    logger.info(f"Starting Whiteboard-to-Infra pipeline for: {image_path}")

    # 0. Cleanup previous output
    cleanup_output_dir()

    # 1. Initialize Agents
    vision_agent = get_vision_agent()
    tf_agent = get_terraform_agent()

    # 2. Vision Phase
    logger.info("Phase 1: Analyzing whiteboard image...")
    
    # Strands takes raw bytes directly, no base64 encoding needed!
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
        
    # Determine the format from the file extension
    ext = image_path.split('.')[-1].lower()
    img_format = "jpeg" if ext in ["jpg", "jpeg"] else ext
    
    # Constructing the multimodal payload using Strands ContentBlock format
    vision_prompt = [
        {
            "text": "Analyze this architecture diagram and output the JSON topology."
        },
        {
            "image": {
                "format": img_format,
                "source": {
                    "bytes": image_bytes
                }
            }
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