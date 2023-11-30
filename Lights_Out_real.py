import pulp as p

# Create a LP minimization problem
problem = p.LpProblem('Problem', p.LpMinimize)

n = int(input("n:"))
m = int(input("m:"))


w0 = 0.2
w1 = 0.1
threshold = 1

# k = int(input("Enter the number of blocks turned off :"))
alpha = [[0 for i in range(m)] for i in range(n)]
# for _ in range(k):
#     i, j = map(int, input("Enter the block index: ").split())
#     alpha[i][j] = 0

#Create a 2D array of binary variables
x=[[None for i in range(m)] for i in range(n)]
z=[[None for i in range(m)] for i in range(n)]
# Create problem variables
for i in range(n):
    for j in range(m):
        x[i][j] = p.LpVariable(f"x_{i}{j}")

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
        c = w0*x[i][j]
        for neighbor in neighboring_cells:
            if 0 <= neighbor[0] < n and 0 <= neighbor[1] < m:
                c += w1*x[neighbor[0]][neighbor[1]]
        problem += c >= threshold   
        problem += x[i][j]>=0

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
