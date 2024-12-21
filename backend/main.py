
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




if __name__ == "__main__":
    #word = input("Enter a word to check: ")
    print(check_and_suggest("සෙල්ලම්"))
    print(check_and_suggest("ඵරිඝනකය"))

    sentence = "අපි ඵරිඝනකය සමග සෙල්ලම් කලෝය."

    print(check_and_suggest_sentence(sentence))
