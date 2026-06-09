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
    last_error = None

    for attempt in range(1, max_retries + 1):
        if attempt == 1:
            prompt = f"Analyze this customer review:\n{review}"
        else:
            prompt = (
                f"Analyze this customer review:\n{review}\n\n"
                "Return output that strictly matches these rules:\n"
                "- rating must be an integer between 1 and 5 inclusive.\n"
                "- sentiment must be exactly one of: positive, negative, neutral, mixed.\n"
                "- summary must be 200 characters or fewer.\n"
                "- key_points must contain between 2 and 5 items."
            )

        try:
            result = await agent.run(prompt)
            return result.output
        except ValidationError as error:
            last_error = error
            print(f"Attempt {attempt} failed validation: {error}")

    if last_error is not None:
        raise last_error

    raise RuntimeError("analyze_with_retry reached an unexpected state")


if __name__ == "__main__":
    review = (
        "The headphones sound clear and balanced, and they are very comfortable for long "
        "calls. Battery life has been excellent so far. On the downside, the app feels "
        "buggy and the touch controls sometimes miss taps."
    )

    analysis = asyncio.run(analyze_with_retry(review))

    print(f"Rating: {analysis.rating}/5")
    print(f"Sentiment: {analysis.sentiment}")
    print(f"Summary: {analysis.summary}")
    print("Key Points:")
    for point in analysis.key_points:
        print(f"- {point}")
