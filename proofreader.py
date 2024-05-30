from openai import OpenAI
from bs4 import BeautifulSoup  
import re
from tqdm import tqdm  
import nltk
from nltk.tokenize import sent_tokenize  
from bs4 import BeautifulSoup, NavigableString
import bs4
from bs4 import NavigableString    
nltk.download('punkt')
import os
client = OpenAI()

categorize_system_prompt = '''
You are a universal proofreader, working for a publishing house.
Your main task is to review and correct book manuscripts, ensuring the highest possible accuracy. 
During this process, you should maintain the provided HTML code structure, as it will be used for the creation of an e-book. 
Your goal is to spot and correct any typos or other mistakes in words, while also ensuring that the chosen words are the most appropriate 
and meaningful in context.
Be especially carefull about typos in german and english words.

- IMPORTANT: never add original content, always limit yourself to correct the grammar and typo.
Examples:
onlo -> only
religios -> religious
voJkisch -> volkisch
'''

def get_categories(description):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    # temperature=0.1,
    # # This is to enable JSON mode, making sure responses are valid json objects
    # response_format={ 
    #     "type": "json_object"
    # },
    messages=[
        {
            "role": "system",
            "content": categorize_system_prompt
        },
        {
            "role": "user",
            "content": description
        }
    ],
    )
    if description is None or description == '':
        return ""
    else:
        return response.choices[0].message.content



def split_text(text, max_length):  
    words = text.split()  
    chunks = []  
    current_chunk = []  

    for word in words:  
        if len(' '.join(current_chunk)) + len(word) <= max_length:  
            current_chunk.append(word)  
        else:  
            chunks.append(' '.join(current_chunk))  
            current_chunk = [word]  
    if current_chunk:  # add the last chunk if any  
        chunks.append(' '.join(current_chunk))  
    return chunks  


# Works but doesn't hanlde tag like <a> etc..
def replace_sentence_in_contents(contents, sentence, corrected_sentence):  
    for i, content in enumerate(contents):  
        if isinstance(content, NavigableString) and sentence.strip() in content.strip():      
            content.replace_with(NavigableString(content.replace(sentence, corrected_sentence))) 
        elif hasattr(content, 'contents') and content.contents:  
            replace_sentence_in_contents(content.contents, sentence, corrected_sentence)  

def process_html(file_path):    
    with open(file_path, 'r', encoding='utf-8') as file:    
        soup = BeautifulSoup(file.read(), 'html.parser')    
    
    paragraphs = soup.find_all('p')    
    
    total_chunks = 0    
    for paragraph in paragraphs:    
        total_chunks += len(sent_tokenize(paragraph.text))    
    
    print(f"Total chunks to process: {total_chunks}")    
    
    processed_chunks = 0    
    pbar = tqdm(total=total_chunks, desc="Processing chunks", unit="chunk")    
    for paragraph in paragraphs:    
        if isinstance(paragraph, bs4.element.Tag) and paragraph.text is not None:   
            sentences = sent_tokenize(paragraph.text)   
            for sentence in sentences:    
                #print(f"sentence: {sentence}")  
                corrected_sentence = get_categories(sentence)    
                #print(f"corrected_sentence: {corrected_sentence}")  
                replace_sentence_in_contents(paragraph.contents, sentence, corrected_sentence) 
            
            processed_chunks += 1   
            pbar.set_description(f"Processed: {processed_chunks}, Remaining: {total_chunks - processed_chunks}")    
            pbar.update(1)    
    
    pbar.close()    

    
    # split the path into a pair (head, tail)  
    # head is the path before the last slash, tail is the filename after the last slash  
    head, tail = os.path.split(file_path)  
    
    # create new filename  
    new_filename = 'corrected_' + tail  
    
    # if you want to join the head back  
    new_file_path = os.path.join(head, new_filename)  
    
    with open(new_file_path, 'w', encoding='utf-8') as file:    
        file.write(str(soup))   

file_name = './your_file.html'
#Output will be "corrected_filename.html" saved in the same folder of the original file
process_html(file_name)  