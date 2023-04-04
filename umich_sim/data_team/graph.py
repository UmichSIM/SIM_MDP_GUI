import matplotlib.pyplot as plt
import numpy as np
import csv

print('hi')

xpoints = np.array([0, 6])
ypoints = np.array([0, 250])

#plt.plot(xpoints, ypoints)
#plt.show()


# Read CSV file
with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

# Convert data to NumPy arrays
col1 = np.array([float(row[1]) for row in data])
col2 = np.array([float(row[2]) for row in data])

# Print the arrays
print(col1)
print(col2)

plt.plot(col1, col2)

fig2 = plt.figure()
plt.plot(col2, col1)
plt.show()
