import pulp as p

# Create a LP minimization problem
problem = p.LpProblem('Problem', p.LpMinimize)

n = int(input("n:"))
m = int(input("m:"))
alpha = [[None for i in range(m)] for i in range(n)]

print("Enter the initial state of the grid: ")

for i in range(n):
    alpha[i] = [int(x) for x in input().split()]

#Create a 2D array of binary variables
x=[[None for i in range(m)] for i in range(n)]
z=[[None for i in range(m)] for i in range(n)]
# Create problem variables
for i in range(n):
    for j in range(m):
        x[i][j] = p.LpVariable(f"x_{i}{j}", cat=p.LpBinary)
        z[i][j] = p.LpVariable(f"z_{i}{j}", cat=p.LpInteger)

# Objective function
s = 0
for i in range(n):
    for j in range(m):
        s += x[i][j] 
  
problem += s

# Constraints
for i in range(n):
    for j in range(m):
        neighboring_cells = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        c = x[i][j]
        for neighbor in neighboring_cells:
            if 0 <= neighbor[0] < n and 0 <= neighbor[1] < m:
                c += x[neighbor[0]][neighbor[1]]
        problem += c == 2*z[i][j] + alpha[i][j]    

solver = p.PULP_CBC_CMD()
problem.solve(solver)


# Print the status of the problem (should be 1 for Optimal)
print("Status:", p.LpStatus[problem.status])

# Print the values of the binary variables
for i in range(n):
    for j in range(m):
        print(x[i][j], "=", x[i][j].value())

# Print the optimized objective function value
print("Objective value:", p.value(problem.objective))
