"""
COMPLETE PYTHON PROGRAMS FOR ALL 16 PROBLEMS
=============================================
This file contains solutions for all 16 problems including:
1. 8-Puzzle Problem
2. 8-Queen Problem
3. Water Jug Problem
4. Crypt-Arithmetic Problem
5. Missionaries Cannibal Problem
6. Vacuum Cleaner Problem
7. BFS Implementation
8. DFS Implementation
9. Travelling Salesman Problem
10. A* Algorithm
11. Map Coloring (CSP)
12. Tic Tac Toe Game
13. Minimax Algorithm
14. Alpha-Beta Pruning
15. Decision Tree
16. Feed Forward Neural Network
"""

import numpy as np
import copy
import random
from collections import deque
import itertools
import math

# ============================================================================
# PROGRAM 1: 8-PUZZLE PROBLEM
# ============================================================================

class EightPuzzle:
    """
    Solve 8-Puzzle problem using BFS
    """
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.size = 3
        
    def find_empty(self, state):
        """Find the position of empty space (0)"""
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] == 0:
                    return i, j
        return None
    
    def get_neighbors(self, state):
        """Generate neighboring states by moving empty space"""
        neighbors = []
        i, j = self.find_empty(state)
        
        # Possible moves: up, down, left, right
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for di, dj in moves:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.size and 0 <= nj < self.size:
                new_state = copy.deepcopy(state)
                new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
                neighbors.append(new_state)
        
        return neighbors
    
    def state_to_tuple(self, state):
        """Convert state to tuple for hashing"""
        return tuple(tuple(row) for row in state)
    
    def solve_bfs(self):
        """Solve using BFS"""
        queue = deque([(self.start, [self.start])])
        visited = set([self.state_to_tuple(self.start)])
        
        while queue:
            current, path = queue.popleft()
            
            if current == self.goal:
                return path
            
            for neighbor in self.get_neighbors(current):
                neighbor_tuple = self.state_to_tuple(neighbor)
                if neighbor_tuple not in visited:
                    visited.add(neighbor_tuple)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def display(self, state):
        """Display the puzzle state"""
        for row in state:
            print(" ".join(str(x) if x != 0 else " " for x in row))
        print("-" * 10)

def run_eight_puzzle():
    print("\n" + "="*60)
    print("PROGRAM 1: 8-PUZZLE PROBLEM")
    print("="*60)
    
    start = [
        [1, 2, 3],
        [4, 0, 5],
        [7, 8, 6]
    ]
    
    goal = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    puzzle = EightPuzzle(start, goal)
    
    print("Start State:")
    puzzle.display(start)
    print("Goal State:")
    puzzle.display(goal)
    
    solution = puzzle.solve_bfs()
    
    if solution:
        print(f"Solution found in {len(solution)-1} moves!")
        for i, state in enumerate(solution):
            print(f"Step {i}:")
            puzzle.display(state)
    else:
        print("No solution found!")


# ============================================================================
# PROGRAM 2: 8-QUEEN PROBLEM
# ============================================================================

