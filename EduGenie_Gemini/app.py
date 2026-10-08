import os

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env file")

client = genai.Client(api_key=API_KEY)

# Change this if your Gemini account exposes a different model.
MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite"
]


SYSTEM_PROMPT = """
You are EduGenie, an AI Learning Assistant.

Your job is to help students learn difficult topics easily.

Rules:
1. Explain concepts in simple English.
2. Use headings and bullet points.
3. Give examples whenever useful.
4. For programming questions, explain the code clearly.
5. For exam preparation, give important points.
6. Keep answers organized and easy to study.
7. If the user asks for a quiz, provide questions and answers.
"""


def ask_gemini(user_question):
    last_error = ""

    for model in MODELS:
        try:
            print(f"Trying Gemini model: {model}")

            response = client.models.generate_content(
                model=model,
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(
                                text=SYSTEM_PROMPT
                                + "\n\nStudent Question:\n"
                                + user_question
                            )
                        ],
                    )
                ],
                config=types.GenerateContentConfig(
                    temperature=0.4,
                    max_output_tokens=2000,
                ),
            )

            print(f"Success: {model}")
            return response.text

        except Exception as e:
            last_error = str(e)
            print(f"{model} failed: {last_error}")

            # Try next model if current model is unavailable
            if "503" in last_error or "UNAVAILABLE" in last_error:
                continue

            return f"Gemini Error: {last_error}"

    return (
        "Gemini is temporarily busy. "
        "Please wait 10-20 seconds and try again."
    )


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    question = data.get("question", "").strip()

    if not question:

        return jsonify({
            "answer": "Please enter a question."
        })

    answer = ask_gemini(question)

    return jsonify({
        "answer": answer
    })


@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()

    topic = data.get("topic", "").strip()
    task = data.get("task", "explain")

    if not topic:

        return jsonify({
            "answer": "Please enter a topic."
        })

    if task == "summary":

        prompt = f"""
Create easy study notes for:

{topic}

Include:
- Definition
- Important points
- Examples
- Key takeaways
"""

    elif task == "quiz":

        prompt = f"""
Create a quiz for the topic:

{topic}

Create 10 questions.

Include:
- 5 multiple choice questions
- 3 short answer questions
- 2 application questions

Give the answer key at the end.
"""

    elif task == "studyplan":

        prompt = f"""
Create a 7-day study plan for:

{topic}

For every day include:
- Topic
- What to learn
- Practice activity
- Revision task
"""

    else:

        prompt = f"""
Explain the following topic for a college student:

{topic}

Include:
- Simple definition
- How it works
- Important concepts
- Example
- Short summary
"""

    answer = ask_gemini(prompt)

    return jsonify({
        "answer": answer
    })


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )