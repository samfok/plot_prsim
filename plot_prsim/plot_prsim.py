import numpy as np
import matplotlib.pyplot as plt

class PRSIMPlotter(object):
    """Plots data from a PRSIM run
    
    Parameters
    ----------
    fsim: string
        file containing PRSIM outputs
    interact: boolean
        whether to turn on matplotlib interactive
    """
    def __init__(self, fsim, interact=False):
        self.signals = {}
        self.max_time = None
        self.plot_rowsize = 1.5
        self.read_file(fsim)
        if interact:
            plt.ion()

    def read_file(self, fsim):
        """reads in a file of PRSIM results"""
        with open(fsim, 'r') as fh:
            lines = fh.readlines()
            time = 0
            for line in lines:
                tokens = line.strip().split(' ')
                if len(tokens) > 0:
                    if tokens[0].isnumeric():
                        time = int(tokens[0])
                        signal = tokens[1]
                        if signal not in self.signals:
                            value = tokens[3]
                            self.signals[signal] = {
                                "v0":value,
                                "t0":time,
                                "transitions":[]}
                        else:
                            self.signals[signal]["transitions"].append(time)
            self.max_time = time

    def get_signals(self):
        """Get the signals available"""
        return list(self.signals.keys())

    def plot_signal(self, ax, signal):
        """Plots an individual signal"""
        transitions = self.signals[signal]["transitions"]
        n_transitions = len(transitions)
        n_pts = 2 + 2*n_transitions
        time = np.zeros(n_pts)
        trace = np.zeros(n_pts)

        time[0] = self.signals[signal]["t0"]
        trace[0] = self.signals[signal]["v0"]
        for idx in range(n_transitions):
            time[2*idx+1] = transitions[idx]
            time[2*idx+2] = transitions[idx]
            trace[2*idx+1] = trace[2*idx]
            trace[2*idx+2] = -trace[2*idx]+1
        time[-1] = self.max_time
        trace[-1] = trace[-2]

        ax.plot(time, trace)
        ax.set_ylim((-0.1, 1.1))
        ax.set_yticks([0.5])
        ax.set_yticklabels([signal])

    def plot_signals(self, signals):
        """Plots the specified signals"""
        n_signals = len(signals)
        fig, axs = plt.subplots(
            nrows=n_signals,
            figsize=(8, self.plot_rowsize*n_signals),
            sharex=True)
        for ax, signal in zip(axs, signals):
            self.plot_signal(ax, signal)
        axs[0].set_xlim((0, self.max_time))
        return fig, axs


    def plot(self):
        """Plots all of the available"""
        self.plot_signals(sorted(self.get_signals()))

    @staticmethod
    def show():
        plt.show()

