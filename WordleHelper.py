import nltk
from nltk.corpus import words

def load_words():
    try:
        word_list = words.words()
    except LookupError:
        print("Word dataset not found. Downloading now...")
        nltk.download('words')
        word_list = words.words()

    # Filter out words to only include 5-letter words
    return [word for word in word_list if len(word) == 5]

def get_exclusions(chars):
    exclusions = {}
    for char in chars:
        exclusion_indices = input(f"Enter indices (1-5) where '{char}' should NOT appear (comma-separated): ")
        # Convert indices to 0-based indexing
        exclusion_indices = [int(i)-1 for i in exclusion_indices.split(",") if i.isdigit()]
        exclusions[char] = exclusion_indices
    return exclusions

def possible_words(exclusions, pattern, forbidden):
    all_words = load_words()
    possible = []

    for word in all_words:
        match = True

        # Check fixed positions from pattern
        for i in range(5):
            if pattern[i] != '_':  # fixed position
                if word[i] != pattern[i]:
                    match = False
                    break

        # Check for character exclusions
        for char, exclude_indices in exclusions.items():
            for i in exclude_indices:
                if word[i] == char:
                    match = False
                    break
            if char not in word:  # Ensure the character appears elsewhere in the word
                match = False
                break

        # Check forbidden characters
        for char in forbidden:
            if char in word:
                match = False
                break

        if match:
            possible.append(word)

    return possible

def main():
    while True:
        unplaced_chars = input("Enter characters that are in the word but placement is unknown: ")
        exclusions = get_exclusions(unplaced_chars)
        pattern = input("Enter the word pattern with known placements (use '_' for unknown spots): ")
        forbidden = input("Enter the characters that are NOT in the word: ")

        words = possible_words(exclusions, pattern, forbidden)

        print("Possible words:", words)

        cont = input("Do you want to continue? (yes/no) ")
        if cont.lower() != "yes":
            break

if __name__ == "__main__":
    main()
