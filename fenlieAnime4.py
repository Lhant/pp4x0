import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
from scipy.integrate import solve_ivp
# Cri = mpatch.Circle((0, 0), 1, angle=30, color="pink", alpha=0.2, capstyle="round")
# Py = mpatch.Arrow(1, 2, 2, 2)
import numpy as np


def keyin(event):
    if event.key == 'q':
        plt.cla()
        plt.close('all')
        print("quit")
        sys.exit()


def drawReact(x, y, alpha, color):
    rect = mpatch.Rectangle((x, y), 3, 3, color=color, alpha=alpha)
    return rect


def func(t, x):
    f = [(11.0 * 1 ** 4) / (1 ** 4 + (0.4 * 0.5 * (x[1] + x[2])) ** 4) - 0.5 * x[0] + 12 * np.cos(t),
         (11.0 * 1 ** 4) / (1 ** 4 + (0.4 * 0.5 * (x[0] + x[3])) ** 4) - 0.5 * x[1],
         (11.0 * 1 ** 4) / (1 ** 4 + (0.4 * 0.5 * (x[0] + x[3])) ** 4) - 0.5 * x[2],
         (11.0 * 1 ** 4) / (1 ** 4 + (0.4 * 0.5 * (x[1] + x[1])) ** 4) - 0.5 * x[3]
         ]
    return np.array(f)


def noLinerXy(x0):
    # x00 = np.array([26.19410977, 34.06791718])
    x00 = x0
    x = solve_ivp(func, (0, 2 * np.pi), x00,
                  # method = 'DOP853',
                  method='RK45',
                  rtol=1e-8)
    return x


if __name__ == '__main__':
    fig, ax = plt.subplots()
    rectList = [[1, 4], [4, 4], [1, 1], [4, 1]]
    # chaos
    # x00 = np.array([11.21, 6.36, 6.36, 2.15])
    # 黑白相间
    x00 = np.array([2.67, 0.0058, 0.0058, 2.2])
    while True:
        # plt.connect('key_press_event',
        #             lambda event: keyin(event))
        plt.connect('key_press_event', keyin)
        xy = noLinerXy(x00).y
        x00 = xy[:, -1]
        maxNum = max(abs(np.max(xy)), abs(np.min(xy)))
        # maxNum = max(max(abs(xy[0])), max(abs(xy[1])))
        for item in range(len(xy[0])):
            ax.set_xlim(0, 8)
            ax.set_ylim(0, 8)
            ax.add_patch(drawReact(rectList[0][0], rectList[0][1], abs(xy[0][item] / maxNum), 'black'))
            ax.add_patch(drawReact(rectList[1][0], rectList[1][1], abs(xy[1][item] / maxNum), 'black'))
            ax.add_patch(drawReact(rectList[2][0], rectList[2][1], abs(xy[2][item] / maxNum), 'black'))
            ax.add_patch(drawReact(rectList[3][0], rectList[3][1], abs(xy[3][item] / maxNum), 'black'))
            plt.pause(0.01)
            plt.cla()
