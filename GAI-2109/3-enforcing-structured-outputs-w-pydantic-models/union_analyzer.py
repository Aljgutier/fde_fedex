import os
from typing import Union
from pydantic_ai import Agent
from dotenv import load_dotenv
from models import ProductReviewAnalysis, ServiceAnalysis

load_dotenv()

# Verify API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found in environment variables. "
        "Make sure .env file exists in the same directory as this script."
    )

# Get model from environment variable
model = os.getenv("AI_MODEL", "openai:gpt-5.4-mini")
print(f"Using model: {model}")

# Agent supporting multiple output types
agent = Agent(
    model,
    output_type=Union[ProductReviewAnalysis, ServiceAnalysis],
    system_prompt="""Analyze customer feedback.
    - For product reviews, use ProductReviewAnalysis format
    - For service reviews, use ServiceAnalysis format
    Choose the appropriate format based on the review content.""",
)

if __name__ == "__main__":
    # YOUR CODE HERE
    pass
