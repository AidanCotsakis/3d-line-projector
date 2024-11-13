# 3D Line Renderer with Pygame

A Python-based 3D graphics engine that simulates a 3D environment, allowing users to explore customizable cuboid objects. This project demonstrates matrix-based transformations, 3D perspective projections, and player-controlled navigation, all rendered in real time using Pygame.

## **Features**

- **3D Object Rendering**: Displays and manipulates 3D cuboid objects in a virtual environment.
- **Player Movement and Rotation**: Enables player-controlled navigation and rotation using keyboard and mouse inputs.
- **Realistic Perspective Projection**: Computes object visibility and perspective based on player position for a dynamic 3D view.
- **Dynamic Edge and Face Rendering**: Updates visible edges and faces of objects based on their proximity to the player.

## **Getting Started**

### **Prerequisites**
- Python 3.x
- Pygame library: Install via `pip install pygame`

### **Installation**
1. Clone this repository.
2. Run the `3d.py` script:
    ```bash
    python 3d.py
    ```
## Usage
- **Movement**:
    - `W` / `Up Arrow`: Move Forward
    - `S` / `Down Arrow`: Move Backward
    - `A` / `Left Arrow`: Move Left
    - `D` / `Right Arrow`: Move Right
    - `Space`: `Move Up`
    - `Shift`: `Move Down`
- **Camera Rotation**:
    - Move the mouse to rotate the player's view in the 3D space.

## Project Structure
- `matrixMultiplication()`: Performs matrix operations necessary for 3D transformations.
- `player`: Manages player position, movement, and view rotation.
- `object3D`: Represents and manages 3D objects with edge and face rendering.
- `draw()`: Renders each frame by updating object positions and drawing edges.