class EightQueen:
    """
    Solve 8-Queen problem using backtracking
    """
    def __init__(self, n=8):
        self.n = n
        self.solutions = []
    
    def is_safe(self, board, row, col):
        """Check if a queen can be placed at board[row][col]"""
        # Check this row on left side
        for i in range(col):
            if board[row][i] == 1:
                return False
        
        # Check upper diagonal on left side
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        
        # Check lower diagonal on left side
        for i, j in zip(range(row, self.n, 1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        
        return True
    
    def solve_util(self, board, col):
        """Utility function to solve using backtracking"""
        if col >= self.n:
            self.solutions.append(copy.deepcopy(board))
            return True
        
        res = False
        for i in range(self.n):
            if self.is_safe(board, i, col):
                board[i][col] = 1
                res = self.solve_util(board, col + 1) or res
                board[i][col] = 0  # Backtrack
        
        return res
    
    def solve(self):
        """Solve the 8-Queen problem"""
        board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.solve_util(board, 0)
        return self.solutions
    
    def display(self, board):
        """Display the board"""
        for i in range(self.n):
            for j in range(self.n):
                if board[i][j] == 1:
                    print("Q", end=" ")
                else:
                    print(".", end=" ")
            print()

def run_eight_queen():
    print("\n" + "="*60)
    print("PROGRAM 2: 8-QUEEN PROBLEM")
    print("="*60)
    
    queen = EightQueen(8)
    solutions = queen.solve()
    
    print(f"Found {len(solutions)} solutions!")
    print("\nFirst solution:")
    queen.display(solutions[0])
    
    print(f"\nTotal number of solutions: {len(solutions)}")


# ============================================================================
# PROGRAM 3: WATER JUG PROBLEM
# ============================================================================

class WaterJug:
    """
    Solve Water Jug Problem using BFS
    Problem: You have two jugs of capacities m and n. 
    Measure exactly d liters of water.
    """
    def __init__(self, jug1_capacity, jug2_capacity, target):
        self.jug1_cap = jug1_capacity
        self.jug2_cap = jug2_capacity
        self.target = target
    
    def get_neighbors(self, state):
        """Generate neighboring states"""
        j1, j2 = state
        neighbors = []
        
        # Fill jug1
        neighbors.append((self.jug1_cap, j2))
        
        # Fill jug2
        neighbors.append((j1, self.jug2_cap))
        
        # Empty jug1
        neighbors.append((0, j2))
        
        # Empty jug2
        neighbors.append((j1, 0))
        
        # Pour from jug1 to jug2
        pour = min(j1, self.jug2_cap - j2)
        neighbors.append((j1 - pour, j2 + pour))
        
        # Pour from jug2 to jug1
        pour = min(j2, self.jug1_cap - j1)
        neighbors.append((j1 + pour, j2 - pour))
        
        return neighbors
    
    def solve_bfs(self):
        """Solve using BFS"""
        start = (0, 0)
        queue = deque([(start, [start])])
        visited = set([start])
        
        while queue:
            state, path = queue.popleft()
            j1, j2 = state
            
            if j1 == self.target or j2 == self.target:
                return path
            
            for neighbor in self.get_neighbors(state):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def display_solution(self, path):
        """Display the solution path"""
        if not path:
            print("No solution found!")
            return
        
        print(f"Solution found in {len(path)-1} steps:")
        for i, (j1, j2) in enumerate(path):
            print(f"Step {i}: Jug1={j1}, Jug2={j2}")

def run_water_jug():
    print("\n" + "="*60)
    print("PROGRAM 3: WATER JUG PROBLEM")
    print("="*60)
    
    jug1 = 4  # 4-gallon jug
    jug2 = 3  # 3-gallon jug
    target = 2  # Want 2 gallons
    
    print(f"Jug1 capacity: {jug1} gallons")
    print(f"Jug2 capacity: {jug2} gallons")
    print(f"Target: {target} gallons")
    
    water_jug = WaterJug(jug1, jug2, target)
    solution = water_jug.solve_bfs()
    water_jug.display_solution(solution)


# ============================================================================
# PROGRAM 4: CRYPT-ARITHMETIC PROBLEM
# ============================================================================

class CryptArithmetic:
    """
    Solve Crypt-Arithmetic puzzle: SEND + MORE = MONEY
    """
    def __init__(self, puzzle):
        """
        puzzle: tuple of (word1, word2, result)
        Example: ('SEND', 'MORE', 'MONEY')
        """
        self.word1, self.word2, self.result = puzzle
        self.letters = set(self.word1 + self.word2 + self.result)
        self.leading_letters = {self.word1[0], self.word2[0], self.result[0]}
    
    def word_to_number(self, word, mapping):
        """Convert word to number based on mapping"""
        num = 0
        for char in word:
            num = num * 10 + mapping[char]
        return num
    
    def is_valid(self, mapping):
        """Check if mapping is valid"""
        # Check leading letters not zero
        for letter in self.leading_letters:
            if mapping[letter] == 0:
                return False
        
        # Check if SEND + MORE = MONEY
        num1 = self.word_to_number(self.word1, mapping)
        num2 = self.word_to_number(self.word2, mapping)
        num3 = self.word_to_number(self.result, mapping)
        
        return num1 + num2 == num3
    
    def solve(self):
        """Solve the puzzle using brute force"""
        letters_list = list(self.letters)
        solutions = []
        
        # Try all permutations of digits 0-9 for the letters
        for perm in itertools.permutations(range(10), len(letters_list)):
            mapping = dict(zip(letters_list, perm))
            if self.is_valid(mapping):
                solutions.append(mapping)
        
        return solutions
    
    def display_solution(self, mapping):
        """Display a solution"""
        num1 = self.word_to_number(self.word1, mapping)
        num2 = self.word_to_number(self.word2, mapping)
        num3 = self.word_to_number(self.result, mapping)
        
        print(f"  {self.word1} = {num1:5d}")
        print(f"+ {self.word2} = {num2:5d}")
        print("-" * 15)
        print(f"  {self.result} = {num3:5d}")
        print("\nMapping:")
        for letter, digit in sorted(mapping.items()):
            print(f"  {letter} -> {digit}")

def run_crypt_arithmetic():
    print("\n" + "="*60)
    print("PROGRAM 4: CRYPT-ARITHMETIC PROBLEM")
    print("="*60)
    
    puzzle = ('SEND', 'MORE', 'MONEY')
    print(f"Puzzle: {puzzle[0]} + {puzzle[1]} = {puzzle[2]}")
    
    crypto = CryptArithmetic(puzzle)
    solutions = crypto.solve()
    
    if solutions:
        print(f"\nFound {len(solutions)} solution(s):")
        for i, sol in enumerate(solutions[:1]):  # Show first solution
            print(f"\nSolution {i+1}:")
            crypto.display_solution(sol)
    else:
        print("No solution found!")


# ============================================================================
# PROGRAM 5: MISSIONARIES AND CANNIBALS PROBLEM
# ============================================================================

class MissionariesCannibals:
    """
    Solve Missionaries and Cannibals problem
    State: (missionaries_left, cannibals_left, boat_position)
    boat_position: 0 for left, 1 for right
    """
    def __init__(self, m=3, c=3):
        self.total_m = m
        self.total_c = c
        self.start = (m, c, 0)  # All on left bank
        self.goal = (0, 0, 1)    # All on right bank
    
    def is_valid(self, state):
        """Check if state is valid"""
        m_left, c_left, _ = state
        m_right = self.total_m - m_left
        c_right = self.total_c - c_left
        
        # Check if any side has more cannibals than missionaries
        # (unless no missionaries on that side)
        if (m_left > 0 and c_left > m_left) or (m_right > 0 and c_right > m_right):
            return False
        
        # Check bounds
        if m_left < 0 or c_left < 0 or m_left > self.total_m or c_left > self.total_c:
            return False
        
        return True
    
    def get_neighbors(self, state):
        """Generate neighboring states"""
        m_left, c_left, boat = state
        neighbors = []
        
        # Possible moves: (missionaries, cannibals)
        moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
        
        for dm, dc in moves:
            if boat == 0:  # Boat on left, moving to right
                new_state = (m_left - dm, c_left - dc, 1)
            else:  # Boat on right, moving to left
                new_state = (m_left + dm, c_left + dc, 0)
            
            if self.is_valid(new_state):
                neighbors.append(new_state)
        
        return neighbors
    
    def solve_bfs(self):
        """Solve using BFS"""
        queue = deque([(self.start, [self.start])])
        visited = set([self.start])
        
        while queue:
            state, path = queue.popleft()
            
            if state == self.goal:
                return path
            
            for neighbor in self.get_neighbors(state):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def display_solution(self, path):
        """Display the solution path"""
        if not path:
            print("No solution found!")
            return
        
        print(f"Solution found in {len(path)-1} steps:")
        for i, (m_left, c_left, boat) in enumerate(path):
            m_right = self.total_m - m_left
            c_right = self.total_c - c_left
            boat_pos = "LEFT" if boat == 0 else "RIGHT"
            print(f"Step {i}: M={m_left}, C={c_left} | Boat={boat_pos} | "
                  f"Right: M={m_right}, C={c_right}")

def run_missionaries_cannibals():
    print("\n" + "="*60)
    print("PROGRAM 5: MISSIONARIES AND CANNIBALS PROBLEM")
    print("="*60)
    
    mc = MissionariesCannibals(3, 3)
    print(f"Start: All 3 missionaries and 3 cannibals on left bank")
    print(f"Goal: All on right bank")
    
    solution = mc.solve_bfs()
    mc.display_solution(solution)


# ============================================================================
# PROGRAM 6: VACUUM CLEANER PROBLEM
# ============================================================================

class VacuumCleaner:
    """
    Vacuum Cleaner problem with 2 rooms
    State: (vacuum_position, room1_status, room2_status)
    vacuum_position: 'A' or 'B'
    room_status: 0 for clean, 1 for dirty
    """
    def __init__(self, start_pos='A', room1_dirty=True, room2_dirty=True):
        self.start = (start_pos, 1 if room1_dirty else 0, 1 if room2_dirty else 0)
        self.goal = (None, 0, 0)  # Both rooms clean
    
    def is_goal(self, state):
        """Check if goal state reached"""
        _, r1, r2 = state
        return r1 == 0 and r2 == 0
    
    def get_neighbors(self, state):
        """Generate neighboring states"""
        pos, r1, r2 = state
        neighbors = []
        
        # Move to other room
        if pos == 'A':
            neighbors.append(('B', r1, r2))
        else:
            neighbors.append(('A', r1, r2))
        
        # Clean current room
        if pos == 'A' and r1 == 1:
            neighbors.append(('A', 0, r2))
        elif pos == 'B' and r2 == 1:
            neighbors.append(('B', r1, 0))
        
        return neighbors
    
    def solve_bfs(self):
        """Solve using BFS"""
        queue = deque([(self.start, [self.start])])
        visited = set([self.start])
        
        while queue:
            state, path = queue.popleft()
            
            if self.is_goal(state):
                return path
            
            for neighbor in self.get_neighbors(state):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def display_solution(self, path):
        """Display the solution path"""
        if not path:
            print("No solution found!")
            return
        
        print(f"Solution found in {len(path)-1} steps:")
        for i, (pos, r1, r2) in enumerate(path):
            status1 = "Dirty" if r1 == 1 else "Clean"
            status2 = "Dirty" if r2 == 1 else "Clean"
            print(f"Step {i}: Vacuum at Room {pos}, "
                  f"Room A: {status1}, Room B: {status2}")

def run_vacuum_cleaner():
    print("\n" + "="*60)
    print("PROGRAM 6: VACUUM CLEANER PROBLEM")
    print("="*60)
    
    vacuum = VacuumCleaner('A', True, True)
    print("Start: Both rooms dirty, vacuum at Room A")
    
    solution = vacuum.solve_bfs()
    vacuum.display_solution(solution)


# ============================================================================
# PROGRAM 7: BFS IMPLEMENTATION
# ============================================================================

class BFS:
    """
    Breadth-First Search implementation
    """
    def __init__(self, graph):
        self.graph = graph
    
    def bfs(self, start):
        """Perform BFS traversal"""
        visited = set()
        queue = deque([start])
        visited.add(start)
        traversal = []
        
        while queue:
            node = queue.popleft()
            traversal.append(node)
            
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return traversal
    
    def bfs_shortest_path(self, start, goal):
        """Find shortest path using BFS"""
        queue = deque([(start, [start])])
        visited = set([start])
        
        while queue:
            node, path = queue.popleft()
            
            if node == goal:
                return path
            
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None

def run_bfs():
    print("\n" + "="*60)
    print("PROGRAM 7: BFS IMPLEMENTATION")
    print("="*60)
    
    # Create a sample graph
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    bfs = BFS(graph)
    
    print("Graph adjacency list:")
    for node, neighbors in graph.items():
        print(f"  {node}: {neighbors}")
    
    start = 'A'
    traversal = bfs.bfs(start)
    print(f"\nBFS traversal from {start}: {traversal}")
    
    goal = 'F'
    path = bfs.bfs_shortest_path(start, goal)
    print(f"Shortest path from {start} to {goal}: {path}")


# ============================================================================
# PROGRAM 8: DFS IMPLEMENTATION
# ============================================================================

class DFS:
    """
    Depth-First Search implementation
    """
    def __init__(self, graph):
        self.graph = graph
    
    def dfs_recursive(self, node, visited=None, traversal=None):
        """DFS traversal using recursion"""
        if visited is None:
            visited = set()
            traversal = []
        
        visited.add(node)
        traversal.append(node)
        
        for neighbor in self.graph[node]:
            if neighbor not in visited:
                self.dfs_recursive(neighbor, visited, traversal)
        
        return traversal
    
    def dfs_iterative(self, start):
        """DFS traversal using stack"""
        visited = set()
        stack = [start]
        traversal = []
        
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                traversal.append(node)
                
                # Add neighbors in reverse order to simulate recursion
                for neighbor in reversed(self.graph[node]):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return traversal
    
    def dfs_path(self, start, goal):
        """Find a path using DFS"""
        stack = [(start, [start])]
        visited = set([start])
        
        while stack:
            node, path = stack.pop()
            
            if node == goal:
                return path
            
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))
        
        return None

