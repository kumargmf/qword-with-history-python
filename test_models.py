#!/usr/bin/env python3
"""
Unit tests for QWords game models (GameState and GuessResult)
"""

import pytest
import sys
import os

# Add parent directory to path to import app module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import GameState, GuessResult


class TestGameState:
    """Test cases for GameState class"""
    
    def test_game_state_initialization(self):
        """Test GameState initializes with correct default values"""
        game = GameState()
        
        assert game.target_word == ""
        assert game.guesses == []
        assert game.current_guess == 0
        assert game.game_over == False
        assert game.won == False
        assert game.start_time == None
        assert game.max_guesses == 6
    
    def test_game_state_attributes_can_be_modified(self):
        """Test that GameState attributes can be modified"""
        game = GameState()
        
        game.target_word = "HELLO"
        game.current_guess = 3
        game.game_over = True
        game.won = True
        game.start_time = 1234567890
        
        assert game.target_word == "HELLO"
        assert game.current_guess == 3
        assert game.game_over == True
        assert game.won == True
        assert game.start_time == 1234567890
    
    def test_game_state_guesses_list_operations(self):
        """Test that guesses list can be manipulated"""
        game = GameState()
        
        # Test adding guesses
        guess1 = GuessResult("WORLD", ["correct", "absent", "present", "absent", "correct"])
        guess2 = GuessResult("ABOUT", ["absent", "correct", "absent", "absent", "absent"])
        
        game.guesses.append(guess1)
        game.guesses.append(guess2)
        
        assert len(game.guesses) == 2
        assert game.guesses[0].word == "WORLD"
        assert game.guesses[1].word == "ABOUT"


class TestGuessResult:
    """Test cases for GuessResult class"""
    
    def test_guess_result_initialization(self):
        """Test GuessResult initializes with correct values"""
        word = "WORLD"
        feedback = ["correct", "absent", "present", "absent", "correct"]
        
        result = GuessResult(word, feedback)
        
        assert result.word == "WORLD"
        assert result.feedback == ["correct", "absent", "present", "absent", "correct"]
    
    def test_guess_result_with_empty_feedback(self):
        """Test GuessResult with empty feedback list"""
        word = "WORLD"
        feedback = []
        
        result = GuessResult(word, feedback)
        
        assert result.word == "WORLD"
        assert result.feedback == []
    
    def test_guess_result_with_all_correct_feedback(self):
        """Test GuessResult with all correct feedback"""
        word = "MATCH"
        feedback = ["correct", "correct", "correct", "correct", "correct"]
        
        result = GuessResult(word, feedback)
        
        assert result.word == "MATCH"
        assert result.feedback == ["correct", "correct", "correct", "correct", "correct"]
    
    def test_guess_result_with_mixed_feedback(self):
        """Test GuessResult with mixed feedback types"""
        word = "MIXED"
        feedback = ["correct", "present", "absent", "present", "correct"]
        
        result = GuessResult(word, feedback)
        
        assert result.word == "MIXED"
        assert result.feedback == ["correct", "present", "absent", "present", "correct"]
        assert len(result.feedback) == 5
    
    def test_guess_result_attributes_can_be_modified(self):
        """Test that GuessResult attributes can be modified after creation"""
        result = GuessResult("WORLD", ["absent", "absent", "absent", "absent", "absent"])
        
        # Modify attributes
        result.word = "ABOUT"
        result.feedback = ["correct", "present", "absent", "present", "correct"]
        
        assert result.word == "ABOUT"
        assert result.feedback == ["correct", "present", "absent", "present", "correct"]