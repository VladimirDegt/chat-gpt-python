import os
from openai import OpenAI
from pickle import dump, load
from colorama import Fore

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
            if user_input.startswith("sk-"):
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
    prompt= """Ти мій помічник з вивчення англійської мови. Я тобі буду писати текст на англійській мові, а ти
     перевіряй граматику та якщо будуть помилки, то пиши виправлений текст англійською. Після кожного свого речення на англійській
     надавай транскрипцію цього речення. Після цього задавай мені питання для підтримки бесіди.  {question}"""
    print(f"{Fore.CYAN}Welcome to the assistant bot!{Fore.RESET}")
    print(f"For exit can use commands: {Fore.GREEN}q, close, exit{Fore.RESET}")
    print(f"{Fore.GREEN}[AI]: {Fore.RESET}Hi, Volodymyr! How was your day?")
    while True:
        user_input = input(f"{Fore.BLUE}[I]: {Fore.RESET}")
        if user_input in ['q', 'close', 'exit']:
            break
        answer = gpt_handler(client=client, user_input=user_input, prompt=prompt)
        print(f"{Fore.GREEN}[AI]: {Fore.RESET}{answer}")
    

if __name__ == "__main__":
    main()