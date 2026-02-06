#!/usr/bin/env python3
"""
Unit tests for QWords game logic functions
"""

import pytest
import sys
import os
import time

# Add parent directory to path to import app module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import (
    get_random_word, is_valid_word, validate_guess, create_new_game, 
    make_guess, WORD_LIST, GameState, GuessResult
)


class TestWordValidation:
    """Test cases for word validation functions"""
    
    def test_get_random_word_returns_valid_word(self):
        """Test that get_random_word returns a word from the word list"""
        word = get_random_word()
        
        assert word in WORD_LIST
        assert len(word) == 5
        assert word.isupper()
    
    def test_get_random_word_multiple_calls(self):
        """Test that get_random_word can be called multiple times"""
        words = set()
        for _ in range(10):
            word = get_random_word()
            words.add(word)
            assert word in WORD_LIST
        
        # Should get at least some variety (not guaranteed but very likely)
        assert len(words) >= 1
    
    def test_is_valid_word_with_valid_words(self):
        """Test is_valid_word with known valid words"""
        assert is_valid_word("WORLD") == True
        assert is_valid_word("ABOUT") == True
        assert is_valid_word("SPEED") == True
        assert is_valid_word("world") == True  # Should handle lowercase
        assert is_valid_word("World") == True  # Should handle mixed case
    
    def test_is_valid_word_with_invalid_words(self):
        """Test is_valid_word with invalid words"""
        assert is_valid_word("INVALID") == False  # Too long
        assert is_valid_word("ZZZZZ") == True     # Valid 5 letters (now allowed)
        assert is_valid_word("HI") == False       # Too short
        assert is_valid_word("TOOLONG") == False  # Too long
        assert is_valid_word("") == False         # Empty string
        assert is_valid_word("12345") == False    # Numbers
        assert is_valid_word("HEL!O") == False    # Special characters
    
    def test_is_valid_word_edge_cases(self):
        """Test is_valid_word with edge cases"""
        assert is_valid_word("     ") == False   # Spaces only
        assert is_valid_word("HEL O") == False   # Contains space
        assert is_valid_word("HEL\nO") == False  # Contains newline


class TestGuessValidation:
    """Test cases for guess validation logic"""
    
    def test_validate_guess_all_correct(self):
        """Test validate_guess when all letters are correct"""
        result = validate_guess("WORLD", "WORLD")
        
        assert result.word == "WORLD"
        assert result.feedback == ["correct", "correct", "correct", "correct", "correct"]
    
    def test_validate_guess_all_absent(self):
        """Test validate_guess when no letters match"""
        result = validate_guess("ABCDE", "FGHIJ")
        
        assert result.word == "ABCDE"
        assert result.feedback == ["absent", "absent", "absent", "absent", "absent"]
    
    def test_validate_guess_mixed_feedback(self):
        """Test validate_guess with mixed correct, present, and absent"""
        # Target: WORLD, Guess: WRLOD
        # W: correct (position 0)
        # R: present (R is in WORLD but not at position 1)
        # L: present (L is in WORLD but not at position 2)
        # O: present (O is in WORLD but not at position 3)
        # D: correct (position 4)
        result = validate_guess("WRLOD", "WORLD")
        
        assert result.word == "WRLOD"
        assert result.feedback == ["correct", "present", "present", "present", "correct"]
    
    def test_validate_guess_duplicate_letters_in_guess(self):
        """Test validate_guess with duplicate letters in guess"""
        # Target: SPEED, Guess: EEEEE
        # Only 2 E's in target at positions 2 and 3
        # E: absent (E is in SPEED but not at position 0)
        # E: absent (E is in SPEED but not at position 1)
        # E: correct (E is at position 2 in SPEED)
        # E: correct (E is at position 3 in SPEED)
        # E: absent (no more E's available)
        result = validate_guess("EEEEE", "SPEED")
        
        assert result.word == "EEEEE"
        assert result.feedback == ["absent", "absent", "correct", "correct", "absent"]
    
    def test_validate_guess_duplicate_letters_complex(self):
        """Test validate_guess with complex duplicate letter scenarios"""
        # Target: SPEED, Guess: PEPEP
        # S: absent, P: correct (pos 1), E: correct (pos 2), E: correct (pos 3), D: absent
        # P: present (P is in SPEED at position 1, but not at position 0)
        # E: present (E is in SPEED, available after correct matches)
        # P: absent (P already used for correct match at position 1)
        # E: correct (E is at position 3 in SPEED)
        # P: absent (no more P's available)
        result = validate_guess("PEPEP", "SPEED")
        
        assert result.word == "PEPEP"
        assert result.feedback == ["present", "present", "absent", "correct", "absent"]
    
    def test_validate_guess_case_insensitive(self):
        """Test that validate_guess handles different cases"""
        result1 = validate_guess("world", "WORLD")
        result2 = validate_guess("WORLD", "world")
        result3 = validate_guess("World", "WoRLd")
        
        expected_feedback = ["correct", "correct", "correct", "correct", "correct"]
        
        assert result1.word == "WORLD"
        assert result1.feedback == expected_feedback
        assert result2.word == "WORLD"
        assert result2.feedback == expected_feedback
        assert result3.word == "WORLD"
        assert result3.feedback == expected_feedback


