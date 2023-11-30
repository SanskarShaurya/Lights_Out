import pulp as p

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, vertex1, vertex2):
        if vertex1 in self.adjacency_list and vertex2 in self.adjacency_list:
            self.adjacency_list[vertex1].append(vertex2)
            self.adjacency_list[vertex2].append(vertex1)

    def display(self):
        for vertex, neighbors in self.adjacency_list.items():
            print(f"{vertex}: {neighbors}")

# Create a LP minimization problem
problem = p.LpProblem('Problem', p.LpMinimize)

n = int(input("Enter number of nodes: "))

graph = Graph()
for i in range(n):
    graph.add_vertex(i)

m = int(input("Enter number of edges: "))
for _ in range(m):
    i, j = map(int, input("Enter the vertices between which an edge is present: ").split())
    if i == -1:
        break
    graph.add_edge(i, j)

k = int(input("Enter the number of blocks turned on :"))
alpha = [1 for _ in range(n)]
for _ in range(k):
    i = int(input("Enter the node: "))
    alpha[i] = 0

#Create a 2D array of binary variables
x=[None for i in range(n)] 
z=[None for i in range(n)]

# Create problem variables
for i in range(n):
    x[i] = p.LpVariable(f"x_{i}", cat=p.LpBinary)
    z[i] = p.LpVariable(f"z_{i}", cat=p.LpInteger)

# Objective function
s = 0
for i in range(n):
    s += x[i]
  
problem += s

# Constraints
for i in range(n):
    neighboring_cells = graph.adjacency_list[i]
    c = x[i]
    for neighbor in neighboring_cells:
            c += x[neighbor]
    problem += c == 2*z[i] + alpha[i]

solver = p.PULP_CBC_CMD()
problem.solve(solver)


# Print the status of the problem (should be 1 for Optimal)
print("Status:", p.LpStatus[problem.status])

# Print the values of the binary variables
for i in range(n):
    print(x[i], "=", x[i].value())

# Print the optimized objective function value
print("Objective value:", p.value(problem.objective))
