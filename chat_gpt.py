import os
from openai import OpenAI
from pickle import dump, load

API_KEY_PATH = 'secret_key.bin'

def get_api_key():
    """
    отримання API KEY from OpenAI
    """
    if os.path.exists(API_KEY_PATH):
        with open(API_KEY_PATH, 'rb') as file:
            api_key = load(file)
    else:
        while True:
            user_input = input("Введіть API KEY from OpenAI: ")
            if len(user_input) == 56 and user_input.startswith("sk-"):
                api_key = user_input
                with open(API_KEY_PATH, 'wb') as file:
                    dump(api_key, file)
                break
            else:
                print("API KEY is not valid, should sk-... and count 56 chars")
    return api_key

def gpt_handler(client: OpenAI, user_input, prompt: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.1,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt.format(question=user_input)}
        ]
    )
    return response.choices[0].message.content

def main():
    api_key = get_api_key()
    client = OpenAI(api_key=api_key)
    prompt= "Уяви, що ти Джейсон Стетхем та дай відповідь на питання: {question}"
    while True:
        user_input = input("Введіть запит: ")
        if user_input in ['q', 'close', 'exit']:
            break
        answer = gpt_handler(client=client, user_input=user_input, prompt=prompt)
        print(answer)
    

if __name__ == "__main__":
    main()