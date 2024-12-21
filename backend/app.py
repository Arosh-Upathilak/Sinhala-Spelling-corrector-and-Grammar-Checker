from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from fuzzywuzzy import fuzz

app = Flask(__name__)
CORS(app)

# Import the existing functions from the provided code
def check_and_suggest(word):
    try:
        with open("./Dictionary/Sinhala_Dictionary.text", "r", encoding="UTF-8") as f:
            contents = f.read()
            dictionary = [
                w.lower().replace('\u200d', '')
                for w in contents.splitlines()
            ]
    except FileNotFoundError:
        return "Dictionary file not found."

    word = word.lower().replace('\u200d', '')

    if word in dictionary:
        return "No suggestions found."

    suggestions = sorted(
        dictionary,
        key=lambda x: fuzz.ratio(word, x),
        reverse=True
    )[:3] 

    return suggestions if suggestions else "No suggestions found."


def check_and_suggest_sentence(sentence):
    words = sentence.split()
    corrected_sentence = []
    errors = []

    for word in words:
        clean_word = re.sub(r'[^\u0D80-\u0DFF]', '', word)
        suggestions = check_and_suggest(clean_word)

        if suggestions != "No suggestions found.":
            errors.append((clean_word, suggestions))
            corrected_word = word.replace(clean_word, suggestions[0])
            corrected_sentence.append(corrected_word)
        else:
            corrected_sentence.append(word)

    error_report = ""
    if errors:
        for error in errors:
            error_report += f"Error: '{error[0]}', Suggestions: {', '.join(error[1])}\n"

    corrected_paragraph = ' '.join(corrected_sentence)
    return {
        "errors": error_report.strip(),
        "corrected_sentence": corrected_paragraph
    }


def correct_sentence_with_rules(text):
    try:
        with open("./Dictionary/Sinhala_Grammer.text", "r", encoding="UTF-8") as f:
            contents = f.read()

        with open("./Dictionary/Sinhala_Subjects.text", "r", encoding="UTF-8") as f:
            subjects = [line.strip() for line in f.readlines() if line.strip()]

    except FileNotFoundError:
        return "Required file(s) not found."

    corrections_data = {}
    subject = None
    for line in contents.splitlines():
        line = line.strip()
        if not line:
            continue
        if ":" in line:
            subject = line[:-1]
            corrections_data[subject] = {}
        elif "->" in line:
            incorrect, correct = line.split("->")
            corrections_data[subject][incorrect.strip()] = correct.strip()

    sentences = [s.strip() for s in text.replace(",", ".").split(".") if s.strip()]
    corrected_sentences = []

    for sentence in sentences:
        words = sentence.split()
        if not words:
            corrected_sentences.append(sentence)
            continue

        corrections = {}
        matched_subjects = []

        for word in words:
            if word in subjects:
                matched_subjects.append(word)
                for key, rules in corrections_data.items():
                    if word in key.split(","):
                        corrections = rules
                        break

        if len(set(matched_subjects)) > 1:
            corrections = corrections_data.get('බහුවචනය', {})

        corrected_sentence = sentence
        for incorrect, correct in corrections.items():
            if incorrect in sentence:
                corrected_sentence = corrected_sentence.replace(incorrect, correct)

        corrected_sentences.append(corrected_sentence)

    corrected_text = ".".join(corrected_sentences) + "." if corrected_sentences else ""
    return corrected_text


@app.route('/check', methods=['POST'])
def check_text():
    data = request.get_json()
    paragraph = data.get('paragraph', '')

    spelling_result = check_and_suggest_sentence(paragraph)
    grammar_correction = correct_sentence_with_rules(spelling_result['corrected_sentence'])

    return jsonify({
        "spelling_correction": spelling_result['corrected_sentence'],
        "grammar_correction": grammar_correction
    })

@app.route("/spellcheck", methods=["POST"])
def spell_check():
    data = request.json
    word = data.get("word")
    if not word:
        return jsonify({"error": "No word provided"}), 400  # Handle missing word input
    suggestions = check_and_suggest(word)
    return jsonify({"suggestions": suggestions})


if __name__ == '__main__':
    app.run(debug=True,port=8080)
