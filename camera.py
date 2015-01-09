import numpy as np


class Camera():
    """

    """

    def __init__(self):
        self.pos = np.zeros([3, 1])
        """:type: ndarray"""
        self.rot = np.zeros([3, 3])
        """:type: ndarray"""
        self.focal = 0
        self.radialDis = np.zeros([1, 2])
        """:type: ndarray"""
        self.measured_points = []  # tuble (Point, point_position)
        """:type: list[(Point, ndarray)]"""





