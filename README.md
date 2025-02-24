# Pathfinding Algorithm Visualization

## Overview
This project is a **visual pathfinding algorithm simulator** implemented using **Python** and **Pygame**. It allows users to interactively place start, end, and obstacle nodes on a grid and visualize various pathfinding algorithms in real time.

## Features
- **Graphical Visualization**: Uses Pygame to provide an intuitive UI for pathfinding.
- **Multiple Algorithms Supported**:
  - **A* Search (A-Star)**
  - **Dijkstra's Algorithm**
  - **Breadth-First Search (BFS)**
  - **Depth-First Search (DFS)**
  - **Uniform Cost Search (UCS)**
- **Interactive Grid System**:
  - Left Click: Place start, end, or barriers.
  - Right Click: Remove barriers or reset start/end.
  - Keyboard Controls: Choose algorithm, run the search, or reset the grid.
- **Customizable Colors** for visualization.

## Installation & Setup
### **Prerequisites**
- Python 3.x
- Pygame library

### **Installing Pygame**
```sh
pip install pygame
```

## Usage Guide
1. **Start the program** by running the Python script.
2. **Placing nodes**:
   - Left Click: Place the **start node** (green), **end node** (pink), and obstacles (blue).
   - Right Click: Remove nodes from the grid.
3. **Selecting an Algorithm**:
   - Press `B` for **BFS**
   - Press `D` for **DFS**
   - Press `U` for **UCS**
   - Press `J` for **Dijkstra's Algorithm**
   - Press `A` for **A* Search**
4. **Running the Algorithm**: Once the start and end nodes are set, press the corresponding key to visualize the pathfinding process.
5. **Reset the Grid**: Press `SPACE` to clear the board and start over.


## Algorithm Descriptions
### **1. A* Search**
- Uses both cost (`g(n)`) and heuristic (`h(n)`) to find the shortest path efficiently.
- Heuristic: **Manhattan Distance**.

### **2. Dijkstra's Algorithm**
- A weighted graph algorithm that guarantees the shortest path.
- Similar to A* but without a heuristic function.

### **3. Breadth-First Search (BFS)**
- Explores all neighbors at the current depth before moving deeper.
- Guarantees the shortest path in an unweighted grid.

### **4. Depth-First Search (DFS)**
- Explores as deep as possible before backtracking.
- May not guarantee the shortest path.

### **5. Uniform Cost Search (UCS)**
- A variant of Dijkstra’s algorithm that expands the lowest-cost node first.

## Future Improvements
- Implement **greedy best-first search**.
- Add **diagonal movement support**.
- Improve **UI/UX with better animations and a sidebar menu**.
- Optimize performance for larger grids.
