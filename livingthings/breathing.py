from gpiozero.devices import GPIOMeta
from time import sleep
from matplotlib import pyplot as plt
from matplotlib import animation
from IPython import display
import numpy as np


class Breathing:
    """
    Instantiate a Breathing object
    device: GPIOMeta() - Instantiated GPIO zero device for raspberry pi.
    bpm: int - beats per minute of the living thing.
    illness_factor: float - Higher than 1 values will correspond to a faster breathing in relation to bpm. Lower values will correspond to slower breathing. Apply illness accordingly.
    alpha: float -
    """

    def __init__(
        self,
        device: GPIOMeta = None,
        bpm: int = 60,
        illness_factor: float = 1,
        alpha: float = 0.5,
    ):
        self.device = device
        self.bpm = bpm
        self.illness_factor: float = illness_factor
        self.alpha = alpha
        self.breathing_cycle = None
        self.pwm_factor = 1000

    def __inhale_exhale(
        self,
        breathing_cycle: float = None,
        mode="inhale",
        alpha: float = 0.5,
        pwm=False,
    ):
        if mode == "inhale":
            inhale_factor = 1 / alpha
            inhale_frequency = 60 / (breathing_cycle * inhale_factor)
            if pwm:
                return sleep(inhale_frequency / self.pwm_factor)
            # print(f"inhale for {inhale_frequency}s")
            return sleep(inhale_frequency)
        else:
            exhale_factor = 1 / (1 - alpha)
            # print(f"exhale for {60 / (breathing_cycle * exhale_factor)}s")
            return sleep(60 / (breathing_cycle * exhale_factor))

    def breath(
        self,
        bpm: int = 60,
        illness_factor: float = 1,
        alpha: float = 0.5,
        pwm=False,
        dry_run=False,
    ):
        """
        Parameters
        -----------------
        bpm: Beats per minute of the living thing. Default: 60
        illness_factor: Factor of illness, lower values may decrease breathing cycle speed, and higher values would increase, apply accordingly to your use case. Default: 1
        alpha: Balances if illness factor must be applied to inhale or exhale. The default value means that illness_factor if existent should be applied to both inhale and exhale equally.
        Default: 0.5

        Returns
        ---------------"""
        self.bpm = bpm
        self.illness_factor = illness_factor
        self.alpha = alpha
        self.breathing_cycle = (0.2 * bpm) * illness_factor

        try:
            while True:
                if not dry_run:
                    if pwm:
                        for i in range(0, self.pwm_factor):
                            self.device.value = round(i * 1 / self.pwm_factor, 3)
                            self.__inhale_exhale(
                                self.breathing_cycle,
                                mode="inhale",
                                alpha=alpha,
                                pwm=True,
                            )
                    else:
                        self.device.on()
                        self.__inhale_exhale(
                            self.breathing_cycle, mode="inhale", alpha=alpha
                        )
                else:
                    print("Inhale")
                    self.__inhale_exhale(
                        self.breathing_cycle, mode="inhale", alpha=alpha
                    )

                if not dry_run:
                    if pwm:
                        for i in range(0, self.pwm_factor):
                            self.device.value = round(1 - (i * 1 / self.pwm_factor), 3)
                            self.__inhale_exhale(
                                self.breathing_cycle,
                                mode="exhale",
                                alpha=alpha,
                                pwm=True,
                            )
                    else:
                        self.device.on()
                        self.__inhale_exhale(
                            self.breathing_cycle, mode="exhale", alpha=alpha
                        )
                else:
                    print("Exhale")
                    self.__inhale_exhale(
                        self.breathing_cycle, mode="exhale", alpha=alpha
                    )

        except (KeyboardInterrupt, SystemExit):
            print("Breathing stopped manually...")

    def visualize(self, frames=300, interval=20, verbose=True):
        plt.clf()
        plt.style.use("dark_background")
        fig = plt.figure()
        ax = plt.axes(xlim=(-2, 60), ylim=(-1, 1))
        ax.set_xlabel("Time")
        (line,) = ax.plot([], [], lw=2)

        # initialization function
        def init():
            # creating an empty plot/frame
            line.set_data([], [])
            return (line,)

        # lists to store x and y axis points
        xdata, ydata = [], []

        # animation function
        def animate(i):
            # t is a parameter
            x = np.linspace(0, self.breathing_cycle * 3 + 1.5, frames)
            # x, y values to be plotted
            y = np.sin(x[i])

            # appending new points to x, y axes points list
            xdata.append(x[i])
            ydata.append(y)
            line.set_data(xdata, ydata)
            return (line,)

        # setting a title for the plot
        plt.title("Breathing cycle per minute")
        # hiding the axis details
        # plt.axis('off')

        # call the animator
        anim = animation.FuncAnimation(
            fig, animate, init_func=init, frames=frames, interval=interval
        )

        video_1 = anim.to_html5_video()
        plt.close()
        html_code_1 = display.HTML(video_1)
        if verbose:
            print(f"BPM: {self.bpm}")
            print(f"Breathing cycle: {self.breathing_cycle} per minute")
            print(f"Illness factor: {self.illness_factor}")
        return display.display(html_code_1)

    def visualize_alpha(self, frames=300, interval=20, verbose=False):
        plt.clf()
        plt.style.use("dark_background")
        fig = plt.figure()
        ax = plt.axes(xlim=(-5, 60), ylim=(-1.5, 1.5))
        ax.set_xlabel("Time")
        (line,) = ax.plot([], [], lw=2)

        plotlays, plotcols = [2], ["green", "red"]
        lines = []
        for index in range(2):
            lobj = ax.plot([], [], lw=2, color=plotcols[index])[0]
            lines.append(lobj)

        # initialization function
        def init():
            for line in lines:
                line.set_data([], [])
            return lines

        # lists to store x and y axis points
        xdata1, xdata2, ydata1, ydata2 = [], [], [], []

        # animation function
        def animate(i):
            # t is a parameter
            x = np.linspace(0, self.breathing_cycle * 3 + 1.5, frames)
            # x, y values to be plotted
            y1 = np.sin(x[i] * self.alpha)
            y2 = np.sin((x[i] * (1 - self.alpha)))

            # appending new points to x, y axes points list
            xdata1.append(x[i])
            xdata2.append(x[i] + 2 * np.pi)
            ydata1.append([y1 if y1 > 0 else 0][0])
            ydata2.append([-y2 if y2 > 0 else 0][0])

            xlist = [xdata1, xdata2]
            ylist = [ydata1, ydata2]

            for lnum, line in enumerate(lines):
                line.set_data(
                    xlist[lnum], ylist[lnum]
                )  # set data for each line separately.
            return lines

        #     line.set_data(xdata1, (np.array(ydata1)))
        #     return (line, )

        # setting a title for the plot
        plt.title("Breathing (inhale and exhale) per minute")
        # hiding the axis details
        # plt.axis('off')

        # call the animator
        anim = animation.FuncAnimation(
            fig, animate, init_func=init, frames=frames, interval=interval
        )

        video_1 = anim.to_html5_video()
        plt.close()
        html_code_1 = display.HTML(video_1)
        if verbose:
            print(f"BPM: {self.bpm}")
            print(f"Breathing cycle: {self.breathing_cycle} per minute")
            print(f"Illness factor: {self.illness_factor}")
            print(f"Alpha: {self.alpha}")
        display.display(html_code_1)
