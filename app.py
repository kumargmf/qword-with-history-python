#!/usr/bin/env python3
"""
QWords - A Wordle-like word guessing game
Python 3.8 compatible implementation for SEG transformation demo
"""

import random
import time
import sys


class GameState:
    """Manages the state of a single game session"""
    
    def __init__(self):
        self.target_word = ""
        self.guesses = []
        self.current_guess = 0
        self.game_over = False
        self.won = False
        self.start_time = None
        self.max_guesses = 6


class GuessResult:
    """Represents the result of a single guess"""
    
    def __init__(self, word, feedback):
        self.word = word
        self.feedback = feedback  # List of 'correct', 'present', 'absent'


# Built-in word list for the game
WORD_LIST = [
    "ABOUT", "ABOVE", "ABUSE", "ACTOR", "ACUTE", "ADMIT", "ADOPT", "ADULT", "AFTER", "AGAIN",
    "AGENT", "AGREE", "AHEAD", "ALARM", "ALBUM", "ALERT", "ALIEN", "ALIGN", "ALIKE", "ALIVE",
    "ALLOW", "ALONE", "ALONG", "ALTER", "ANGEL", "ANGER", "ANGLE", "ANGRY", "APART", "APPLE",
    "APPLY", "ARENA", "ARGUE", "ARISE", "ARRAY", "ASIDE", "ASSET", "AUDIO", "AUDIT", "AVOID",
    "AWAKE", "AWARD", "AWARE", "BADLY", "BAKER", "BASES", "BASIC", "BEACH", "BEGAN", "BEGIN",
    "BEING", "BELOW", "BENCH", "BILLY", "BIRTH", "BLACK", "BLAME", "BLANK", "BLIND", "BLOCK",
    "BLOOD", "BOARD", "BOAST", "BOBBY", "BOOST", "BOOTH", "BOUND", "BRAIN", "BRAND", "BRASS",
    "BRAVE", "BREAD", "BREAK", "BREED", "BRIEF", "BRING", "BROAD", "BROKE", "BROWN", "BUILD",
    "BUILT", "BUYER", "CABLE", "CALIF", "CARRY", "CATCH", "CAUSE", "CHAIN", "CHAIR", "CHAOS",
    "CHARM", "CHART", "CHASE", "CHEAP", "CHECK", "CHEST", "CHIEF", "CHILD", "CHINA", "CHOSE",
    "CIVIL", "CLAIM", "CLASS", "CLEAN", "CLEAR", "CLICK", "CLIMB", "CLOCK", "CLOSE", "CLOUD",
    "COACH", "COAST", "COULD", "COUNT", "COURT", "COVER", "CRAFT", "CRASH", "CRAZY", "CREAM",
    "CRIME", "CROSS", "CROWD", "CROWN", "CRUDE", "CURVE", "CYCLE", "DAILY", "DANCE", "DATED",
    "DEALT", "DEATH", "DEBUT", "DELAY", "DEPTH", "DOING", "DOUBT", "DOZEN", "DRAFT", "DRAMA",
    "DRANK", "DRAWN", "DREAM", "DRESS", "DRILL", "DRINK", "DRIVE", "DROVE", "DYING", "EAGER",
    "EARLY", "EARTH", "EIGHT", "ELITE", "EMPTY", "ENEMY", "ENJOY", "ENTER", "ENTRY", "EQUAL",
    "ERROR", "EVENT", "EVERY", "EXACT", "EXIST", "EXTRA", "FAITH", "FALSE", "FAULT", "FIBER",
    "FIELD", "FIFTH", "FIFTY", "FIGHT", "FINAL", "FIRST", "FIXED", "FLASH", "FLEET", "FLOOR",
    "FLUID", "FOCUS", "FORCE", "FORTH", "FORTY", "FORUM", "FOUND", "FRAME", "FRANK", "FRAUD",
    "FRESH", "FRONT", "FRUIT", "FULLY", "FUNNY", "GIANT", "GIVEN", "GLASS", "GLOBE", "GOING",
    "GRACE", "GRADE", "GRAND", "GRANT", "GRASS", "GRAVE", "GREAT", "GREEN", "GROSS", "GROUP",
    "GROWN", "GUARD", "GUESS", "GUEST", "GUIDE", "HAPPY", "HARRY", "HEART", "HEAVY", "HENCE",
    "HENRY", "HORSE", "HOTEL", "HOUSE", "HUMAN", "IDEAL", "IMAGE", "INDEX", "INNER", "INPUT",
    "ISSUE", "JAPAN", "JIMMY", "JOINT", "JONES", "JUDGE", "KNOWN", "LABEL", "LARGE", "LASER",
    "LATER", "LAUGH", "LAYER", "LEARN", "LEASE", "LEAST", "LEAVE", "LEGAL", "LEVEL", "LEWIS",
    "LIGHT", "LIMIT", "LINKS", "LIVES", "LOCAL", "LOOSE", "LOWER", "LUCKY", "LUNCH", "LYING",
    "MAGIC", "MAJOR", "MAKER", "MARCH", "MARIA", "MATCH", "MAYBE", "MAYOR", "MEANT", "MEDIA",
    "METAL", "MIGHT", "MINOR", "MINUS", "MIXED", "MODEL", "MONEY", "MONTH", "MORAL", "MOTOR",
    "MOUNT", "MOUSE", "MOUTH", "MOVED", "MOVIE", "MUSIC", "NEEDS", "NEVER", "NEWLY", "NIGHT",
    "NOISE", "NORTH", "NOTED", "NOVEL", "NURSE", "OCCUR", "OCEAN", "OFFER", "OFTEN", "ORDER",
    "OTHER", "OUGHT", "PAINT", "PANEL", "PAPER", "PARTY", "PEACE", "PETER", "PHASE", "PHONE",
    "PHOTO", "PIANO", "PIECE", "PILOT", "PITCH", "PLACE", "PLAIN", "PLANE", "PLANT", "PLATE",
    "POINT", "POUND", "POWER", "PRESS", "PRICE", "PRIDE", "PRIME", "PRINT", "PRIOR", "PRIZE",
    "PROOF", "PROUD", "PROVE", "QUEEN", "QUICK", "QUIET", "QUITE", "RADIO", "RAISE", "RANGE",
    "RAPID", "RATIO", "REACH", "READY", "REALM", "REBEL", "REFER", "RELAX", "REPAY", "REPLY",
    "RIGHT", "RIGID", "RIVAL", "RIVER", "ROBIN", "ROGER", "ROMAN", "ROUGH", "ROUND", "ROUTE",
    "ROYAL", "RURAL", "SCALE", "SCENE", "SCOPE", "SCORE", "SENSE", "SERVE", "SEVEN", "SHALL",
    "SHAPE", "SHARE", "SHARP", "SHEET", "SHELF", "SHELL", "SHIFT", "SHINE", "SHIRT", "SHOCK",
    "SHOOT", "SHORT", "SHOWN", "SIGHT", "SIMON", "SIXTH", "SIXTY", "SIZED", "SKILL", "SLEEP",
    "SLIDE", "SMALL", "SMART", "SMILE", "SMITH", "SMOKE", "SOLID", "SOLVE", "SORRY", "SOUND",
    "SOUTH", "SPACE", "SPARE", "SPEAK", "SPEED", "SPEND", "SPENT", "SPLIT", "SPOKE", "SPORT",
    "STAFF", "STAGE", "STAKE", "STAND", "START", "STATE", "STEAM", "STEEL", "STEEP", "STEER",
    "STICK", "STILL", "STOCK", "STONE", "STOOD", "STORE", "STORM", "STORY", "STRIP", "STUCK",
    "STUDY", "STUFF", "STYLE", "SUGAR", "SUITE", "SUPER", "SWEET", "TABLE", "TAKEN", "TASTE",
    "TAXES", "TEACH", "TEAMS", "TEETH", "TERRY", "TEXAS", "THANK", "THEFT", "THEIR", "THEME",
    "THERE", "THESE", "THICK", "THING", "THINK", "THIRD", "THOSE", "THREE", "THREW", "THROW",
    "THUMB", "TIGHT", "TIMES", "TIRED", "TITLE", "TODAY", "TOPIC", "TOTAL", "TOUCH", "TOUGH",
    "TOWER", "TRACK", "TRADE", "TRAIN", "TREAT", "TREND", "TRIAL", "TRIBE", "TRICK", "TRIED",
    "TRIES", "TRUCK", "TRULY", "TRUNK", "TRUST", "TRUTH", "TWICE", "TWIST", "TYLER", "UNCLE",
    "UNDUE", "UNION", "UNITY", "UNTIL", "UPPER", "UPSET", "URBAN", "USAGE", "USUAL", "VALID",
    "VALUE", "VIDEO", "VIRUS", "VISIT", "VITAL", "VOCAL", "VOICE", "WASTE", "WATCH", "WATER",
    "WHEEL", "WHERE", "WHICH", "WHILE", "WHITE", "WHOLE", "WHOSE", "WOMAN", "WOMEN", "WORLD",
    "WORRY", "WORSE", "WORST", "WORTH", "WOULD", "WRITE", "WRONG", "WROTE", "YOUNG", "YOUTH"
]


