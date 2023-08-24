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

def valid_exclusion_indices(input_str):
    """Check if the input string for exclusion indices is valid"""
    valid_nums = ["1", "2", "3", "4", "5"]
    nums = input_str.split(",")
    return all(num.strip() in valid_nums for num in nums) and len(nums) == len(set(nums))

def get_exclusions(chars):
    exclusions = {}
    for char in chars:
        while True:
            exclusion_indices = input(f"Enter indices (1-5) where '{char}' should NOT appear (comma-separated): ")
            if valid_exclusion_indices(exclusion_indices):
                # Convert indices to 0-based indexing
                exclusion_indices = [int(i)-1 for i in exclusion_indices.split(",") if i.isdigit()]
                exclusions[char] = exclusion_indices
                break
            else:
                print("Invalid input. Please try again.")
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

def valid_unplaced_chars(input_str):
    """Check if the input string for unplaced characters is valid"""
    return all(char.isalpha() for char in input_str)

def valid_pattern(input_str):
    """Check if the input string for word pattern is valid"""
    return len(input_str) == 5 and all(char.isalpha() or char == '_' for char in input_str)

def valid_forbidden_chars(input_str):
    """Check if the input string for forbidden characters is valid"""
    return all(char.isalpha() for char in input_str)

def get_valid_input(prompt, validation_func):
    """Get valid input using the provided prompt and validation function"""
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        else:
            print("Invalid input. Please try again.")

def main():
    while True:
        unplaced_chars = get_valid_input("Enter characters that are in the word but placement is unknown: ", valid_unplaced_chars)
        exclusions = get_exclusions(unplaced_chars)
        pattern = get_valid_input("Enter the word pattern with known placements (use '_' for unknown spots): ", valid_pattern)
        forbidden = get_valid_input("Enter the characters that are NOT in the word: ", valid_forbidden_chars)

        words = possible_words(exclusions, pattern, forbidden)

        print("Possible words:", words)

        cont = input("Do you want to continue? (yes/no) ")
        if cont.lower() != "yes":
            break

if __name__ == '__main__':
    main()