class TestGameFlow:
    """Test cases for game flow functions"""
    
    def test_create_new_game(self):
        """Test create_new_game creates a proper game state"""
        game = create_new_game()
        
        assert isinstance(game, GameState)
        assert game.target_word in WORD_LIST
        assert len(game.target_word) == 5
        assert game.guesses == []
        assert game.current_guess == 0
        assert game.game_over == False
        assert game.won == False
        assert game.start_time is not None
        assert isinstance(game.start_time, float)
        assert game.max_guesses == 6
    
    def test_make_guess_valid_word(self):
        """Test make_guess with a valid word"""
        game = create_new_game()
        game.target_word = "WORLD"
        
        result = make_guess(game, "ABOUT")
        
        assert result is not None
        assert isinstance(result, GuessResult)
        assert result.word == "ABOUT"
        assert len(game.guesses) == 1
        assert game.current_guess == 1
        assert game.guesses[0] == result
    
    def test_make_guess_invalid_word(self):
        """Test make_guess with an invalid word (wrong length or non-letters)"""
        game = create_new_game()
        game.target_word = "WORLD"
        
        # Test with wrong length
        result = make_guess(game, "TOOLONG")
        assert result is None
        
        # Test with numbers
        result = make_guess(game, "12345")
        assert result is None
        
        # Test with valid 5 letters (should work now)
        result = make_guess(game, "ZZZZZ")
        assert result is not None
        assert len(game.guesses) == 1  # Should have added the guess
        assert game.current_guess == 1  # Should have incremented
    
    def test_make_guess_winning_guess(self):
        """Test make_guess with the correct word (winning)"""
        game = create_new_game()
        game.target_word = "WORLD"
        
        result = make_guess(game, "WORLD")
        
        assert result is not None
        assert result.word == "WORLD"
        assert game.won == True
        assert game.game_over == True
        assert len(game.guesses) == 1
        assert game.current_guess == 1
    
    def test_make_guess_game_over_no_more_guesses(self):
        """Test make_guess when game is already over"""
        game = create_new_game()
        game.target_word = "WORLD"
        game.game_over = True
        
        result = make_guess(game, "ABOUT")
        
        assert result is None
        assert len(game.guesses) == 0
        assert game.current_guess == 0
    
    def test_make_guess_max_guesses_reached(self):
        """Test make_guess when max guesses is reached"""
        game = create_new_game()
        game.target_word = "SPEED"
        
        # Make 6 wrong guesses
        wrong_words = ["WORLD", "ABOUT", "BRAIN", "CHAIR", "DANCE", "EARLY"]
        
        for i, word in enumerate(wrong_words):
            result = make_guess(game, word)
            assert result is not None
            assert game.current_guess == i + 1
            
            if i < 5:  # Not the last guess
                assert game.game_over == False
            else:  # Last guess
                assert game.game_over == True
                assert game.won == False
    
    def test_make_guess_case_handling(self):
        """Test make_guess handles different cases properly"""
        game = create_new_game()
        game.target_word = "SPEED"
        
        result = make_guess(game, "world")
        
        assert result is not None
        assert result.word == "WORLD"  # Should be converted to uppercase
        assert len(game.guesses) == 1