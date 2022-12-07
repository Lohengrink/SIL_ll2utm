"""
:copyright: 2019 Geophysics Labs
:author: Joseph Barraud
:license: BSD License
"""

"""
:modified: Chin-Yeh Chen
"""

# import numpy
import numpy as np

# import local modules
from spatial_CY import projectPoints
# ==============================================================================
# segy2segy
# ==============================================================================


def segy2segy(s_srs, t_srs, X, Y):
    '''
    Both of X and Y are list type.
    convert one XY projection to other one XY projection only
    '''

    XYarray = np.zeros((len(X), 2), dtype=np.float)

    #important----------------------------------------------------
    if s_srs == 4326:
        XYarray[:, 0] = Y
        XYarray[:, 1] = X

        # XYarray[:, 0] = STH[Ycoord] * XYscale / 3600 if this is sec
        # XYarray[:, 1] = STH[Xcoord] * XYscale / 3600
    else:
        XYarray[:, 0] = X
        XYarray[:, 1] = Y

    #important----------------------------------------------------


    # transform coordinates
    return_dict = {}
    newXYarray = projectPoints(XYarray, s_srs, t_srs)

    new_y_list =[] #y
    new_x_list =[]
    for yx_set in newXYarray:
        new_y_list.append(str(yx_set[1]))

    for yx_set in newXYarray:
        new_x_list.append(str(yx_set[0]))


    return_dict['cdpy'] = new_y_list
    return_dict['cdpx'] = new_x_list

    return return_dict