def get_random_word():
    """Select a random word from the word list"""
    return random.choice(WORD_LIST)


def is_valid_word(word):
    """Check if a word is valid (5 letters and contains only letters)"""
    if len(word) != 5:
        return False
    return word.isalpha()


def validate_guess(guess, target):
    """
    Validate a guess against the target word
    Returns a GuessResult with feedback for each letter
    """
    guess = guess.upper()
    target = target.upper()
    feedback = []
    
    # Count letters in target for handling duplicates
    target_counts = {}
    for letter in target:
        target_counts[letter] = target_counts.get(letter, 0) + 1
    
    # First pass: mark correct positions
    for i in range(5):
        if guess[i] == target[i]:
            feedback.append('correct')
            target_counts[guess[i]] -= 1
        else:
            feedback.append('unknown')
    
    # Second pass: mark present/absent for non-correct positions
    for i in range(5):
        if feedback[i] == 'unknown':
            if guess[i] in target_counts and target_counts[guess[i]] > 0:
                feedback[i] = 'present'
                target_counts[guess[i]] -= 1
            else:
                feedback[i] = 'absent'
    
    return GuessResult(guess, feedback)


def format_guess_display(guess_result):
    """Format a guess result for display with color codes"""
    # ANSI color codes for terminal display
    colors = {
        'correct': '\033[42m',    # Green background
        'present': '\033[43m',    # Yellow background
        'absent': '\033[47m',     # White background
        'reset': '\033[0m'        # Reset color
    }
    
    display = ""
    for i, letter in enumerate(guess_result.word):
        color = colors[guess_result.feedback[i]]
        display += "{}{} {}{}".format(color, letter, colors['reset'], " ")
    
    return display.strip()


