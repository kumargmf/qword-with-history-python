#!/usr/bin/env python3
"""
Integration tests for QWords application
Tests complete game workflows and interactions between components
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path to import app module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import (
    main, play_game, create_new_game, make_guess, 
    GameState, GuessResult, WORD_LIST
)


class TestCompleteGameWorkflows:
    """Integration tests for complete game workflows"""
    
    @patch('builtins.input', side_effect=['ABOUT', 'WORLD'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_complete_winning_game_session(self, mock_stdout, mock_input):
        """Test a complete game session where player wins"""
        # Create a game with known target
        with patch('app.get_random_word', return_value='WORLD'):
            with patch('app.time.time', return_value=1234567890.0):
                play_game()
        
        output = mock_stdout.getvalue()
        
        # Verify game started
        assert "Starting new game!" in output
        
        # Verify game completion
        assert "Congratulations! You won!" in output
        assert "You guessed 'WORLD' in 2 tries" in output
    
    @patch('builtins.input', side_effect=['ABOUT', 'BRAIN', 'CHAIR', 'DANCE', 'EARLY', 'FIRST'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_complete_losing_game_session(self, mock_stdout, mock_input):
        """Test a complete game session where player loses"""
        # Create a game with known target that won't be guessed
        with patch('app.get_random_word', return_value='WORLD'):
            play_game()
        
        output = mock_stdout.getvalue()
        
        # Verify game started
        assert "Starting new game!" in output
        
        # Verify game completion with loss
        assert "Game Over! The word was: WORLD" in output
        assert "Better luck next time!" in output
    
    @patch('builtins.input', side_effect=['quit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_quit_during_game(self, mock_stdout, mock_input):
        """Test quitting during a game"""
        with patch('app.get_random_word', return_value='WORLD'):
            play_game()
        
        output = mock_stdout.getvalue()
        assert "Thanks for playing!" in output
    
    @patch('builtins.input', side_effect=['hi', 'toolong', '12345', 'WORLD'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_input_handling(self, mock_stdout, mock_input):
        """Test handling of various invalid inputs"""
        with patch('app.get_random_word', return_value='WORLD'):
            play_game()
        
        output = mock_stdout.getvalue()
        
        # Should show error messages for invalid inputs
        assert "Please enter exactly 5 letters" in output
        assert "must be exactly 5 letters with no numbers or symbols" in output
        
        # Should eventually accept valid input and win
        assert "Congratulations! You won!" in output


class TestMainMenuIntegration:
    """Integration tests for main menu functionality"""
    
    @patch('builtins.input', side_effect=['2', '4'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_view_rules_then_quit(self, mock_stdout, mock_input):
        """Test viewing rules from main menu then quitting"""
        main()
        
        output = mock_stdout.getvalue()
        
        # Should show welcome message
        assert "Welcome to QWords!" in output
        
        # Should show main menu
        assert "QWords - Word Guessing Game" in output
        
        # Should show rules when option 2 is selected
        assert "QWords Game Rules:" in output
        
        # Should quit gracefully
        assert "Thanks for playing QWords!" in output
    
    @patch('builtins.input', side_effect=['3', '4'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_view_stats_then_quit(self, mock_stdout, mock_input):
        """Test viewing statistics from main menu then quitting"""
        main()
        
        output = mock_stdout.getvalue()
        
        # Should show statistics
        assert "Game Statistics:" in output
        assert "Games played this session:" in output
    
    @patch('builtins.input', side_effect=['5', '1', 'WORLD', '4'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_invalid_choice_then_play_game(self, mock_stdout, mock_input):
        """Test invalid menu choice, then playing a game"""
        with patch('app.get_random_word', return_value='WORLD'):
            main()
        
        output = mock_stdout.getvalue()
        
        # Should show error for invalid choice
        assert "Invalid choice. Please select 1-4." in output
        
        # Should then allow playing game
        assert "Starting new game!" in output
        assert "Congratulations! You won!" in output


class TestGameStateIntegration:
    """Integration tests for game state management"""
    
    def test_game_state_progression_through_multiple_guesses(self):
        """Test game state changes correctly through multiple guesses"""
        game = create_new_game()
        game.target_word = "WORLD"
        
        # Track game state through multiple guesses
        assert game.current_guess == 0
        assert len(game.guesses) == 0
        assert game.game_over == False
        assert game.won == False
        
        # First guess
        result1 = make_guess(game, "ABOUT")
        assert game.current_guess == 1
        assert len(game.guesses) == 1
        assert game.game_over == False
        assert game.won == False
        
        # Second guess
        result2 = make_guess(game, "SPEED")
        assert game.current_guess == 2
        assert len(game.guesses) == 2
        assert game.game_over == False
        assert game.won == False
        
        # Winning guess
        result3 = make_guess(game, "WORLD")
        assert game.current_guess == 3
        assert len(game.guesses) == 3
        assert game.game_over == True
        assert game.won == True
        
        # Verify guess results are stored correctly
        assert game.guesses[0].word == "ABOUT"
        assert game.guesses[1].word == "SPEED"
        assert game.guesses[2].word == "WORLD"
    
    def test_game_timing_integration(self):
        """Test that game timing works correctly"""
        import time
        
        start_time = time.time()
        game = create_new_game()
        
        # Game should have a start time
        assert game.start_time is not None
        assert isinstance(game.start_time, float)
        assert game.start_time >= start_time
    
    def test_word_list_integration(self):
        """Test that word list integration works correctly"""
        # Test that random words come from the list
        for _ in range(10):
            game = create_new_game()
            assert game.target_word in WORD_LIST
            assert len(game.target_word) == 5
        
        # Test that validation works with word list
        from app import is_valid_word
        
        # All words in WORD_LIST should be valid
        for word in WORD_LIST[:10]:  # Test first 10 for performance
            assert is_valid_word(word) == True
        
        # Random 5-letter strings should now be valid
        assert is_valid_word("ZZZZZ") == True
        
        # But invalid formats should still be rejected
        assert is_valid_word("12345") == False  # Numbers
        assert is_valid_word("TOOLONG") == False  # Too long


class TestErrorHandlingIntegration:
    """Integration tests for error handling across the application"""
    
    def test_keyboard_interrupt_handling_in_game(self):
        """Test KeyboardInterrupt handling during game play"""
        with patch('builtins.input', side_effect=KeyboardInterrupt):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with patch('app.get_random_word', return_value='HELLO'):
                    play_game()
                
                output = mock_stdout.getvalue()
                assert "Thanks for playing!" in output
    
    def test_edge_case_word_validation_integration(self):
        """Test edge cases in word validation integration"""
        game = create_new_game()
        game.target_word = "HELLO"
        
        # Test various invalid inputs
        invalid_inputs = ["", "HI", "TOOLONG", "12345", "HEL!O", "     "]
        
        for invalid_input in invalid_inputs:
            result = make_guess(game, invalid_input)
            assert result is None
            
        # Game state should be unchanged
        assert len(game.guesses) == 0
        assert game.current_guess == 0
        assert game.game_over == False
        assert game.won == False
    
    def test_duplicate_letter_handling_integration(self):
        """Test complex duplicate letter scenarios in full game context"""
        game = create_new_game()
        game.target_word = "SPEED"  # Has duplicate E's
        
        # Test guess with a valid word that has duplicates
        result = make_guess(game, "WHEEL")  # WHEEL is in word list and has duplicate E's
        assert result is not None
        
        # Verify feedback handles duplicates correctly
        # W: absent, H: absent, E: correct (pos 2), E: correct (pos 3), L: absent
        expected_feedback = ["absent", "absent", "correct", "correct", "absent"]
        assert result.feedback == expected_feedback
        
        # Game should continue normally
        assert game.game_over == False
        assert game.won == False
        assert len(game.guesses) == 1