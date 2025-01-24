import logging.config
from flask import Flask, request, jsonify
#import nqrok
from pyngrok import ngrok, conf
from dotenv import load_dotenv
import os
import sys
import logging
from pathlib import Path


# Get the absolute path to the project root directory
project_root = Path(__file__).resolve().parents[2]

# Add the project root to sys.path
sys.path.append(str(project_root))
from src.api.openai.client import OpenAIClient
from src.utils.file_handler import FileHandler
from src.utils.text_processor import TextProcessor
# Condigure ngrok authenticaion
conf.get_default().auth_token = os.getenv("NGROK_AUTH_KEY")

app = Flask(__name__)

# Set up logging to see the ngrok URL
logging.basicConfig(level=logging.INFO)

openai_client = OpenAIClient()
file_handler = FileHandler()
text_processor = TextProcessor()
system_prompt = file_handler.load_txt("tasks/s04e04/system_prompt.txt")

@app.route("/test_api", methods=["POST"])
def generate_answer():
    print("Received request!")  # Debug print
    # Get JSON data from request
    data = request.get_json()
    instruction = data.get("instruction")
    print(f"Received instruction: {instruction}")
    if not instruction:
        return jsonify({"error": "Brak danych w formacie JSON"}), 400
    # Podstawowa walidacja
    if instruction is None:
        return jsonify({"error": "Brak instrukcji."}), 400

    # LLM response
    completion = openai_client.generate_response(
        system_prompt=system_prompt,
        message=instruction,
        model="gpt-4o",
        max_tokens=200,
        temperature=1.0,
        top_p=1.0
    )
    result = text_processor.extract_text_between_tags(completion, "Result")
    logging.info(f"Completion content : {result}")
    #res_json = {"description":result}

    # Zwróć odpowiedź w formie JSON wraz z kodem statusu 200
    return jsonify({"description": result}), 200

if __name__ == "__main__":
    # Start ngrok
    public_url = ngrok.connect(5001)
    print(f" * ngrok tunnel available at : {public_url}")

    # Run Flask app
    app.run(host='0.0.0.0', port=5001)
