import time

from numba import jit
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
from scipy.integrate import solve_ivp
# Cri = mpatch.Circle((0, 0), 1, angle=30, color="pink", alpha=0.2, capstyle="round")
# Py = mpatch.Arrow(1, 2, 2, 2)
import numpy as np

def drawReact(x, y, alpha, color):
    rect = mpatch.Rectangle((x, y), 3, 3, color=color, alpha=alpha)
    return rect

@jit
def func(t, x):
    f = [(10.0 * 1 ** 4) / (1 ** 4 + (0.4 * x[1]) ** 4) - 0.5 * x[0] + 18.7 * np.cos(t),
         (10.0 * 1 ** 4) / (1 ** 4 + (0.4 * x[0]) ** 4) - 0.5 * x[1]
         ]
    return np.array(f)


def func2(t, x):
    f = [(11 * 1 ** 4) / (1 ** 4 + (0.4 * x[1]) ** 4) - 0.5 * x[0],
         (11 * 1 ** 4) / (1 ** 4 + (0.4 * x[0]) ** 4) - 0.5 * x[1]
         ]
    return np.array(f)


def noLinerXy(x0):
    # x00 = np.array([26.19410977, 34.06791718])
    x00 = x0
    tstart = time.time()
    x = solve_ivp(func, (0, 2 * np.pi), x00,
                  # method = 'DOP853',
                  method='RK45',
                  rtol=1e-8)
    print('my solver:', time.time() - tstart)
    return x


if __name__ == '__main__':
    fig, ax = plt.subplots()
    rectList = [[1, 1], [4, 1]]
    # x00 = np.array([26.19410977, 34.06791718])
    x00 = np.array([26, 0.7])
    while True:
        print(x00)
        xy = noLinerXy(x00).y
        x00 = xy[:, -1]
        maxNum = max(max(abs(xy[0])), max(abs(xy[1])))
        for item in range(len(xy[0])):
            ax.set_xlim(0, 8)
            ax.set_ylim(0, 8)
            ax.add_patch(drawReact(rectList[0][0], rectList[0][1], abs(xy[0][item] / maxNum), 'blue'))
            ax.add_patch(drawReact(rectList[1][0], rectList[1][1], abs(xy[1][item] / maxNum), 'blue'))
            plt.pause(0.01)
            # plt.savefig('./img3/' + str(i) + '.jpg')
            plt.cla()
