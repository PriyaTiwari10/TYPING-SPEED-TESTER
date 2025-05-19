from flask import Flask, render_template, request
import random
import re

app = Flask(__name__)

sample_texts = [
    "The gentle breeze whispered through the tall trees, carrying with it the subtle scent of blooming jasmine. As the sun dipped below the horizon, painting the sky in hues of orange and pink, the world seemed to pause in a moment of serene beauty. Birds settled into their nests, and the first stars began to twinkle softly overhead. It was a perfect evening, inviting quiet reflection and a deep sense of calm."
]

def preprocess(text):
    # Remove punctuation, lowercase, and split into words
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    return text.lower().strip().split()

@app.route("/", methods=["GET"])
def index():
    sample_text = random.choice(sample_texts)
    return render_template("index.html", sample_text=sample_text)

@app.route("/", methods=["POST"])
def result():
    typed_text = request.form["typed_text"]
    sample_text = sample_texts[0]
    time_taken = float(request.form["time_taken"])

    # Preprocess both texts
    typed_words = preprocess(typed_text)
    original_words = preprocess(sample_text)

    # Compare only the number of words the user typed
    compared_length = min(len(typed_words), len(original_words))
    correct = sum(1 for tw, ow in zip(typed_words[:compared_length], original_words[:compared_length]) if tw == ow)

    accuracy = round((correct / compared_length) * 100, 2) if compared_length > 0 else 0
    wpm = round((len(typed_words) / time_taken) * 60, 2) if time_taken > 0 else 0

    return render_template("result.html",
                           typed_text=typed_text,
                           time_taken=round(time_taken, 2),
                           wpm=wpm,
                           accuracy=accuracy)

if __name__ == "__main__":
    app.run(debug=True)
