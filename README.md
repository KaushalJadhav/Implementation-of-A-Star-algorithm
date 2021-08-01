# Implementation-of-A-Star-algorithm
Studied the variations in time and number of nodes traversed using different heuristics and cost functions

Introduction
A-star (also referred to as A*) is one of the most successful search algorithms to find the shortest path between nodes or graphs. It is an informed search algorithm, as it uses information about path cost and also uses heuristics to find the solution. A* algorithm is a searching algorithm that searches for the shortest path between the initial and the final state. 
 It is used in various applications, such as maps. In maps, the A* algorithm is used to calculate the shortest distance between the source (initial state) and the destination (final state). 
 Example: Imagine a square grid which possesses many obstacles, scattered randomly. The initial and the final cell is provided. The aim is to reach the final cell in the shortest amount of time. Here A* search Algorithm comes to the rescue. 
Explanation: 
A* algorithm has 3 parameters.
1) g: It is the cost of moving from the initial cell to the current cell. Basically, it is the sum of all the cells that have been visited since leaving the first cell.
2) h: It is also known as the heuristic value, it is the estimated cost of moving from the current cell to the final cell. The actual cost cannot be calculated until the final cell is reached. Hence, h is the estimated cost. One must make sure that there is never an over estimation of the cost.
3) f: It is the sum of g and h. 
So, f = g + h 
The algorithm makes its decisions by taking the f-value into account. The algorithm selects the smallest f-valued cell and moves to that cell. This process continues until the algorithm reaches its goal cell. 
Terminology:
    • Node (also called State) — all potential positions or stops with a unique identification 
    • Transition — the act of moving between states or nodes.
    • Starting Node — where to start searching 
    • Goal Node — the target to stop searching
    • Search Space — a collection of nodes, like all board positions of a board game 
    • Cost — numerical value (say distance, time, or financial expense) for the path from a node to another node. 
    • g(n) —the exact cost of the path from the starting node to any node n 
    • h(n) —the heuristic estimated cost from node n to the goal node 
    • f(n) — lowest cost in the neighbouring node n 
Each time A* enters a node, it calculates the cost, f(n) (n being the neighbouring node), to travel to all of the neighbouring nodes and then enters the node with the lowest value of f(n). These values are calculated using following formula.
 f(n) = g(n) + h(n)
