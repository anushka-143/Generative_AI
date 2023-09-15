import openai
from secret_key import openai_key
openai.api_key=openai_key
def poem_on_solace():
    prompt = "write a poem on solace. 4 lines only please."
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
        {"role": "user","content": 'write a poem on solace. 4 lines only please.'}
        ]
    )
    print(response.choices[0]['message']['content'])

if __name__== '__main__':
    poem_on_solace()