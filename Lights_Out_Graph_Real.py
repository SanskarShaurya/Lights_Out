import pulp as p

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, vertex1, vertex2, weight):
        if vertex1 in self.adjacency_list and vertex2 in self.adjacency_list:
            self.adjacency_list[vertex1].append((vertex2,weight))
            self.adjacency_list[vertex2].append((vertex1,weight))

    def display(self):
        for vertex, neighbors in self.adjacency_list.items():
            print(f"{vertex}: {neighbors}")


# Create a LP minimization problem
problem = p.LpProblem('Problem', p.LpMinimize)

n = int(input("Enter number of sectors: "))

graph = Graph()
for i in range(n):
    graph.add_vertex(i)

m = int(input("Enter number of edges: "))
for _ in range(m):
    i, j, k = map(int, input("Enter the vertices between which an edge is present and the corresponding edge weight: ").split())
    if i == -1:
        break
    graph.add_edge(i, j, k)

graph.display()

threshold = int(input("Enter the threshold value: "))

y = [0 for _ in range(n)]
for _ in range(n):
    i = int(input(f"Enter the initial money spent on sector {_}: "))
    y[_] = i

u = [0 for _ in range(n)]
for _ in range(n):
    i = int(input(f"Enter the reward constant of sector {_}: "))
    u[_] = i

alpha = [0 for _ in range(n)]
for _ in range(n):
    i = int(input(f"Enter the lower limit of sector {_}: "))
    alpha[_] = i

beta = [0 for _ in range(n)]
for _ in range(n):
    i = int(input(f"Enter the upper limit of sector {_}: "))
    beta[_] = i

#Create a 2D array of binary variables
x=[None for i in range(n)] 
z=[None for i in range(n)]

# Create problem variables
for i in range(n):
    x[i] = p.LpVariable(f"x_{i}")

# Objective function
s = 0
for i in range(n):
    s += x[i]
  
problem += s

# Constraints
for i in range(n):
    neighboring_cells = graph.adjacency_list[i]
    c = x[i]*u[i]
    for neighbor in neighboring_cells:
            c += x[neighbor[0]]*neighbor[1]*u[i]
    problem += c + y[i]>= threshold
    problem += x[i]>=alpha[i]
    problem += x[i]<=beta[i]

solver = p.PULP_CBC_CMD()
problem.solve(solver)


# Print the status of the problem (should be 1 for Optimal)
print("Status:", p.LpStatus[problem.status])

# Print the values of the binary variables
for i in range(n):
    print(x[i], "=", x[i].value())

# Print the optimized objective function value
print("Objective value:", p.value(problem.objective))
