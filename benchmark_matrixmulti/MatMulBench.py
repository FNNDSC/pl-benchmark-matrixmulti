from __future__ import division
from numba import cuda, float32
import numpy
import math
import time

# Controls threads per block and shared memory usage.
# The computation will be done on blocks of TPBxTPB elements.
TPB = 32

@cuda.jit
def fast_matmul(A, B, C):
    # Define an array in the shared memory
    # The size and type of the arrays must be known at compile time
    sA = cuda.shared.array(shape=(TPB, TPB), dtype=float32)
    sB = cuda.shared.array(shape=(TPB, TPB), dtype=float32)

    x, y = cuda.grid(2)

    tx = cuda.threadIdx.x
    ty = cuda.threadIdx.y
    bpg = cuda.gridDim.x    # blocks per grid

    if x >= C.shape[0] and y >= C.shape[1]:
        # Quit if (x, y) is outside of valid C boundary
        return

    # Each thread computes one element in the result matrix.
    # The dot product is chunked into dot products of TPB-long vectors.
    tmp = 0.
    for i in range(bpg):
        # Preload data into shared memory
        sA[tx, ty] = A[x, ty + i * TPB]
        sB[tx, ty] = B[tx + i * TPB, y]

        # Wait until all threads finish preloading
        cuda.syncthreads()

        # Computes partial product on the shared memory
        for j in range(TPB):
            tmp += sA[tx, j] * sB[j, ty]

        # Wait until all threads finish computing
        cuda.syncthreads()
    C[x, y] = tmp

class MatMulBench:
    #TPB One thread block size
    #COE TPBxCOE = matrix size(Ract matrix)
    #DUP will Run DUP times
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'COEnumber': self.COE = value

    # Controls threads per block and shared memory usage.
    # The computation will be done on blocks of TPBxTPB elements.
    def Run(self):# -> float:
        COE = self.COE
        start_time = time.time()
        # The data array
        A = numpy.full((TPB*COE, TPB*COE), 3, numpy.float) # [32 x 48] matrix containing all 3's
        B = numpy.full((TPB*COE, TPB*COE), 4, numpy.float) # [48 x 16] matrix containing all 4's

        A_global_mem = cuda.to_device(A)
        B_global_mem = cuda.to_device(B)
        C_global_mem = cuda.device_array((TPB*COE, TPB*COE)) # [32 x 16] matrix result

        # Configure the blocks
        threadsperblock = (TPB, TPB)
        blockspergrid_x = int(math.ceil(A.shape[0] / threadsperblock[1]))
        blockspergrid_y = int(math.ceil(B.shape[1] / threadsperblock[0]))
        blockspergrid = (blockspergrid_x, blockspergrid_y)

        # Start the kernel
        fast_matmul[blockspergrid, threadsperblock](A_global_mem, B_global_mem, C_global_mem)
        res = C_global_mem.copy_to_host()
        return time.time() - start_time