import numpy as np
import matplotlib.pyplot as plt

class PRSIMPlotter(object):
    """Plots data from a PRSIM run
    
    Parameters
    ----------
    fsim: string
        file containing PRSIM outputs
    max_events: int or None
        maximum number of events to read in 
    ignore_timing: Boolean
        whether to ignore the timing information in the data
        if you only care about the transition sequence
    """
    def __init__(self, fsim, max_events=500, ignore_timing=False):
        self.signals = {}
        self.max_time = None
        self.plot_rowsize = 1.5
        self.read_file(fsim, max_events, ignore_timing)

    def read_file(self, fsim, max_events=None, ignore_timing=False):
        """Reads in a file of PRSIM results
        
        Parameters
        ----------
        fsim: string
            file containing PRSIM outputs
        max_events: int or None
            maximum number of events to read in 
        ignore_timing: Boolean
            whether to ignore the timing information in the data
            if you only care about the transition sequence
        """
        with open(fsim, 'r') as fh:
            lines = fh.readlines()
            time = 0
            prev_time = 0
            n_unique_times = 0 # number of unique times stamps -1
            n_events = 1
            for line in lines:
                if max_events and n_events > max_events:
                    break
                tokens = line.strip().split(' ')
                if len(tokens) > 0:
                    if tokens[0].isnumeric():
                        time = int(tokens[0])
                        if time > prev_time:
                            n_unique_times += 1
                            prev_time = time
                        signal = tokens[1]
                        if signal not in self.signals:
                            value = tokens[3]
                            self.signals[signal] = {
                                "v0":value,
                                "t0":time,
                                "transitions":[]}
                            if ignore_timing:
                                self.signals[signal]["t0"] = n_unique_times
                        else:
                            self.signals[signal]["transitions"].append(time)
                            if ignore_timing:
                                self.signals[signal]["transitions"][-1] = n_unique_times
                        n_events += 1
            self.max_time = time
            if ignore_timing:
                self.max_time = n_unique_times

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

    def plot(self, signals=None):
        """Plots available signals"""
        if signals == None:
            signals = sorted(self.get_signals())
        n_signals = len(signals)
        fig, axs = plt.subplots(
            nrows=n_signals,
            figsize=(8, self.plot_rowsize*n_signals),
            sharex=True)
        for ax, signal in zip(axs, signals):
            self.plot_signal(ax, signal)
        axs[0].set_xlim((0, self.max_time))
        return fig, axs

    @staticmethod
    def show():
        plt.show()