def run_dfs():
    print("\n" + "="*60)
    print("PROGRAM 8: DFS IMPLEMENTATION")
    print("="*60)
    
    # Create a sample graph
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    dfs = DFS(graph)
    
    print("Graph adjacency list:")
    for node, neighbors in graph.items():
        print(f"  {node}: {neighbors}")
    
    start = 'A'
    
    recursive_traversal = dfs.dfs_recursive(start)
    print(f"\nDFS recursive traversal from {start}: {recursive_traversal}")
    
    iterative_traversal = dfs.dfs_iterative(start)
    print(f"DFS iterative traversal from {start}: {iterative_traversal}")
    
    goal = 'F'
    path = dfs.dfs_path(start, goal)
    print(f"Path from {start} to {goal} using DFS: {path}")


# ============================================================================
# PROGRAM 9: TRAVELLING SALESMAN PROBLEM
# ============================================================================

class TravellingSalesman:
    """
    Solve Travelling Salesman Problem using brute force
    """
    def __init__(self, distances):
        self.distances = distances
        self.n = len(distances)
        self.cities = list(range(self.n))
    
    def calculate_distance(self, path):
        """Calculate total distance of a path"""
        total = 0
        for i in range(len(path) - 1):
            total += self.distances[path[i]][path[i+1]]
        # Return to start
        total += self.distances[path[-1]][path[0]]
        return total
    
    def solve_brute_force(self):
        """Solve using brute force (try all permutations)"""
        if self.n <= 1:
            return self.cities, 0
        
        min_path = None
        min_distance = float('inf')
        
        # Fix first city to reduce permutations
        for perm in itertools.permutations(self.cities[1:]):
            path = [self.cities[0]] + list(perm)
            distance = self.calculate_distance(path)
            
            if distance < min_distance:
                min_distance = distance
                min_path = path
        
        return min_path, min_distance
    
    def solve_nearest_neighbor(self, start=0):
        """Solve using nearest neighbor heuristic"""
        unvisited = set(self.cities)
        path = [start]
        unvisited.remove(start)
        current = start
        
        while unvisited:
            next_city = min(unvisited, key=lambda city: self.distances[current][city])
            path.append(next_city)
            unvisited.remove(next_city)
            current = next_city
        
        distance = self.calculate_distance(path)
        return path, distance

