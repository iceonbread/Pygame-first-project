# Game Architecture

## File Structure
```
Pygame-first-project/
├── game.py              # Main game file
├── test_game.py         # Test suite
├── requirements.txt     # Dependencies
├── README.md           # Documentation
├── .gitignore          # Git ignore patterns
└── ARCHITECTURE.md     # This file
```

## Class Hierarchy

```
Game
├── Player (pygame.sprite.Sprite)
│   ├── Movement (left, right, jump, stop)
│   ├── Physics (gravity, velocity)
│   └── Collision detection
│
├── Platform (pygame.sprite.Sprite)
│   └── Static surface for standing
│
├── Enemy (pygame.sprite.Sprite)
│   ├── Patrol movement
│   └── Collision detection
│
└── Goal (pygame.sprite.Sprite)
    └── Win condition trigger
```

## Game Flow

```
Initialize Game
    │
    ├─> Create Player
    ├─> Create Platforms
    ├─> Create Enemies
    └─> Create Goal
    │
Game Loop
    │
    ├─> Handle Events
    │   ├─> Keyboard input
    │   ├─> Jump (Space)
    │   └─> Restart (R)
    │
    ├─> Update
    │   ├─> Player physics
    │   ├─> Enemy movement
    │   ├─> Collision detection
    │   └─> Game state checks
    │
    └─> Render
        ├─> Clear screen
        ├─> Draw all sprites
        ├─> Draw UI text
        └─> Update display
```

## Game States

1. **Playing**: Normal gameplay
   - Player can move and jump
   - Enemies patrol
   - Check for collisions

2. **Game Over**: Player touched enemy or fell
   - Display "Game Over" message
   - Wait for restart (R key)

3. **Won**: Player reached goal
   - Display "You Win!" message
   - Wait for restart (R key)

## Collision System

- **Player vs Platforms**: Stop vertical movement, allow standing
- **Player vs Enemies**: Trigger game over
- **Player vs Goal**: Trigger win condition
- **Screen Boundaries**: Keep player on screen

## Physics System

- **Gravity**: Constant downward acceleration (0.8)
- **Terminal Velocity**: Maximum fall speed (10)
- **Jump Power**: Initial upward velocity (-15)
- **Movement Speed**: Horizontal velocity (5)

## Visual Elements

| Element | Color | Size | Purpose |
|---------|-------|------|---------|
| Player | Blue | 40x50 | Main character |
| Platforms | Green | Various | Surfaces to stand on |
| Enemies | Red | 30x30 | Moving obstacles |
| Goal | Yellow | 40x40 | Win objective |
| Background | White | Full screen | Game background |
