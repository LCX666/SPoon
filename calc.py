import numpy as np

from utils.dispatcher import dispatch
from utils.debugger import Logger

# set logging test update lcx added by wenake
logger = Logger(__name__)

def getINF():
    """
    function: 
        return the INF of this tool.
    
    parameters: 
        None, no parameter.
    
    return:
        int, the INF in this tools.
    """

    from utils.settings import INF as inf

    return inf


def calc(graph = None, useCUDA = True, useMultiPro = False, pathRecordBool = False, srclist = None, block = None, grid = None):
    
    """
    function: 
        a calculate interface.
    
    parameters: 
        graph: class Graph, must, the graph data that you want to get the shortest path.
            (more info please see the developer documentation).
        useCUDA: bool, use CUDA to speedup or not.
        useMultiPro, bool, use multiprocessing in CPU or not. only support dijkstra APSP and MSSP.
        pathRecordBool: bool, record the path or not.
        srclist: int/lsit/None, the source list, can be [None, list, number].(more info please see the developer documentation).
        block: tuple, a 3-tuple of integers as (x, y, z), the block size, to shape the kernal threads.
        grid: tuple, a 2-tuple of integers as (x, y), the grid size, to shape the kernal blocks.

    return:
        class, Result object. (see the 'sparry/classes/result.py/Result') 
    """
    # turn to dispatch to dispatch
    # we only accept graphic data in edgeSet format 

    logger.info(f"entering calc func...")
     
    return dispatch(graph = graph, useCUDA = useCUDA, useMultiPro = useMultiPro, pathRecordBool = pathRecordBool, srclist = srclist, block = block, grid = grid)
    


if __name__ == "__main__":
    calc()