def run_tsp():
    print("\n" + "="*60)
    print("PROGRAM 9: TRAVELLING SALESMAN PROBLEM")
    print("="*60)
    
    # Distance matrix for 4 cities
    distances = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    
    print("Distance matrix:")
    for i, row in enumerate(distances):
        print(f"  City {i}: {row}")
    
    tsp = TravellingSalesman(distances)
    
    # Brute force solution
    path, distance = tsp.solve_brute_force()
    print(f"\nBrute force solution:")
    print(f"  Path: {path} -> back to {path[0]}")
    print(f"  Total distance: {distance}")
    
    # Nearest neighbor solution
    path_nn, distance_nn = tsp.solve_nearest_neighbor(0)
    print(f"\nNearest neighbor heuristic:")
    print(f"  Path: {path_nn} -> back to {path_nn[0]}")
    print(f"  Total distance: {distance_nn}")


# ============================================================================
# PROGRAM 10: A* ALGORITHM
# ============================================================================

class AStar:
    """
    A* Algorithm implementation
    """
    def __init__(self, graph, heuristic):
        self.graph = graph
        self.heuristic = heuristic
    
    def a_star(self, start, goal):
        """Find shortest path using A*"""
        # Priority queue: (f_score, node, path)
        open_set = [(self.heuristic[start], start, [start])]
        closed_set = set()
        
        # g_score: cost from start to node
        g_score = {start: 0}
        
        while open_set:
            # Get node with lowest f_score
            open_set.sort()  # Simple sort for demonstration
            f, current, path = open_set.pop(0)
            
            if current == goal:
                return path, g_score[current]
            
            closed_set.add(current)
            
            for neighbor, cost in self.graph[current]:
                if neighbor in closed_set:
                    continue
                
                tentative_g = g_score[current] + cost
                
                # Check if neighbor is in open_set
                in_open = False
                for i, (_, node, _) in enumerate(open_set):
                    if node == neighbor:
                        in_open = True
                        if tentative_g < g_score.get(neighbor, float('inf')):
                            g_score[neighbor] = tentative_g
                            f = tentative_g + self.heuristic[neighbor]
                            open_set[i] = (f, neighbor, path + [neighbor])
                        break
                
                if not in_open:
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self.heuristic[neighbor]
                    open_set.append((f, neighbor, path + [neighbor]))
        
        return None, float('inf')