def create_new_game():
    """Create a new game session"""
    game = GameState()
    game.target_word = get_random_word()
    game.start_time = time.time()
    return game


def make_guess(game, guess_word):
    """Process a guess and update game state"""
    if game.game_over:
        return None
    
    if not is_valid_word(guess_word):
        return None
    
    result = validate_guess(guess_word, game.target_word)
    game.guesses.append(result)
    game.current_guess += 1
    
    # Check if won
    if result.word.upper() == game.target_word.upper():
        game.won = True
        game.game_over = True
    
    # Check if out of guesses
    if game.current_guess >= game.max_guesses:
        game.game_over = True
    
    return result


def display_attempt_history(game):
    """Display history of all previous attempts"""
    if not game.guesses:
        return
    
    print("\nPrevious Guesses:")
    for i, guess in enumerate(game.guesses):
        print("Guess {}: {}".format(i + 1, format_guess_display(guess)))


def display_game_board(game):
    """Display the current game board"""
    print("\nCurrent Game Board:")
    print("-" * 25)
    
    for i, guess in enumerate(game.guesses):
        print("Guess {}: {}".format(i + 1, format_guess_display(guess)))
    
    # Show remaining empty slots
    for i in range(len(game.guesses), game.max_guesses):
        print("Guess {}: _ _ _ _ _".format(i + 1))
    
    print("-" * 25)
    
    display_attempt_history(game)


def display_game_stats():
    """Display simple game statistics"""
    print("\nGame Statistics:")
    print("- Games played this session: Available after implementing stats tracking")
    print("- Win rate: Available after implementing stats tracking")


def show_game_rules():
    """Display the game rules"""
    print("\nQWords Game Rules:")
    print("=" * 20)
    print("1. Guess the 5-letter word in 6 tries or less")
    print("2. Each guess must be exactly 5 letters (any word)")
    print("3. After each guess, colors will show how close you are:")
    print("   - Green: Letter is correct and in the right position")
    print("   - Yellow: Letter is in the word but in wrong position")
    print("   - White: Letter is not in the word")
    print("4. Type 'quit' to exit the game")
    print("=" * 20)


def get_user_input(prompt):
    """Get user input with Python 3.8 compatible method"""
    try:
        return input(prompt).strip()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
        return "quit"


def play_game():
    """Main game loop"""
    game = create_new_game()
    
    print("\nStarting new game!")
    print("Target word has been selected. Good luck!")
    
    while not game.game_over:
        display_game_board(game)
        
        print("\nGuesses remaining: {}".format(game.max_guesses - game.current_guess))
        guess = get_user_input("Enter your guess (or 'quit' to exit): ").upper()
        
        if guess == "QUIT":
            print("Thanks for playing!")
            return
        
        if len(guess) != 5:
            print("Please enter exactly 5 letters.")
            continue
        
        if not is_valid_word(guess):
            print("'{}' must be exactly 5 letters with no numbers or symbols. Try again.".format(guess))
            continue
        
        result = make_guess(game, guess)
        if result:
            print("\nYour guess: {}".format(format_guess_display(result)))
    
    # Game over - show final results
    display_game_board(game)
    
    if game.won:
        elapsed_time = time.time() - game.start_time
        print("\nCongratulations! You won!")
        print("You guessed '{}' in {} tries".format(game.target_word, len(game.guesses)))
        print("Time taken: {:.1f} seconds".format(elapsed_time))
    else:
        print("\nGame Over! The word was: {}".format(game.target_word))
        print("Better luck next time!")


def show_main_menu():
    """Display the main menu options"""
    print("\n" + "=" * 30)
    print("QWords - Word Guessing Game")
    print("=" * 30)
    print("1. Start New Game")
    print("2. View Game Rules")
    print("3. View Statistics")
    print("4. Quit")
    print("=" * 30)


def main():
    """Main application entry point"""
    print("Welcome to QWords!")
    print("A Wordle-like word guessing game")
    
    while True:
        show_main_menu()
        choice = get_user_input("Select an option (1-4): ")
        
        if choice == "1":
            play_game()
        elif choice == "2":
            show_game_rules()
        elif choice == "3":
            display_game_stats()
        elif choice == "4":
            print("Thanks for playing QWords!")
            break
        else:
            print("Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    main()