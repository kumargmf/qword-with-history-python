#!/usr/bin/env python3
"""
Unit tests for QWords CLI interface functions
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path to import app module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import (
    format_guess_display, display_game_board, get_user_input,
    show_game_rules, show_main_menu, GameState, GuessResult
)


class TestDisplayFunctions:
    """Test cases for display and formatting functions"""
    
    def test_format_guess_display_all_correct(self):
        """Test format_guess_display with all correct letters"""
        result = GuessResult("HELLO", ["correct", "correct", "correct", "correct", "correct"])
        display = format_guess_display(result)
        
        # Should contain the word and ANSI color codes
        assert "H" in display
        assert "E" in display
        assert "L" in display
        assert "O" in display
        assert "\033[42m" in display  # Green background for correct
        assert "\033[0m" in display   # Reset code
    
    def test_format_guess_display_mixed_feedback(self):
        """Test format_guess_display with mixed feedback"""
        result = GuessResult("HELLO", ["correct", "present", "absent", "present", "correct"])
        display = format_guess_display(result)
        
        assert "HELLO" in display.replace("\033[42m", "").replace("\033[43m", "").replace("\033[47m", "").replace("\033[0m", "").replace(" ", "")
        assert "\033[42m" in display  # Green for correct
        assert "\033[43m" in display  # Yellow for present
        assert "\033[47m" in display  # White for absent
    
    def test_format_guess_display_all_absent(self):
        """Test format_guess_display with all absent letters"""
        result = GuessResult("ZZZZZ", ["absent", "absent", "absent", "absent", "absent"])
        display = format_guess_display(result)
        
        assert "Z" in display
        assert "\033[47m" in display  # White background for absent
        assert display.count("\033[47m") == 5  # Should have 5 white backgrounds
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_game_board_empty_game(self, mock_stdout):
        """Test display_game_board with no guesses"""
        game = GameState()
        game.target_word = "HELLO"
        
        display_game_board(game)
        output = mock_stdout.getvalue()
        
        assert "Current Game Board:" in output
        assert "Guess 1: _ _ _ _ _" in output
        assert "Guess 6: _ _ _ _ _" in output
        assert output.count("_ _ _ _ _") == 6
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_game_board_with_guesses(self, mock_stdout):
        """Test display_game_board with some guesses made"""
        game = GameState()
        game.target_word = "HELLO"
        
        # Add some guesses
        guess1 = GuessResult("WORLD", ["absent", "correct", "absent", "present", "absent"])
        guess2 = GuessResult("HORSE", ["correct", "absent", "absent", "absent", "absent"])
        game.guesses = [guess1, guess2]
        
        display_game_board(game)
        output = mock_stdout.getvalue()
        
        assert "Current Game Board:" in output
        assert "Guess 1:" in output
        assert "Guess 2:" in output
        assert "Guess 3: _ _ _ _ _" in output  # Remaining empty slots
        assert output.count("_ _ _ _ _") == 4  # 4 remaining slots
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_game_rules(self, mock_stdout):
        """Test show_game_rules displays correct information"""
        show_game_rules()
        output = mock_stdout.getvalue()
        
        assert "QWords Game Rules:" in output
        assert "5-letter word" in output
        assert "6 tries" in output
        assert "Green:" in output
        assert "Yellow:" in output
        assert "White:" in output
        assert "quit" in output
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_main_menu(self, mock_stdout):
        """Test show_main_menu displays correct options"""
        show_main_menu()
        output = mock_stdout.getvalue()
        
        assert "QWords - Word Guessing Game" in output
        assert "1. Start New Game" in output
        assert "2. View Game Rules" in output
        assert "3. View Statistics" in output
        assert "4. Quit" in output


class TestUserInput:
    """Test cases for user input functions"""
    
    @patch('builtins.input', return_value='hello world')
    def test_get_user_input_normal_input(self, mock_input):
        """Test get_user_input with normal input"""
        result = get_user_input("Enter something: ")
        
        assert result == "hello world"
        mock_input.assert_called_once_with("Enter something: ")
    
    @patch('builtins.input', return_value='  spaced input  ')
    def test_get_user_input_strips_whitespace(self, mock_input):
        """Test get_user_input strips whitespace"""
        result = get_user_input("Enter: ")
        
        assert result == "spaced input"
    
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    def test_get_user_input_keyboard_interrupt(self, mock_input):
        """Test get_user_input handles KeyboardInterrupt"""
        result = get_user_input("Enter: ")
        
        assert result == "quit"
    
    @patch('builtins.input', return_value='')
    def test_get_user_input_empty_input(self, mock_input):
        """Test get_user_input with empty input"""
        result = get_user_input("Enter: ")
        
        assert result == ""


class TestGameIntegration:
    """Integration tests for game flow"""
    
    def test_complete_winning_game_flow(self):
        """Test a complete game where player wins"""
        game = GameState()
        game.target_word = "WORLD"
        game.start_time = 1234567890.0
        
        # Make some guesses leading to a win
        from app import make_guess
        
        # First guess - wrong
        result1 = make_guess(game, "ABOUT")
        assert result1 is not None
        assert game.won == False
        assert game.game_over == False
        
        # Second guess - correct
        result2 = make_guess(game, "WORLD")
        assert result2 is not None
        assert game.won == True
        assert game.game_over == True
        assert len(game.guesses) == 2
    
    def test_complete_losing_game_flow(self):
        """Test a complete game where player loses"""
        game = GameState()
        game.target_word = "SPEED"
        
        from app import make_guess
        
        # Make 6 wrong guesses
        wrong_words = ["WORLD", "ABOUT", "BRAIN", "CHAIR", "DANCE", "EARLY"]
        
        for i, word in enumerate(wrong_words):
            result = make_guess(game, word)
            assert result is not None
            
            if i < 5:  # Not the last guess
                assert game.won == False
                assert game.game_over == False
            else:  # Last guess - game should end
                assert game.won == False
                assert game.game_over == True
        
        assert len(game.guesses) == 6
        assert game.current_guess == 6
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_game_board_display_during_play(self, mock_stdout):
        """Test game board display updates correctly during play"""
        game = GameState()
        game.target_word = "SPEED"
        
        from app import make_guess
        
        # Make a guess and display board
        make_guess(game, "WORLD")
        display_game_board(game)
        
        output = mock_stdout.getvalue()
        assert "Guess 1:" in output
        assert "Guess 2: _ _ _ _ _" in output
        assert output.count("_ _ _ _ _") == 5  # 5 remaining empty slots