def run_astar():
    print("\n" + "="*60)
    print("PROGRAM 10: A* ALGORITHM")
    print("="*60)
    
    # Graph: (node, cost)
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('D', 5), ('E', 2)],
        'C': [('A', 4), ('F', 3)],
        'D': [('B', 5)],
        'E': [('B', 2), ('F', 1)],
        'F': [('C', 3), ('E', 1)]
    }
    
    # Heuristic (straight-line distance to goal 'F')
    heuristic = {
        'A': 5,
        'B': 3,
        'C': 2,
        'D': 6,
        'E': 1,
        'F': 0
    }
    
    print("Graph edges:")
    for node, edges in graph.items():
        print(f"  {node}: {edges}")
    print(f"Heuristic (estimated distance to goal): {heuristic}")
    
    astar = AStar(graph, heuristic)
    
    start = 'A'
    goal = 'F'
    path, cost = astar.a_star(start, goal)
    
    if path:
        print(f"\nA* path from {start} to {goal}: {' -> '.join(path)}")
        print(f"Total cost: {cost}")
    else:
        print(f"\nNo path found from {start} to {goal}")


# ============================================================================
# PROGRAM 11: MAP COLORING (CSP)
# ============================================================================

class MapColoring:
    """
    Map Coloring using Constraint Satisfaction Problem
    """
    def __init__(self, regions, neighbors, colors):
        self.regions = regions
        self.neighbors = neighbors
        self.colors = colors
        self.assignment = {}
    
    def is_consistent(self, region, color):
        """Check if assigning color to region is consistent"""
        for neighbor in self.neighbors[region]:
            if neighbor in self.assignment and self.assignment[neighbor] == color:
                return False
        return True
    
    def select_unassigned_region(self):
        """Select next unassigned region"""
        for region in self.regions:
            if region not in self.assignment:
                return region
        return None
    
    def backtrack(self):
        """Backtracking search"""
        if len(self.assignment) == len(self.regions):
            return self.assignment
        
        region = self.select_unassigned_region()
        
        for color in self.colors:
            if self.is_consistent(region, color):
                self.assignment[region] = color
                result = self.backtrack()
                if result:
                    return result
                del self.assignment[region]
        
        return None
    
    def solve(self):
        """Solve the map coloring problem"""
        return self.backtrack()

def run_map_coloring():
    print("\n" + "="*60)
    print("PROGRAM 11: MAP COLORING (CSP)")
    print("="*60)
    
    # Australia map coloring
    regions = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    
    neighbors = {
        'WA': ['NT', 'SA'],
        'NT': ['WA', 'SA', 'Q'],
        'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
        'Q': ['NT', 'SA', 'NSW'],
        'NSW': ['Q', 'SA', 'V'],
        'V': ['SA', 'NSW'],
        'T': []
    }
    
    colors = ['Red', 'Green', 'Blue']
    
    print(f"Regions: {regions}")
    print(f"Colors available: {colors}")
    print("\nNeighbors:")
    for region, neigh in neighbors.items():
        print(f"  {region}: {neigh}")
    
    map_csp = MapColoring(regions, neighbors, colors)
    solution = map_csp.solve()
    
    if solution:
        print("\nSolution found:")
        for region in regions:
            print(f"  {region}: {solution[region]}")
    else:
        print("\nNo solution found!")


# ============================================================================
# PROGRAM 12: TIC TAC TOE GAME
# ============================================================================

class TicTacToe:
    """
    Tic Tac Toe game implementation
    """
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
    
    def display(self):
        """Display the board"""
        print("\n")
        for i in range(0, 9, 3):
            print(f" {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} ")
            if i < 6:
                print("-----------")
        print("\n")
    
    def make_move(self, position):
        """Make a move at the given position"""
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False
    
    def check_winner(self):
        """Check if there's a winner"""
        # Winning combinations
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]               # Diagonals
        ]
        
        for line in lines:
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != ' ':
                return self.board[line[0]]
        
        if ' ' not in self.board:
            return 'Tie'
        
        return None
    
    def get_available_moves(self):
        """Get list of available moves"""
        return [i for i in range(9) if self.board[i] == ' ']
    
    def play_game(self):
        """Play a game with human players"""
        winner = None
        
        while not winner:
            self.display()
            
            move = None
            while move not in self.get_available_moves():
                try:
                    move = int(input(f"Player {self.current_player}, enter position (1-9): ")) - 1
                except:
                    continue
            
            self.make_move(move)
            winner = self.check_winner()
        
        self.display()
        
        if winner == 'Tie':
            print("It's a tie!")
        else:
            print(f"Player {winner} wins!")

def run_tic_tac_toe():
    print("\n" + "="*60)
    print("PROGRAM 12: TIC TAC TOE GAME")
    print("="*60)
    
    game = TicTacToe()
    print("Tic Tac Toe - Positions (1-9):")
    print(" 1 | 2 | 3 ")
    print("-----------")
    print(" 4 | 5 | 6 ")
    print("-----------")
    print(" 7 | 8 | 9 ")
    
    # For demonstration, we'll simulate a game instead of interactive play
    print("\nSimulating a game...")
    
    # Simulate a game
    moves = [4, 0, 2, 6, 8, 5, 7, 3, 1]  # Predefined moves
    for i, move in enumerate(moves):
        print(f"\nMove {i+1}: Player {game.current_player} at position {move+1}")
        game.make_move(move)
        game.display()
        
        winner = game.check_winner()
        if winner:
            if winner == 'Tie':
                print("Game ended in a tie!")
            else:
                print(f"Player {winner} wins!")
            break


# ============================================================================
# PROGRAM 13: MINIMAX ALGORITHM FOR GAMING
# ============================================================================

