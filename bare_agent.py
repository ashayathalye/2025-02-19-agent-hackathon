import os
from smolagents import LiteLLMModel, CodeAgent

model = LiteLLMModel('openai/gpt-4o')

agent = CodeAgent(tools=[], model=model, add_base_tools=True)

while True:
    agent.run(input("Question: "), reset=True)
