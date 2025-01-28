from ollama import chat

def find_books_in_transcript(transcript: str):
    messages = [
        {
            'role': 'system',
            'content': 'You are an expert in finding book titles. Identify books mentioned in the transcript. For each book found, provide: Title and Author. Add <title></title> around the title. Add <author></author> around the author. No other information is needed. If you are not sure, you can say "</blank>".',
        },
        {
            'role': 'user',
            'content': 'here is a transscrip <start> :' + transcript + '<end>',
        }
    ]
    #model = 'deepseek-r1:1.5b'
    #model = 'llama3.2'
    model = 'phi4'
    response = chat(model, messages=messages)
    retval =  response['message']['content']
    print(retval)
    return retval

if __name__ == '__main__':
    test = """ I did have a good talk abou the book "The Hobbit" by J.R.R. Tolkien. I also mentioned "The Lord of the Rings" by the same author. """
    print(find_books_in_transcript(test))