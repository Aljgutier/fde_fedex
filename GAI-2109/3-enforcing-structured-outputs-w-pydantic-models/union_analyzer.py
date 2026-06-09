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
    product_review = (
        "This blender is powerful and easy to clean, and smoothies come out very smooth. "
        "The lid feels a little flimsy, but overall it has been a great kitchen upgrade."
    )
    service_review = (
        "The salon staff were welcoming and attentive, and my appointment started on time. "
        "The haircut was good, though checkout took longer than expected."
    )

    product_result = agent.run_sync(f"Analyze this review:\n{product_review}")
    service_result = agent.run_sync(f"Analyze this review:\n{service_review}")

    print(f"Product Result Type: {type(product_result.output).__name__}")
    print(f"Product Rating: {product_result.output.rating}/5")
    print(f"Product Sentiment: {product_result.output.sentiment}")

    print(f"Service Result Type: {type(service_result.output).__name__}")
    print(f"Service Rating: {service_result.output.rating}/5")
    print(f"Service Sentiment: {service_result.output.sentiment}")

    if isinstance(service_result.output, ServiceAnalysis):
        print(f"Service Staff Rating: {service_result.output.staff_rating}/5")
        print(f"Service Would Return: {service_result.output.would_return}")
