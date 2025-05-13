from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Game categories and words
categories = {
    "Animal": ["tiger", "lion", "dog", "horse"],
    "Bird": ["crow", "owl", "dove", "emu"],
    "Insect": ["ant", "spider", "dragonfly", "fly"],
    "Fruits": ["orange", "mango", "kiwi", "apple", "banana"],
    "Vegetables": ["potato", "carrot", "beans", "tomato", "chilli"]
}

# Game state (temporary, global)
current_word = ''
guessed_letters = set()
attempts_left = 6
current_category = ''

def reset_game():
    global current_word, guessed_letters, attempts_left, current_category
    current_category = random.choice(list(categories.keys()))
    current_word = random.choice(categories[current_category])
    guessed_letters = set()
    attempts_left = 6

# Initialize game at startup
reset_game()
@app.route('/', methods=['GET', 'POST'])
def hangman():
    global current_word, guessed_letters, attempts_left, current_category

    if request.method == 'POST':
        guess = request.form['guess'].lower()
        if guess and guess not in guessed_letters:
            guessed_letters.add(guess)
            if guess not in current_word:
                attempts_left -= 1

    # Build the display word
    display_chars = [char if char in guessed_letters else '_' for char in current_word]
    display_word = ' '.join(display_chars)

    # Win or lose check
    if '_' not in display_chars:
        result = f'You won! The word was "{current_word}" 🎉.'
        reset_game()
        return render_template('result.html', result=result)
    elif attempts_left == 0:
        result = f'You lost! The word was "{current_word}" ☹.'
        reset_game()
        return render_template('result.html', result=result)

    return render_template(
        'index.html',
        display_word=display_word,
        attempts_left='❤️' * attempts_left,
        category=current_category
    )

if __name__ == '__main__':
    app.run(debug=True)
