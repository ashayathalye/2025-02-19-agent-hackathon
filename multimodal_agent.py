import os
from smolagents import LiteLLMModel, CodeAgent
import argparse

SYSTEM_PROMPT = """
Your task is to look at the attached receipt and figure out the number of unique items on the bill.
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=str, help="Path to the image file")
    args = parser.parse_args()

    model = LiteLLMModel('openai/gpt-4o')
    agent = CodeAgent(tools=[], model=model, add_base_tools=True)
    agent.run(SYSTEM_PROMPT, images=[args.image])

if __name__ == "__main__":
    main()
