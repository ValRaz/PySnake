# Overview

I wrote PySnake to deepen my understanding of real-time game loops, sprite handling, and user input management in Python. My goal was to build a fully featured Snake game from scratch—complete with multiple levels, sound effects, and on-screen notifications—so that I could strengthen my skills with the Arcade library and practice structuring a growing codebase. I wrote this software both to learn how to structure a game loop in Python and to explore sprite‐based rendering, collision detection, timed events, and sound management. I built this as a learning exercise and a foundation for more advanced 2D game projects.

PySnake is a classic Snake‐style game where the player controls a snake that moves around a grid, eating “food” (represented by a rabbit sprite) to grow longer. Each time the snake eats, the score increments by one and, at certain score thresholds, the game enters a new level: the snake moves faster, and a “Level X” banner appears briefly. The player steers the snake using the arrow keys. Hitting any wall (or bumping into the snake’s own body) ends the game. At Game Over, the player can press “R” to restart from level 1.

[Software Demo Video](https://www.youtube.com/watch?v=oDYSY56p858)

# Development Environment

- **Operating System:** Windows 10 (development)
- **Editor/IDE:** Visual Studio Code (with Python and Pylance extensions)
- **Version Control:** Git (hosted on GitHub)
- **Python 3.11**
- **Arcade 2.7.15**

{Describe the programming language that you used and any libraries.}

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [Arcade Library Documentation](https://api.arcade.academy/en/latest/)
* [Arcade Tutorials (arcade.academy)](https://api.arcade.academy/en/latest/programming_guide/sprites/index.html)
* [Python 3.11 Documentation](https://docs.python.org/3.11/)
* [Pyglet Sound Documentation](https://pyglet.readthedocs.io/en/latest/programming_guide/media.html)

# Future Work
* Add a pause screen and “mute” toggle for background music and effects.
* Implement high-score tracking and persistent save/load functionality.
* Polish level transitions with animated banners or particle effects.