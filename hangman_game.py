import random

def choose_word():
    words = ["python", "datheon", "internship", "programming", "developer", "algorithm", "software"]
    return random.choice(words)

def display_word(word, guessed_letters):
    return " ".join([letter if letter in guessed_letters else "_" for letter in word])

def play_hangman():
    word = choose_word()
    guessed_letters = set()
    attempts = 6

    print("=== Welcome to the Hangman Word Guessing Game! ===")
    print(f"You have {attempts} incorrect attempts allowed.\n")

    while attempts > 0:
        print("Word:", display_word(word, guessed_letters))
        print("Guessed letters:", ", ".join(sorted(guessed_letters)) if guessed_letters else "None")
        
        guess = input("Guess a letter: ").lower().strip()

        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please enter a single alphabet letter.\n")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter. Try another one.\n")
            continue

        guessed_letters.add(guess)

        if guess in word:
            print(f"Good job! '{guess}' is in the word.\n")
            if all(letter in guessed_letters for letter in word):
                print(f"Congratulations! You guessed the word: {word.upper()}")
                break
        else:
            attempts -= 1
            print(f"Wrong guess! '{guess}' is not in the word. Attempts left: {attempts}\n")

    if attempts == 0:
        print(f"Game Over! The word was: {word.upper()}")

if __name__ == "__main__":
    play_hangman()
