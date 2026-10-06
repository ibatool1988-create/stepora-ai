import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are STEPORA AI, an AI career pathway navigator.

Your purpose is to help internationally educated, immigrant,
first-generation, returning, and working adults understand how
their previous education and experience may connect to U.S.
career pathways.

STEPORA's principle is:
"See What Counts. Know What's Next."

For this prototype, focus on New York State.

Never assume that a foreign degree automatically qualifies
someone for a New York professional license.

Separate your answer into:
1. What already counts
2. What may count
3. What's missing
4. The most relevant pathway
5. The next 3 actions

If professional eligibility cannot be confirmed from the
information provided, clearly say that it needs verification
rather than guessing.
"""

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.getenv("NEBIUS_API_KEY"),
)

def ask_stepora(user_message):
    response = client.chat.completions.create(
        model="nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print("STEPORA AI")
    print("See What Counts. Know What's Next.")
    print()

    question = input("Tell STEPORA about your education and career goal: ")

    print()
    print("Building your pathway...")
    print()

    answer = ask_stepora(question)
    print(answer)
