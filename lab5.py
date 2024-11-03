import pygame
import math
from queue import PriorityQueue

pygame.init()
pygame.font.init()

PASTEL_YELLOW = (251, 248, 204)    
PASTEL_PEACH = (243, 198, 177)     
PASTEL_PINK = (255, 205, 210)      
PASTEL_LAVENDER = (241, 192, 232)  
PASTEL_PURPLE = (207, 186, 240)    
PASTEL_LIGHT_BLUE = (163, 196, 243) 
PASTEL_BLUE = (144, 219, 244)      
PASTEL_SKY_BLUE = (142, 236, 245)  
PASTEL_TURQUOISE = (157, 250, 230) 
PASTEL_MINT = (185, 251, 192) 
WHITE = (255, 255, 255)	     

class Cell:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = PASTEL_YELLOW  
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == PASTEL_PEACH

    def is_open(self):
        return self.color == PASTEL_TURQUOISE

    def is_barrier(self):
        return self.color == PASTEL_LIGHT_BLUE

    def is_start(self):
        return self.color == PASTEL_MINT

    def is_end(self):
        return self.color == PASTEL_PINK

    def reset(self):
        self.color = PASTEL_YELLOW

    def make_closed(self):
        self.color = PASTEL_PEACH

    def make_open(self):
        self.color = PASTEL_TURQUOISE

    def make_barrier(self):
        self.color = PASTEL_LIGHT_BLUE

    def make_start(self):
        self.color = PASTEL_MINT

    def make_end(self):
        self.color = PASTEL_PINK

    def make_path(self):
        self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False
    
def heuristic(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for row in range(rows):
        grid.append([])
        for col in range(rows):
            node = Cell(row, col, gap, rows)
            grid[row].append(node)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for row in range(rows):
        pygame.draw.line(win, PASTEL_PURPLE, (0, row * gap), (width, row * gap))
        for col in range(rows):
            pygame.draw.line(win, PASTEL_PURPLE, (col * gap, 0), (col * gap, width))

def draw(win, grid, rows, width):
    win.fill(PASTEL_YELLOW)

    for row in grid:
        for cell in row:
            cell.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_position(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start] = 0

    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path = []
            while current in came_from:
                path.append(current.get_pos())
                current = came_from[current]
                current.make_path()
                draw()

            path.reverse()
           
            print("Path")
            print("Start:")
            for pos in path:
                print(f"  {pos},")
            print("Goal")
            print(f"Length: {len(path)} steps")

            start.make_start()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def dfs(draw, grid, start, end):
    stack = [start]
    visited = {start}
    came_from = {}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()

        if current == end:
            path = []
            while current in came_from:
                path.append(current.get_pos())
                current = came_from[current]
                current.make_path()
                draw()

            path.reverse()
           
            print("Path")
            print("Start:")
            for pos in path:
                print(f"  {pos},")
            print("Goal")
            print(f"Length: {len(path)} steps")

            start.make_start()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)  
                stack.append(neighbor)
                came_from[neighbor] = current
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def bfs(draw, grid, start, end):
    queue = [start]
    visited = {start}
    came_from = {}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.pop(0)

        if current == end:
            path = []
            while current in came_from:
                path.append(current.get_pos())
                current = came_from[current]
                current.make_path()
                draw()

            path.reverse()
           
            print("Path")
            print("Start:")
            for pos in path:
                print(f"  {pos},")
            print("Goal")
            print(f"Length: {len(path)} steps")

            start.make_start()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)  
                queue.append(neighbor)
                came_from[neighbor] = current
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def ucs(draw, grid, start, end):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()

        if current == end:
            path = []
            while current in came_from:
                path.append(current.get_pos())
                current = came_from[current]
                current.make_path()
                draw()

            path.reverse()
           
            print("Path")
            print("Start:")
            for pos in path:
                print(f"  {pos},")
            print("Goal")
            print(f"Length: {len(path)} steps")

            start.make_start()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            new_cost = cost_so_far[current] + 1 

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                neighbor.make_open()
                open_set.put((new_cost, neighbor))

        draw()

        if current != start:
            current.make_closed()

    return False

