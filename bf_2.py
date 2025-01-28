from newspaper import Article
import ollama_interface as OLLAMA
import re
import json

def extract_text_from_url(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        # Print article metadata
        print(f"Title: {article.title}")
        if article.authors:
            print(f"Authors: {', '.join(article.authors)}")
        if article.publish_date:
            print(f"Date: {article.publish_date}")
        print("-" * 50)
        
        return article.text
    except Exception as e:
        raise Exception(f"Failed to retrieve the webpage: {e}")

def split_text(text: str, max_length: int) -> list:
    """
    Split the text into chunks not exceeding max_length characters.
    Splits at sentence boundaries to maintain context.

    Args:
        text (str): The text to split.
        max_length (int): The maximum length of each chunk.

    Returns:
        list: A list of text chunks.
    """
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def process_transcript(text: str, context_length: int = 4096):
    """
    Analyze the transcript by splitting it into chunks and querying Ollama for each chunk.

    Args:
        text (str): The transcript text.
        context_length (int): Maximum number of characters per chunk.

    Returns:
        list: A list of book references from all chunks.
    """
    chunks = split_text(text, context_length)
    all_book_references = []

    for idx, chunk in enumerate(chunks, 1):
        print(f"Processing chunk {idx}/{len(chunks)}...")
        references = OLLAMA.find_books_in_transcript(chunk)

        all_book_references.append(references)

    return all_book_references

import re
import json

def extract_titles_and_authors(text):
    # Regular expressions to find <title> and <author> tags
    title_pattern = r"<title>(.*?)</title>"
    author_pattern = r"<author>(.*?)</author>"

    # Find all matches
    titles = re.findall(title_pattern, text)
    authors = re.findall(author_pattern, text)

    return titles, authors

def main():
    #url = 'https://lexfridman.com/marc-andreessen-2-transcript'
    try:
        #text = extract_text_from_url(url)
        text = """Marc Andreessen
(00:41:49) Yeah, yeah. So this is one of the all time great books. Incredible. About 20, 30-year-old book, but it’s completely modern and current in what it talks about as well as very deeply historically informed. So it’s called Private Truths, Public Lies, and it’s written by a social science professor named Timur Kuran, at I think Duke, and his definitive work on this. And so he has this concept, he calls Preference Falsification. And so preference falsification is two things, and you get it from the title of the book, Private Truths, Public Lies. So preference falsification is when you believe something and you can’t say it, or, and this is very important, you don’t believe something and you must say it. And the commonality there is in both cases, you’re lying. You believe something internally, and then you’re lying about it in public."""
        print("Processing transcript for book references...")
        book_references = process_transcript(text)
        print("\nFound Book References:")
        print("-" * 50)
        # Concatenate the list of book references into a single string
        concatenated_references = ' '.join(book_references)
        titles, authors = extract_titles_and_authors(concatenated_references)
        print(titles)
        #print(authors)
        with open('titles.json', 'w') as titles_file:
            json.dump(titles, titles_file)
        
        with open('authors.json', 'w') as authors_file:
            json.dump(authors, authors_file)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()