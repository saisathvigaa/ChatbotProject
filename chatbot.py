# app.py
from flask import Flask, render_template, request
import openai
import fitz

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "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"

def extract_pdf_text(pdf_path):
    text = ""
    pdf_document = fitz.open(pdf_path)
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        text += page.get_text()
    pdf_document.close()
    return text

def generate_response(pdf_text, user_input):
    prompt = f"User Question: {user_input} PDF Content: {pdf_text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the gpt-3.5-turbo model
        messages=[
            {"role": "system", "content": "You are a chatbot that provides information from a PDF document."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50  # Set the desired maximum token count
    )
    return response.choices[0].message["content"]

@app.route("/", methods=["GET", "POST"])
def chat():
    pdf_path = "Mantra.pdf"  # Update with your PDF file name
    pdf_text = extract_pdf_text(pdf_path)
    response = ""
    chat_history = []

    if request.method == "POST":
        user_input = request.form["user_input"]
        bot_response = generate_response(pdf_text, user_input)
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "bot", "content": bot_response})

    return render_template("index.html", chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
