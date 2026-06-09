"""
Challenge 2 Solution: Asynchronous Execution
Demonstrates using async/await for parallel query execution
"""

import asyncio
import os
from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

# Verify API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

model = os.getenv("AI_MODEL", "openai:gpt-5.4-mini")
print(f"Using model: {model}")

agent = Agent(
    model,
    system_prompt="""You are a helpful customer support representative
    for TechCorp, a software company. You provide clear, accurate, and
    friendly assistance to customers.""",
)


async def main():
    """Execute multiple queries in parallel using asyncio"""
    queries = [
        "How do I reset my TechCorp account password?",
        "Where can I download the latest desktop app?",
        "What are your support hours for live chat?",
    ]

    # Build coroutine tasks without awaiting each call individually
    tasks = [agent.run(query) for query in queries]

    # Run all queries concurrently
    results = await asyncio.gather(*tasks)

    # Print each query with its corresponding result
    for query, result in zip(queries, results):
        print(f"\nQuery: {query}")
        print(f"Response: {result.output}")

if __name__ == "__main__":
    asyncio.run(main())
