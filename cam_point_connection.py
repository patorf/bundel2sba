__author__ = 'philipp.atorf'
import numpy as np


class cam_point_connection:
    """

    :param camID:
    :param pointID:
    :param pos:
    """

    def __init__(self, camID, pointID, pos=np.zeros([2, 1])):
        self.cam = camID
        """:type: int"""
        self.point_intern = pointID
        """:type: int"""
        self.pos = pos
        """:type: ndarray"""
        self.point_global = None
        """:type: int"""