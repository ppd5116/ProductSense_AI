from flask import Flask, render_template, request, redirect, url_for, flash
import os
#!pip install openai
# !pip install requests
# !pip install ast
'''from google.colab import drive
drive.mount('/content/drive')'''
import openai
import requests
import ast

gpt_key3 = "your_api_key"
ocr_key = "your_api_key"

app = Flask(__name__)
app.secret_key = "secret_key"

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        compounds_raw = image_to_text(filename)
        substring = "corrupt"
        if substring in compounds_raw:
            print ("Image is corrupt, pleaese use a different image.")
        else:
            crit = True
            while crit:
                ingredients_list = extract_ingredients_from_ocr(compounds_raw)
                ingredients_list = ingredients_list.split(', ')
                # print (ingredients_list)
                # print (type(ingredients_list))
                # print (len(ingredients_list))
                if len(ingredients_list)>5:
                    crit = False
        output = final_output(ingredients_list)

        # output = "Here goes the final output...."
        return render_template('result.html', output=output, image = filename)

def process_image(image_path):
    return f"You've uploaded: {image_path} now let's begin sensing the product ...."

def image_to_text(filename): # overlay=False, api_key=ocr_key, language='eng'
    payload = {'isOverlayRequired': False,
               'apikey': ocr_key,
               'language': 'eng',
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()

def extract_ingredients_from_ocr(raw_text):
    openai.api_key = gpt_key3  # Replace with your OpenAI API key
    prompt = f"Please extract the ingredients from the following OCR-generated text and correct any spelling mistakes, return list of ingredients only within () and use ',' to separate compounds. Example (ingredient1, ingredient2 ...) :\n{raw_text}"
    response = openai.Completion.create(
        engine="text-davinci-002",  # GPT-3.5 Turbo engine
        prompt=prompt,
        max_tokens=500,  # Adjust the max tokens based on expected response length
        n=1,  # Generate a single response
    )
    ingredients = response.choices[0].text.strip()
    return ingredients

def final_output(compounds):
    openai.api_key = gpt_key3
    # prompt= f"role: dermatologist, Now classify the toxicity levels (none(0), low(1), moderate(2), high(3), very high(4), and extremely high(5)) for the following list of compounds passed in the end. The asnwer should be a list of labels in the format 'l1, l2, l3, ..., ln', where n is the number of compounds and li is the label for compound i. Do not provide code, introduction, explanations, or any additional information. The compounds are:\n{compounds}"
    # prompt = f"Please classify the following compounds on a toxicity scale from 0 (non-toxic) to 5 (highly toxic):\n{compounds}. The response should be toxicity level (0-5) for all compounds as list of numbers in single line. The response will be interpreted  as a list"
    prompt = f"{compounds}\n Act like a doctor and based on the ingredients please provide 3 benefits and 3 drawback (related to skin) of using the product. Cut short to main content, avoid disclaimers, write short sentences in 50 words, plain text, use doctors jargon"
    response = openai.Completion.create(
    engine="text-davinci-002",  # GPT-3.5 Turbo engine
    prompt=prompt,
    max_tokens=200,
    n=1,
    )
    ratings = response.choices[0].text.strip()
    return ratings


if __name__ == '__main__':
    app.run(debug=True)
