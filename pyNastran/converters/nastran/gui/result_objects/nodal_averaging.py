from typing import Callable
from collections import defaultdict
import numpy as np


def abs_max_scalar(x: np.ndarray):
    mini = np.nanmin(x)
    maxi = np.nanmax(x)
    if np.abs(mini) > np.abs(maxi):
        return mini
    return maxi

def difference_scalar(x: np.ndarray):
    out = np.nanmax(x) - np.nanmin(x)
    return out

nodal_combine_map = {
    'Absolute Max': abs_max_scalar,
    'Mean': np.nanmean,
    'Max': np.nanmax,
    'Min': np.nanmin,
    'Difference': difference_scalar,
    'Std. Dev.': np.nanstd,
}


def nodal_average(nodal_combine_func: Callable[[np.ndarray], np.ndarray],
                  element_node: np.ndarray,
                  data: np.ndarray,
                  nids: np.ndarray,
                  #inid: np.ndarray,
                  nid_to_inid_map: dict[int, int]) -> np.ndarray:
    data_dict = defaultdict(list)
    nnode = len(nids)

    data2 = np.full(nnode, np.nan, dtype=data.dtype)
    for (eid, nid), datai in zip(element_node, data):
        data_dict[nid].append(datai)
    for nid, datasi in data_dict.items():
        collapsed_value = nodal_combine_func(datasi)
        inidi = nid_to_inid_map[nid]
        data2[inidi] = collapsed_value
    return data2