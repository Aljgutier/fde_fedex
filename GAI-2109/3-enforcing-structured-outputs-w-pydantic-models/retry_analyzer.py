import os
import asyncio
from pydantic import ValidationError
from pydantic_ai import Agent
from dotenv import load_dotenv
from models import ReviewAnalysis

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

# Agent with structured output
agent = Agent(
    model,
    output_type=ReviewAnalysis,
    system_prompt="""You are a review analysis system.
    Extract structured information from customer reviews.
    Be accurate and objective in your analysis.""",
)


async def analyze_with_retry(review: str, max_retries: int = 3):
    """Analyze review with custom retry logic."""
    # YOUR CODE HERE
    pass
if __name__ == "__main__":
    # YOUR CODE HERE
    pass
