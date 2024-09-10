import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Настройки графика
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'b-', animated=True)
plt.xlim(0, 2 * np.pi)
plt.ylim(-1.5, 1.5)

# Функция инициализации графика
def init():
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-1.5, 1.5)
    return ln,

# Функция обновления данных на графике
def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    if len(xdata) > 100:  # Ограничение количества отображаемых точек
        xdata.pop(0)
        ydata.pop(0)
    ln.set_data(xdata, ydata)
    ax.set_xlim(frame - 2 * np.pi, frame)  # Движение графика слева направо
    return ln,

# Настройка анимации
ani = animation.FuncAnimation(fig, update, frames=np.linspace(0, 10 * np.pi, 1000),
                              init_func=init, blit=True, interval=50)

plt.show()

