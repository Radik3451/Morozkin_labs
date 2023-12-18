import matplotlib.pyplot as plt

# Данные
data = [
    [0.541, 0.541, 0.614, 53.285],
    [0.464, 0.464, 0.527, 53.285],
    [0.387, 0.387, 0.440, 53.285],
    [0.310, 0.310, 0.352, 53.285],
    [0.232, 0.232, 0.264, 53.285],
    [0.155, 0.155, 0.176, 53.285],
    [0.078, 0.078, 0.088, 53.285],
    [0.000, 0.000, 0.000, 53.285]
]

# Индексы для x-оси (0, 1, 2, ...)
x_values = list(range(len(data)))

# Построение графика для каждого столбца
for col_index in range(len(data[0])):
    y_values = [row[col_index] for row in data]
    plt.plot(x_values, y_values, label=f'Column {col_index + 1}')

# Настройка графика
plt.xlabel('Index')
plt.ylabel('Value')
plt.legend()
plt.title('Графики столбцов')

# Отображение графика
plt.show()