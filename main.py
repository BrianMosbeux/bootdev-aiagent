import sys
import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function


MAX_ITERS = 20

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
    
    for _ in range(MAX_ITERS):
        try:
            content = generate_content(client, messages, verbose)
            if content is not None:
                print("Final response:")
                print(content)
                return
        except Exception as e:
            print(f"Error generating content: {e}")
            sys.exit(1)

    print(f"We ran out of iterations ({MAX_ITERS})! Let's avoid burning credits")
    sys.exit(1)


def generate_content(client: OpenAI, messages: list[dict], verbose: bool) -> str | None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    if not response.usage:
        raise RuntimeError("Failed API request")
    user_prompt = messages[1]["content"]
    prompt_tokens = response.usage.prompt_tokens
    response_tokens = response.usage.completion_tokens

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        print("Response:")

    message = response.choices[0].message
    messages.append(message)
    if not message.tool_calls:
        return message.content


    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue
        result_message = call_function(tool_call, verbose)
        if not result_message.get('content'):
            raise RuntimeError(f"Error: message content is empty for {tool_call.function.name}")
        if verbose:
            print(f"-> {result_message['content']}")
        messages.append(result_message)

    return None
        





if __name__ == "__main__":
    main()


