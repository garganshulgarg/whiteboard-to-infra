import os

# Standard Bedrock Claude 3 Sonnet model ID - great for vision and coding tasks
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")