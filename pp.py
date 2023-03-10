import sys, json
import time
import numpy as np
from numpy import cos, sin
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

import pptools


def func(t, x, data):
    v = []
    for i in np.arange(len(data.dic['func'])):
        v.append(eval(data.dic['func'][i]))
    return v


def main():
    data = pptools.init()

    state0 = data.dic['x0']
    tick = data.dic['tick']

    fperiod = 2.0 * np.pi
    duration = fperiod * data.dic['period']
    tspan = np.arange(0, duration, tick)
    running = True
    while running:
        if pptools.window_closed(data.ax) == True:
            sys.exit()
        state = solve_ivp(func, (0, duration), state0,
                          t_eval=tspan,
                          rtol=1e-6,
                          # method = 'DOP853',
                          method='RK45', args=(data,))
        for i in range(data.dic['fun_num']):
            plt.subplot(data.dic['fig_arr']+i)
            if data.visual_orbit == 1:
                plt.plot(state.y[0, :], state.y[i, :],
                         linewidth=1, color=(0, 0, 0),
                         ls="-", alpha=data.dic['alpha'])
            plt.plot(state.y[0, -1], state.y[i, -1], 'o',
                     markersize=2, color="red", alpha=data.dic['alpha'])

        state0 = data.dic['x0'] = state.y[:, -1]
        plt.pause(0.01)  # REQIRED


if __name__ == '__main__':
    main()
