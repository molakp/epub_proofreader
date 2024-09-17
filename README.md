# AI-Powered HTML Proofreader with OpenAI  
  
This Python program leverages OpenAI's advanced language model to assist with proofreading HTML files. It targets grammar and typos specifically in English and German text.

**CURRENLTY DOES NOT SUPPORT EPUB** workaround:
- Open your epub with your favourite editor, my reccomendation is the FOSS Sigil, available at https://sigil-ebook.com/sigil/download/
- Copy the HTML file you want to proofread and save it to a file (ex. file1.html)
- run the program like described


## Key Features  
  
- Integrates OpenAI's gpt-3.5-turbo model for suggesting intelligent corrections.  
- Splits text into manageable sections for efficient interaction with the API.  
- Maintains the integrity of the original HTML structure during the correction process.  
  
## Requirements  
  
- Python 3 (tested with version 3.x)  
- OpenAI API Key ([https://openai.com/](https://openai.com/))
  
## Usage  

- **Export OPENAI API KEY**: In linux terminal terminal run `export OPENAI_API_KEY= your_openai_api_key`
- **Install dependencies**: in terminal `pip install requirements.txt` 
- **Update File Path**: Replace `./your_file.html` with the actual path to your HTML file within the script.  
- **Obtain OpenAI API Key**: Acquire an OpenAI API key and configure it in the code (instructions for setup are not included here).  
- **Run the Program**: Execute the program.  
  
## Output  
  
The program generates a new file named `corrected_filename.html` in the same directory as the original file. This new file contains the proofread content.  
  
## Limitations  
  
- Presently, the program cannot handle HTML tags embedded within sentences during correction.  
- The quality of corrections relies on the quality of the provided sentence and the performance of the OpenAI model.  
  
## Future Considerations  
  
- This program serves as a foundational implementation. You can enhance its robustness by incorporating error handling and more sophisticated processing techniques.  
- Explore alternative language models or rule-based approaches to potentially improve accuracy.  
  
## Disclaimer  
  
This program is designed for educational purposes only. It's crucial to meticulously review the corrected content before finalizing it.
