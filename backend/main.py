
from fuzzywuzzy import fuzz

def check_and_suggest_use_distance(word):
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

    # Use fuzzywuzzy to find the best matches
    suggestions = sorted(
        dictionary,
        key=lambda x: fuzz.ratio(word, x),
        reverse=True
    )[:3]  # Get top 3 matches

    return suggestions if suggestions else "No suggestions found."


if __name__ == "__main__":
    #word = input("Enter a word to check: ")
    print(check_and_suggest_use_distance("ඵරිඝනකය")[0])
