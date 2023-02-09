import sys, json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
from matplotlib.backends.backend_pdf import PdfPages


class DataStruct():
    def __init__(self):
        if len(sys.argv) != 2:
            print(f"Usage: python {sys.argv[0]} filename")
            sys.exit(0)
        fd = open(sys.argv[1], 'r')
        self.dic = json.load(fd)
        fd.close()
        self.param_ptr = 0
        self.ax = None
        self.fig = None
        if self.dic.get('alpha', None) == None:
            self.dic['alpha'] = 1.0


def init():
    plt.rcParams['keymap.save'].remove('s')
    plt.rcParams['keymap.quit'].remove('q')
    data = DataStruct()

    data.fig = plt.figure(figsize=(10, 10))
    data.ax = [data.fig.add_subplot(i) for i in range(221, 225)]
    redraw_frame(data)
    data.visual_orbit = 1

    plt.connect('button_press_event',
                lambda event: on_click(event, data))
    plt.connect('key_press_event',
                lambda event: keyin(event, data))
    #	plt.connect('close_event',
    #		lambda event: window_closed(data.ax))
    plt.ion()  # I/O non blocking
    return data


def redraw_frame(data):
    # plt.rcParams["text.usetex"]  = True
    # rc("font", **{"family": "serif", "serif": ["Computer Modern"]})
    # rc("text", usetex=True)
    xr = data.dic['xrange']
    yr = data.dic['yrange']
    for axItem in data.ax:
        axItem.set_xlim(xr)
        axItem.set_ylim(yr)
        # data.ax.set_xlabel(r'$\sin x$')
        # data.ax.set_ylabel(r'$y$')
        axItem.set_xlabel("x")
        axItem.set_ylabel("y")


# data.ax.grid(c = 'gainsboro', zorder = 9)

class jsonconvert(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(jsonconvert, self).default(obj)


def window_closed(ax):
    fig = ax[0].figure.canvas.manager
    mgr = plt._pylab_helpers.Gcf.figs.values()
    return fig not in mgr


def keyin(event, data):
    ptr = data.param_ptr
    if event.key == 'q':
        plt.close('all')
        print("quit")
        sys.exit()
    elif event.key == 'w':
        jd = json.dumps(data.dic, cls=jsonconvert)
        print(jd, end='\n')
        with open("__ppout__.json", 'w') as fd:
            json.dump(data.dic, fd, indent=4, cls=jsonconvert)
        print("now writing...", end="")
        pdf = PdfPages('snapshot.pdf')
        pdf.savefig()
        pdf.close()
        print("done.")
    elif event.key == ' ' or event.key == 'e':
        # plt.cla()
        for i in range(221, 225):
            plt.subplot(i)
            plt.cla()
        redraw_frame(data)
    elif event.key == 'f':
        plt.cla()
        redraw_frame(data)
        data.visual_orbit = 1 - data.visual_orbit
    elif event.key == 's':
        for i in data.dic['params']:
            print(i, end=' ')
        print(data.dic['x0'])
        print(data.dic['period'])
    elif event.key == 'p':
        data.param_ptr += 1
        if data.param_ptr >= len(data.dic['params']):
            data.param_ptr = 0
        print(f"changable parameter: {data.param_ptr}")
    elif event.key == 'up':
        ptr = data.param_ptr
        data.dic['params'][ptr] += data.dic['dparams'][ptr]
    elif event.key == 'down':
        ptr = data.param_ptr
        data.dic['params'][ptr] -= data.dic['dparams'][ptr]
    show_param(data)


def show_param(data):
    plt.subplot(221)
    s = ""
    cnt = 0
    for key in data.dic['params']:
        s += " p{:d}: {:.5f}  ".format(cnt, key)
        cnt += 1
    plt.title(s, color='b')


def on_click(event, data):
    print(event.inaxes == data.ax[0])
    if event.xdata == None or event.ydata == None:
        return
    # if event.inaxes == data.ax[0]:
    #     print('x0,x0')
    #     print(data.dic['x0'])
    #     data.dic['x0'][0] = event.xdata
    #     data.dic['x0'][0] = event.ydata
    #     plt.subplot(221)
    #     plt.plot(event.xdata, event.ydata, 'o', markersize=2, color="blue")
    #     print(data.dic['x0'])
    if event.inaxes == data.ax[1]:
        print('x0,x1')
        print(data.dic['x0'])
        data.dic['x0'][0] = event.xdata
        data.dic['x0'][1] = event.ydata
        plt.subplot(222)
        plt.plot(event.xdata, event.ydata, 'o', markersize=2, color="blue")
        print(data.dic['x0'])
    if event.inaxes == data.ax[2]:
        print('x0,x2')
        print(data.dic['x0'])
        data.dic['x0'][0] = event.xdata
        data.dic['x0'][2] = event.ydata
        plt.subplot(223)
        plt.plot(event.xdata, event.ydata, 'o', markersize=2, color="blue")
        print(data.dic['x0'])
    if event.inaxes == data.ax[3]:
        print('x0,x3')
        print(data.dic['x0'])
        data.dic['x0'][0] = event.xdata
        data.dic['x0'][3] = event.ydata
        plt.subplot(224)
        plt.plot(event.xdata, event.ydata, 'o', markersize=2, color="blue")
        print(data.dic['x0'])
    redraw_frame(data)
    show_param(data)
    return


def on_close():
    running = False
