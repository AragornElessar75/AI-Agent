import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI


def generate_content(client: OpenAI, messages: list[dict], verbose: bool = False) -> str:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    if not response.usage:
        raise RuntimeError("failed API request: usage metadata missing")

    if verbose:
        print(
            f"Prompt tokens: {response.usage.prompt_tokens}\n"
            f"Response tokens: {response.usage.completion_tokens}"
        )

    return response.choices[0].message.content


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
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    content = generate_content(client, messages, verbose=args.verbose)
    print(f"Response:\n{content}")


if __name__ == "__main__":
    main()