class MinimaxTicTacToe(TicTacToe):
    """
    Tic Tac Toe with Minimax AI
    """
    def __init__(self):
        super().__init__()
        self.ai_player = 'O'
        self.human_player = 'X'
    
    def evaluate(self):
        """Evaluate the board for minimax"""
        winner = self.check_winner()
        if winner == self.ai_player:
            return 10
        elif winner == self.human_player:
            return -10
        else:
            return 0
    
    def minimax(self, depth, is_maximizing):
        """Minimax algorithm"""
        score = self.evaluate()
        
        # If AI wins
        if score == 10:
            return score - depth
        # If Human wins
        if score == -10:
            return score + depth
        # If tie
        if ' ' not in self.board:
            return 0
        
        if is_maximizing:
            best = -float('inf')
            for move in self.get_available_moves():
                self.board[move] = self.ai_player
                best = max(best, self.minimax(depth + 1, False))
                self.board[move] = ' '
            return best
        else:
            best = float('inf')
            for move in self.get_available_moves():
                self.board[move] = self.human_player
                best = min(best, self.minimax(depth + 1, True))
                self.board[move] = ' '
            return best
    
    def find_best_move(self):
        """Find the best move for AI"""
        best_val = -float('inf')
        best_move = -1
        
        for move in self.get_available_moves():
            self.board[move] = self.ai_player
            move_val = self.minimax(0, False)
            self.board[move] = ' '
            
            if move_val > best_val:
                best_val = move_val
                best_move = move
        
        return best_move
    
    def play_against_ai(self):
        """Play against AI"""
        print("You are X, AI is O")
        print("Positions 1-9 as shown")
        
        winner = None
        
        while not winner:
            self.display()
            
            if self.current_player == self.human_player:
                move = None
                while move not in self.get_available_moves():
                    try:
                        move = int(input("Your move (1-9): ")) - 1
                    except:
                        continue
                self.make_move(move)
            else:
                print("AI thinking...")
                move = self.find_best_move()
                print(f"AI plays at position {move + 1}")
                self.make_move(move)
            
            winner = self.check_winner()
        
        self.display()
        
        if winner == 'Tie':
            print("It's a tie!")
        elif winner == self.ai_player:
            print("AI wins!")
        else:
            print("You win!")

def run_minimax():
    print("\n" + "="*60)
    print("PROGRAM 13: MINIMAX ALGORITHM FOR GAMING")
    print("="*60)
    
    print("Demonstrating Minimax for Tic Tac Toe")
    game = MinimaxTicTacToe()
    
    # Show a simple example
    game.board = ['X', 'O', 'X',
                  'O', ' ', ' ',
                  ' ', ' ', ' ']
    game.current_player = 'O'
    
    print("Current board:")
    game.display()
    
    best_move = game.find_best_move()
    print(f"Minimax recommends move at position {best_move + 1}")
    
    # Simulate a complete game
    print("\nSimulating a game with Minimax AI...")
    game = MinimaxTicTacToe()
    
    # Predefined moves for demonstration
    moves = [4, 0, 2, 6]  # Human moves
    for i, move in enumerate(moves):
        if game.current_player == game.human_player:
            game.make_move(move)
        else:
            ai_move = game.find_best_move()
            game.make_move(ai_move)
            print(f"AI plays at position {ai_move + 1}")
        
        game.display()
        if game.check_winner():
            break


# ============================================================================
# PROGRAM 14: ALPHA-BETA PRUNING
# ============================================================================

class AlphaBetaTicTacToe(MinimaxTicTacToe):
    """
    Tic Tac Toe with Alpha-Beta Pruning
    """
    def alphabeta(self, depth, alpha, beta, is_maximizing):
        """Alpha-Beta pruning algorithm"""
        score = self.evaluate()
        
        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        if ' ' not in self.board:
            return 0
        
        if is_maximizing:
            best = -float('inf')
            for move in self.get_available_moves():
                self.board[move] = self.ai_player
                best = max(best, self.alphabeta(depth + 1, alpha, beta, False))
                self.board[move] = ' '
                alpha = max(alpha, best)
                if beta <= alpha:
                    break  # Beta cutoff
            return best
        else:
            best = float('inf')
            for move in self.get_available_moves():
                self.board[move] = self.human_player
                best = min(best, self.alphabeta(depth + 1, alpha, beta, True))
                self.board[move] = ' '
                beta = min(beta, best)
                if beta <= alpha:
                    break  # Alpha cutoff
            return best
    
    def find_best_move_alphabeta(self):
        """Find best move using Alpha-Beta pruning"""
        best_val = -float('inf')
        best_move = -1
        alpha = -float('inf')
        beta = float('inf')
        
        for move in self.get_available_moves():
            self.board[move] = self.ai_player
            move_val = self.alphabeta(0, alpha, beta, False)
            self.board[move] = ' '
            
            if move_val > best_val:
                best_val = move_val
                best_move = move
            
            alpha = max(alpha, best_val)
        
        return best_move

def run_alpha_beta():
    print("\n" + "="*60)
    print("PROGRAM 14: ALPHA-BETA PRUNING")
    print("="*60)
    
    print("Demonstrating Alpha-Beta Pruning for Tic Tac Toe")
    game = AlphaBetaTicTacToe()
    
    # Compare Minimax vs Alpha-Beta
    game.board = ['X', 'O', ' ',
                  'O', 'X', ' ',
                  ' ', ' ', ' ']
    
    print("Current board:")
    game.display()
    
    import time
    
    start = time.time()
    minimax_move = game.find_best_move()
    minimax_time = time.time() - start
    
    start = time.time()
    alphabeta_move = game.find_best_move_alphabeta()
    alphabeta_time = time.time() - start
    
    print(f"Minimax recommends: {minimax_move + 1} (time: {minimax_time:.6f}s)")
    print(f"Alpha-Beta recommends: {alphabeta_move + 1} (time: {alphabeta_time:.6f}s)")
    print("Both algorithms find the same move, but Alpha-Beta is faster!")


