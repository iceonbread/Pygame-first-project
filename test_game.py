"""
Tests for the 2D platformer game.
These tests verify the core game mechanics and components.
"""
import pygame
import sys
import os

# Initialize pygame for testing
pygame.init()

# Import game components
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from game import Player, Platform, Enemy, Goal, Game

def test_player_creation():
    """Test that a player can be created with correct initial properties."""
    player = Player(100, 200)
    assert player.rect.x == 100
    assert player.rect.y == 200
    assert player.vel_x == 0
    assert player.vel_y == 0
    assert player.on_ground == False
    print("✓ Player creation test passed")

def test_player_movement():
    """Test player movement methods."""
    player = Player(100, 200)
    
    # Test move right
    player.move_right()
    assert player.vel_x == player.speed
    
    # Test move left
    player.move_left()
    assert player.vel_x == -player.speed
    
    # Test stop
    player.stop()
    assert player.vel_x == 0
    print("✓ Player movement test passed")

def test_platform_creation():
    """Test that platforms can be created."""
    platform = Platform(0, 500, 800, 50)
    assert platform.rect.x == 0
    assert platform.rect.y == 500
    assert platform.rect.width == 800
    assert platform.rect.height == 50
    print("✓ Platform creation test passed")

def test_enemy_creation():
    """Test that enemies can be created with correct properties."""
    enemy = Enemy(100, 200, 150)
    assert enemy.rect.x == 100
    assert enemy.rect.y == 200
    assert enemy.start_x == 100
    assert enemy.move_range == 150
    assert enemy.vel_x != 0
    print("✓ Enemy creation test passed")

def test_enemy_movement():
    """Test that enemies move back and forth."""
    enemy = Enemy(100, 200, 100)
    initial_vel = enemy.vel_x
    
    # Move enemy to the edge of its range
    for _ in range(100):
        enemy.update()
    
    # Velocity should have reversed at some point
    assert enemy.rect.x <= enemy.start_x + enemy.move_range
    assert enemy.rect.x >= enemy.start_x
    print("✓ Enemy movement test passed")

def test_goal_creation():
    """Test that goal can be created."""
    goal = Goal(400, 100)
    assert goal.rect.x == 400
    assert goal.rect.y == 100
    print("✓ Goal creation test passed")

def test_game_initialization():
    """Test that the game initializes correctly."""
    game = Game()
    assert game.running == True
    assert game.game_over == False
    assert game.game_won == False
    assert game.player is not None
    assert len(game.platforms) > 0
    assert len(game.enemies) > 0
    assert len(game.goal_group) > 0
    print("✓ Game initialization test passed")

def test_collision_groups():
    """Test that collision groups are set up correctly."""
    game = Game()
    
    # Check that sprite groups are properly populated
    assert game.player in game.all_sprites
    assert len(game.platforms) > 0
    assert len(game.enemies) > 0
    assert len(game.goal_group) == 1
    print("✓ Collision groups test passed")

def run_all_tests():
    """Run all tests."""
    print("Running 2D Game Tests...")
    print("-" * 50)
    
    try:
        test_player_creation()
        test_player_movement()
        test_platform_creation()
        test_enemy_creation()
        test_enemy_movement()
        test_goal_creation()
        test_game_initialization()
        test_collision_groups()
        
        print("-" * 50)
        print("All tests passed! ✓")
        return True
    except AssertionError as e:
        print(f"Test failed: {e}")
        return False
    except Exception as e:
        print(f"Error running tests: {e}")
        return False
    finally:
        pygame.quit()

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
