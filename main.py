import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt


def generate_content(client: OpenAI, messages: list[dict], verbose: bool = False) -> str:
    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0,
            tools=available_functions,
        )

        if not response.usage:
            raise RuntimeError("failed API request: usage metadata missing")

        message = response.choices[0].message
        messages.append(message)
        if not message.tool_calls:
            return (f"Response: {message.content}")
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose)
            messages.append(result_message)
            if not result_message["content"]:
                raise Exception("Error: no content")
            if verbose:
                print(f"-> {result_message['content']}")
    print("Failed AI Agent response, please try again")
    sys.exit(1)



def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable is not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    print(generate_content(client, messages, verbose=args.verbose))


if __name__ == "__main__":
    main()