# ============================================================================
# PROGRAM 15: DECISION TREE
# ============================================================================

class DecisionTree:
    """
    Simple Decision Tree implementation for classification
    """
    class Node:
        def __init__(self):
            self.feature = None
            self.value = None
            self.left = None
            self.right = None
            self.prediction = None
    
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.root = None
    
    def entropy(self, y):
        """Calculate entropy"""
        classes = np.unique(y)
        entropy_val = 0
        for cls in classes:
            p = np.sum(y == cls) / len(y)
            if p > 0:
                entropy_val -= p * np.log2(p)
        return entropy_val
    
    def information_gain(self, X, y, feature):
        """Calculate information gain for a feature"""
        # Total entropy
        total_entropy = self.entropy(y)
        
        # Split based on feature values
        values = np.unique(X[:, feature])
        weighted_entropy = 0
        
        for value in values:
            subset_indices = X[:, feature] == value
            subset_y = y[subset_indices]
            weight = len(subset_y) / len(y)
            weighted_entropy += weight * self.entropy(subset_y)
        
        return total_entropy - weighted_entropy
    
    def build_tree(self, X, y, depth=0):
        """Build decision tree recursively"""
        node = self.Node()
        
        # Check stopping conditions
        if len(np.unique(y)) == 1 or depth >= self.max_depth:
            node.prediction = np.bincount(y).argmax()
            return node
        
        # Find best feature to split on
        best_gain = -1
        best_feature = None
        
        for feature in range(X.shape[1]):
            gain = self.information_gain(X, y, feature)
            if gain > best_gain:
                best_gain = gain
                best_feature = feature
        
        if best_gain <= 0:
            node.prediction = np.bincount(y).argmax()
            return node
        
        node.feature = best_feature
        
        # Split data
        values = np.unique(X[:, best_feature])
        left_indices = X[:, best_feature] == values[0]
        right_indices = X[:, best_feature] == values[1] if len(values) > 1 else []
        
        node.left = self.build_tree(X[left_indices], y[left_indices], depth + 1)
        node.left.value = values[0]
        
        if len(values) > 1:
            node.right = self.build_tree(X[right_indices], y[right_indices], depth + 1)
            node.right.value = values[1]
        
        return node
    
    def fit(self, X, y):
        """Fit the decision tree"""
        self.root = self.build_tree(X, y)
    
    def predict_sample(self, node, sample):
        """Predict a single sample"""
        if node.prediction is not None:
            return node.prediction
        
        if sample[node.feature] == node.left.value:
            return self.predict_sample(node.left, sample)
        elif node.right and sample[node.feature] == node.right.value:
            return self.predict_sample(node.right, sample)
        else:
            return np.bincount([]).argmax()  # Default
    
    def predict(self, X):
        """Predict multiple samples"""
        return np.array([self.predict_sample(self.root, x) for x in X])
    
    def print_tree(self, node=None, depth=0):
        """Print the decision tree"""
        if node is None:
            node = self.root
        
        indent = "  " * depth
        
        if node.prediction is not None:
            print(f"{indent}Predict: {node.prediction}")
        else:
            print(f"{indent}Feature {node.feature}?")
            if node.left:
                print(f"{indent}  If = {node.left.value}:")
                self.print_tree(node.left, depth + 2)
            if node.right:
                print(f"{indent}  If = {node.right.value}:")
                self.print_tree(node.right, depth + 2)

def run_decision_tree():
    print("\n" + "="*60)
    print("PROGRAM 15: DECISION TREE")
    print("="*60)
    
    # Create a simple dataset
    # Features: [Outlook, Temperature, Humidity, Wind]
    # Outlook: 0=Sunny, 1=Overcast, 2=Rainy
    # Temperature: 0=Hot, 1=Mild, 2=Cool
    # Humidity: 0=High, 1=Normal
    # Wind: 0=Weak, 1=Strong
    # Target: 0=No Play, 1=Play
    
    X = np.array([
        [0, 0, 0, 0],  # Sunny, Hot, High, Weak
        [0, 0, 0, 1],  # Sunny, Hot, High, Strong
        [1, 0, 0, 0],  # Overcast, Hot, High, Weak
        [2, 1, 0, 0],  # Rainy, Mild, High, Weak
        [2, 2, 1, 0],  # Rainy, Cool, Normal, Weak
        [2, 2, 1, 1],  # Rainy, Cool, Normal, Strong
        [1, 2, 1, 1],  # Overcast, Cool, Normal, Strong
        [0, 1, 0, 0],  # Sunny, Mild, High, Weak
        [0, 2, 1, 0],  # Sunny, Cool, Normal, Weak
        [2, 1, 1, 0],  # Rainy, Mild, Normal, Weak
        [0, 1, 1, 1],  # Sunny, Mild, Normal, Strong
        [1, 1, 0, 1],  # Overcast, Mild, High, Strong
        [1, 0, 1, 0],  # Overcast, Hot, Normal, Weak
        [2, 1, 0, 1]   # Rainy, Mild, High, Strong
    ])
    
    y = np.array([0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0])
    
    print("Dataset for playing tennis:")
    feature_names = ["Outlook", "Temperature", "Humidity", "Wind"]
    print("Features: " + ", ".join(feature_names))
    print("Target: Play Tennis (0=No, 1=Yes)")
    
    tree = DecisionTree(max_depth=3)
    tree.fit(X, y)
    
    print("\nDecision Tree structure:")
    tree.print_tree()
    
    # Make predictions
    new_samples = np.array([
        [0, 1, 1, 0],  # Sunny, Mild, Normal, Weak
        [2, 0, 0, 1]   # Rainy, Hot, High, Strong
    ])
    
    predictions = tree.predict(new_samples)
    
    print("\nPredictions for new samples:")
    for i, sample in enumerate(new_samples):
        features = [feature_names[j] + "=" + str(sample[j]) for j in range(len(sample))]
        print(f"Sample {i+1}: {', '.join(features)} -> {'Play' if predictions[i] == 1 else 'No Play'}")


