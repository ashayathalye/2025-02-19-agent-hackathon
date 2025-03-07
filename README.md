# Agent Hackathon
A receipt-splitting agent that extracts items from a restaurant bill, independently messages each participant to ask what they ordered, and sends Venmo requests accordingly.

## Pseudocode

One basic sketch:

```
@tool
def send_message(phone_number: str, message: str) -> None:
    ...

@tool
def wait_for_input() -> dict[str, str]:
    """
    Waits for something to happen. Types of events that may happen are:
    - Recieve a message from a user
        - This will have return value {"event_type": "message", "from": "<phone number>", "message": "<message>"}
    """
    ...

@tool
def send_venmo_request(username: str, amount: float) -> None:
    ...

SYSTEM_PROMPT = f"""
You are an assistant responsible for coordinating splitting a restaurant bill between multiple people. Your task is to exchange messages with each individual, until you determine what item on the bill was ordered by which person. To send a message, you can use the `send_message` tool. To receive text messages, you can use the `wait_for_input` tool. If at any point, you don't have any additional work to do (like sending a text message to someone) and you just want to wait until you get a response, call this tool.

Every item on the bill must be assigned to a person, otherwise you need to keep talking to people until you figure it out.

Do not send people unnecessary messages.

Once you know which item belongs to which person, send Venmo requests for the appropriate amount to each person.

After that, you're done!

Here are the people, along with their phone numbers:

{people}

And I have attached the receipt as an image.
"""

class Person:
    name: str
    phone_number: str

def run_agent(people: List[Person], receipt_path: str) -> None:
    people_str = "\n".join(f"- {p.name} ({p.number})" for p in people)
    task = SYSTEM_PROMPT.format(people_str)
    agent = CodeAgent(task,
                      tools=[send_message, wait_for_input, send_venmo_request],
                      images=[receipt_path])
```

## To figure out potentially in parallel

### Code

- "Wait for input"
    - Could explore this in the context of a simple self-contained demo, getting the AI to coordinate a meeting between two people
    - Use a tool that is implemented as just `input()` to get any next input from the environment (kind of like [`select(2)`](https://man7.org/linux/man-pages/man2/select.2.html)
- Multimodal or separate OCR integration (receipt -> text)
    - Look into smolagents `images` or `additional_args` argument
- Twilio integration (low priority)
- Demo UI (alternative to Twilio integration): way to simulate threaded conversation with multiple "people"
- Splitwise or Venmo integration (or what's the output format?)

### Concepts

- What is the right interface to multiple threaded conversations? Here's one basic sketch that should work with an all-powerful agent, but probably won't work with today's agents. Have a `send_message(number, text)` tool, and have a `wait()` tool that returns the next available information; if there's an incoming text message, it can just return the string "New message from: <number> --- <contents>", but then the agent will need to correlate that with the previous messages in that particular conversation, based on the number. Might be better to supply the last N messages in that conversation? Or having that as a tool, to let the agent look it up?
- What's the right way to do async? The "wait for input" tool seems like one hacky way, is there a better way? Better way with smolagents, or need another library?

### Features
- Menu items are either payed for by one person, or split evenly between multiple people.
- Have some support for allowing people to correct someone else's mistake.
- Handle cases where tip isn't visible on the receipt and ask the user "what % tip did you give"? 
- Handle cases where the tip is calculated as a percentage of the total bill -- where this is usually written on the receipt.
- Check that the sum of all the items, tax, and tip adds up to the total that was written, let the user know if it doesn't, and adjust the total amount to the correct value.
- If someone hasn't responded in a while, bump them.
- If someone bought nothing, make sure to not charge them a portion of the tax or tip.
- If there are unclaimed items, make sure to ask everyone if they ordered them.
- Handle cases where someone's response does not exactly specify an item (there's ambiguity). 
- Handle cases where multiple people claim the same item.

### Getting started
 1. Read this `README.md`
 1. Then read `bare_agent.py` and understand what it does by asking it questions directly in console.
 2. Then read `receipt_agent.py` and understand what it does (again, by asking it questions directly in console)
