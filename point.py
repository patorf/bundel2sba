import numpy as np


class Point():
    """

    """

    def __init__(self):
        self.pos = np.zeros([3, 1])
        """:type: ndarray"""
        self.color = np.zeros([3, 1])
        """:type: ndarray"""
        self.no = -1
        """:type: int"""
        self.measured_in=[]
        """:type: list[int]"""

    def x(self):
        return self.pos[0]

    def y(self):
        return self.pos[1]
    def z(self):
        return self.pos[2]