# ============================================================================
# PROGRAM 16: FEED FORWARD NEURAL NETWORK
# ============================================================================

class FeedForwardNeuralNetwork:
    """
    Simple Feed Forward Neural Network with backpropagation
    """
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.1):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.lr = learning_rate
        
        # Initialize weights and biases
        self.W1 = np.random.randn(input_size, hidden_size) * 0.1
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.1
        self.b2 = np.zeros((1, output_size))
    
    def sigmoid(self, x):
        """Sigmoid activation function"""
        return 1 / (1 + np.exp(-np.clip(x, -250, 250)))
    
    def sigmoid_derivative(self, x):
        """Derivative of sigmoid"""
        return x * (1 - x)
    
    def forward(self, X):
        """Forward propagation"""
        # Hidden layer
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        
        # Output layer
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.sigmoid(self.z2)
        
        return self.a2
    
    def backward(self, X, y, output):
        """Backward propagation"""
        m = X.shape[0]
        
        # Output layer error
        self.output_error = y - output
        self.output_delta = self.output_error * self.sigmoid_derivative(output)
        
        # Hidden layer error
        self.hidden_error = self.output_delta.dot(self.W2.T)
        self.hidden_delta = self.hidden_error * self.sigmoid_derivative(self.a1)
        
        # Update weights and biases
        self.W2 += self.a1.T.dot(self.output_delta) * self.lr
        self.b2 += np.sum(self.output_delta, axis=0, keepdims=True) * self.lr
        self.W1 += X.T.dot(self.hidden_delta) * self.lr
        self.b1 += np.sum(self.hidden_delta, axis=0, keepdims=True) * self.lr
    
    def train(self, X, y, epochs=1000, verbose=True):
        """Train the network"""
        losses = []
        
        for epoch in range(epochs):
            # Forward pass
            output = self.forward(X)
            
            # Calculate loss (mean squared error)
            loss = np.mean((y - output) ** 2)
            losses.append(loss)
            
            # Backward pass
            self.backward(X, y, output)
            
            if verbose and epoch % 200 == 0:
                print(f"Epoch {epoch}, Loss: {loss:.6f}")
        
        return losses
    
    def predict(self, X):
        """Make predictions"""
        output = self.forward(X)
        return (output > 0.5).astype(int)
    
    def calculate_accuracy(self, X, y):
        """Calculate accuracy"""
        predictions = self.predict(X)
        accuracy = np.mean(predictions == y) * 100
        return accuracy

def run_neural_network():
    print("\n" + "="*60)
    print("PROGRAM 16: FEED FORWARD NEURAL NETWORK")
    print("="*60)
    
    # Create XOR dataset
    X = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ])
    
    y = np.array([[0], [1], [1], [0]])  # XOR
    
    print("XOR Dataset:")
    for i in range(len(X)):
        print(f"Input: {X[i]} -> Output: {y[i][0]}")
    
    # Create and train network
    nn = FeedForwardNeuralNetwork(input_size=2, hidden_size=4, output_size=1, learning_rate=0.5)
    
    print("\nTraining Neural Network...")
    losses = nn.train(X, y, epochs=2000, verbose=True)
    
    # Test the network
    print("\nTesting trained network:")
    predictions = nn.predict(X)
    for i in range(len(X)):
        print(f"Input: {X[i]}, Target: {y[i][0]}, Prediction: {predictions[i][0]}")
    
    accuracy = nn.calculate_accuracy(X, y)
    print(f"\nAccuracy: {accuracy:.2f}%")
    
    # Show final weights
    print("\nNetwork weights after training:")
    print(f"W1 shape: {nn.W1.shape}")
    print(f"W2 shape: {nn.W2.shape}")


# ============================================================================
# MAIN FUNCTION TO RUN ALL PROGRAMS
# ============================================================================

def main():
    """Run all 16 programs"""
    print("\n" + "="*80)
    print("RUNNING ALL 16 PYTHON PROGRAMS")
    print("="*80)
    
    programs = [
        run_eight_puzzle,
        run_eight_queen,
        run_water_jug,
        run_crypt_arithmetic,
        run_missionaries_cannibals,
        run_vacuum_cleaner,
        run_bfs,
        run_dfs,
        run_tsp,
        run_astar,
        run_map_coloring,
        run_tic_tac_toe,
        run_minimax,
        run_alpha_beta,
        run_decision_tree,
        run_neural_network
    ]
    
    for i, program in enumerate(programs, 1):
        program()
        input(f"\nProgram {i} completed. Press Enter to continue...")

if __name__ == "__main__":
    # To run a specific program, uncomment the line below
    # run_eight_puzzle()
    
    # To run all programs, uncomment the line below
    main()
    
    # Or run individual programs:
    # run_eight_puzzle()
    # run_eight_queen()
    # run_water_jug()
    # run_crypt_arithmetic()
    # run_missionaries_cannibals()
    # run_vacuum_cleaner()
    # run_bfs()
    # run_dfs()
    # run_tsp()
    # run_astar()
    # run_map_coloring()
    # run_tic_tac_toe()
    # run_minimax()
    # run_alpha_beta()
    # run_decision_tree()
    # run_neural_network()