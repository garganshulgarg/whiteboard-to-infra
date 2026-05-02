import os

# Standard Bedrock Claude 4.5 Sonnet model ID - great for vision and coding tasks
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-sonnet-4-5-20250929-v1:0")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")