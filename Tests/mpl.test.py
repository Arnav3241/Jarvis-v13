import matplotlib.pyplot as plt

# Data from the paragraph
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
temperatures = [4, 5, 9, 13, 18, 23, 27, 26, 21, 15, 9, 5]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(months, temperatures, marker='o', linestyle='-', color='b')

# Add titles and labels
plt.title('Average Monthly Temperature Over a Year')
plt.xlabel('Month')
plt.ylabel('Average Temperature (°C)')

# Display the graph
plt.grid(True)
plt.show()