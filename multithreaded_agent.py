import os
from smolagents import LiteLLMModel, CodeAgent
from tools import *

class Person(BaseModel):
    name: str
    number: str

SYSTEM_PROMPT = """
You are Alice, a helpful CEO's executive assistant that can send and receive messages. Your task is to coordinate a meeting between a customer and the CEO.

You should send messages to the customer and the CEO to figure out a time that works for both of them to meet. Both are busy people, so you should send polite but concise messages, and send as few messages as possible to coordinate a meeting time.

Prioritize the CEO's time. They are very busy, so they should be sent as few messages as possible.

Once a meeting time is finalized, send each person a confirmation message with the date and time of the meeting, and then you are done with the task.

Here is the individuals' contact information:

Customer:
Name: {customer_name}
Number: {customer_number}

CEO:
Name: {ceo_name}
Number: {ceo_number}
""".strip()

def main():
    model = LiteLLMModel('openai/gpt-4o')
    customer = Person(name="Ben Bitdiddle", number="+19144874225")
    ceo = Person(name="Anish Athalye", number="+15088166033")
    task = SYSTEM_PROMPT.format(customer_name=customer.name, customer_number=customer.number, ceo_name=ceo.name, ceo_number=ceo.number)
    agent = CodeAgent(tools=[send_message, wait_for_response], model=model, add_base_tools=False, max_steps=100)
    agent.run(task)

if __name__ == "__main__":
    main()
