# QWords - Word Guessing Game

A Wordle-like word guessing game implemented in Python 3.8 for the AWS Transform demo.

## Overview

QWords is a terminal-based word guessing game where players try to guess a 5-letter word in 6 attempts or less. The game provides color-coded feedback to help players narrow down the correct word.

## Features

- 5-letter word guessing with visual feedback
- Built-in word list with over 500 words
- Color-coded terminal output (Green=correct position, Yellow=wrong position, White=not in word)
- Game statistics tracking
- Simple CLI menu system

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Terminal with color support (most modern terminals)

### Installation

1. Navigate to the qwords directory:
   ```bash
   cd qwords
   ```

2. Create a virtual environment:
   ```bash
   uv python install 3.8 --force
   uv venv --python 3.8 .venv38
   source .venv38/bin/activate  # On Windows: .venv38\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

### Running the Game

```bash
python app.py
```

## How to Play

1. **Start a New Game**: Select option 1 from the main menu
2. **Make a Guess**: Enter any 5-letter word when prompted
3. **Interpret Feedback**: 
   - **Green background**: Letter is correct and in the right position
   - **Yellow background**: Letter is in the word but in wrong position  
   - **White background**: Letter is not in the word at all
4. **Continue Guessing**: You have 6 attempts to guess the word
5. **Win Condition**: Guess the word correctly within 6 attempts

## CLI Commands

### Main Menu Options
- `1` - Start New Game
- `2` - View Game Rules  
- `3` - View Statistics
- `4` - Quit

### During Gameplay
- Enter any 5-letter word to make a guess
- Type `quit` to exit the current game
- Invalid inputs (non-5-letter words) will prompt for re-entry

## Game Rules

1. Guess the 5-letter word in 6 tries or less
2. Each guess must be exactly 5 letters (any word)
3. After each guess, colors show how close you are:
   - **Green**: Letter is correct and in the right position
   - **Yellow**: Letter is in the word but in wrong position
   - **White**: Letter is not in the word
4. Type 'quit' to exit the game at any time

## Example Gameplay

```
QWords - Word Guessing Game
============================
1. Start New Game
2. View Game Rules
3. View Statistics
4. Quit
============================
Select an option (1-4): 1

Starting new game!
Target word has been selected. Good luck!

Current Game Board:
-------------------------
Guess 1: _ _ _ _ _
Guess 2: _ _ _ _ _
Guess 3: _ _ _ _ _
Guess 4: _ _ _ _ _
Guess 5: _ _ _ _ _
Guess 6: _ _ _ _ _
-------------------------

Guesses remaining: 6
Enter your guess (or 'quit' to exit): HOUSE

Your guess: H O U S E 
           (colors would appear here in terminal)
```

## Technical Details

- **Language**: Python 3.8
- **Dependencies**: pytest==6.2.5
- **Architecture**: Single-file application (app.py)
- **Word List**: Built-in list of 500+ common 5-letter words
- **Storage**: In-memory game state (no persistent storage)

## Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```
