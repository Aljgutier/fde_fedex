import os
from pydantic_ai import Agent
from dotenv import load_dotenv
from models import DetailedReviewAnalysis

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

# Agent with nested structured output
agent = Agent(
    model,
    output_type=DetailedReviewAnalysis,
    system_prompt="""Analyze reviews and extract:
    - Overall rating and sentiment
    - Specific pros and cons
    - Whether product is recommended
    Be thorough and objective.""",
)

if __name__ == "__main__":
    review = (
        "I've been using this coffee maker for three weeks, and the coffee quality is "
        "excellent with rich flavor every morning. Setup was simple, and I like how "
        "compact it is on my countertop. That said, the water tank is smaller than I "
        "expected, so I have to refill it often when guests visit. The machine is also "
        "louder than advertised, especially during the first minute of brewing. Overall, "
        "it's a solid product with great taste and convenience, but the noise and small "
        "reservoir keep it from being perfect."
    )

    result = agent.run_sync(
        "Analyze the following customer review. Identify overall sentiment, a rating, "
        "specific pros and cons, and whether the customer recommends the product.\n\n"
        f"Review:\n{review}"
    )

    analysis = result.output

    print(f"Rating: {analysis.rating}/5")
    print(f"Sentiment: {analysis.sentiment}")
    print(f"Summary: {analysis.summary}")

    for pro in analysis.pros.items:
        print(f"Pro: {pro}")

    for con in analysis.cons.items:
        print(f"Con: {con}")

    print(f"Recommended: {analysis.recommended}")
