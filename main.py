import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("openrouter apikey not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    parser = argparse.ArgumentParser(description="ChatBot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    verbose = args.verbose
    messages = [
        {
            "role": "system", 
            "content": system_prompt
        },
        {
            "role": "user",
            "content": args.user_prompt,
        },
    ]
    generate_content(client, messages, verbose)


def generate_content(client: OpenAI, messages: list[dict], verbose: bool):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0
    )
    if not response.usage:
        raise RuntimeError("Failed API request")
    user_prompt = messages[0]["content"]
    prompt_tokens = response.usage.prompt_tokens
    response_tokens = response.usage.completion_tokens

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        print("Response:")

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()