def dijkstra(draw, grid, start, end):
    open_set = PriorityQueue()
    open_set.put((0, start))
    
    came_from = {}
    cost_so_far = {node: math.inf for row in grid for node in row}
    cost_so_far[start] = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_cost, current = open_set.get()

        for neighbor in current.neighbors:
            new_cost = cost_so_far[current] + 1  

            if new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                neighbor.make_open()
                open_set.put((new_cost, neighbor))

        if current != start:
            current.make_closed()

        draw()

    if end in came_from: 
        path = [] 
        current = end
        while current in came_from:
            path.append(current.get_pos())
            current.make_path()
            current = came_from[current]
        path.reverse()
           
        print("Path")
        print("Start:")
        for pos in path:
            print(f"  {pos},")
        print("Goal")
        print(f"Length: {len(path)} steps")
        
        start.make_start()
        end.make_end()
        return True

    return False

def draw_info_panel(win):
    panel_width, panel_height = 250, 280
    panel_surface = pygame.Surface((panel_width, panel_height))
    panel_surface.fill(PASTEL_LIGHT_BLUE)
    
    font = pygame.font.SysFont(None, 20)
    info_text = [
        "     ----------------------------",
        "            Hello! :)",
        "     -> Press B for BFS",
        "     -> Press D for DFS",
        "     -> Press U for UFS",
        "     -> Press J for Dijkstra",
        "     -> Press A for A*",
        "     -> Press SPACE to reset",
        "     ----------------------------",
    ]
    y_offset = 10
    for line in info_text:
        text_surface = font.render(line, True, (0, 0, 0))
        panel_surface.blit(text_surface, (10, y_offset))
        y_offset += 30

    panel_x = (WIDTH - panel_width) // 2
    panel_y = (WIDTH - panel_height) // 2
    win.blit(panel_surface, (panel_x, panel_y))

def main(win, width):
    ROWS = 30
    grid = make_grid(ROWS, width)

    start = None
    end = None
    run = True
    started = False
    algorithm = None
    found_path = False 

    show_info_panel = True

    while run:
        draw(win, grid, ROWS, width)

        while show_info_panel:
            draw_info_panel(win)
            pygame.display.update()
            pygame.time.delay(4000)
            show_info_panel = False
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    algorithm = 'BFS'
                elif event.key == pygame.K_d:
                    algorithm = 'DFS'
                elif event.key == pygame.K_u:
                    algorithm = 'UFS'
                elif event.key == pygame.K_j:
                    algorithm = 'DIJKSTRA'
                elif event.key == pygame.K_a:
                    algorithm = 'A_STAR'
                elif event.key == pygame.K_SPACE:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    started = False
                    found_path = False
                    continue
                
            if started:
                continue

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                cell = grid[row][col]
                if not start and cell != end:
                    start = cell
                    start.make_start()

                elif not end and cell != start:
                    end = cell
                    end.make_end()

                elif cell != end and cell != start:
                    cell.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                cell = grid[row][col]
                cell.reset()
                if cell == start:
                    start = None
                elif cell == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if not started:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)
                    started = True
                    if algorithm == 'BFS':
                        found_path = bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    elif algorithm == 'DFS':
                        found_path = dfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    elif algorithm == 'UFS':
                        found_path = ucs(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    elif algorithm == 'DIJKSTRA':
                        found_path = dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    elif algorithm == 'A_STAR':
                        found_path = a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if found_path:
                    print("Path found!")
                else:
                    print("No path found. Try again!")
                    pygame.time.delay(3000)
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    started = False 

    pygame.quit()

WIN = pygame.display.set_mode((800, 800))
WIDTH = 800
pygame.display.set_caption("Path Finding Algorithms Visualization")

main(WIN, WIDTH) 