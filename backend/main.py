
from fuzzywuzzy import fuzz
import re

def check_and_suggest(word):
    try:
        with open("./Dictionary/Sinhala_Dictionary.text", "r", encoding="UTF-8") as f:
            contents = f.read()
            dictionary = [
                w.lower().replace('\u200d', '')
                for w in contents.splitlines()
            ]
    except FileNotFoundError:
        return "Dictionary file not found. Please ensure the file is in the correct location."

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
    count = 0

    for word in words:
        clean_word = re.sub(r'[^\u0D80-\u0DFF]', '', word)
        suggestions = check_and_suggest(clean_word)

        if suggestions != "No suggestions found.":
            count=+1
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
    result = error_report + f"Corrected Sentence: {corrected_paragraph}"
    
    if count == 0:
        return "No errors found."
    else:
        return result


def correct_sentence_with_rules(text):
    try:
        with open("./Dictionary/Sinhala_Grammer.text", "r", encoding="UTF-8") as f:
            contents = f.read()

        with open("./Dictionary/Sinhala_Subjects.text", "r", encoding="UTF-8") as f:
            subjects = [line.strip() for line in f.readlines() if line.strip()]

    except FileNotFoundError:
        return "Required file(s) not found. Please ensure the files are in the correct location."

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










if __name__ == "__main__":
    #word = input("Enter a word to check: ")
    print(check_and_suggest("සෙල්ලම්"))
    print(check_and_suggest("ඵරිඝනකය"))

    sentence = "ශ්‍රී ලංකාවේ ණය ශ්‍රේණිගත කිරීම්වල ධනාත්මක ප්‍රවණතාවක් පෙන්නුම් කරන බව ෆිච් රේටින් සමාගම පවසයි.අපි සෙල්ලම් කලෝය."

    print(check_and_suggest_sentence(sentence))

    print('\n')
    corrected_sentence = correct_sentence_with_rules(sentence)
    print(f"Corrected Sentence: {corrected_sentence}")

    print(f"Corrected Sentence: {correct_sentence_with_rules('අනතුර සිදුවන අවස්ථාවේ බස් රථයේ මගීන් 20ත් 25ත් අතර ප්‍රමාණයක් සිට ඇති අතර ඔවුන් සියලු දෙනාම කඩිනමින් දික්ඔය සහ වටවල රෝහල්වලට ඇතුළත් කිරීමට කටයුතු කළාය')}")