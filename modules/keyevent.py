import matplotlib.pyplot as plt


class KeyEvent(object):
    def __init__(self, ax=None):
        self.ax = ax or plt.gca()

        def selector(event):
            if event.key in ['Q', 'q']:
                plt.close()

        self.ax.figure.canvas.mpl_connect('key_press_event', selector)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.release)

    def release(self, event):
        self.ax.figure.canvas.draw()
