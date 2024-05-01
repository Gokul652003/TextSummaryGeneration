import openai
api_key = 'Enter Your Key'
openai.api_key = api_key
def summ(text,num):
    
    content = text
    number=str(num)
    content=content+" i need summery in"+number+" sentence"

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # #Use the GPT-3.5-turbo model
        messages=[
            {"role": "user", "content": content}
        ]
    )
    chat_response = completion.choices[0].message.content
    return chat_response