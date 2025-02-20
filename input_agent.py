import os
from smolagents import LiteLLMModel, CodeAgent, tool

def multiline_input(prompt):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)

@tool
def ask_for_input(prompt: str) -> str:
    """
    This is a tool that asks the user for input.

    Args:
        prompt: The prompt to ask the user for input.

    Returns:
        The user's input.
    """
    return multiline_input(prompt)

SYSTEM_PROMPT = """
Ask the user to write a short poem, and then return a version of the poem with the first letter of each line capitalized.
""".strip()

def main():
    model = LiteLLMModel('openai/gpt-4o')
    agent = CodeAgent(tools=[ask_for_input], model=model, add_base_tools=False)
    agent.run(SYSTEM_PROMPT)

if __name__ == "__main__":
    main()
