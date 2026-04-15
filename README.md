# Conway's Game of Life

<!-- Preview image: Upload to GitHub and use: -->
<!-- ![Preview](https://raw.githubusercontent.com/nayaksomkar/ConwaysGameOfLife/main/assets/screenshots/preview.png) -->

A simple, modern implementation with colored cells and adaptive UI.

## About Conway's Game of Life

Conway's Game of Life is a cellular automaton created by mathematician **John Conway** in 1970. Despite simple rules, it produces incredibly complex patterns.

**John Conway (1937-2020)** was a British mathematician known for his work in game theory, group theory, and recreational mathematics. He invented this "game" to demonstrate how complex behavior could emerge from simple rules.

The "game" isn't played - you watch patterns evolve. It's used in:
- Computer science education
- Art and generative design
- Studying emergence and complexity
- Mathematical research

## Rules

- Live cell with <2 neighbors dies (lonely)
- Live cell with 2-3 neighbors lives
- Live cell with >3 neighbors dies (overcrowded)
- Dead cell with exactly 3 neighbors becomes alive

## Run

```bash
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| SPACE | Play/Pause |
| C | Clear |
| R | Random |
| G | Grid |
| 1-6 | Patterns |
| ESC | Quit |

## Features

- Multi-color cells (adjustable 1-8 colors)
- Speed control slider
- Responsive UI
- Pattern presets: Glider, Blinker, Beehive, LWSS, Pulsar, Gosper Gun