# -*- coding:utf-8 -*-

from matplotlib import pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap
from mowerstestplayer import MowersTestPlayer
from mower import Mower
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyArrow

TITLE_LINE1 = '\nTest file: {}\n'
TITLE_LINE2 = '\nMower {}\n\nStatus: position=({} ,{}), orientation={}\n Step: {}'
TITLE_LINE3 = '\n Next action: {}'


class MowersViz(object):
    """
    This class allows to visualize the steps of the program applied to a given mower in a test file.
    It uses numpy and matplotlib ==> it should be executed in an anaconda3 python environment.
    Inspired from this article: https://eli.thegreenplace.net/2016/drawing-animated-gifs-with-matplotlib/
    """

    LARGE_GREENS_CMAP = cm.get_cmap('Greens', 512)
    # Create a new green colormap from the 'Greens' matplotlib colormap
    FULL_GREEN_CMAP = ListedColormap(LARGE_GREENS_CMAP(np.linspace(0.4, 0.6, 256)))

    def __init__(self, scenario_file):
        """
        Constructor. Initialize the test visualizer.
        :param scenario_file: path of test file
        """
        self._scenario_file = scenario_file
        # Create the test player and apply test
        mplayer = MowersTestPlayer(self._scenario_file)
        mplayer.open()
        self._scenario, self._initmowers = mplayer.apply(with_history=True)
        # other instance variables initialization
        self._fig, self._ax, self._img_grid, self._grid_lawn = self.create_graphic_ctx()
        self._circle, self._arrow = None, None
        self._mower_index = 0
        self.draw_mower(0, 0)

    def create_graphic_ctx(self):
        """
        Create a graphic context for the visualization.
        :return: a figure, an axe, a numpy array, an image grid
        """
        fig, ax = plt.subplots(figsize=(7, 7))
        fig.set_tight_layout(True)
        plt.xlim(-0.5, Mower.GRID_UP_RIGHT_CORNER[0] + 0.5)
        plt.ylim(-0.5, Mower.GRID_UP_RIGHT_CORNER[0] + 0.5)
        plt.xticks(np.arange(0, Mower.GRID_UP_RIGHT_CORNER[0] + 1, 1.0))
        plt.yticks(np.arange(0, Mower.GRID_UP_RIGHT_CORNER[1] + 1, 1.0))
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(14)
            for tick in ax.xaxis.get_major_ticks():
                tick.label1.set_fontsize(14)
                tick.label1.set_fontweight('bold')
            tick.label1.set_fontweight('bold')
        fig.suptitle(TITLE_LINE1.format(self._scenario_file), fontsize='xx-large')
        grid_lawn = np.ones((Mower.GRID_UP_RIGHT_CORNER[1] + 1, Mower.GRID_UP_RIGHT_CORNER[0] + 1))
        grid_lawn[0, 0] = 0
        img_grid = plt.imshow(grid_lawn, cmap=MowersViz.FULL_GREEN_CMAP)
        # plt.show()
        return fig, ax, img_grid, grid_lawn

    def clear_graphic_ctx(self):
        """
        Clear the graphic context.
        :return: None
        """
        if self._circle is not None:
            self._circle.remove()
            self._circle = None
        if self._arrow is not None:
            self._arrow.remove()
            self._arrow = None
        self._grid_lawn[:, :] = 1
        self._img_grid.set_data(self._grid_lawn)

    def draw_mower(self, mower_index, step_number):
        """
        Create a representation of a mower on the grid_lawn.
        Our representation is a filled circle with an arrow for the mower orientation.
        :param mower_index: mower rank in the test file (0 is first)
        :param step_number: program step to represent (0 ==> initial status. Other steps are from 1 to
                            the length of the program associated to the mower: [1, len(program])
        :return: None
        """
        if step_number == 0:
            circle_x = self._initmowers[mower_index][0][0]
            circle_y = self._initmowers[mower_index][0][1]
            orientation = self._initmowers[mower_index][1]
            self._grid_lawn.fill(1)
        else:
            circle_x = self._scenario[mower_index][step_number - 1][0][0][0]
            circle_y = self._scenario[mower_index][step_number - 1][0][0][1]
            orientation = self._scenario[mower_index][step_number - 1][0][1]
        self._grid_lawn[circle_y, circle_x] = 0
        self._img_grid.set_data(self._grid_lawn)
        self._circle = plt.Circle((circle_x, circle_y), 0.4, color='blue', alpha=0.3)
        self._ax.add_patch(self._circle)
        if orientation == 'N':
            self._arrow = FancyArrow(circle_x, circle_y, 0, 0.37, color='w', width=0.03, joinstyle='miter')
        elif orientation == 'E':
            self._arrow = FancyArrow(circle_x, circle_y, 0.37, 0, color='w', width=0.03, joinstyle='miter')
        elif orientation == 'S':
            self._arrow = FancyArrow(circle_x, circle_y, 0, -0.37, color='w', width=0.03, joinstyle='miter')
        elif orientation == 'W':
            self._arrow = FancyArrow(circle_x, circle_y, -0.37, 0, color='w', width=0.03, joinstyle='miter')
        self._ax.add_patch(self._arrow)
        title = TITLE_LINE1.format(self._scenario_file)
        title += TITLE_LINE2.format(self._mower_index + 1, circle_x, circle_y, orientation, step_number)
        if step_number < len(self._scenario[self._mower_index]):
            title += TITLE_LINE3.format(self._scenario[self._mower_index][step_number][1])
        self._fig.suptitle(title, fontsize='xx-large')

    def get_mower_index_and_step(self, refresh_step):
        """
        Retrieve the mower index and the step in the mower program for the current refresh step of the animation.
        :param refresh_step: step in the animation
        :return: the mower index in the scenario and the step in the mower program
        """
        idx = 0
        steps = 0
        for mower in self._scenario:
            if refresh_step < steps + len(mower) + 1:
                return idx, refresh_step - steps  # - len(mower) - 1
            else:
                steps += len(mower) + 1
                idx += 1

    def update(self, i):
        """
        Refresh matplotlib objects to display the next step of the scenario.
        :param i: step considered
        :return: None
        """
        if self._circle is not None:
            self._circle.remove()
            self._circle = None
        if self._arrow is not None:
            self._arrow.remove()
            self._arrow = None
        mower_index, step = self.get_mower_index_and_step(i)
        if mower_index != self._mower_index:
            self.clear_graphic_ctx()
            self._mower_index = mower_index
        self.draw_mower(self._mower_index, step)

    def anim(self, anim_gif=None):
        """
        Animate the test scenario or generate an animated gif of the test scenario.
        :param anim_gif: file to generate (optional)
        :return: None
        """
        scenario_steps = 0
        for mower in self._scenario:
            scenario_steps += len(mower) + 1
        anim = FuncAnimation(self._fig, self.update,
                             frames=np.arange(0, scenario_steps),
                             interval=2000)
        if anim_gif:
            anim.save(anim_gif, dpi=80, writer='imagemagick')
        else:
            plt.show()


if __name__ == '__main__':
    mViz = MowersViz('testmowers1.data')
    # mViz.anim(anim_gif='testmowers1.gif')
    mViz.anim()
    # plt.show()
